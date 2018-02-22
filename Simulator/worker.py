import os
import urllib
import zipfile
from azure.storage.blob import PageBlobService
from time import sleep, time
import numpy as np
from scipy.interpolate import interp1d
from scipy import signal
from azure.storage.table import TableService, Entity, TablePermissions

# ACCOUNT_NAME = os.environ['StorageAccountName']
# ACCOUNT_KEY = os.environ['StorageAccountKey']
# CONTAINER_NAME = os.environ['TelemetryContainerName']

ACCOUNT_NAME = "snsr"
ACCOUNT_KEY = "YU4+T41CmWSRyxuV0v1KMKAGRfaz6PXnbcZK8mjgvV3TKj3jqHvU4T0uvrcQ6YWUuLu84KRCi17vIqlhaq1dRA=="
CONTAINER_NAME = "simulation"


table_service = TableService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)
table_service.create_table('devices')

device = {'PartitionKey': 'engine', 'RowKey': '1'}

table_service.insert_or_merge_entity('devices', device)

wk = np.array([1, 2, 3, 5, 12, 15])
Ak = [5, 8, 2/3, 8, 13, 5]

length = 1
fs = 8000

def generate(t, wk, Ak, s = None, last_speed = 0, target_speed = 0):    
    N = length * fs
    ts = np.linspace(t, t + length, num = N)

    x = np.array([0, length]) + t
    points = np.array([last_speed, target_speed])

    rpm = interp1d(x, points, kind='linear')

    f = rpm(ts)

    # interpolation is not positive-preserving
    f[f < 0] = 0

    #fi = np.cumsum(f / fs) / 60
    fi = ts * target_speed / 60

    N = len(fi)
    base = 2 * np.pi * fi
    b = np.array([np.sin(base * w) * a for w, a in zip(wk, Ak)])
    a = b.sum(axis = 0)
    a = a #+ np.random.normal(-0.01, 0.01, N)
    if s is not None:
        a += s
    return np.int16(a/np.max(np.abs(a)) * 32767), points[-1]


az_blob_service = PageBlobService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)

az_blob_service.create_container(CONTAINER_NAME, 
                                 fail_on_exist=False)

#if not az_blob_service.exists(CONTAINER_NAME, "buffer"):
properties = az_blob_service.create_blob(CONTAINER_NAME, "buffer", 512 * 320, sequence_number=0)

i = 0
t = 0
start = time()

last_speed = 0

while True:
    # data = (np.sin(2*np.pi*np.arange(8000)*440/8000)).astype(np.float32)
    # scaled = np.int16(data/np.max(np.abs(data)) * 32767)
    # scaled.resize(16*512)
    # d = scaled.tobytes()

    entity = table_service.get_entity(table_name = 'devices', partition_key = 'engine', row_key = '1')
    
    signal, last_speed = generate(t, wk, Ak, last_speed = last_speed, target_speed = entity.speed)    
    
    signal.resize(16*512)
    signal[fs] = last_speed

    d = signal.tobytes()

    page_start = i * 32 * 512
    page_end = page_start + 32 * 512 - 1    

    r = az_blob_service.set_sequence_number(CONTAINER_NAME, "buffer", sequence_number_action="increment")
    az_blob_service.update_page(CONTAINER_NAME, "buffer", d, page_start, page_end)
    
    i = (i + 1) % 10
    t += 1
    print(time())
    sleep(max(0, start + t - time()))
