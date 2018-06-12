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
IOT_HUB_OWNER_KEY = os.environ['IOT_HUB_OWNER_KEY']
DSVM_NAME = os.environ['DSVM_NAME']

table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

def login_required(f):    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'x-ms-token-aad-refresh-token' not in request.headers:
            pass
            #return redirect(url_for('setup'))
        return f(*args, **kwargs)
    return decorated_function

def get_identity():
    id_token = request.headers['x-ms-token-aad-id-token']
    return jwt.decode(id_token, verify=False)

#@app.context_processor
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

@app.route('/devices')
@register_breadcrumb(app, '.devices', 'IoT Devices')
@login_required
def devices():
    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
    devices = iot_hub.get_device_list()
    devices.sort(key = lambda x: x.deviceId)
    return render_template('devices.html', assets = devices)

@app.route('/createDevices', methods=['POST'])
@login_required
def create_devices():
    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
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

    return redirect(url_for('devices'))

def view_asset_dlc(*args, **kwargs):
    device_id = request.view_args['device_id']
    return [
        {'text': device_id, 'url': '/devices/{0}'.format(device_id)}]

@register_breadcrumb(app, '.devices.twin', '', dynamic_list_constructor=view_asset_dlc)
@app.route('/devices/<device_id>')
@login_required
def device(device_id):
    return render_template('twin.html', device_id = device_id)

@app.route('/api/devices/<device_id>', methods=['GET'])
@login_required
def get_device_twin(device_id):
    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
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

    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
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

@app.route('/modeling')
@register_breadcrumb(app, '.modeling', 'Modeling')
@login_required
def analytics():    
    return render_template('modeling.html', dsvmName = DSVM_NAME)

@app.route('/intelligence')
@register_breadcrumb(app, '.intelligence', 'Intelligence')
@login_required
def intelligence():
    return render_template('intelligence.html')


if __name__ == "__main__":
    app.run('0.0.0.0', 8000, debug=True)
