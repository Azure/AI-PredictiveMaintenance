import os
import io
from azure.storage.blob import BlockBlobService
from azure.storage.blob import AppendBlobService

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

LOGS_CONTAINER_NAME = 'logs'
LOGS_ARCHIVE_CONTAINER_NAME = 'logs-archive'

append_blob_service = AppendBlobService(
    account_name=STORAGE_ACCOUNT_NAME,
    account_key=STORAGE_ACCOUNT_KEY)
block_blob_service = BlockBlobService(
    account_name=STORAGE_ACCOUNT_NAME,
    account_key=STORAGE_ACCOUNT_KEY)

if not block_blob_service.exists(LOGS_ARCHIVE_CONTAINER_NAME):
    block_blob_service.create_container(LOGS_ARCHIVE_CONTAINER_NAME)

generator = append_blob_service.list_blobs(LOGS_CONTAINER_NAME)
for blob in generator:
    with io.BytesIO() as stream:
        append_blob_service.get_blob_to_stream(container_name=LOGS_CONTAINER_NAME, blob_name=blob.name, stream=stream, max_connections=2)
        stream.seek(0)
        block_blob_service.create_blob_from_stream(container_name=LOGS_ARCHIVE_CONTAINER_NAME, blob_name=blob.name, stream = stream, max_connections= 2)
