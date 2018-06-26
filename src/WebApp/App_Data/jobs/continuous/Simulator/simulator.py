import os
import io
import pickle
import random
import uuid
import datetime
import time
import json
import numpy as np
import logging
import csv
from multiprocessing import Pool, TimeoutError, cpu_count
from multiprocessing.dummy import Pool as DummyPool
from multiprocessing import Process
from iot_hub_helpers import IoTHub, IoTHubDevice
from devices import SimulatorFactory
from azure.storage.table import TableService, Entity, TablePermissions

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
IOT_HUB_OWNER_KEY = os.environ['IOT_HUB_OWNER_KEY']
IOT_HUB_DEVICE_KEY = os.environ['IOT_HUB_DEVICE_KEY']

def claim_and_run_device(driver_id):
    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
    device, device_twin = iot_hub.claim_device(driver_id)
    device_twin_json = json.loads(device_twin)
    device_id = device_twin_json['deviceId']

    iothub_device = IoTHubDevice(IOT_HUB_NAME, device_id, device.primaryKey)

    table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
    table_service.create_table('logs', fail_on_exist=False)

    def report_state(state):
        iothub_device.send_reported_state(state)

    def send_telemetry(data):
        iothub_device.send_message(data)

    def log(message, code, level):
        level_name = logging.getLevelName(level)
        log_entity = {
            'PartitionKey': device_id,
            'RowKey': uuid.uuid4().hex,
            'Level': level_name,
            'Code': code,
            'Message': message,
            '_Driver': driver_id
        }
        print(', '.join([driver_id, device_id, str(level_name), str(code), str(message)]))
        table_service.insert_or_replace_entity('logs', log_entity)
        if level == logging.CRITICAL:
            # disable device
            iot_hub.disable_device(device_id)

    device_simulator = SimulatorFactory.create('devices.engines.Engine', report_state, send_telemetry, log)
    if not device_simulator.initialize(device_twin_json):
        return

    def device_twin_callback(update_state, payload, user_context):
        device_simulator.on_update(str(update_state), json.loads(payload))

    iothub_device.client.set_device_twin_callback(device_twin_callback, 0)

    device_simulator.run()

def device_driver():
    driver_unique_id = str(uuid.uuid4())
    while True:
        try:
            claim_and_run_device(driver_unique_id)
            logging.log(logging.WARNING, 'Driver {0} finished execution.'.format(driver_unique_id))
        except Exception as e:
            logging.log(logging.ERROR, 'Driver {0} threw an exception: {1}.'.format(driver_unique_id, str(e)))
        except:
            logging.log(logging.ERROR, 'Driver {0} threw an exception.')

if __name__ == '__main__':
    device_driver_count = 20

    processes = []
    for _ in range(device_driver_count):
        processes.append(Process(target=device_driver))

    for process in processes:
        process.daemon = True
        process.start()

    while all(map(lambda c: c.is_alive(), processes)):
        time.sleep(3)
