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
