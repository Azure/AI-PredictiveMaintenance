import pickle
import requests
import json
from azure.servicebus import ServiceBusService, Message, Queue

batch_size = 20

scoringServiceConfig = {"scoringUri": "http://52.161.160.30/api/v1/service/test1/score", "primaryKey": "bc1fcda1665e4a868ec88365ee008c6f"}

bus_service = ServiceBusService(
    service_namespace='serviceBusmuw4i6tq5532i',
    shared_access_key_name='Listen',
    shared_access_key_value='K7ZOyKkcSgGY9n/gA/rAKeO2y9lWHEtM9NR3NnXJpx4=')

while True:
    batch = []

    for _ in range(batch_size):
        msg = bus_service.receive_queue_message('servicebusqueuemuw4i6tq5532i', peek_lock=False)
        data = pickle.loads(msg.body)
        # TODO: everything needs to be float, otherwise PySpark breaks
        data['ambient_temperature'] = 20.0
        data['ambient_pressure'] = 101.0
        batch.append(data)

    json_payload = {
        'input_df': batch
    }

    headers = {
        'Authorization': 'Bearer ' + scoringServiceConfig['primaryKey'],
        'Content-Type': 'application/json'
    }
    
    r = requests.post(scoringServiceConfig['scoringUri'], headers = headers, json = json_payload)
    
    print(r.text)

