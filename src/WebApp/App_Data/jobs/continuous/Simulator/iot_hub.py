from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from urllib.parse import quote_plus, urlencode
from hmac import HMAC
from iothub_service_client import IoTHubRegistryManager, IoTHubRegistryManagerAuthMethod, IoTHubDeviceTwin
from iothub_client import IoTHubClient, IoTHubMessage, IoTHubConfig, IoTHubTransportProvider

class IotHub:
    def __init__(self, iothub_name, owner_key, device_key, suffix='.azure-devices.net'):
        self.iothub_name = iothub_name
        self.owner_key = owner_key
        self.device_key = device_key
        self.suffix = suffix
        self.owner_connection_string ='HostName={0}{1};SharedAccessKeyName=iothubowner;SharedAccessKey={2}'.format(self.iothub_name, self.suffix, owner_key)
        self.registry_manager = IoTHubRegistryManager(self.owner_connection_string)
        self.device_twin = IoTHubDeviceTwin(self.owner_connection_string)
        self.__device_clients = {}
    
    def create_device(self, device_id, primary_key = '', secondary_key = ''):
        return self.registry_manager.create_device(device_id, primary_key, secondary_key, IoTHubRegistryManagerAuthMethod.SHARED_PRIVATE_KEY)

    def get_device_twin(self, device_id):
        return self.device_twin.get_twin(device_id)

    def send_device_message(self, device_id, message):
        if device_id not in self.__device_clients:
            device_connection_string = self.__get_device_connection_string(device_id, 'device', self.device_key)
            client = IoTHubClient(device_connection_string, IoTHubTransportProvider.HTTP) # HTTP, AMQP, MQTT ?
            self.__device_clients[device_id] = client
        else:
            client = self.__device_clients[device_id]

        m = IoTHubMessage(message) # string or bytearray
        client.send_event_async(m, IotHub.__dummy_send_confirmation_callback, 0)

    def __get_device_connection_string(self, device, policy_name, key, expiry=3600):        
        ttl = time() + expiry
        uri = '{0}{1}/devices/{2}'.format(self.iothub_name, self.suffix, device)
        sign_key = "%s\n%d" % ((quote_plus(uri)), int(ttl))
        
        signature = b64encode(HMAC(b64decode(key), sign_key.encode('utf-8'), sha256).digest())

        rawtoken = {
            'sr' :  uri,
            'sig': signature,
            'se' : str(int(ttl))
        }

        if policy_name is not None:
            rawtoken['skn'] = policy_name

        sas = 'SharedAccessSignature ' + urlencode(rawtoken)
        return 'HostName={0}{1};DeviceId={2};SharedAccessSignature={3}'.format(self.iothub_name, self.suffix, device, sas)
    
    @staticmethod
    def __dummy_send_confirmation_callback(message, result, user_context):
        print(result)

if __name__ == '__main__':
    iot_hub = IotHub('iothub-sz3hgnexzw2ty', 'A0GOfwxELSw6mxaw4nHYfT1ivdhBTYOK1+OVDmAOKxw=', 'Lgpcbv1X7BhRc49M+8bbZ8Z1Q7O1dv3FMtVq6kcltq0=')
    print(iot_hub.get_device_twin('test_device'))
    iot_hub.send_device_message('test_device', "hello")
