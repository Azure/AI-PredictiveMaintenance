import os
import base64
import hmac
import hashlib
import time
import requests
import urllib
import urllib.parse
from multiprocessing import Pool
import json
from random import randint

class D2CMsgSender:
    
    API_VERSION = '2016-02-03'
    TOKEN_VALID_SECS = 300
    TOKEN_FORMAT = 'SharedAccessSignature sig=%s&se=%s&skn=%s&sr=%s'
    
    def __init__(self, connectionString=None):
        if connectionString != None:
            iotHost, keyName, keyValue = [sub[sub.index('=') + 1:] for sub in connectionString.split(";")]
            self.iotHost = iotHost
            self.keyName = keyName
            self.keyValue = keyValue
            
    def _buildExpiryOn(self):
        return '%d' % (time.time() + self.TOKEN_VALID_SECS)
    
    def _buildIoTHubSasToken(self, deviceId):
        resourceUri = '%s/devices/%s' % (self.iotHost, deviceId)
        targetUri = resourceUri.lower()
        expiryTime = self._buildExpiryOn()
        toSign = '%s\n%s' % (targetUri, expiryTime)
        key = base64.b64decode(self.keyValue.encode('utf-8'))
        signature = urllib.parse.quote(
            base64.b64encode(
                hmac.HMAC(key, toSign.encode('utf-8'), hashlib.sha256).digest()
            )
        ).replace('/', '%2F')
        return self.TOKEN_FORMAT % (signature, expiryTime, self.keyName, targetUri)
    
    def sendD2CMsg(self, deviceId, message):
        sasToken = self._buildIoTHubSasToken(deviceId)
        url = 'https://%s/devices/%s/messages/events?api-version=%s' % (self.iotHost, deviceId, self.API_VERSION)
        r = requests.post(url, headers={'Authorization': sasToken}, data=message)
        return r.text, r.status_code

if __name__ == '__main__':
    IOT_HUB_NAME = os.environ['IotHubName']
    IOT_HUB_DEVICE_KEY = os.environ['IotHubDeviceKey']
    DEVICE_COUNT = os.environ['IotDeviceCount']

    connectionString = 'HostName=%s.azure-devices.net;SharedAccessKeyName=device;SharedAccessKey=%s' % (IOT_HUB_NAME, IOT_HUB_DEVICE_KEY)

    #worker = Worker(connectionString, 10)
    #worker.start()
    deviceNo = int(os.path.getctime(os.environ['myTimer'])) % 1000 + 1
    sender = D2CMsgSender(connectionString)
 
    deviceId = 'machine%05d' % (deviceNo)
    m = {'volt': randint(130, 170), 'rotate': randint(500, 600), 'pressure': randint(80, 130), 'vibration': randint(35, 60)}
    message = json.dumps(m)
    print(message)
    print('%s - %s' % (deviceId, sender.sendD2CMsg(deviceId, message)))