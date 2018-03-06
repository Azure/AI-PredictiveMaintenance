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

table_service.create_table('equipment')

asset = {'PartitionKey': 'pm1', 'RowKey': 'pm1-353', 'Installed': datetime(2009, 10, 10), 'Model': 'M009', 'Speed': 1000}
table_service.insert_or_merge_entity('equipment', asset)

asset = {'PartitionKey': 'pm1', 'RowKey': 'pm1-354', 'Installed': datetime(2001, 1, 13), 'Model': 'M009', 'Speed': 1220}
table_service.insert_or_merge_entity('equipment', asset)

file_service = FileService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
file_service.create_share(share_name='notebooks', quota=1)

source=os.environ['NOTEBOOKS_URL']
dest='notebooks.zip'

urllib.request.urlretrieve(source, dest)

with zipfile.ZipFile(dest,"r") as zip_ref:
    zip_ref.extractall("notebooks")

for root, dirs, files in os.walk('notebooks', topdown=True):
    directory = os.path.relpath(root, 'notebooks')
    if directory != '.':
        file_service.create_directory('notebooks', directory)
    for f in files:
        file_service.create_file_from_path(
            'notebooks',
            directory,
            f,
            os.path.join(root, f))

