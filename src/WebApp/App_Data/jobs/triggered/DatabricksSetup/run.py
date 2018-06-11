import urllib
import os, time
import requests
import json
import uuid
import json

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

databricks_url = os.environ['DATABRICKS_URL']
FEATURIZER_JAR_URL = os.environ['FEATURIZER_JAR_URL'] 
access_token = os.environ['DATABRICKS_TOKEN'] 
IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
EVENT_HUB_ENDPOINT = os.environ['EVENT_HUB_ENDPOINT']
StorageConnectionString = "DefaultEndpointsProtocol=https;AccountName=" + STORAGE_ACCOUNT_NAME + ";AccountKey=" + STORAGE_ACCOUNT_KEY + ";EndpointSuffix=core.windows.net"

bearer_token = 'Bearer ' + access_token
json_data = { 'Authorization': bearer_token }
        
url = FEATURIZER_JAR_URL + '/featurizer_2.11-1.0.jar'  
urllib.request.urlretrieve(url, 'D:/home/site/jars/featurizer_2.11-1.0.jar') 

#upload jar
dbfs_path = "/mnt/pdm/"
bdfs = "/mnt/pdm/featurizer_2.11-1.0.jar"
mkdirs_payload = { 'path': dbfs_path }
resp = requests.post('https://' + databricks_url + '/api/2.0/dbfs/mkdirs',headers=json_data, json = mkdirs_payload).json()

file = 'D:/home/site/jars/featurizer_2.11-1.0.jar'
image = dbfs_path + file
files = {'file': open(file, 'rb')}
put_payload = { 'path' : bdfs, 'overwrite' : 'true' }
# push the images to DBFS
resp = requests.post('https://' + databricks_url + '/api/2.0/dbfs/put', headers=json_data,data = put_payload, files = files).json()

sparkSpec= {
    'spark.speculation' : 'true'
}
payload = {
    'spark_version' : '4.0.x-scala2.11',
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
    'timeout_seconds' : 3600,
    'max_retries' : 1,
    'spark_jar_task' : spark_jar_task
}

run_id = requests.post('https://' + databricks_url + '/api/2.0/jobs/runs/submit', headers=json_data, json = payload).json()
print(run_id)
run_details = requests.get('https://' + databricks_url + '/api/2.0/jobs/runs/get?run_id=' + str(run_id['run_id']), headers=json_data).json()

while run_details['state']['life_cycle_state'] in ['PENDING']:
    run_details = requests.get('https://' + databricks_url + '/api/2.0/jobs/runs/get?run_id=' + str(run_id['run_id']), headers=json_data).json()
    time.sleep(10)

if run_details['state']['life_cycle_state'] == 'RUNNING':
    print("Success")
else:
    errorMessage = 'Run state:' + run_details['state']['life_cycle_state'] + " Reason:" + run_details['state']['state_message']
    print(errorMessage)
    raise Exception(errorMessage)

