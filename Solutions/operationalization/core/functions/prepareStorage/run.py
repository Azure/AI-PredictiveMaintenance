import os
import urllib
import zipfile
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.file import FileService

ACCOUNT_NAME = os.environ['StorageAccountName']
ACCOUNT_KEY = os.environ['StorageAccountKey']
CONTAINER_NAME = os.environ['TelemetryContainerName']

az_blob_service = BlockBlobService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)

az_blob_service.create_container(CONTAINER_NAME, 
                                 fail_on_exist=False)

file_service = FileService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)
file_service.create_share(share_name='model', quota=1)

source=os.environ['ModelZipUrl']
dest='model.zip'

urllib.request.urlretrieve(source, dest)

with zipfile.ZipFile(dest,"r") as zip_ref:
    zip_ref.extractall("model")

for root, dirs, files in os.walk('model', topdown=True):
    directory = os.path.relpath(root, 'model')
    if directory != '.':
        file_service.create_directory('model', directory)
    for f in files:
        file_service.create_file_from_path(
            'model',
            directory,
            f,
            os.path.join(root, f))

