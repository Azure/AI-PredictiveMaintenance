import urllib
import os, time
import requests
import json
import uuid
import json
from azure.storage.table import TableService, Entity, TablePermissions

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

DATABRICKS_WORKSPACE_URL = os.environ['DATABRICKS_WORKSPACE_URL']
FEATURIZER_JAR_URL = os.environ['FEATURIZER_JAR_URL']
DATABRICKS_ACCESS_TOKEN = os.environ['DATABRICKS_TOKEN']
IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
EVENT_HUB_ENDPOINT = os.environ['EVENT_HUB_ENDPOINT']
STORAGE_ACCOUNT_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=" + STORAGE_ACCOUNT_NAME + ";AccountKey=" + STORAGE_ACCOUNT_KEY + ";EndpointSuffix=core.windows.net"

table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
databricks_cluster_details = table_service.query_entities('databricks', filter="PartitionKey eq 'pdm'")

headers = { 'Authorization': 'Bearer ' + DATABRICKS_ACCESS_TOKEN }

if not list(databricks_cluster_details):
    jar_local_path = 'D:/home/site/jars/featurizer_2.11-1.0.jar'
    jar_dbfs_path = "/mnt/pdm/featurizer_2.11-1.0.jar"
    
    urllib.request.urlretrieve(FEATURIZER_JAR_URL, 'D:/home/site/jars/featurizer_2.11-1.0.jar')

    #upload jar
    dbfs_path = "/mnt/pdm/"
    
    mkdirs_payload = { 'path': dbfs_path }
    resp = requests.post(DATABRICKS_WORKSPACE_URL + '/api/2.0/dbfs/mkdirs', headers=headers, json = mkdirs_payload).json()
    
    files = {'file': open(file, 'rb')}
    put_payload = { 'path' : bdfs, 'overwrite' : 'true' }
    # push the images to DBFS
    resp = requests.post(DATABRICKS_WORKSPACE_URL '/api/2.0/dbfs/put', headers=headers, data = put_payload, files = files).json()

    sparkSpec= {
        'spark.speculation' : 'true'
    }
    payload = {
        'spark_version' : '4.1.x-scala2.11',
        'node_type_id' : 'Standard_D3_v2',
        'spark_conf' : sparkSpec,
        'num_workers' : 2
    }

    #run job

    jar_path = "dbfs:" + bdfs
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

    jar_params = [EVENT_HUB_ENDPOINT,IOT_HUB_NAME,StorageConnectionString]

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

    run_details = requests.post(DATABRICKS_WORKSPACE_URL + '/api/2.0/jobs/runs/submit', headers=headers, json = payload).json()
    runid = run_details['run_id']
    databricks_details = {'PartitionKey': 'pdm', 'RowKey': 'pdm', 'run_id' : str(runid)}
    table_service.insert_entity('databricks', databricks_details)
    print(run_details)
else:
    runid = list(databricks_cluster_details)[0]['run_id']

run_details = requests.get(DATABRICKS_WORKSPACE_URL + '/api/2.0/jobs/runs/get?run_id=' + str(runid), headers=headers).json()
run_state = run_details['state']['life_cycle_state']
while run_state in ['PENDING', 'RESIZING']:
    run_details = requests.get(DATABRICKS_WORKSPACE_URL + '/api/2.0/jobs/runs/get?run_id=' + str(runid), headers=headers).json()
    run_state = run_details['state']['life_cycle_state']
    time.sleep(10)

if run_state in ['RUNNING']:
    print("Success")
else:
    errorMessage = 'Run state:' + run_details['state']['life_cycle_state'] + " Reason:" + run_details['state']['state_message']
    print(errorMessage)
    table_service.delete_entity('databricks', 'pdm', 'pdm')
    raise Exception(errorMessage)
