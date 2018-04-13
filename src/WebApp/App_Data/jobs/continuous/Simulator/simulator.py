import os
import pickle
import random
import uuid
import datetime
import time
import json
import numpy as np
from multiprocessing import Pool, TimeoutError, cpu_count
from multiprocessing.dummy import Pool as DummyPool
from multiprocessing import Process
from iot_hub import IoTHub, IoTHubDevice
from azure.storage.table import TableService, Entity, TablePermissions
from devices import SimulatorFactory

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
IOT_HUB_OWNER_KEY = os.environ['IOT_HUB_OWNER_KEY']
IOT_HUB_DEVICE_KEY = os.environ['IOT_HUB_DEVICE_KEY']

def device_driver():
    driver_unique_id = str(uuid.uuid4())

    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
    device, device_twin = iot_hub.claim_device(driver_unique_id)

    device_twin_json = json.loads(device_twin)
    device_id = device_twin_json['deviceId']

    iothub_device = IoTHubDevice(IOT_HUB_NAME, device_id, device.primaryKey)

    def report_state(state):
        iothub_device.send_reported_state(state)

    def send_telemetry(data):
        iothub_device.send_message(data)

    device_simulator = SimulatorFactory.create('devices.engines.Engine', report_state, send_telemetry)
    device_simulator.initialize(device_twin_json)

    def device_twin_callback(update_state, payload, user_context):
        device_simulator.on_update(update_state, json.loads(payload))

    iothub_device.client.set_device_twin_callback(device_twin_callback, 0)

    device_simulator.run()

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
