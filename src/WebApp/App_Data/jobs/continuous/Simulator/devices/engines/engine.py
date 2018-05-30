import time
import json
import pickle
import logging
import random
import math
from devices.simulated_device import SimulatedDevice
from .device import RotationalMachine

class Engine(SimulatedDevice):
    def initialize(self, device_info):
        device_id = device_info['deviceId']
        properties_desired = device_info['properties']['desired']
        properties_reported = device_info['properties']['reported']

        d = 0.05
        a = -0.3
        b = 0.2
        th = 0.45
        ttf1 = random.randint(5000, 50000)
        ttf2 = random.randint(5000, 90000)

        def h_generator(ttf, d, a, b, th = 0):
            for t in range(ttf, -1, -1):
                h = 1 - d - math.exp(a*t**b)
                if h < th:
                    break
                yield t, h

        h1 = h_generator(ttf1, d, a, b)
        h2 = h_generator(ttf2, d, a, b)
        
        self.digital_twin = RotationalMachine(device_id, h1, h2)
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

            #self.log('failure', self.failure_onset, logging.CRITICAL)

            #pl = bytearray(pickle.dumps(state))
            #self.send_telemetry(pl)
            state['vibration'] = None
            telemetry_json = json.dumps(state)
            self.send_telemetry(telemetry_json)

            self.report_state({
                'speed': state['speed'],
                'temperature': state['temperature'],
                'pressure': state['pressure'],
                'ambientTemperature': state['ambient_temperature'],
                'ambientPressure': state['ambient_pressure']
                })

            # if self.auto_pilot and self.biased_coin_flip(p = 0.2):
            #     self.target_speed = random.randint(600, 1500)

            time_elapsed = time.time() - interval_start
            # print('Cadence: {0}'.format(time_elapsed))
            time.sleep(max(1 - time_elapsed, 0))
