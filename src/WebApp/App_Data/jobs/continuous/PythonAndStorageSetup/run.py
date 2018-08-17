import os
from azure.storage.table import TableService, Entity, TablePermissions
from azure.storage.blob import BlockBlobService

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

table_service.create_table('cycles')
table_service.create_table('features')
table_service.create_table('predictions')
table_service.create_table('databricks')
