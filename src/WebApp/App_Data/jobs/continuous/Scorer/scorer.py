import os
import requests
import json
import time
from azure.storage.table import TableService, Entity, TablePermissions

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']
SCORE_URL = os.environ['SCORE_URL']
table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

def call_score_web_service(url, payload):
    response = requests.post(url, json=payload)
    return response.json()

def publish(prediction):
    prediction_text = prediction[1] or 'Healthy'
    entity = {
        'PartitionKey': prediction[0][0],
        'RowKey': prediction[0][1],
        'Prediction': prediction_text
    }
    table_service.insert_or_replace_entity('predictions', entity)

    index_entity = {
        'PartitionKey': '_INDEX_',
        'RowKey': prediction[0][0],
        'Date': prediction[0][1],
        'Prediction': prediction_text
    }
    table_service.insert_or_replace_entity('predictions', index_entity)


def score():
    indices = table_service.query_entities('cycles', filter="PartitionKey eq '_INDEX_'")

    latest_features = []
    for index in indices:
        machine_id = index.RowKey
        rolling_window = json.loads(index.RollingWindow)
        for cycle in rolling_window:
            try:
                features = table_service.get_entity('features', machine_id, cycle)
                latest_features.append(features)
                break
            except:
                pass

    payload = [json.loads(x.FeaturesJson) for x in latest_features]

    predictions = zip([(x.PartitionKey, x.CycleEnd) for x in latest_features], call_score_web_service(SCORE_URL, payload))

    for prediction in predictions:
        publish(prediction)

if __name__ == '__main__':
    while True:
        score()
        time.sleep(30)
