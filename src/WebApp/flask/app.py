import numpy as np
import sys, os, time, glob
import requests
import json
import uuid
import json
import random
import markdown
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, Response, request,  redirect, url_for
from threading import Thread
from azure.storage.blob import BlockBlobService
from azure.storage.file import FileService
from azure.storage.file.models import FilePermissions
from azure.storage.blob.models import BlobPermissions
from azure.storage.table import TableService, Entity, TablePermissions
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb

# TODO: Fix possible WebJob restarts because of this.
simulator_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../App_Data/jobs/continuous/Simulator'))
sys.path.append(simulator_path)
from iot_hub import IoTHub

app = Flask(__name__)
app.debug = True

# Initialize Flask-Breadcrumbs
Breadcrumbs(app=app)

STORAGE_ACCOUNT_SUFFIX = 'core.windows.net'
STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']
TELEMETRY_CONTAINER_NAME = 'telemetry'
IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
EVENT_HUB_ENDPOINT = os.environ['EVENT_HUB_ENDPOINT']
StorageConnectionString = "DefaultEndpointsProtocol=https;AccountName=" + STORAGE_ACCOUNT_NAME + ";AccountKey=" + STORAGE_ACCOUNT_KEY + ";EndpointSuffix=core.windows.net"

table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'x-ms-token-aad-refresh-token' not in request.headers:
            return redirect(url_for('setup'))
        return f(*args, **kwargs)
    return decorated_function

def get_identity():
    id_token = request.headers['x-ms-token-aad-id-token']
    return jwt.decode(id_token, verify=False)

@app.context_processor
def context_processor():
    return dict(user_name=get_identity()['name'])

@app.route('/')
@register_breadcrumb(app, '.', 'Home')
@login_required
def home():
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'README.md'))
    with open(readme_path, 'r') as f:
        content = f.read()

    html = markdown.markdown(content)
    return render_template('home.html', content = html)

@app.route('/telemetry')
@register_breadcrumb(app, '.telemetry', 'Telemetry')
@login_required
def telemetry():
    iot_hub = IoTHub(os.environ['IOT_HUB_NAME'], os.environ['IOT_HUB_OWNER_KEY'])
    devices = iot_hub.get_device_list()
    devices.sort(key = lambda x: x.deviceId)
    return render_template('telemetry.html', assets = devices)

@app.route('/createDevices', methods=['POST'])
@login_required
def create_devices():
    iot_hub = IoTHub(os.environ['IOT_HUB_NAME'], os.environ['IOT_HUB_OWNER_KEY'])
    iot_device_count = 10

    devices = []
    for i in range(iot_device_count):
        device_id = 'MACHINE-{0:03d}'.format(i)
        device = iot_hub.create_device(device_id)
        devices.append(device)

    rotor_imbalance_device_id = devices[-1].deviceId
    low_pressure_device_id = devices[-2].deviceId

    def failure_onset(device_id):
        if device_id == rotor_imbalance_device_id:
            return 'F01'
        if device_id == low_pressure_device_id:
            return 'F02'
        return None

    for device in devices:
        twin_properties = {
            'tags': {
                'simulated': True,
                'simulator': 'devices.engines.Engine'
            },
            'properties': {
                'desired': {
                    'speed': random.randint(600, 1500),
                    'mode': 'auto',
                    'failureOnset': failure_onset(device.deviceId)
                }
            }
        }

        iot_hub.update_twin(device.deviceId, json.dumps(twin_properties))

    return redirect(url_for('telemetry'))

def view_asset_dlc(*args, **kwargs):
    device_id = request.view_args['device_id']
    return [
        {'text': device_id, 'url': '/telemetry/{0}'.format(device_id)}]

@register_breadcrumb(app, '.telemetry.twin', '', dynamic_list_constructor=view_asset_dlc)
@app.route('/telemetry/<device_id>')
@login_required
def telemetry_twin(device_id):
    return render_template('twin.html', device_id = device_id)

