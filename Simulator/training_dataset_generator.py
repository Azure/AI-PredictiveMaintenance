from iot_hub import DeviceManager, D2CMessageSender
from device import Device
import numpy as np
import pickle
import random

# IOT_HUB_NAME = os.environ['IotHubName']
# IOT_HUB_OWNER_KEY = os.environ['IotHubOwnerKey']
# DEVICE_COUNT = int(os.environ['IotDeviceCount'])

IOT_HUB_NAME = 'iothub-w74e5yvuyvfs2'
IOT_HUB_OWNER_KEY = 'Pl839QpYfaiBMbbOt8RxbrLk2RvOpuy+z+aSsecr+28='
IOT_HUB_DEVICE_KEY = '1n7jyr+tccLWN1FYgOBh9PAhEiZ0RDg1EGmpxo50o4w='
DEVICE_COUNT = 4

connectionString ='HostName=%s.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=%s' % (IOT_HUB_NAME, IOT_HUB_OWNER_KEY)

dm = DeviceManager(connectionString)
for i in range(DEVICE_COUNT):
    deviceId = 'machine%05d' % (i + 1)
    dm.createDeviceId(deviceId)
    #print(dm.retrieveDeviceId(deviceId))

#print(dm.listDeviceIds())


connectionString = 'HostName=%s.azure-devices.net;SharedAccessKeyName=device;SharedAccessKey=%s' % (IOT_HUB_NAME, IOT_HUB_DEVICE_KEY)

sender = D2CMessageSender(connectionString)

def process(device_id, state):
    samples.append(state['vibration'])
    # sending iothub message
    iot_device_id = 'machine%05d' % (device_id)
    pl = pickle.dumps(state)
    print('%s - %s' % (iot_device_id, sender.sendD2CMsg(iot_device_id, pl)))
    #print(state)

devices = [
    Device(1, W = (1, 2, 3, 4, 5, 12, 15), A = (5, 8, 2/3, 9, 8, 13, 5)),
    Device(2, W = (1/3, 2/3, 3/4, 1, 2, 3, 4, 5, 12, 15), A = (40, 20, 25, 5, 8, 2/3, 9, 8, 13, 5)),
    Device(3, W = (1, 2, 3, 4, 5, 12, 15, 17), A = (5, 8, 2/3, 9, 8, 13, 5, 80)),
    Device(4, W = (1, 2, 3, 4, 5, 12, 15), A = (5, 8, 2/3, 9, 8, 13, 5))
]

devices[3].pressure_factor = 1.5

for _ in range(500):    
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
        write('test{:02}.wav'.format(device.device_id), 8000, wave_data)
