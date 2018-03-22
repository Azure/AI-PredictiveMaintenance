import pickle
import requests
import json
import time
import re
import os
from azure.servicebus import ServiceBusService, Message, Queue
from multiprocessing import Queue, Process

BATCH_SIZE = 10
MAX_QUEUE_LENGTH = 10

def parse_connection_string(connection_string):
    connection_string_regex = re.compile('^Endpoint=sb://(.+).servicebus.windows.net/;SharedAccessKeyName=(.+);SharedAccessKey=(.+)$')
    m = connection_string_regex.match(connection_string)
    return m.group(1), m.group(2), m.group(3)

def poll_service_bus(sb_connection_string, sb_queue_name, queue):
    SERVICE_NAMESPACE, SHARED_ACCESS_KEY_NAME, SHARED_ACCESS_KEY_VALUE = parse_connection_string(sb_connection_string)

    bus_service = ServiceBusService(
        service_namespace = SERVICE_NAMESPACE,
        shared_access_key_name = SHARED_ACCESS_KEY_NAME,
        shared_access_key_value = SHARED_ACCESS_KEY_VALUE)

    while True:
            batch = []
            for _ in range(BATCH_SIZE):
                msg = bus_service.receive_queue_message(sb_queue_name, peek_lock=False)
                data = pickle.loads(msg.body)
                # TODO: everything needs to be float, otherwise PySpark breaks
                data['ambient_temperature'] = 20.0
                data['ambient_pressure'] = 101.0
                batch.append(data)
            queue.put(batch)

def score_and_report(queue):    
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

        batch = queue.get()
        json_payload = {
            'input_df': batch
        }

        headers = {
            'Authorization': 'Bearer ' + primary_key,
            'Content-Type': 'application/json'
        }

        r = requests.post(scoring_uri, headers = headers, json = json_payload)
        print(r.text)

def drain_queue(queue):
    """
        If ML WebService can't keep up, this will drain the queue and shed some messages.
        The assumption is that scoring every single message is not necessary to get a sense
        of how the equipment is performing.
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
    queue = Queue()

    service_bus_connection_string = os.environ['SERVICE_BUS_CONNECTION_STRING']
    service_bus_queue_name = os.environ['SERVICE_BUS_QUEUE_NAME']

    producer = Process(target=poll_service_bus, args=(service_bus_connection_string, service_bus_queue_name, queue, ))
    producer.daemon = True

    consumers = [
        Process(target=score_and_report, args=(queue, )),
        Process(target=score_and_report, args=(queue, )),
        Process(target=drain_queue, args=(queue, ))
    ]

    producer.start()

    for consumer in consumers:
        consumer.daemon = True

    # bus_service.receive_queue_message doesn't handle the KeyboardInterrupt well and hangs forever...
    while True:
        time.sleep(60)
