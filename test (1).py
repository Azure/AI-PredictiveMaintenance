import json
import base64
import requests
import os
import time


#upload jar
dbfs_path = "/mnt/laks/"
bdfs = "/mnt/laks/avro.jar"
mkdirs_payload = { 'path': dbfs_path }
resp = requests.post('https://southeastasia.azuredatabricks.net/api/2.0/dbfs/mkdirs',headers={"Authorization": "Bearer dapiecd0e7f5cec3af7e411ed5d9ef244edc"}, json = mkdirs_payload).json()
print(resp)

file = 'D:/home/site/wwwroot/flask/spark/spark/jars/spark-avro_2.11-4.0.0.jar'
image = dbfs_path + file
files = {'file': open(file, 'rb')}
put_payload = { 'path' : bdfs, 'overwrite' : 'true' }
# push the images to DBFS
resp = requests.post('https://southeastasia.azuredatabricks.net/api/2.0/dbfs/put', headers={"Authorization": "Bearer dapiecd0e7f5cec3af7e411ed5d9ef244edc"},data = put_payload, files = files).json()
print(resp)



#create cluster

sparkSpec= {
    'spark.speculation' : 'true'
}
payload = {
    'cluster_name' : 'laks-cluster2',
    'spark_version' : '4.0.x-scala2.11',
    'node_type_id' : 'Standard_D3_v2',
    'spark_conf' : sparkSpec,
    'num_workers' : 2
}

cluster_details = requests.post('https://southeastasia.azuredatabricks.net/api/2.0/clusters/create', headers={"Authorization": "Bearer dapiecd0e7f5cec3af7e411ed5d9ef244edc"}, json = payload).json()
print(cluster_details)

clusterid = cluster_details['cluster_id']

#get cluster
request_url = 'https://southeastasia.azuredatabricks.net/api/2.0/clusters/get?cluster_id=' + clusterid
cluster_details = requests.get(request_url, headers={"Authorization": "Bearer dapiecd0e7f5cec3af7e411ed5d9ef244edc"}, json = payload).json()
print(cluster_details)
while cluster_details['state'] != 'RUNNING' and cluster_details['state'] != 'TERMINATED':
    time.sleep(10)
    cluster_details = requests.get(request_url, headers={"Authorization": "Bearer dapiecd0e7f5cec3af7e411ed5d9ef244edc"}, json = payload).json()

#create job

jar_path = "dbfs:" + bdfs
jar = {
    'jar' : jar_path
}

maven = {
    'maven' : {
        'coordinates' : 'org.jsoup:jsoup:1.7.2'
    }
}

libraries = [jar, maven]

spark_jar_task= {
    'main_class_name' : 'com.databricks.ComputeModels'
}

payload = {
    'name' : 'Job1',
    'existing_cluster_id' : clusterid,
    'libraries' : libraries,
    'timeout_seconds' : 3600,
    'max_retries' : 1,
    'spark_jar_task' : spark_jar_task
}

job_details = requests.post('https://southeastasia.azuredatabricks.net/api/2.0/jobs/create', headers={"Authorization": "Bearer dapiecd0e7f5cec3af7e411ed5d9ef244edc"}, json = payload).json()
print(job_details)

jobid = job_details['job_id']

#run a job

jar_params = ["", ""]

payload = {
    'job_id' : jobid,
    'jar_params' : jar_params
}

job_run_details = requests.post('https://southeastasia.azuredatabricks.net/api/2.0/jobs/run-now', headers={"Authorization": "Bearer dapiecd0e7f5cec3af7e411ed5d9ef244edc"}, json = payload).json()
print(job_run_details)

runid = job_run_details['run_id']