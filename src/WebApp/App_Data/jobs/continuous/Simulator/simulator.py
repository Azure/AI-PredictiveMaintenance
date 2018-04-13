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


"""
simulator


def pr():
    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)

    devices = iot_hub.get_device_list()

    if len(devices) == 0:
        devices = []
        for i in range(iot_device_count):
            device_id = 'MACHINE-{0:03d}'.format(i)
            device = iot_hub.create_device(device_id)
            devices.append(device)

    healthy_spectral_profile = {
        'W': [1, 2, 3, 4, 5, 12, 15],
        'A': [5, 8, 2/3, 9, 8, 13, 5]
    }

    rotor_imbalance_speactral_profile = {
        'W': [1/2, 1, 2, 3, 5, 7, 12, 18],
        'A': [1, 5, 80, 2/3, 8, 2, 14, 50]
    }

    rotor_imbalance_device_id = devices[-1].deviceId
    low_pressure_device_id = devices[-2].deviceId

    for device in devices:
        twin_data = iot_hub.get_device_twin(device.deviceId)
        twin_data_json = json.loads(twin_data)
        twin_properties = twin_data_json['properties']
        if 'speed' not in twin_properties['desired']:
            twin_properties = {
                'properties': {
                    'desired': {
                        'speed': random.randint(600, 1500),
                        'spectralProfile': json.dumps(healthy_spectral_profile if device.deviceId != rotor_imbalance_device_id else rotor_imbalance_speactral_profile),
                        'pressureFactor': 2 if device.deviceId != low_pressure_device_id else 1.5
                    }
                }
            }

            iot_hub.update_twin(device.deviceId, json.dumps(twin_properties))
"""

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

    device_simulator = SimulatorFactory.create('devices.engines.Engine', report_state, send_telemetry, device_twin)

    def device_twin_callback(update_state, payload, user_context):
        device_simulator.on_update(update_state, payload)

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
