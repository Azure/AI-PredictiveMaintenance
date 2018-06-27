import numpy as np
import random
from datetime import date, datetime
from scipy.interpolate import interp1d

class VibrationSensorSignalSample:
    CUTOFF = 150

    def __init__(self, W, A, fundamental_from, fundamental_to, t = 0, interval = 1, previous_sample = None, sample_rate = 1024):
        self.interval = interval
        self.sample_rate = sample_rate
        self.W = W
        self.A = A
        self.t = t
        self.base_frequency = fundamental_from
        self.target_base_frequency = fundamental_to
        self.add_noise = True
        self.__previous_sample = previous_sample
        self.__N = sample_rate * interval

    def pcm(self):
        ts = np.linspace(self.t, self.t + self.interval, num = self.__N, endpoint=False)

        x = np.array([0, self.interval]) + self.t
        points = np.array([self.base_frequency, self.target_base_frequency])
        rpm = interp1d(x, points, kind='linear')

        f = rpm(ts)
        f[f < 0] = 0

        fi = np.cumsum(f / self.sample_rate) + (self.__previous_sample.__last_cumsum if self.__previous_sample else 0)

        base = 2 * np.pi * fi
        b = np.array([np.sin(base * w) * a for w, a in zip(self.W, self.A)])
        a = b.sum(axis = 0)

        if self.add_noise:
            a += np.random.normal(0, 0.1, self.__N)

        self.__last_cumsum = fi[-1]
        self.base_frequency = self.target_base_frequency

        a[a > self.CUTOFF] = self.CUTOFF
        a[a < -self.CUTOFF] = -self.CUTOFF

        return np.int16(a / self.CUTOFF * 32767)

class RotationalMachine:
    ambient_temperature = 20 # degrees Celsius
    max_temperature = 120
    ambient_pressure = 101 # kPa

    def __init__(self, name, h1, h2):
        self.W = [1/2, 1, 2, 3, 5, 7, 12, 18]
        self.A = [1, 5, 80, 2/3, 8, 2, 14, 50]
        self.t = 0
        self.name = name
        self.speed = 0
        self.speed_desired = 0
        self.temperature = RotationalMachine.ambient_temperature
        self.pressure = RotationalMachine.ambient_pressure
        self.pressure_factor = 2
        self.__vibration_sample = None
        self.__h1 = h1
        self.__h2 = h2
        self.broken = False
        self.h1 = None
        self.h2 = None

    def set_health(self, h1, h2):
        self.__h1 = h1
        self.__h2 = h2
        self.broken = False

    def set_speed(self, speed):
        self.speed_desired = speed

    def __g(self, v, min_v, max_v, target, rate):
        delta = (target - v) * rate
        return max(min(v + delta, max_v), min_v)

    def noise(self, magnitude):
        return random.uniform(-magnitude, magnitude)

    def next_state(self):
        try:
            _, self.h1 = next(self.__h1)
        except:
            self.broken = True
            raise Exception("F1")

        try:
            _, self.h2 = next(self.__h2)
        except:
            self.broken = True
            raise Exception("F2")

        v_from = self.speed / 60
        self.speed = (self.speed + (2 - self.h2) * self.speed_desired) / 2
        v_to = self.speed / 60

        self.temperature = (2 - self.h1) * self.__g(self.temperature, self.ambient_temperature, self.max_temperature, self.speed / 10, 0.01 * self.speed / 1000)
        self.pressure = self.h1 * self.__g(self.pressure, self.ambient_pressure, np.inf, self.speed * self.pressure_factor, 0.3 * self.speed / 1000)
        self.__vibration_sample = VibrationSensorSignalSample(
            #self.W, self.A, v_from, v_to, t = self.t, previous_sample = self.__vibration_sample)
            self.W, self.A, v_from, v_to, t = self.t)

        state = {
            'speed_desired': self.speed_desired,
            'ambient_temperature': self.ambient_temperature + self.noise(0.1),
            'ambient_pressure': self.ambient_pressure + self.noise(0.1),
            'speed': self.speed + self.noise(5),
            'temperature': self.temperature + self.noise(0.1),
            'pressure': self.pressure + self.noise(20),
            'vibration': self.__vibration_sample
        }

        self.t += 1

        for key in state:
            value = state[key]
            if isinstance(value, (int, float)):
                state[key] = round(value, 2)

        return state