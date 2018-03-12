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

    def __g(self, v, min_v, max_v, p, decrement):
        limit = max(min_v, p, v - decrement)
        delta = (limit - v) * np.sqrt(limit - v) * (decrement ** 2)
        return min(max_v, limit, v + delta)

    def next_state_device(self):
        self.temperature = self.__g(self.temperature, self.ambient_temperature, self.max_temperature, self.speed / 10, 0.01)
        self.pressure = self.__g(self.pressure, self.ambient_pressure, np.inf, self.speed * self.pressure_factor, 100 / self.speed)
        device = self
        return device
    
    def next_state(self):
        state = {        
            'ambient_temperature': self.ambient_temperature,
            'ambient_pressure': self.ambient_pressure,
            'speed': self.speed,
            'temperature': self.temperature,
            'pressure': self.pressure,
            'vibration': self.__vibration_sensor.next_sample(self.speed / 60)
        }
        return state
        
    

if __name__ == '__main__':
    pass
