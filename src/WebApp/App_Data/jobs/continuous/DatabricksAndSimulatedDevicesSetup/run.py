import urllib
import os
import time
import requests
import uuid
import json
import zipfile
import base64
from azure.storage.table import TableService, Entity, TablePermissions

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

DATABRICKS_API_BASE_URL = os.environ['DATABRICKS_WORKSPACE_URL'] + '/api/'
FEATURIZER_JAR_URL = os.environ['FEATURIZER_JAR_URL']
DATABRICKS_TOKEN = os.environ['DATABRICKS_TOKEN']
IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
EVENT_HUB_ENDPOINT = os.environ['EVENT_HUB_ENDPOINT']
TMP = os.environ['TMP']
NOTEBOOKS_URL = os.environ['NOTEBOOKS_URL']
STORAGE_ACCOUNT_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=" + STORAGE_ACCOUNT_NAME + ";AccountKey=" + STORAGE_ACCOUNT_KEY + ";EndpointSuffix=core.windows.net"

def call_api(uri, method=requests.get, json=None, data=None, files=None):
    headers = { 'Authorization': 'Bearer ' + DATABRICKS_TOKEN }
    #TODO: add retries
    response = method(DATABRICKS_API_BASE_URL + uri, headers=headers, json=json, data=data, files=files)
    if response.status_code != 200:
        raise Exception('Error when calling Databricks API {0}. Response:\n{1}'.format(uri, response.text))
    return response

def get_last_run_id():
    table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
    databricks_cluster_details_entries = table_service.query_entities('databricks', filter="PartitionKey eq 'pdm'")
    databricks_cluster_details = list(databricks_cluster_details_entries)
    if databricks_cluster_details:
        return databricks_cluster_details[0]['run_id']
    return None

def set_last_run_id(run_id):
    table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
    databricks_details = {'PartitionKey': 'pdm', 'RowKey': 'pdm', 'run_id' : str(run_id)}
    table_service.insert_or_replace_entity('databricks', databricks_details)

def get_run(run_id):
    run_state = 'PENDING'
    while run_state in ['PENDING', 'RESIZING']:
        run_details = call_api('2.0/jobs/runs/get?run_id=' + str(run_id)).json()
        run_state = run_details['state']['life_cycle_state']
        time.sleep(10)
    return run_details

def is_job_active(run_details):
    run_state = run_details['state']['life_cycle_state']
    return run_state == 'RUNNING'

def upload_notebooks_databricks():
    #upload notebook to app service
    notebooks_zip_local_path = os.path.join(TMP, 'Notebooks.zip')
    urllib.request.urlretrieve(NOTEBOOKS_URL, notebooks_zip_local_path)

    zip_ref = zipfile.ZipFile(notebooks_zip_local_path, 'r')
    notebooks_local_path = os.path.join(TMP, 'Notebooks')
    zip_ref.extractall(notebooks_local_path)

    #upload feature engineering notebook to databricks workspace
    featureEngineering_local_path = os.path.join(notebooks_local_path, 'FeatureEngineering.ipynb')
    files = {'file': open(featureEngineering_local_path, 'rb')}
    bdfs = "/FeatureEngineering"
    put_payload = { 'path' : bdfs, 'overwrite' : 'true', 'language':'PYTHON', 'format':'JUPYTER' }
    resp = call_api('2.0/workspace/import', method=requests.post, data=put_payload, files = files).json()

    #upload data ingestion notebook to databricks workspace
    dataIngestion_local_path = os.path.join(notebooks_local_path, 'DataIngestion.ipynb')
    files = {'file': open(dataIngestion_local_path, 'rb')}
    bdfs = "/DataIngestion"
    put_payload = { 'path' : bdfs, 'overwrite' : 'true', 'language':'PYTHON', 'format':'JUPYTER' }
    resp = call_api('2.0/workspace/import', method=requests.post, data=put_payload, files = files).json()

upload_notebooks_databricks()
data = '{"DataIngestion" : { "STORAGE_ACCOUNT_NAME" :"' + STORAGE_ACCOUNT_NAME + '", "STORAGE_ACCOUNT_KEY" :"' + STORAGE_ACCOUNT_KEY +'", "TELEMETRY_CONTAINER_NAME" : "telemetry", "LOG_TABLE_NAME" : "Logs", "DATA_ROOT_FOLDER" : "/root"}}'

file = open('D:/home/site/NotebookEnvironmentVariablesConfig.json','w')
file.write(data)
file.close()
    
config_path = '/root/NotebookEnvironmentVariablesConfig.json'
files = {'file': open('D:/home/site/NotebookEnvironmentVariablesConfig.json', 'rb')}
put_payload = { 'path' : config_path, 'overwrite' : 'true' }

call_api('2.0/dbfs/put', method=requests.post, data=put_payload, files=files)

last_run_id = get_last_run_id()

if last_run_id is not None and is_job_active(get_run(last_run_id)):
    exit(0)

jar_local_path = os.path.join(TMP, 'featurizer_2.11-1.0.jar')

dbfs_path = '/predictive-maintenance/jars/'
jar_dbfs_path = dbfs_path + 'featurizer_2.11-1.0.jar'

urllib.request.urlretrieve(FEATURIZER_JAR_URL, jar_local_path)

mkdirs_payload = { 'path': dbfs_path }
call_api('2.0/dbfs/mkdirs', method=requests.post, json=mkdirs_payload)

files = {'file': open(jar_local_path, 'rb')}
put_payload = { 'path' : jar_dbfs_path, 'overwrite' : 'true' }

call_api('2.0/dbfs/put', method=requests.post, data=put_payload, files=files)

sparkSpec= {
    'spark.speculation' : 'true'
}
payload = {
    'spark_version' : '4.2.x-scala2.11',
    'node_type_id' : 'Standard_D3_v2',
    'spark_conf' : sparkSpec,
    'num_workers' : 1
}

#run job
jar_path = "dbfs:" + jar_dbfs_path
jar = {
    'jar' : jar_path
}

maven_coordinates = {
    'coordinates' : 'com.microsoft.azure:azure-eventhubs-spark_2.11:2.3.1'
}

maven = {
    'maven' : maven_coordinates
}

libraries = [jar, maven]
jar_params = [EVENT_HUB_ENDPOINT, IOT_HUB_NAME, STORAGE_ACCOUNT_CONNECTION_STRING]

spark_jar_task= {
    'main_class_name' : 'com.microsoft.ciqs.predictivemaintenance.Featurizer',
    'parameters' : jar_params
}

payload = {
    "run_name": "featurization_task",
    "new_cluster" : payload,
    'libraries' : libraries,
    'max_retries' : 1,
    'spark_jar_task' : spark_jar_task
}

run_job = True
i = 0
while run_job and i < 5:
    run_details = call_api('2.0/jobs/runs/submit', method=requests.post, json=payload).json()
    run_id = run_details['run_id']
    set_last_run_id(run_id)
    run_details = get_run(run_id)
    i= i + 1
    if not is_job_active(run_details):
        run_job = True
        errorMessage = 'Unable to create Spark job. Run ID: {0}. Failure Details: {1}'.format(run_id, run_details['state']['state_message'])
        print(errorMessage)
    else:
        run_job = False
