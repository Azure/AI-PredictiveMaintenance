import numpy as np
from scipy.interpolate import interp1d

class VibrationSensorSimulator:
    CUTOFF = 100

    def __init__(self, interval = 1, sample_rate = 8000, W = None, A = None):
        self.interval = interval
        self.sample_rate = sample_rate
        self.W = W
        self.A = A
        self.base_frequency = 0 # Hz
        self.target_base_frequency = 0 # Hz
        self.time = 0
        self.add_noise = False
        self.__last_cumsum = 0
        self.__N = sample_rate * interval

    def set_target_base_frequency(self, frequency):
        self.target_base_frequency = frequency

    def set_spectral_properties(self, W, A):
        self.W = W
        self.A = A

    def next_sample(self, frequency = None):
        if not frequency is None:
            self.set_target_base_frequency(frequency)

        ts = np.linspace(self.time,
            self.time + self.interval,
            num = self.__N,
            endpoint=False)

        x = np.array([0, self.interval]) + self.time
        points = np.array([self.base_frequency, self.target_base_frequency])
        rpm = interp1d(x, points, kind='slinear')

        f = rpm(ts)
        # cubic interpolation, if used, is not positive-preserving
        f[f < 0] = 0

        fi = np.cumsum(f / self.sample_rate) + self.__last_cumsum

        base = 2 * np.pi * fi
        b = np.array([np.sin(base * w) * a for w, a in zip(self.W, self.A)])
        a = b.sum(axis = 0)

        if self.add_noise:
            a += np.random.normal(0, 0.1, self.__N)
        
        self.__last_cumsum = fi[-1]
        self.base_frequency = self.target_base_frequency
        self.time += 1

        a[a > self.CUTOFF] = self.CUTOFF
        a[a < -self.CUTOFF] = -self.CUTOFF

        return np.int16(a / 100 * 32767).tolist()

if __name__ == '__main__':
    # test code
    W = (1/10, 1, 2, 3, 5, 12, 15, 18)
    A = (0, 5, 8, 30, 8, 13, 5, 8)

    sensor = VibrationSensorSimulator(W = W, A = A)
    
    rpm = np.array([120, 300, 1200, 1500, 1200, 600, 60])
    freqs_hz = rpm / 60

    samples = [sensor.next_sample(f) for f in freqs_hz]
    from scipy.io.wavfile import write
    write('test.wav', 8000, np.concatenate(np.array(samples, dtype=np.int16)))
