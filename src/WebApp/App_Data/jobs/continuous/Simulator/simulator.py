import os
import numpy as np
import pickle
import random
#import concurrent.futures
from multiprocessing import Pool, TimeoutError, cpu_count
from multiprocessing.dummy import Pool as DummyPool

from iot_hub import DeviceManager, D2CMessageSender
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

ownerConnectionString ='HostName=%s.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=%s' % (IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
deviceConnectionString = 'HostName=%s.azure-devices.net;SharedAccessKeyName=device;SharedAccessKey=%s' % (IOT_HUB_NAME, IOT_HUB_DEVICE_KEY)

dm = DeviceManager(ownerConnectionString)

sender = D2CMessageSender(deviceConnectionString)

def get_target_speed(device):
    asset = table_service.get_entity('equipment', device.make, device.device_id)
    return asset['Speed']

def process(device):
    # sending iothub message
    pl = pickle.dumps(device.next_state())
    return sender.sendD2CMsg(device.device_id, pl)


if __name__ == '__main__':

    assets = table_service.query_entities('equipment')
    
    for asset in assets:
        deviceId = asset.RowKey
        dm.createDeviceId(deviceId)
        print(dm.retrieveDeviceId(deviceId))

    print(dm.listDeviceIds())

    devices = []
    for asset in assets:
        devices.append(
            Device(asset.RowKey, make=asset.PartitionKey, W = (1, 2, 3, 4, 5, 12, 15), A = (5, 8, 2/3, 9, 8, 13, 5))
        )

    devices[3].pressure_factor = 1.5
    print('CPU count: {0}'.format(cpu_count()))
    pool = Pool(processes=cpu_count())
    dummyPool = DummyPool(100)

    async_result = None
    target_speeds = None

    #for _ in range(19):
    while True:
        interval_start = time.time()

        states = None

        if async_result is None:
            #start = time.time()
            async_result = dummyPool.map_async(get_target_speed, devices)
        
        if target_speeds is None or async_result.ready():
            target_speeds = async_result.get()
            async_result = None

        print(target_speeds)

        for device, target_speed in zip(devices, target_speeds):
            device.set_speed((target_speed + device.get_speed()) / 2)

        start = time.time()
        devices = pool.map(Device.next_state_device, devices)
        end = time.time()
        print(end - start)

        start = time.time()
        dummyPool.starmap(process, zip(devices))
        end = time.time()
        print(end - start)

        time_elapsed = time.time() - interval_start
        print('Cadence: {0}'.format(time_elapsed))
        time.sleep(max(1 - time_elapsed, 0))

        # for device, state in zip(devices, states):
        #     process(device.device_id, state)
            # from scipy.io.wavfile import write
            # write('test-{0}.wav'.format(device.device_id), 8000, wave_data)
