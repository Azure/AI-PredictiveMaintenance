import os
import numpy as np
import pickle
import random
from multiprocessing import Pool, TimeoutError, cpu_count
from multiprocessing.dummy import Pool as DummyPool
from multiprocessing import Process
from iot_hub import IoTHub, IoTHubDevice
from device import Device
from azure.storage.table import TableService, Entity, TablePermissions
import datetime
import time
import json

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
IOT_HUB_OWNER_KEY = os.environ['IOT_HUB_OWNER_KEY']
IOT_HUB_DEVICE_KEY = os.environ['IOT_HUB_DEVICE_KEY']

table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

def device_driver(device_id):
    global digital_twin
    global target_speed
    
    iothub_device = IoTHubDevice(IOT_HUB_NAME, device_id, IOT_HUB_DEVICE_KEY)
    target_speed = 0
    digital_twin = None

    def device_twin_callback(update_state, payload, user_context):
        global digital_twin
        global target_speed

        properties_json = json.loads(payload)
        if str(update_state) == 'COMPLETE':
            properties_json = properties_json['desired']
            spectral_profile = json.loads(properties_json['spectralProfile'])
            pressure_factor = properties_json['pressureFactor']
            digital_twin = Device(device_id, make='model1', W = spectral_profile['W'], A = spectral_profile['A'])
            digital_twin.pressure_factor = pressure_factor
        if 'speed' in properties_json:
            target_speed = properties_json['speed']

    iothub_device.client.set_device_twin_callback(device_twin_callback, 0)

    while True:
        if digital_twin == None:
            time.sleep(1)
            continue
        
        interval_start = time.time()
        state = digital_twin.next_state()
        
        if state['speed'] == 0 and target_speed == 0:
            # the device is fully turned off
            time.sleep(1)
            continue

        pl = bytearray(pickle.dumps(state))
        iothub_device.send_message(pl)
        
        digital_twin.set_speed((target_speed + digital_twin.get_speed()) / 2)

        iothub_device.send_reported_state({
            'speed': state['speed'],
            'temperature': state['temperature'],
            'pressure': state['pressure'],
            'ambientTemperature': state['ambient_temperature'],
            'ambientPressure': state['ambient_pressure']
            })

        time_elapsed = time.time() - interval_start
        # print('Cadence: {0}'.format(time_elapsed))
        time.sleep(max(1 - time_elapsed, 0))

if __name__ == '__main__':
    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
    
    iot_device_count = 10

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

    processes = []
    for device in devices:        
        processes.append(Process(target=device_driver, args=(device.deviceId, )))

    for process in processes:
        process.daemon = True
        process.start()

    while all(map(lambda c: c.is_alive(), processes)):
        time.sleep(3)
