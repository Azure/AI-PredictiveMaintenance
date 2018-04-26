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
from iot_hub import IoTHub, IoTHubDevice
from azure.storage.blob import AppendBlobService
from devices import SimulatorFactory

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
    append_blob_service = AppendBlobService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
    logs_container_name = 'logs'
    append_blob_service.create_container(logs_container_name, fail_on_exist=False)
    log_blob_name = '{0}.log'.format(device_id)

    def report_state(state):
        iothub_device.send_reported_state(state)

    def send_telemetry(data):
        iothub_device.send_message(data)

    def log(message, code, level):
        if not append_blob_service.exists(logs_container_name, log_blob_name):
            append_blob_service.create_blob(logs_container_name, log_blob_name, if_none_match='*', )

        level_name = logging.getLevelName(level)

        output = io.StringIO()
        entry_data = [str(datetime.datetime.utcnow()) + 'Z', level_name, device_id, code, message]
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(entry_data)
        entry_text = output.getvalue()
        append_blob_service.append_blob_from_text(logs_container_name, log_blob_name, entry_text)

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
        claim_and_run_device(driver_unique_id)

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
