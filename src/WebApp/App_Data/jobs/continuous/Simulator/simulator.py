import os
import numpy as np
import pickle
import random
from iot_hub import DeviceManager, D2CMessageSender
from device import Device
from azure.storage.table import TableService, Entity, TablePermissions

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

IOT_HUB_NAME = os.environ['IOT_HUB_NAME']
IOT_HUB_OWNER_KEY = os.environ['IOT_HUB_OWNER_KEY']
IOT_HUB_DEVICE_KEY = os.environ['IOT_HUB_DEVICE_KEY']

table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

connectionString ='HostName=%s.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=%s' % (IOT_HUB_NAME, IOT_HUB_OWNER_KEY)

assets = table_service.query_entities('equipment')

dm = DeviceManager(connectionString)

for asset in assets:
    deviceId = asset.RowKey
    dm.createDeviceId(deviceId)
    print(dm.retrieveDeviceId(deviceId))

print(dm.listDeviceIds())

connectionString = 'HostName=%s.azure-devices.net;SharedAccessKeyName=device;SharedAccessKey=%s' % (IOT_HUB_NAME, IOT_HUB_DEVICE_KEY)

sender = D2CMessageSender(connectionString)

def process(device_id, state):
    samples.append(state['vibration'])
    # sending iothub message    
    pl = pickle.dumps(state)
    print('%s - %s' % (device_id, sender.sendD2CMsg(device_id, pl)))
    #print(state)

devices = []
for asset in assets:
    devices.append(
        Device(asset.RowKey, W = (1, 2, 3, 4, 5, 12, 15), A = (5, 8, 2/3, 9, 8, 13, 5))
    )


#devices[3].pressure_factor = 1.5

for _ in range(1):
    for device in devices:
        schedule = (
            (random.randint(20, 40), random.randint(999, 1100)),
            (random.randint(20, 40), random.randint(1400, 1600)),
            (random.randint(3, 10), random.randint(400, 600)),
            (random.randint(3, 5), 0))
        samples = []
        device.simulate_schedule(schedule, process)
        wave_data = np.concatenate(np.array(samples, dtype=np.int16))
        from scipy.io.wavfile import write
        write('test-{0}.wav'.format(device.device_id), 8000, wave_data)
