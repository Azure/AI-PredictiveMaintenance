import numpy as np
import random
from datetime import date
from vibration_sensor_simulator import VibrationSensorSimulator

class Device:
    ambient_temperature = 20 # degrees Celsius
    max_temperature = 120
    ambient_pressure = 101 # kPa

    def __init__(self, device_id, make = 'model1', manufacturing_date = date(2015, 1, 1), W = None, A = None):
        self.device_id = device_id
        self.speed = 0
        self.temperature = Device.ambient_temperature
        self.pressure = Device.ambient_pressure
        self.W = W
        self.A = A
        self.t = 0
        self.pressure_factor = 2

        self.manufacturing_date = manufacturing_date
        self.make = make
        
        self.__vibration_sensor = VibrationSensorSimulator(W = self.W, A = self.A)
        self.__vibration_sensor.add_noise = True

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def __g(self, v, min_v, max_v, target, rate):
        delta = (target - v) * rate
        return max(min(v + delta, max_v), min_v)

    def next_state(self):
        self.temperature = self.__g(self.temperature, self.ambient_temperature, self.max_temperature, self.speed / 10, 0.01 * self.speed / 1000)
        self.pressure = self.__g(self.pressure, self.ambient_pressure, np.inf, self.speed * self.pressure_factor, 0.3 * self.speed / 1000)
        state = {        
            'ambient_temperature': self.ambient_temperature,
            'ambient_pressure': self.ambient_pressure,
            'speed': self.speed,
            'temperature': self.temperature,
            'pressure': self.pressure,
            'vibration': self.__vibration_sensor.next_sample(self.speed / 60)
        }

        for key in state:
            value = state[key]
            if isinstance(value, (int, float)):
                state[key] = round(value, 2)

        return state

if __name__ == '__main__':
    pass
