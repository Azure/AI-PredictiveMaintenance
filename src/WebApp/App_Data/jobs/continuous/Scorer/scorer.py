import pickle
import requests
import json
import time
import re
import os
import sys
import datetime
from azure.servicebus import ServiceBusService, Message, Queue
from multiprocessing import Queue, Process
from azure.storage.table import TableService, Entity, TablePermissions

BATCH_SIZE = 5
MAX_QUEUE_LENGTH = 10

def parse_connection_string(connection_string):
    connection_string_regex = re.compile('^Endpoint=sb://(.+).servicebus.windows.net/;SharedAccessKeyName=(.+);SharedAccessKey=(.+)$')
    m = connection_string_regex.match(connection_string)
    return m.group(1), m.group(2), m.group(3)

def preprocess_telemetry_entity(telemetry_entity):
    # everything needs to be float, otherwise PySpark breaks
    for k in telemetry_entity:
        if type(telemetry_entity[k]) is int:
            telemetry_entity[k] = float(telemetry_entity[k])

def poll_service_bus(sb_connection_string, sb_queue_name, queue):
    SERVICE_NAMESPACE, SHARED_ACCESS_KEY_NAME, SHARED_ACCESS_KEY_VALUE = parse_connection_string(sb_connection_string)

    bus_service = ServiceBusService(
        service_namespace = SERVICE_NAMESPACE,
        shared_access_key_name = SHARED_ACCESS_KEY_NAME,
        shared_access_key_value = SHARED_ACCESS_KEY_VALUE)

    while True:
        timestamps = []
        device_ids = []
        telemetry_entities = []
        for _ in range(BATCH_SIZE):
            msg = bus_service.receive_queue_message(sb_queue_name, peek_lock=False)
            enqueued_time = datetime.datetime.strptime(msg.broker_properties['EnqueuedTimeUtc'], '%a, %d %b %Y %H:%M:%S %Z')
            device_id = msg.custom_properties['iothub-connection-device-id']
            telemetry_entity = pickle.loads(msg.body)
            preprocess_telemetry_entity(telemetry_entity)
            timestamps.append(enqueued_time)
            device_ids.append(device_id)
            telemetry_entities.append(telemetry_entity)

        queue.put((timestamps, device_ids, telemetry_entities))

def write_scores(predictions_queue):
    STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
    STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']
    table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
    table_service.create_table('predictions')
    
    aggregate_predictions = {}

    while True:
        prediction_row = predictions_queue.get()
        stripped_datetime = str(prediction_row[0].replace(second=0, microsecond=0))
        device_id = prediction_row[1]
        prediction = prediction_row[2]

        if stripped_datetime not in aggregate_predictions:
            aggregate_predictions[stripped_datetime] = {}

        if device_id not in aggregate_predictions[stripped_datetime]:
            aggregate_predictions[stripped_datetime][device_id] = {}

        if prediction not in aggregate_predictions[stripped_datetime][device_id]:
            aggregate_predictions[stripped_datetime][device_id][prediction] = 0

        aggregate_predictions[stripped_datetime][device_id][prediction] += 1
        
        if len(aggregate_predictions) < 2:
            continue 

        timestamps = list(aggregate_predictions.keys())
        timestamps.sort()

        oldest_timestamp = timestamps[0]
        device_ids = aggregate_predictions[oldest_timestamp].keys()
        predictions = aggregate_predictions[oldest_timestamp].values()

        for partition_key, row_key, data in zip([oldest_timestamp] * len(device_ids), device_ids, predictions):
            entity = {
                'PartitionKey': partition_key,
                'RowKey': row_key,
                'Prediction': max(data, key=data.get),
                'Debug': json.dumps(data)
            }

            # TODO: implement optimistic concurrency and merge to run this truly at scale.
            # For now, simply inserting the record...
            table_service.insert_entity('predictions', entity)
        
        del aggregate_predictions[oldest_timestamp]
        


def score(telemetry_queue, predictions_queue):
    while True:
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../scoring.json'))
        if not os.path.isfile(config_path):
            print('Scoring configuration missing.')
            time.sleep(10)
            continue

        with open(config_path, 'r') as f:
            scoring_config = json.loads(f.read())
            scoring_uri = scoring_config['scoringUri']
            primary_key = scoring_config['primaryKey']

        print('Using ML scoring URI: {0}'.format(scoring_uri))

        batch = telemetry_queue.get()
        timestamps, device_ids, telemetry_entities = batch

        json_payload = {
            'input_df': telemetry_entities
        }

        headers = {
            'Authorization': 'Bearer ' + primary_key,
            'Content-Type': 'application/json'
        }

        response = requests.post(scoring_uri, headers = headers, json = json_payload)
        
        if response.status_code == 200:
            for prediction in zip(timestamps, device_ids, response.json()):
                predictions_queue.put(prediction)
        else:
            print('error')

def drain_queue(queue):
    """
        If ML WebService can't keep up, this will drain the queue and shed some messages.
        The assumption is that scoring every single message is not necessary to get a sense
        of how the equipment is performing in real time.
    """
    while True:
        queue_size = queue.qsize()
        if queue_size > MAX_QUEUE_LENGTH:
            try:
                queue.get()
            except:
                pass
        else:
            time.sleep(5)

if __name__ == '__main__':
    telemetry_queue = Queue()
    predictions_queue = Queue()

    service_bus_connection_string = os.environ['SERVICE_BUS_CONNECTION_STRING']
    service_bus_queue_name = os.environ['SERVICE_BUS_QUEUE_NAME']
    
    processes = [
        Process(target=poll_service_bus, args=(service_bus_connection_string, service_bus_queue_name, telemetry_queue)),
        Process(target=score, args=(telemetry_queue, predictions_queue)),
        Process(target=score, args=(telemetry_queue, predictions_queue)),
        Process(target=write_scores, args=(predictions_queue, )),
        Process(target=drain_queue, args=(telemetry_queue, ))
    ]

    for process in processes:
        process.daemon = True
        process.start()
    
    # producer.join()
    # bus_service.receive_queue_message doesn't handle the KeyboardInterrupt well and hangs forever...
    while all(map(lambda c: c.is_alive(), processes)):
        sys.stdout.flush()
        time.sleep(3)
