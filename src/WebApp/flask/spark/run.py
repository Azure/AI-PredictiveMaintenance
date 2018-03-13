import sys, os, time, glob
import aztk.models
import aztk.spark
import json
from pprint import pprint
from aztk.error import AztkError

if "IOT_HUB_NAME" not in os.environ:
    exit()

BATCH_ACCOUNT_NAME = os.environ['BATCH_ACCOUNT_NAME']
BATCH_ACCOUNT_KEY = os.environ['BATCH_ACCOUNT_KEY']
BATCH_SERVICE_URL = os.environ['BATCH_ACCOUNT_URL']
STORAGE_ACCOUNT_SUFFIX = 'core.windows.net'
STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']
TELEMETRY_CONTAINER_NAME = 'telemetry'
IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
USER_NAME = sys.argv[1]
PASSWORD = sys.argv[2]

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

# list available clusters
clusters = client.list_clusters()

SPARK_CONFIG_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), 'spark', '.config'))
SPARK_JARS_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), 'spark', 'jars'))
SPARK_APPLICATION_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), 'spark', 'application'))

SPARK_CORE_SITE = os.path.join(SPARK_CONFIG_PATH, 'core-site.xml')

f = open(SPARK_CORE_SITE,'r')
message = f.read()
message = message.replace('STORAGE_ACCOUNT_NAME', STORAGE_ACCOUNT_NAME)
message = message.replace('STORAGE_ACCOUNT_KEY', STORAGE_ACCOUNT_KEY)
f.close()

f = open(SPARK_CORE_SITE,'w')
f.write(message)
f.close()

jars = glob.glob(os.path.join(SPARK_JARS_PATH, '*.jar'))

# define spark configuration
spark_conf = aztk.spark.models.SparkConfiguration(
    spark_defaults_conf=os.path.join(SPARK_CONFIG_PATH, 'spark-defaults.conf'),
    spark_env_sh=os.path.join(SPARK_CONFIG_PATH, 'spark-env.sh'),
    core_site_xml=SPARK_CORE_SITE,
    jars=jars
)

modelCustomScript = aztk.models.CustomScript("jupyter", "D:/home/site/wwwroot/flask/spark/customScripts/jupyter.sh","all-nodes")
modelFileShare = aztk.models.FileShare(STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY, 'notebooks', '/mnt/notebooks')
# configure my cluster
cluster_config = aztk.spark.models.ClusterConfiguration(
    docker_repo='aztk/python:spark2.2.0-python3.6.2-base',
    cluster_id="predictive-maintenance", # Warning: this name must be a valid Azure Blob Storage container name
    vm_count=2,
    # vm_low_pri_count=2, #this and vm_count are mutually exclusive
    vm_size="standard_d2_v2",
    custom_scripts=[modelCustomScript],
    spark_configuration=spark_conf,
    file_shares=[modelFileShare]
)

cluster = client.create_cluster(cluster_config)
cluster = client.wait_until_cluster_is_ready(cluster.id)


client.create_user(cluster_id = "predictive-maintenance", username = USER_NAME, password = PASSWORD)

cluster = client.get_cluster(cluster_id="predictive-maintenance")

node_count = '{}'.format(cluster.total_current_nodes)

print("")
print("Cluster         %s", cluster.id)
print("------------------------------------------")
print("State:          %s", cluster.visible_state)
print("Node Size:      %s", cluster.vm_size)
print("Nodes:          %s", node_count)
print("| Dedicated:    %s", '{}'.format(cluster.current_dedicated_nodes))
print("| Low priority: %s", '{}'.format(cluster.current_low_pri_nodes))
print("")

print_format = '|{:^36}| {:^19} | {:^21}| {:^10} | {:^8} |'
print_format_underline = '|{:-^36}|{:-^21}|{:-^22}|{:-^12}|{:-^10}|'
print(print_format.format("Nodes", "State", "IP:Port", "Dedicated", "Master"))
print(print_format_underline.format('', '', '', '', ''))
    
for node in cluster.nodes:
    remote_login_settings = client.get_remote_login_settings(cluster.id, node.id)
    print(
        print_format.format(
            node.id,
            node.state.value,
            '{}:{}'.format(remote_login_settings.ip_address, remote_login_settings.port),
            "*" if node.is_dedicated else '',
            '*' if node.id == cluster.master_node_id else '')
    )
print('')


