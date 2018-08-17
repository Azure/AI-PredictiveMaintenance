import numpy as np
import sys, os, time, glob
import requests
import json
import uuid
import json
import random
import markdown
import jwt
import io
import csv
import collections
from urllib.parse import urlparse
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
from iot_hub_helpers import IoTHub
from http import HTTPStatus

app = Flask(__name__)
app.debug = True

# Initialize Flask-Breadcrumbs
Breadcrumbs(app=app)

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']
IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
IOT_HUB_OWNER_KEY = os.environ['IOT_HUB_OWNER_KEY']
DSVM_NAME = os.environ['DSVM_NAME']
DATABRICKS_WORKSPACE_LOGIN_URL = os.environ['DATABRICKS_WORKSPACE_LOGIN_URL']
VERSION_INFO = open(os.path.join(os.path.dirname(__file__), 'version.info')).readlines()[0]

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

@app.context_processor
def context_processor():
    return dict(
        #user_name=get_identity()['name']
        version_info = VERSION_INFO)

@app.route('/home')
@register_breadcrumb(app, '.', 'Home')
@login_required
def home():
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'README.md'))
    with open(readme_path, 'r') as f:
        content = f.read()

    html = markdown.markdown(content)
    return render_template('home.html', content = html)

@app.route('/devices')
@register_breadcrumb(app, '.devices', 'Simulated IoT Devices')
@login_required
def devices():
    return render_template('devices.html')

def error_response(error_code, message, http_status_code):
    data = {
        'code': error_code,
        'message': message
    }

    return Response(json.dumps(data), http_status_code, mimetype='application/json')

@app.route('/api/devices', methods=['GET'])
@login_required
def get_devices():
    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
    devices = iot_hub.get_device_list()
    devices.sort(key = lambda x: x.deviceId)
    device_properties = json.dumps([{
        'deviceId': device.deviceId,
        'lastActivityTime': device.lastActivityTime,
        'connectionState':str(device.connectionState) } for device in devices])
    return Response(device_properties, mimetype='application/json')

@app.route('/api/devices', methods=['PUT'])
@login_required
def create_device():
    device_id = str.strip(request.form['deviceId'])

    if not device_id:
        return error_response('INVALID_ID', 'Device ID cannot be empty.', HTTPStatus.BAD_REQUEST)

    try:
        simulation_properties = json.loads(request.form['simulationProperties'])
    except Exception as e:
        return error_response('INVALID_PARAMETERS', str(e), HTTPStatus.BAD_REQUEST)

    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)

    try:
        iot_hub.create_device(device_id)
    except Exception as e:
        return error_response('INVALID_ID', str(e), HTTPStatus.BAD_REQUEST)

    tags = {
        'simulated': True
    }
    tags.update(simulation_properties)

    twin_properties = {
        'tags': tags
    }

    try:
        iot_hub.update_twin(device_id, json.dumps(twin_properties))
    except Exception as e:
        return error_response('INVALID_PARAMETERS', str(e), HTTPStatus.BAD_REQUEST)

    return Response()


@app.route('/api/devices/<device_id>', methods=['DELETE'])
@login_required
def delete_device(device_id):
    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
    iot_hub.delete_device(device_id)

    resp = Response()
    return resp

def view_device_dlc(*args, **kwargs):
    device_id = request.view_args['device_id']
    url = urlparse(request.url)
    base_path = os.path.split(url.path)[0]
    return [{'text': device_id, 'url': '{0}/{1}'.format(base_path, device_id)}]

@register_breadcrumb(app, '.devices.device', '', dynamic_list_constructor=view_device_dlc)
@app.route('/devices/<device_id>')
@login_required
def devices_device(device_id):
    return render_template('devices_device.html', device_id = device_id)

@app.route('/api/devices/<device_id>/logs', methods=['GET'])
@login_required
def get_device_logs(device_id):
    query_filter = "PartitionKey eq '{0}'".format(device_id)
    log_entities = table_service.query_entities('logs', filter=query_filter)

    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    for entity in sorted(log_entities, key=lambda e: e.Timestamp):
        level = entity.Level if 'Level' in entity else None
        code = entity.Code if 'Code' in entity else None
        message = entity.Message if 'Message' in entity else None
        if code == 'SIM_HEALTH':
            continue
        row = (str(entity.Timestamp), entity.PartitionKey, level, code, message)
        writer.writerow(row)

    log_output = output.getvalue()

    resp = Response(log_output)
    resp.headers['Content-type'] = 'text/plain'
    return resp

