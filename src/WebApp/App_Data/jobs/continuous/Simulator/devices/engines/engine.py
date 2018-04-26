import time
import json
import pickle
import logging
import random
from devices.simulated_device import SimulatedDevice
from .device import Device

class Engine(SimulatedDevice):
    def initialize(self, device_info):
        properties_desired = device_info['properties']['desired']
        properties_reported = device_info['properties']['reported']

        if 'failure' in properties_reported and properties_reported['failure']:
            return False

        spectral_profile = {
            'W': [1, 2, 3, 4, 5, 12, 15],
            'A': [5, 8, 2/3, 9, 8, 13, 5]
        }
        pressure_factor = 2

        self.failure_onset = None if 'failureOnset' not in properties_desired else properties_desired['failureOnset']

        if self.failure_onset == 'F01':
            spectral_profile = {
                'W': [1/2, 1, 2, 3, 5, 7, 12, 18],
                'A': [1, 5, 80, 2/3, 8, 2, 14, 50]
            }
        elif self.failure_onset == 'F02':
            pressure_factor = 1.5

        self.target_speed = properties_desired['speed']
        self.digital_twin = Device(W = spectral_profile['W'], A = spectral_profile['A'])
        self.digital_twin.pressure_factor = pressure_factor
        self.auto_pilot = False
        self.version = properties_reported['$version']
        return True

    def on_update(self, update_state, properties_json):
        if update_state == 'COMPLETE':
            properties_json = properties_json['desired']
        if 'speed' in properties_json:
            self.target_speed = properties_json['speed']
        if 'mode' in properties_json:
            mode = properties_json['mode']
            self.log(mode, 'MODE_CHANGE')
            self.auto_pilot = mode == 'auto'

    def biased_coin_flip(self, p = 0.5):
        return True if random.random() < p else False

    def run(self):
        self.log('Simulation started.')
        while True:
            interval_start = time.time()
            state = self.digital_twin.next_state()

            if state['speed'] == 0 and self.target_speed == 0:
                # the device is fully turned off
                time.sleep(1)
                continue

            if self.failure_onset is not None and self.version > 600:
                self.report_state({
                    'failure': True
                })
                self.log('failure', self.failure_onset, logging.CRITICAL)
                return

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

            self.version += 1

            if self.auto_pilot and self.biased_coin_flip(p = 0.2):
                self.target_speed = random.randint(600, 1500)

            time_elapsed = time.time() - interval_start
            # print('Cadence: {0}'.format(time_elapsed))
            time.sleep(max(1 - time_elapsed, 0))