@app.route('/twin/<device_id>', methods=['GET'])
@login_required
def get_device_twin(device_id):
    iot_hub = IoTHub(os.environ['IOT_HUB_NAME'], os.environ['IOT_HUB_OWNER_KEY'])
    twin_data = iot_hub.get_device_twin(device_id)
    resp = Response(twin_data)
    resp.headers['Content-type'] = 'application/json'
    return resp

@app.route('/twin/<device_id>', methods=['POST'])
@login_required
def set_desired_properties(device_id):
    desired_props = {}
    for key in request.form:
        if key == 'speed':
            desired_props[key] = int(request.form[key])
        else:
            desired_props[key] = request.form[key]

    payload = {
        'properties': {
            'desired': desired_props
        }
    }
    payload_json = json.dumps(payload)

    iot_hub = IoTHub(os.environ['IOT_HUB_NAME'], os.environ['IOT_HUB_OWNER_KEY'])
    twin_data = iot_hub.update_twin(device_id, payload_json)
    resp = Response(twin_data)
    resp.headers['Content-type'] = 'application/json'
    return resp

def get_access_token():
    refresh_token = request.headers['x-ms-token-aad-refresh-token']

    parameters = {
        'grant_type': 'refresh_token',
        'client_id': os.environ['WEBSITE_AUTH_CLIENT_ID'],
        'client_secret': os.environ['WEBSITE_AUTH_CLIENT_SECRET'],
        'refresh_token': refresh_token,
        'resource': 'https://management.core.windows.net/'
    }

    tid = get_identity()['tid']

    result = requests.post('https://login.microsoftonline.com/{0}/oauth2/token'.format(tid), data = parameters)
    access_token = result.json()['access_token']
    return access_token


def parse_website_owner_name():
    owner_name = os.environ['WEBSITE_OWNER_NAME']
    subscription, resource_group_location = owner_name.split('+', 1)
    resource_group, location = resource_group_location.split('-', 1)
    return subscription, resource_group, location

@app.route('/setup')
def setup():
    subscription, resource_group, _ = parse_website_owner_name()
    # TODO: use correct tenant name
    return render_template('setup.html',
        tenant_name = 'microsoft.onmicrosoft.com',
        subscription = subscription,
        resource_group = resource_group,
        web_site_name = os.environ['WEBSITE_SITE_NAME'])

@app.route('/analytics')
@register_breadcrumb(app, '.analytics', 'Analytics')
@login_required
def analytics():
    dsvmName = os.environ['DSVM_NAME']
    return render_template('analytics.html', dsvmName = dsvmName)

@app.route('/operationalization')
@register_breadcrumb(app, '.operationalization', 'Operationalization')
@login_required
def operationalization():
    return render_template('operationalization.html')

def create_snapshot(file_share, directory_name, file_name, container_name, correlation_guid = str(uuid.uuid4())):
    file_service = FileService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
    blob_service = BlockBlobService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
    file_sas_token = file_service.generate_file_shared_access_signature(
        file_share,
        directory_name,
        file_name,
        permission = FilePermissions.READ,
        expiry = datetime.now() + timedelta(minutes = 10))

    file_url = file_service.make_file_url(file_share, directory_name, file_name, sas_token = file_sas_token)

    blob_name = '{0}/{1}/{2}'.format(correlation_guid, directory_name, file_name)
    blob_service.create_container(container_name)

    try:
        blob_service.copy_blob(container_name, blob_name, file_url)
    except Exception as e:
        raise ValueError('Missing file ' + file_name)

    blob_sas_token = blob_service.generate_blob_shared_access_signature(
        container_name,
        blob_name,
        permission = BlobPermissions.READ,
        expiry = datetime.now() + timedelta(days = 1000))

    return blob_service.make_blob_url(container_name, blob_name, sas_token = blob_sas_token)

@app.route('/intelligence')
@register_breadcrumb(app, '.intelligence', 'Intelligence')
@login_required
def intelligence():
    return render_template('intelligence.html')


if __name__ == "__main__":
    app.run('0.0.0.0', 8000, debug=True)
