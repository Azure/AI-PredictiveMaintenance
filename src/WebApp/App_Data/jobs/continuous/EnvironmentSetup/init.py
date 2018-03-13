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

asset = {'PartitionKey': 'pm1', 'RowKey': 'pm1-355', 'Installed': datetime(2003, 3, 23), 'Model': 'M009', 'Speed': 1330}
table_service.insert_or_merge_entity('equipment', asset)

asset = {'PartitionKey': 'pm1', 'RowKey': 'pm1-356', 'Installed': datetime(2005, 3, 1), 'Model': 'M009', 'Speed': 800}
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
        fi = open(os.path.join(root, f),'r')
        message = fi.read()
        message = message.replace('STORAGE_ACCOUNT_NAME_TO_REPLACE', STORAGE_ACCOUNT_NAME)
        fi.close()

        fi = open(os.path.join(root, f),'w')
        fi.write(message)
        fi.close()

        file_service.create_file_from_path(
            'notebooks',
            directory,
            f,
            os.path.join(root, f))

