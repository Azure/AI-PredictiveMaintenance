import sys, os, time, glob
import aztk.models
import aztk.spark
from aztk.error import AztkError

if "IotHubName" not in os.environ:
    exit()

BATCH_ACCOUNT_NAME = os.environ['BatchAccountName']
BATCH_ACCOUNT_KEY = os.environ['BatchAccountKey']
BATCH_SERVICE_URL = os.environ['BatchAccountUrl']
STORAGE_ACCOUNT_SUFFIX = 'core.windows.net'
STORAGE_ACCOUNT_NAME = os.environ['StorageAccountName']
STORAGE_ACCOUNT_KEY = os.environ['StorageAccountKey']
TELEMETRY_CONTAINER_NAME = os.environ['TelemetryContainerName']
IOT_HUB_NAME = os.environ['IotHubName']

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

modelFileShare = aztk.models.FileShare(STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY, 'model', '/mnt/model')

# configure my cluster
cluster_config = aztk.spark.models.ClusterConfiguration(
    docker_repo='aztk/python:spark2.2.0-python3.6.2-base',
    cluster_id="predictive-maintenance", # Warning: this name must be a valid Azure Blob Storage container name
    vm_count=2,
    # vm_low_pri_count=2, #this and vm_count are mutually exclusive
    vm_size="standard_d2_v2",
    custom_scripts=[],
    spark_configuration=spark_conf,
    file_shares=[modelFileShare]
)

cluster = client.create_cluster(cluster_config)
cluster = client.wait_until_cluster_is_ready(cluster.id)

wasbUrlInput = "wasb://{0}@{1}.blob.{2}/{3}/*/*/*/*/*/*".format(
            TELEMETRY_CONTAINER_NAME,
            STORAGE_ACCOUNT_NAME,
            STORAGE_ACCOUNT_SUFFIX,
            IOT_HUB_NAME)

wasbUrlOutput = "wasbs://{0}@{1}.blob.{2}/{3}".format(
            'predictions',  
            STORAGE_ACCOUNT_NAME,
            STORAGE_ACCOUNT_SUFFIX,
            'predictions.csv')

app = aztk.spark.models.ApplicationConfiguration(
    name="featurize-and-score-{}".format(int(time.time())),
    application=os.path.join(SPARK_APPLICATION_PATH, 'featurize_and_score.py'),
    application_args=[wasbUrlInput, wasbUrlOutput, STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY]
)

client.submit(cluster.id, app)
client.wait_until_application_done(cluster.id, app.name)

# get logs for app, print to console
app_logs = client.get_application_log(cluster_id=cluster.id, application_name=app.name)
print(app_logs.log)

# kill cluster
client.delete_cluster(cluster.id)
