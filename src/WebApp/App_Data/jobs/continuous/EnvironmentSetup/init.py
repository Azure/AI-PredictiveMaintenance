import os
import urllib
import zipfile
from datetime import datetime
from azure.storage.table import TableService, Entity, TablePermissions
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.file import FileService


STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

table_service.create_table('cluster')

file_service = FileService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
file_service.create_share(share_name='azureml-project', quota=1)
file_service.create_share(share_name='azureml-share', quota=1)

source=os.environ['AML_ASSETS_URL']
dest='azureml_project.zip'

urllib.request.urlretrieve(source, dest)

with zipfile.ZipFile(dest,"r") as zip_ref:
    zip_ref.extractall("azureml-project")

for root, dirs, files in os.walk('azureml-project', topdown=True):
    directory = os.path.relpath(root, 'azureml-project')
    if directory != '.':
        file_service.create_directory('azureml-project', directory)
    for f in files:
        file_service.create_file_from_path(
            'azureml-project',
            directory,
            f,
            os.path.join(root, f))