@app.route('/api/devices/<device_id>', methods=['GET'])
@login_required
def get_device(device_id):
    #iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
    #twin_data = iot_hub.get_device_twin(device_id)
    query_filter = "PartitionKey eq '{0}' and Code eq '{1}'".format(device_id, 'SIM_HEALTH')
    health_history_entities = table_service.query_entities('logs', filter=query_filter)

    health_history = []
    for entity in health_history_entities:
        timestamp = entity.Timestamp
        message_json = json.loads(entity.Message)
        #indices = [x[1] for x in sorted(message_json.items())]
        health_history.append((timestamp, message_json))

    health_history.sort(key = lambda x: x[0])

    health_history_by_index = {}
    for entry in health_history:
        timestamp = entry[0].replace(tzinfo=None).isoformat()
        indices_json = entry[1]
        for k, v in indices_json.items():
            if k not in health_history_by_index:
                health_history_by_index[k] = {'t': [], 'h': []}
            health_history_by_index[k]['t'].append(timestamp)
            health_history_by_index[k]['h'].append(v)


    response_json = {
        #'twin': json.loads(twin_data),
        'health_history': health_history_by_index
    }

    resp = Response(json.dumps(response_json))
    resp.headers['Content-type'] = 'application/json'
    return resp

@app.route('/api/devices/<device_id>', methods=['POST'])
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
    return render_template('modeling.html', dsvmName = DSVM_NAME, databricks_workspace= DATABRICKS_WORKSPACE_LOGIN_URL)

@app.route('/intelligence')
@register_breadcrumb(app, '.intelligence', 'Intelligence')
@login_required
def intelligence():
    return render_template('intelligence.html')

@register_breadcrumb(app, '.intelligence.device', '', dynamic_list_constructor=view_device_dlc)
@app.route('/intelligence/<device_id>')
@login_required
def intelligence_device(device_id):
    return render_template('intelligence_device.html', device_id = device_id)

@app.route('/api/intelligence')
@login_required
def get_intelligence():
    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
    devices = iot_hub.get_device_list()
    device_ids = [d.deviceId for d in devices]

    latest_predictions = table_service.query_entities('predictions', filter="PartitionKey eq '_INDEX_'")

    predictions_by_device = dict([(p.RowKey, (p.Prediction, p.Date)) for p in  latest_predictions])
    unknown_predictions = dict([(device_id, ('Unknown', None)) for device_id in device_ids if device_id not in predictions_by_device])
    combined = {**predictions_by_device, **unknown_predictions}

    summary = {
        'Failure predicted': 0,
        'Healthy': 0,
        'Need maintenance': 0,
        'Unknown': 0
    }

    summary_computed = collections.Counter(['Failure predicted' if v[0].startswith('F') else v[0] for v in combined.values()])
    summary.update(summary_computed)

    payload = {
        'predictions': [{
            'deviceId': k,
            'prediction': v[0],
            'lastUpdated': v[1]
        } for (k, v) in combined.items()],
        'summary': summary
    }

    payload_json = json.dumps(payload)
    resp = Response(payload_json)
    resp.headers['Content-type'] = 'application/json'
    return resp

@app.route('/api/intelligence/<device_id>/cycles')
@login_required
def get_intelligence_device_cycles(device_id):
    # cycles_index = table_service.get_entity('cycles', '_INDEX_', device_id)
    # latest_cycles = json.loads(cycles_index['RollingWindow'])

    # max_cycle = latest_cycles[0]
    # min_cycle = latest_cycles[-1]

    all_cycles = table_service.query_entities('cycles', filter="PartitionKey eq '{0}'".format(device_id))
    all_cycles = list(all_cycles)
    all_cycles.sort(key = lambda x: x.RowKey)
    x = []
    y = {}

    for cycle in all_cycles:
        x.append(cycle.RowKey)
        for key in cycle.keys():
            if key in ['PartitionKey', 'RowKey', 'CycleEnd', 'Timestamp', 'etag']:
                continue
            if key not in y:
                y[key] = []
            y[key].append(cycle[key])

    payload = {
        'x': x,
        'y': y
    }

    payload_json = json.dumps(payload)
    resp = Response(payload_json)
    resp.headers['Content-type'] = 'application/json'
    return resp

@app.route('/api/intelligence/<device_id>/predictions')
@login_required
def get_intelligence_device_predictions(device_id):
    all_predictions = table_service.query_entities('predictions', filter="PartitionKey eq '{0}'".format(device_id))
    all_predictions = list(all_predictions)
    all_predictions.sort(key = lambda x: x.RowKey)

    count = len(all_predictions)
    if count > 50:
        all_predictions = all_predictions[-50:-1]

    x = []
    y = []
    for prediction in all_predictions:
        x.append(prediction.RowKey)
        y.append(prediction.Prediction)

    payload = {
        'x': x,
        'y': y
    }

    payload_json = json.dumps(payload)
    resp = Response(payload_json)
    resp.headers['Content-type'] = 'application/json'
    return resp


if __name__ == "__main__":
    app.run('0.0.0.0', 8000, debug=True)
