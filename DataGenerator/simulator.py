from iot_hub import DeviceManager, D2CMessageSender
from device import Device
from azure.storage.table import TableService, Entity, TablePermissions
import numpy as np
import pickle
import random

# IOT_HUB_NAME = os.environ['IotHubName']
# IOT_HUB_OWNER_KEY = os.environ['IotHubOwnerKey']
# DEVICE_COUNT = int(os.environ['IotDeviceCount'])

IOT_HUB_NAME = 'iothub-w74e5yvuyvfs2'
IOT_HUB_OWNER_KEY = 'Pl839QpYfaiBMbbOt8RxbrLk2RvOpuy+z+aSsecr+28='
IOT_HUB_DEVICE_KEY = '1n7jyr+tccLWN1FYgOBh9PAhEiZ0RDg1EGmpxo50o4w='

ACCOUNT_NAME = "stgw74e5yvuyvfs2"
ACCOUNT_KEY = "CKXt/8SpgY6JHfVwBQUkwBCDeBKyJzQV10sgut3L4dS/bjKlSxQsPedHkrI7td8I0NBWJoQOSkcChGo1MIf9Cw=="

table_service = TableService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)

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
