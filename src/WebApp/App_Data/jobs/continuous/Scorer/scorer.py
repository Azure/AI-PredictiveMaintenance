import os
import requests
import json

from azure.storage.table import TableService, Entity, TablePermissions

if __name__ == '__main__':
    storage_account_name = os.environ['STORAGE_ACCOUNT_NAME']
    storage_account_key = os.environ['STORAGE_ACCOUNT_KEY']
    score_url = 'http://40.114.125.83:5001/score'
    pass
