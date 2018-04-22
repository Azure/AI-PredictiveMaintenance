import time
import json
import pickle
import random
from devices.simulated_device import SimulatedDevice
from .device import Device

class Engine(SimulatedDevice):
    def initialize(self, device_info):
        properties_desired = device_info['properties']['desired']
        properties_reported = device_info['properties']['reported']
        print(properties_reported)

        spectral_profile = {
            'W': [1, 2, 3, 4, 5, 12, 15],
            'A': [5, 8, 2/3, 9, 8, 13, 5]
        }
        pressure_factor = 2

        if 'failureOnset' not in properties_desired:
            pass
        elif properties_desired['failureOnset'] == 'F01':
            spectral_profile = {
                'W': [1/2, 1, 2, 3, 5, 7, 12, 18],
                'A': [1, 5, 80, 2/3, 8, 2, 14, 50]
            }
        elif properties_desired['failureOnset'] == 'F02':
            pressure_factor = 1.5
        
        self.target_speed = properties_desired['speed']
        self.digital_twin = Device(W = spectral_profile['W'], A = spectral_profile['A'])
        self.digital_twin.pressure_factor = pressure_factor
        self.auto_pilot = False

    def on_update(self, update_state, properties_json):
        if update_state == 'COMPLETE':
            properties_json = properties_json['desired']
        if 'speed' in properties_json:
            self.target_speed = properties_json['speed']
        if 'mode' in properties_json:
            self.auto_pilot = properties_json['mode'] == 'auto'

    def biased_coin_flip(self, p = 0.5):
        return True if random.random() < p else False

    def run(self):
        while True:
            interval_start = time.time()
            state = self.digital_twin.next_state()

            if state['speed'] == 0 and self.target_speed == 0:
                # the device is fully turned off
                time.sleep(1)
                continue

            pl = bytearray(pickle.dumps(state))
            self.send_telemetry(pl)

            self.digital_twin.set_speed((self.target_speed + self.digital_twin.get_speed()) / 2)

            self.report_state({
                'speed': state['speed'],
                'temperature': state['temperature'],
                'pressure': state['pressure'],
                'ambientTemperature': state['ambient_temperature'],
                'ambientPressure': state['ambient_pressure']
                })

            if self.auto_pilot and self.biased_coin_flip(p = 0.2):
                self.target_speed = random.randint(600, 1500)

            time_elapsed = time.time() - interval_start
            # print('Cadence: {0}'.format(time_elapsed))
            time.sleep(max(1 - time_elapsed, 0))
