import os
import numpy as np
import pickle
import random
from multiprocessing import Pool, TimeoutError, cpu_count
from multiprocessing.dummy import Pool as DummyPool
from multiprocessing import Process
from iot_hub import IotHub
from device import Device
from azure.storage.table import TableService, Entity, TablePermissions
import datetime
import time

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
IOT_HUB_OWNER_KEY = os.environ['IOT_HUB_OWNER_KEY']
IOT_HUB_DEVICE_KEY = os.environ['IOT_HUB_DEVICE_KEY']

table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

def device_driver(device):
    iot_hub = IotHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY, IOT_HUB_DEVICE_KEY)

    def get_target_speed(device):
        asset = table_service.get_entity('equipment', device.make, device.device_id)
        return asset['Speed']

    while True:
        interval_start = time.time()
        device = device.next_state_device()
        
        pl = pickle.dumps(device.state())
        iot_hub.send_device_message(device.device_id, pl)

        target_speed = get_target_speed(device)
        device.set_speed((target_speed + device.get_speed()) / 2)
        time_elapsed = time.time() - interval_start
        print('Cadence: {0}'.format(time_elapsed))
        time.sleep(max(1 - time_elapsed, 0))

if __name__ == '__main__':

    assets = table_service.query_entities('equipment')
    
    for asset in assets:
        device_id = asset.RowKey
        #iot_hub.create_device(device_id)

    devices = []
    processes = []
    for asset in assets:
        device = Device(asset.RowKey, make=asset.PartitionKey, W = (1, 2, 3, 4, 5, 12, 15), A = (5, 8, 2/3, 9, 8, 13, 5))
        processes.append(Process(target=device_driver, args=(device, )))

    for process in processes:
        process.daemon = True
        process.start()
        
    while all(map(lambda c: c.is_alive(), processes)):
        time.sleep(3)

    exit(0)

    #devices[3].pressure_factor = 1.5
