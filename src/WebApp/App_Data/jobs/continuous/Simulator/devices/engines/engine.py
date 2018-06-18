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
                    state['timestamp'] = datetime.now().isoformat()
                    state['machineID'] = self.digital_twin.name

                    telemetry_json = json.dumps(state)
                    self.send_telemetry(telemetry_json)

                    # self.report_state({
                    #     'speed': state['speed'],
                    #     'temperature': state['temperature'],
                    #     'pressure': state['pressure'],
                    #     'ambientTemperature': state['ambient_temperature'],
                    #     'ambientPressure': state['ambient_pressure']
                    #     })

                    time_elapsed = time.time() - interval_start
                    time.sleep(max(1 - time_elapsed, 0))

                    if not state['speed']:
                        break
                except Exception as e:
                    self.log('failure', str(e), logging.CRITICAL)
                    return

            time.sleep(60)
