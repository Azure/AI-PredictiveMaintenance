import json
from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from urllib.parse import quote_plus, urlencode
from hmac import HMAC
from iothub_service_client import IoTHubRegistryManager, IoTHubRegistryManagerAuthMethod, IoTHubDeviceTwin
from iothub_client import IoTHubClient, IoTHubMessage, IoTHubConfig, IoTHubTransportProvider

class IoTHub:
    def __init__(self, iothub_name, owner_key, suffix='.azure-devices.net'):
        self.iothub_name = iothub_name
        self.owner_key = owner_key
        self.suffix = suffix
        self.owner_connection_string ='HostName={0}{1};SharedAccessKeyName=iothubowner;SharedAccessKey={2}'.format(self.iothub_name, self.suffix, owner_key)
        self.registry_manager = IoTHubRegistryManager(self.owner_connection_string)
        self.device_twin = IoTHubDeviceTwin(self.owner_connection_string)
        self.__device_clients = {}
    
    def create_device(self, device_id, primary_key = '', secondary_key = ''):
        return self.registry_manager.create_device(device_id, primary_key, secondary_key, IoTHubRegistryManagerAuthMethod.SHARED_PRIVATE_KEY)

    def get_device_twin(self, device_id):
        return self.device_twin.get_twin(device_id)

class IoTHubDevice:
    def __init__(self, iothub_name, device_id, device_key, suffix='.azure-devices.net'):
        self.iothub_name = iothub_name
        self.device_id = device_id
        self.device_key = device_key
        self.policy_name = 'device'
        self.suffix = suffix
        device_connection_string = self.__get_device_connection_string()
        self.client = IoTHubClient(device_connection_string, IoTHubTransportProvider.MQTT) # HTTP, AMQP, MQTT ? 

    def send_message(self, message):
        m = IoTHubMessage(message) # string or bytearray
        self.client.send_event_async(m, IoTHubDevice.__dummy_send_confirmation_callback, 0)

    def send_reported_state(self, state):
        state_json = json.dumps(state)
        self.client.send_reported_state(state_json, len(state_json), IoTHubDevice.__dummy_send_reported_state_callback, 0)

    def __get_device_connection_string(self, expiry=3600):        
        ttl = time() + expiry
        uri = '{0}{1}/devices/{2}'.format(self.iothub_name, self.suffix, self.device_id)
        sign_key = "%s\n%d" % ((quote_plus(uri)), int(ttl))
        
        signature = b64encode(HMAC(b64decode(self.device_key), sign_key.encode('utf-8'), sha256).digest())

        rawtoken = {
            'sr' :  uri,
            'sig': signature,
            'se' : str(int(ttl))
        }

        if self.policy_name is not None:
            rawtoken['skn'] = self.policy_name

        sas = 'SharedAccessSignature ' + urlencode(rawtoken)
        return 'HostName={0}{1};DeviceId={2};SharedAccessSignature={3}'.format(self.iothub_name, self.suffix, self.device_id, sas)
    
    @staticmethod
    def __dummy_send_confirmation_callback(message, result, user_context):
        print(result)

    @staticmethod
    def __dummy_send_reported_state_callback(status_code, user_context):
        print(status_code)
        
if __name__ == '__main__':
    iot_hub = IoTHub('iothub-sz3hgnexzw2ty', 'A0GOfwxELSw6mxaw4nHYfT1ivdhBTYOK1+OVDmAOKxw=')
    print(iot_hub.get_device_twin('test_device'))
