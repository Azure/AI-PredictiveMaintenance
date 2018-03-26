import numpy as np
import sys, os, time, glob	
import requests
import json
import uuid
import json
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
from aztk_cluster import AztkCluster
from model_management import ModelManagement

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

table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'x-ms-token-aad-refresh-token' not in request.headers:
            return redirect(url_for('setup'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@register_breadcrumb(app, '.', 'Home')
@login_required
def home():
    return render_template('home.html')

@app.route('/telemetry')
@register_breadcrumb(app, '.telemetry', 'Telemetry')
@login_required
def telemetry():
    iot_hub = IoTHub(os.environ['IOT_HUB_NAME'], os.environ['IOT_HUB_OWNER_KEY'])
    assets = table_service.query_entities('equipment')
    devices = iot_hub.get_device_list()
    return render_template('telemetry.html', assets = devices)
    
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
    speed = request.form["speed"]
    payload = {
        'properties': {
            'desired': {
                'speed': int(speed)
            }
        }
    }
    payload_json = json.dumps(payload)

    iot_hub = IoTHub(os.environ['IOT_HUB_NAME'], os.environ['IOT_HUB_OWNER_KEY'])    
    twin_data = iot_hub.update_twin(device_id, payload_json)
    resp = Response(twin_data)
    resp.headers['Content-type'] = 'application/json'
    return resp

def get_access_token():
    parameters = {
        'grant_type': 'refresh_token',
        'client_id': os.environ['WEBSITE_AUTH_CLIENT_ID'],
        'client_secret': os.environ['WEBSITE_AUTH_CLIENT_SECRET'],
        'refresh_token': request.headers['x-ms-token-aad-refresh-token'],
        'resource': 'https://management.core.windows.net/'
    }

    result = requests.post('https://login.microsoftonline.com/microsoft.com/oauth2/token', data = parameters)
    
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
    aztkcluster = AztkCluster()
    clusterDetails = aztkcluster.getCluster()
    return render_template('analytics.html', clusterDetails = clusterDetails)
    
@app.route('/createCluster', methods=['POST'])
@login_required
def createCluster():
    aztkcluster = AztkCluster(request.form['vmsize'], request.form['skutype'], request.form['user'], request.form['password'])
    aztkcluster.createCluster()
    return redirect('/analytics')

@app.route('/deleteCluster', methods=['POST'])
@login_required
def deleteCluster():
    aztkcluster = AztkCluster()
    aztkcluster.deleteCluster()
    return redirect('/analytics')
    
@app.route('/operationalization')
@register_breadcrumb(app, '.operationalization', 'Operationalization')
@login_required
def operationalization():
    return render_template('operationalization.html')


@app.route('/operationalization/<operation>', methods=['GET'])
@app.route('/operationalization/<operation>/<id>', methods=['GET'])
@login_required
def operationalization_get_operation(operation, id = None):
    model_management = ModelManagement(os.environ['MODEL_MANAGEMENT_SWAGGER_URL'], get_access_token())
    operation = operation.lower()
    if operation == 'models':
        mm_response = model_management.get('models?name=failure-prediction-model')
        mm_response_json = json.loads(mm_response.text)    
        resp = Response(json.dumps(mm_response_json['value']))
        resp.headers['Content-type'] = 'application/json'
        return resp
    elif operation == 'manifests':
        mm_response = model_management.get('manifests?manifestName=failure-prediction-manifest')
        mm_response_json = json.loads(mm_response.text)    
        resp = Response(json.dumps(mm_response_json['value']))
        resp.headers['Content-type'] = 'application/json'
        return resp        
    elif operation == 'images':
        if id == None:        
            mm_response = model_management.get('images')
            mm_response_json = json.loads(mm_response.text)    
            resp = Response(json.dumps(mm_response_json['value']))
            resp.headers['Content-type'] = 'application/json'
            return resp
        else:
            mm_response = model_management.get('images/{0}'.format(id))                
            resp = Response(mm_response.text)
            resp.headers['Content-type'] = 'application/json'
            return resp
    elif operation == 'services':
        if id == None:        
            mm_response = model_management.get('services')
            mm_response_json = json.loads(mm_response.text)    
            resp = Response(json.dumps(mm_response_json['value']))
            resp.headers['Content-type'] = 'application/json'
            return resp
        else:
            mm_response = model_management.get('services/{0}'.format(id))                
            resp = Response(mm_response.text)
            resp.headers['Content-type'] = 'application/json'
            return resp            
    elif operation == 'operations':
        mm_response = model_management.get('operations/{0}'.format(id))        
        resp = Response(mm_response.text, status = mm_response.status_code)
        resp.headers['Content-type'] = 'application/json'
        return resp

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
    
    blob_service.copy_blob(container_name, blob_name, file_url)
    
    blob_sas_token = blob_service.generate_blob_shared_access_signature(
        container_name,
        blob_name,
        permission = BlobPermissions.READ,
        expiry = datetime.now() + timedelta(days = 1000))
    
    return blob_service.make_blob_url(container_name, blob_name, sas_token = blob_sas_token)


@app.route('/operationalization/<operation>', methods=['POST'])
@login_required
def operationalization_post_operation(operation):
    model_management = ModelManagement(os.environ['MODEL_MANAGEMENT_SWAGGER_URL'], get_access_token())

    operation = operation.lower()
    if operation == 'registermodel':
        model_blob_url = create_snapshot('notebooks', None, 'model.tar.gz', 'o16n')
        payload = {
    		"name": "failure-prediction-model",
    		"tags": ["pdms"],
    		"url": model_blob_url,
    		"mimeType": "application/json",
    		"description": "Testing",
    		"unpack": True
    	}

        mm_response = model_management.post('models', payload)
        resp = Response(mm_response.text)
        resp.headers['Content-type'] = 'application/json'
        return resp
    elif operation == 'registermanifest':
        model_id = request.form["modelId"]
        
        # take a snapshots of driver.py, score.py, requirements.txt and conda_dependencies.yml
        correlation_guid = str(uuid.uuid4())
        driver_url = create_snapshot('notebooks', None, 'driver.py', 'o16n', correlation_guid)
        score_url = create_snapshot('notebooks', None, 'score.py', 'o16n', correlation_guid)
        schema_url = create_snapshot('notebooks', None, 'service_schema.json', 'o16n', correlation_guid)
        requirements_url = create_snapshot('notebooks', 'aml_config', 'requirements.txt', 'o16n', correlation_guid)
        conda_dependencies_url = create_snapshot('notebooks', 'aml_config', 'conda_dependencies.yml', 'o16n', correlation_guid)
        payload = {
                    "modelIds": [model_id],
                	"name": "failure-prediction-manifest",        	
                	"description": "Failure prediction manifest",
                	"driverProgram": "driver",            
                	"assets": [{
                		"id": "driver",
                		"mimeType": "application/x-python",
                		"url": driver_url,
                		"unpack": False
                	},
                    {
                		"id": "score",
                		"mimeType": "application/x-python",
                		"url": score_url,
                		"unpack": False
                	},
                    {
                		"id": "schema",
                		"mimeType": "application/json",
                		"url": schema_url,
                		"unpack": False
                	}],
                	"targetRuntime": {
                		"runtimeType": "SparkPython",
                		"properties": {
                			"pipRequirements": requirements_url,
                            "condaEnvFile": conda_dependencies_url
                		}
                	},
                	"webserviceType": "Realtime",
                    "modelType": "Registered"
                }
                
        mm_response = model_management.post('manifests', payload)
        resp = Response(mm_response.text)
        resp.headers['Content-type'] = 'application/json'
        return resp
    elif operation == 'createimage':
        manifest_id = request.form["manifestId"]
        
        payload = {
            "computeResourceId": os.environ['ML_COMPUTE_RESOURCE_ID'],
    		"name": "failure-prediction-image",    		
    		"manifestId": manifest_id,    		
    		"imageType": "Docker"
    	}
        
        mm_response = model_management.post('images', payload)
        
        operation_location = mm_response.headers['operation-location']                       
        resp = Response(status = mm_response.status_code)
        resp.headers['Operation-Location'] = operation_location
        return resp
    elif operation == 'createservice':
        image_id = request.form["imageId"]
        name = request.form["name"]
        
        payload = {
            "computeResource": {
                "id": os.environ['ML_COMPUTE_RESOURCE_ID'],
                "type": "Cluster"
            },
    		"name": name,    		
    		"imageId": image_id
    	}
        
        mm_response = model_management.post('services', payload)
        
        resp = Response(mm_response.text, status = mm_response.status_code)
        if mm_response.status_code == 202:
            operation_location = mm_response.headers['operation-location']                       
            resp.headers['Operation-Location'] = operation_location
        return resp
    elif operation == 'consume':
        service_id = request.form["serviceId"]               
        mm_response_service = model_management.get('services/{0}'.format(service_id))
        mm_response_service_keys = model_management.get('services/{0}/keys'.format(service_id))
        
        mm_response_service_json = json.loads(mm_response_service.text)
        mm_response_service_keys_json = json.loads(mm_response_service_keys.text)
        
        scoring_config = json.dumps({
            'id': service_id,
            'scoringUri': mm_response_service_json['scoringUri'],
            'primaryKey': mm_response_service_keys_json['primaryKey']
        })
        
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../App_Data/scoring.json'))

        with open(config_path, 'w') as f:
            f.write(scoring_config)
        
        resp = Response(scoring_config)
        resp.headers['Content-type'] = 'application/json'
        return resp

@app.route('/intelligence')
@register_breadcrumb(app, '.intelligence', 'Intelligence')
@login_required
def intelligence():    
    return render_template('intelligence.html')


if __name__ == "__main__":
    app.run('0.0.0.0', 8000, debug=True)
