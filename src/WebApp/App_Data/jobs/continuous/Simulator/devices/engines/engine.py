import time
import json
import pickle
from devices.simulated_device import SimulatedDevice
from .device import Device

class Engine(SimulatedDevice):
    def initialize(self):


        self.__digital_twin = Device(W = spectral_profile['W'], A = spectral_profile['A'])

    def on_update(self, update_state, payload):
            global digital_twin
            global target_speed

            properties_json = json.loads(payload)
            if str(update_state) == 'COMPLETE':
                properties_json = properties_json['desired']
                spectral_profile = json.loads(properties_json['spectralProfile'])
                pressure_factor = properties_json['pressureFactor']
                digital_twin =
                digital_twin.pressure_factor = pressure_factor
            if 'speed' in properties_json:
                target_speed = properties_json['speed']


    def run(self):
        while True:
            if digital_twin == None:
                time.sleep(1)
                continue

            interval_start = time.time()
            state = digital_twin.next_state()

            if state['speed'] == 0 and target_speed == 0:
                # the device is fully turned off
                time.sleep(1)
                continue

            pl = bytearray(pickle.dumps(state))
            iothub_device.send_message(pl)

            digital_twin.set_speed((target_speed + digital_twin.get_speed()) / 2)

            self.__report_state({
                'speed': state['speed'],
                'temperature': state['temperature'],
                'pressure': state['pressure'],
                'ambientTemperature': state['ambient_temperature'],
                'ambientPressure': state['ambient_pressure']
                })

            time_elapsed = time.time() - interval_start
            # print('Cadence: {0}'.format(time_elapsed))
            time.sleep(max(1 - time_elapsed, 0))

"""
global digital_twin
global target_speed
target_speed = 0
digital_twin = None

def device_twin_callback(update_state, payload, user_context):
    global digital_twin
    global target_speed

    properties_json = json.loads(payload)
    if str(update_state) == 'COMPLETE':
        properties_json = properties_json['desired']
        spectral_profile = json.loads(properties_json['spectralProfile'])
        pressure_factor = properties_json['pressureFactor']
        digital_twin = Device(iothub_device.device_id, make='model1', W = spectral_profile['W'], A = spectral_profile['A'])
        digital_twin.pressure_factor = pressure_factor
    if 'speed' in properties_json:
        target_speed = properties_json['speed']

def send_reported_state_callback(status_code, user_context):
    pass
    #print (status_code)

iothub_device.client.set_device_twin_callback(device_twin_callback, 0)

print('Driver {0} has claimed IoT device \'{1}\''.format(driver_unique_id, device_id))

while True:
    if digital_twin == None:
        time.sleep(1)
        continue

    interval_start = time.time()
    state = digital_twin.next_state()

    if state['speed'] == 0 and target_speed == 0:
        # the device is fully turned off
        time.sleep(1)
        continue

    pl = bytearray(pickle.dumps(state))
    iothub_device.send_message(pl)

    digital_twin.set_speed((target_speed + digital_twin.get_speed()) / 2)

    iothub_device.send_reported_state({
        'speed': state['speed'],
        'temperature': state['temperature'],
        'pressure': state['pressure'],
        'ambientTemperature': state['ambient_temperature'],
        'ambientPressure': state['ambient_pressure']
        }, send_reported_state_callback)

    time_elapsed = time.time() - interval_start
    # print('Cadence: {0}'.format(time_elapsed))
    time.sleep(max(1 - time_elapsed, 0))
"""