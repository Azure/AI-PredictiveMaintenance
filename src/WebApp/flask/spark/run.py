import sys, os, time, glob
import aztk.models
import aztk.spark
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

jars = glob.glob(os.path.join(SPARK_JARS_PATH, '*.jar'))

# define spark configuration
spark_conf = aztk.spark.models.SparkConfiguration(
    spark_defaults_conf=os.path.join(SPARK_CONFIG_PATH, 'spark-defaults.conf'),
    spark_env_sh=os.path.join(SPARK_CONFIG_PATH, 'spark-env.sh'),
    jars=jars
)


# configure my cluster
cluster_config = aztk.spark.models.ClusterConfiguration(
    docker_repo='aztk/python:spark2.2.0-python3.6.2-base',
    cluster_id="predictive-maintenance", # Warning: this name must be a valid Azure Blob Storage container name
    vm_count=2,
    # vm_low_pri_count=2, #this and vm_count are mutually exclusive
    vm_size="standard_d2_v2",
    custom_scripts=[],
    spark_configuration=spark_conf
)

cluster = client.create_cluster(cluster_config)
cluster = client.wait_until_cluster_is_ready(cluster.id)

cluster_info.create_user(cluster_id = cluster.id, username = 'admin', password = 'admin')

cluster_info = client.get_cluster(cluster_id=cluster.id)
print(cluster_info)


