import json
import time
import requests
import random
import datetime
import dateutil.parser
import logging
from base64 import b64encode, b64decode
from hashlib import sha256
from time import time, sleep
from urllib.parse import quote_plus, urlencode
from hmac import HMAC
from iothub_service_client import IoTHubRegistryManager, IoTHubRegistryManagerAuthMethod, IoTHubDeviceTwin, IoTHubDeviceConnectionState, IoTHubDeviceStatus
from iothub_client import IoTHubClient, IoTHubMessage, IoTHubConfig, IoTHubTransportProvider
from http import HTTPStatus

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

    def delete_device(self, device_id):
        return self.registry_manager.delete_device(device_id)

    def disable_device(self, device_id):
        self.registry_manager.update_device(device_id, '', '', IoTHubDeviceStatus.DISABLED, IoTHubRegistryManagerAuthMethod.SHARED_PRIVATE_KEY)

    def get_device_list(self):
        return self.registry_manager.get_device_list(1000)  # NOTE: this API is marked as deprecated,
                                                            # but Python SDK doesn't seem to offer
                                                            # an alternative yet (03/25/2018).

    def get_device_twin(self, device_id):
        return self.device_twin.get_twin(device_id)

    def __get_sas_token(self, device_id, key, policy, expiry=3600):
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


    def update_twin(self, device_id, payload, etag = '*'):
        """
            Update device twin.
            Unfortunately, Python IoTHub SDK does not implement optimistic concurrency, so
            falling back to the REST API.

            SDK equivalent:
            return self.device_twin.update_twin(device_id, payload)
        """
        twin_url = 'https://{0}/twins/{1}?api-version=2017-06-30'.format(self.iothub_host, device_id)
        sas_token = self.__get_sas_token(device_id, self.owner_key, 'iothubowner')
        headers = {
            'Authorization': sas_token,
            'Content-Type': 'application/json',
            'If-Match': '"{0}"'.format(etag)
        }

        payload_json = json.loads(payload)

        keys = map(str.lower, payload_json.keys())

        if 'tags' not in keys:
            payload_json['tags'] = {}

        if 'desiredproperties' not in keys:
            payload_json['desiredProperties'] = {}

        payload= json.dumps(payload_json)

        r = requests.patch(twin_url, data=payload, headers=headers)

        if r.status_code != HTTPStatus.OK:
            raise Exception(r.text)

        return r.text

    def claim_device(self, client_id):
        while True:
            claimed_device = self.try_claim_device(client_id)
            if claimed_device:
                return claimed_device
            sleep(random.randint(5, 10))

    def try_claim_device(self, client_id):
        try:
            devices = self.get_device_list()
        except:
            return

        random.shuffle(devices)
        for device in devices:
            current_time = datetime.datetime.utcnow().replace(tzinfo=None)
            last_activity_time = dateutil.parser.parse(device.lastActivityTime).replace(tzinfo=None)

            # it seems that sometimes devices remain in a CONNECTED state long after the connection is lost,
            # so claiming CONNECTED devices that have been inactive for at least 10 minutes
            if device.connectionState == IoTHubDeviceConnectionState.CONNECTED and (current_time - last_activity_time).total_seconds() < 600:
                continue

            if device.status == IoTHubDeviceStatus.DISABLED:
                continue

            # attempt to acquire lock using device twin's optimistic concurrency
            twin_data = self.get_device_twin(device.deviceId)
            twin_data_json = json.loads(twin_data)
            random.randint(5, 10)
            etag = twin_data_json['etag']

            twin_tags = None
            if 'tags' not in twin_data_json:
                twin_tags = {}
            else:
                twin_tags = twin_data_json['tags']

            if 'simulated' not in twin_tags or not twin_tags['simulated']:
                continue

            if 'simulator' not in twin_tags:
                continue

            if '_claim' in twin_tags:
                simulator_data = twin_tags['_claim']
                if 'lastClaimed' in simulator_data:
                    last_claimed = dateutil.parser.parse(simulator_data['lastClaimed']).replace(tzinfo=None)
                    if (current_time - last_claimed).total_seconds() < 600:
                        continue

            twin_tags['_claim'] = {
                'clientId': client_id,
                'lastClaimed': current_time.isoformat()
            }

            updated_properties = {
                'tags': twin_tags
            }

            try:
                updated_twin_data = self.update_twin(device.deviceId, json.dumps(updated_properties), etag)
                logging.log(logging.INFO, 'Claimed device %s.', device.deviceId)
                return device, updated_twin_data
            except:
                continue

class IoTHubDevice:
    def __init__(self, iothub_name, device_id, device_key, suffix='.azure-devices.net'):
        self.device_id = device_id
        device_connection_string = 'HostName={0}{1};DeviceId={2};SharedAccessKey={3}'.format(
            iothub_name, suffix, device_id, device_key
        )
        self.client = IoTHubClient(device_connection_string, IoTHubTransportProvider.MQTT) # HTTP, AMQP, MQTT ?

    def send_message(self, message):
        m = IoTHubMessage(message) # string or bytearray
        self.client.send_event_async(m, IoTHubDevice.__dummy_send_confirmation_callback, 0)

    def send_reported_state(self, state, send_reported_state_callback = None, user_context = None):
        if send_reported_state_callback is None:
            send_reported_state_callback = IoTHubDevice.__dummy_send_reported_state_callback
        state_json = json.dumps(state)
        self.client.send_reported_state(state_json, len(state_json), send_reported_state_callback, user_context)

    @staticmethod
    def __dummy_send_confirmation_callback(message, result, user_context):
        pass
        #print(result)

    @staticmethod
    def __dummy_send_reported_state_callback(status_code, user_context):
        pass
        # print(status_code)

if __name__ == '__main__':
    pass
