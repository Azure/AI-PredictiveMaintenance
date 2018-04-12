import json
import requests
from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from urllib.parse import quote_plus, urlencode
from hmac import HMAC
from iothub_service_client import IoTHubRegistryManager, IoTHubRegistryManagerAuthMethod, IoTHubDeviceTwin, IoTHubDeviceConnectionState
from iothub_client import IoTHubClient, IoTHubMessage, IoTHubConfig, IoTHubTransportProvider

class IoTHub:
    def __init__(self, iothub_name, owner_key, suffix='.azure-devices.net'):
        self.iothub_name = iothub_name
        self.owner_key = owner_key
        self.iothub_host = iothub_name + suffix
        self.owner_connection_string ='HostName={0};SharedAccessKeyName=iothubowner;SharedAccessKey={1}'.format(self.iothub_host, owner_key)
        self.registry_manager = IoTHubRegistryManager(self.owner_connection_string)
        self.device_twin = IoTHubDeviceTwin(self.owner_connection_string)
        self.__device_clients = {}
    
    def create_device(self, device_id, primary_key = '', secondary_key = ''):
        return self.registry_manager.create_device(device_id, primary_key, secondary_key, IoTHubRegistryManagerAuthMethod.SHARED_PRIVATE_KEY)

    def get_device_list(self):
        return self.registry_manager.get_device_list(1000)  # NOTE: this API is marked as deprecated,
                                                            # but Python SDK doesn't seem to offer
                                                            # an alternative yet (03/25/2018).

    def get_device_twin(self, device_id):
        return self.device_twin.get_twin(device_id)



    def __get_device_connection_string(self, device_id, key, policy, expiry=3600):
        ttl = time() + expiry
        uri = '{0}/devices/{1}'.format(self.iothub_host, device_id)
        sign_key = "%s\n%d" % ((quote_plus(uri)), int(ttl))
        
        signature = b64encode(HMAC(b64decode(key), sign_key.encode('utf-8'), sha256).digest())

        rawtoken = {
            'sr' :  uri,
            'sig': signature,
            'se' : str(int(ttl))
        }
        
        rawtoken['skn'] = policy

        sas = 'SharedAccessSignature ' + urlencode(rawtoken)
        return sas
        # return 'HostName={0}{1};DeviceId={2};SharedAccessSignature={3}'.format(self.iothub_name, self.suffix, device_id, sas)


    def update_twin(self, device_id, payload):
        twin_url = 'https://{0}/twins/{1}?api-version=2017-06-30'.format(self.iothub_host, device_id)
        sas_token = self.__get_device_connection_string(device_id, self.owner_key, 'iothubowner')
        headers = {
            'Authorization': sas_token,
            'If-Match': '*'
        }

        payload_dict = {
            'DeviceId': device_id,
            'Tags': {}
        }

        payload= json.dumps(payload_dict)

        r = requests.patch(twin_url, data=payload, headers=headers)
        print(r.text)
        return None
        # return self.device_twin.update_twin(device_id, payload)

    def acquire_device(self):
        devices = self.get_device_list()
        for device in devices:
            if device.connectionState == IoTHubDeviceConnectionState.DISCONNECTED:
                # attempt to acquire lock using device twin's optimistic concurrency
                twin_data = self.get_device_twin(device.deviceId)
                twin_data_json = json.loads(twin_data)

                twin_tags = None
                if 'tags' not in twin_data_json:
                    twin_tags = {}
                else:
                    twin_tags = twin_data_json['tags']
                
                twin_tags['hello'] = 'yes561'

                #twin_tags['$etag'] = twin_data_json['etag']
                #twin_tags['etag'] = twin_data_json['etag']

                updated_properties = {
                    #'$etag': twin_data_json['etag'] + 'ts',
                    #'etag': twin_data_json['etag'],
                    'tags': twin_tags
                }

                updated_twin_data = self.update_twin(device.deviceId, json.dumps(updated_properties))
                print(updated_twin_data)

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

    def send_reported_state(self, state, send_reported_state_callback = None, user_context = None):
        if send_reported_state_callback is None:
            send_reported_state_callback = IoTHubDevice.__dummy_send_reported_state_callback
        state_json = json.dumps(state)        
        self.client.send_reported_state(state_json, len(state_json), send_reported_state_callback, user_context)

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
        #pass

    @staticmethod
    def __dummy_send_reported_state_callback(status_code, user_context):
        pass
        # print(status_code)
        
if __name__ == '__main__':
    iot_hub = IoTHub('iothub-sz3hgnexzw2ty', 'A0GOfwxELSw6mxaw4nHYfT1ivdhBTYOK1+OVDmAOKxw=')
    print(iot_hub.get_device_twin('test_device'))
