import time
import json
import pickle
import logging
import random
import math
from datetime import datetime
from devices.simulated_device import SimulatedDevice
from .device import RotationalMachine

class Engine(SimulatedDevice):
    def initialize(self, device_info):
        device_id = device_info['deviceId']
        tags = device_info['tags']
        # properties_desired = device_info['properties']['desired']
        properties_reported = device_info['properties']['reported']

        d = 0.05
        a = -0.3
        b = 0.2
        th = 0.45

        # the inverse of the health function
        ttf = lambda h: math.pow((math.log(1 - d - h) / a), 1 / b)

        h1_initial = float(tags['h1'])
        h2_initial = float(tags['h2'])

        if 'h1' in properties_reported and 'h2' in properties_reported:
            h1_initial = float(properties_reported['h1'])
            h2_initial = float(properties_reported['h2'])

        ttf1 = ttf(h1_initial)
        ttf2 = ttf(h2_initial)

        def h_generator(ttf, d, a, b, th = 0):
            for t in range(int(ttf), -1, -1):
                h = 1 - d - math.exp(a*t**b)
                if h < th:
                    break
                yield t, h

        h1_gen = h_generator(ttf1, d, a, b)
        h2_gen = h_generator(ttf2, d, a, b)

        self.digital_twin = RotationalMachine(device_id, h1_gen, h2_gen)
        return True

    def on_update(self, update_state, properties_json):
        if update_state == 'COMPLETE':
            properties_json = properties_json['desired'] if 'desired' in properties_json else {}
        # update internal state based on the desired properties here

    def report_health(self):
        health = {
            'h1': self.digital_twin.h1,
            'h2': self.digital_twin.h2
        }
        self.report_state(health)
        self.log(json.dumps(health), 'SIM_HEALTH', logging.DEBUG)

    def run(self):
        self.log('Simulation started.')

        cycle_length_min = 1
        cycle_length_max = 5

        while True: # cycle
            l = random.randint(cycle_length_min, cycle_length_max)
            duration = l * 60
            cooldown_point = duration - 20

            self.digital_twin.set_speed(1000)

            for i in range(duration):
                if i == cooldown_point:
                    self.digital_twin.set_speed(0)

                try:
                    interval_start = time.time()
                    state = self.digital_twin.next_state()

                    state['vibration'] = None
                    state['timestamp'] = datetime.utcnow().isoformat()
                    state['machineID'] = self.digital_twin.name

                    telemetry_json = json.dumps(state)
                    self.send_telemetry(telemetry_json)

                    time_elapsed = time.time() - interval_start
                    time.sleep(max(1 - time_elapsed, 0))

                    if not state['speed']:
                        break
                except Exception as e:
                    self.report_health()
                    self.log('failure', str(e), logging.CRITICAL)
                    return

            self.report_health()
            time.sleep(60)
