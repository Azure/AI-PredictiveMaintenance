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

# STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
# STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

# IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
# IOT_HUB_OWNER_KEY = os.environ['IOT_HUB_OWNER_KEY']
# IOT_HUB_DEVICE_KEY = os.environ['IOT_HUB_DEVICE_KEY']

STORAGE_ACCOUNT_NAME = 'stg3u4jj65poah32'
STORAGE_ACCOUNT_KEY = 'nChg7vz6IgjVyGw6ZCx/xL04HmRH8XJ3ojC70B1LAO34HmeS37Zzyl2VKfYSm3cDGMtuWbdtTjifFvTintU4dg=='

IOT_HUB_NAME = 'iothub-3u4jj65poah32'
IOT_HUB_OWNER_KEY = '1/pqDwtTt3DZ/eitCpSSiIJzoY2/S/K6LU0Dzch55mM='
IOT_HUB_DEVICE_KEY = 'Yq26jolRuECmAWQdLAvW/GnR9TOkxXF1/61c760sjzk='


table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

def device_driver(device):
    iothub_device = IoTHubDevice(IOT_HUB_NAME, device.device_id, IOT_HUB_DEVICE_KEY)
    
    global target_speed
    target_speed = 0

    def device_twin_callback(update_state, payload, user_context):
        target_speed = 900
        print ( "" )
        print ( "Twin callback called with:" )
        print ( "    updateStatus: %s" % update_state )
        print ( "    payload: %s" % payload )

    iothub_device.client.set_device_twin_callback(device_twin_callback, 0)

    while True:
        interval_start = time.time()
        device = device.next_state_device()
        state = device.state()
        
        pl = bytearray(pickle.dumps(device.state()))

        iothub_device.send_message(pl)
        
        device.set_speed((target_speed + device.get_speed()) / 2)

        iothub_device.send_reported_state({
            'speed': state['speed'],
            'temperature': state['temperature'],
            'pressure': state['pressure'],
            'ambientTemperature': state['ambient_temperature'],
            'ambientPressure': state['ambient_pressure']
            })

        time_elapsed = time.time() - interval_start
        print('Cadence: {0}'.format(time_elapsed))
        time.sleep(max(1 - time_elapsed, 0))

if __name__ == '__main__':    
    iot_hub = IoTHub(IOT_HUB_NAME, IOT_HUB_OWNER_KEY)
    
    devices = iot_hub.get_device_list()

    # for device in devices:
    #     device_id = asset.RowKey
        #iot_hub.create_device(device_id)

    processes = []
    for device in devices:
        digital_twin = Device(device.deviceId, make='model1', W = (1, 2, 3, 4, 5, 12, 15), A = (5, 8, 2/3, 9, 8, 13, 5))
        processes.append(Process(target=device_driver, args=(digital_twin, )))

    for process in processes:
        process.daemon = True
        process.start()
        
    while all(map(lambda c: c.is_alive(), processes)):
        time.sleep(3)

    exit(0)

    #devices[3].pressure_factor = 1.5
