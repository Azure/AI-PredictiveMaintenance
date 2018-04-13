import time
import json
import pickle
from devices.simulated_device import SimulatedDevice
from .device import Device

class Engine(SimulatedDevice):
    def initialize(self, device_info):
        properties_desired = device_info['properties']['desired']

        if 'failureOnset' not in properties_desired:
            spectral_profile = {
                'W': [1, 2, 3, 4, 5, 12, 15],
                'A': [5, 8, 2/3, 9, 8, 13, 5]
            }
            pressure_factor = 2
            
        # rotor_imbalance_speactral_profile = {
        #     'W': [1/2, 1, 2, 3, 5, 7, 12, 18],
        #     'A': [1, 5, 80, 2/3, 8, 2, 14, 50]
        # }        
        
        self.target_speed = properties_desired['speed']
        self.digital_twin = Device(W = spectral_profile['W'], A = spectral_profile['A'])
        self.digital_twin.pressure_factor = pressure_factor

    def on_update(self, update_state, properties_json):
        if 'speed' in properties_json:
            self.target_speed = properties_json['speed']

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

            time_elapsed = time.time() - interval_start
            # print('Cadence: {0}'.format(time_elapsed))
            time.sleep(max(1 - time_elapsed, 0))
