import numpy as np
import sys, os, time, glob	
import requests
import json
from flask import Flask, render_template, Response, request
from threading import Thread
from azure.storage.blob import PageBlobService
from azure.storage.blob import BlockBlobService
from datetime import datetime
from azure.storage.table import TableService, Entity, TablePermissions
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
import aztk.models	
import aztk.spark	
from aztk.error import AztkError

app = Flask(__name__)
app.debug = True

# Initialize Flask-Breadcrumbs
Breadcrumbs(app=app)

BATCH_ACCOUNT_NAME = os.environ['BATCH_ACCOUNT_NAME']	
BATCH_ACCOUNT_KEY = os.environ['BATCH_ACCOUNT_KEY']	
BATCH_SERVICE_URL = os.environ['BATCH_ACCOUNT_URL']	
STORAGE_ACCOUNT_SUFFIX = 'core.windows.net'
STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']
TELEMETRY_CONTAINER_NAME = 'telemetry'
IOT_HUB_NAME = os.environ['IOT_HUB_NAME']

table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

@app.route('/')
@register_breadcrumb(app, '.', 'Home')
def home():
    return render_template('home.html')

@app.route('/equipment')
@register_breadcrumb(app, '.equipment', 'Equipment')
def equipment():
    assets = table_service.query_entities('equipment')
    return render_template('equipment.html', assets = assets)

def get_access_token():
    parameters = {
        'grant_type': 'refresh_token',
        'client_id': os.environ['WEBSITE_AUTH_CLIENT_ID'],
        'client_secret': os.environ['WEBSITE_AUTH_CLIENT_SECRET'],
        'refresh_token': request.headers['x-ms-token-aad-refresh-token'],
        'resource': 'https://management.core.windows.net/'
    }

    result = requests.post('https://login.microsoftonline.com/microsoft.com/oauth2/token', data = parameters)
    
    #return json.dumps(result.json())
    access_token = result.json()['access_token']
    return access_token

@app.route('/test')
def test_model_management_access():
    modelManagementSwaggerUrl = os.environ['MODEL_MANAGEMENT_SWAGGER_URL']
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + get_access_token()
    }
    
    #endpoint = 'https://westcentralus.modelmanagement.azureml.net/api/subscriptions/786d6510-8f1e-4ae7-b55b-5178716e6ac8/resourceGroups/pdm09/accounts/mgntek6ttv7wqjwts/models?api-version=2017-09-01-preview'
    endpoint = modelManagementSwaggerUrl
    response = requests.get(endpoint, headers=headers)
    return response.text
    #return json.dumps(response.json())
 

@app.route('/aztkIns')
@register_breadcrumb(app, '.aztkIns', 'AZTK Instructions')
def aztkIns():
    secrets_confg = aztk.spark.models.SecretsConfiguration(
    shared_key=aztk.models.SharedKeyConfiguration(
        batch_account_name = BATCH_ACCOUNT_NAME,
        batch_account_key = BATCH_ACCOUNT_KEY,
        batch_service_url = BATCH_SERVICE_URL,
        storage_account_name = STORAGE_ACCOUNT_NAME,
        storage_account_key = STORAGE_ACCOUNT_KEY,
        storage_account_suffix = STORAGE_ACCOUNT_SUFFIX
    ),

    ssh_pub_key=""
    )

    # create a client
    client = aztk.spark.Client(secrets_confg)

    cluster = client.get_cluster(cluster_id="predictive-maintenance1")
    
    cluster_info = ""
    
    for node in cluster.nodes:
        remote_login_settings = client.get_remote_login_settings(cluster.id, node.id)
        if node.id == cluster.master_node_id:
            cluster_info = '{}:{}'.format(remote_login_settings.ip_address, remote_login_settings.port)
        

    assets = os.environ['WEBSITE_SITE_NAME']
    return render_template('aztkIns.html', assets = assets, cluster_info = cluster_info)

def view_asset_dlc(*args, **kwargs):
    kind = request.view_args['kind']
    tag = request.view_args['tag']
    return [
        {'text': kind, 'url': '/equipment/{0}'.format(kind)},
        {'text': tag, 'url': '/equipment/{0}/{1}'.format(kind, tag)}]


@app.route('/equipment/<kind>/<tag>')
@register_breadcrumb(app, '.equipment.asset', '', dynamic_list_constructor=view_asset_dlc)
def equipment_asset(kind, tag):
    asset = table_service.get_entity('equipment', kind, tag)
    print(asset)
    return render_template('asset.html', assets = [asset])

if __name__ == "__main__":
    table_service.create_table('equipment')

    asset = {'PartitionKey': 'pm1', 'RowKey': 'pm1-353', 'Installed': datetime(2009, 10, 10), 'Model': 'M009'}
    table_service.insert_or_merge_entity('equipment', asset)

    asset = {'PartitionKey': 'pm1', 'RowKey': 'pm1-354', 'Installed': datetime(2001, 1, 13), 'Model': 'M009'}
    table_service.insert_or_merge_entity('equipment', asset)

    app.run('0.0.0.0', 8000, debug=True)
