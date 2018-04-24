import importlib
import logging
from abc import ABC, abstractmethod

class SimulatedDevice(ABC):
    def __init__(self, report_state_function, send_telemetry_function, log_function):
        self.__report_state = report_state_function
        self.__send_telemetry = send_telemetry_function
        self.__log_function = log_function

    def report_state(self, state):
        self.__report_state(state)

    def send_telemetry(self, data):
        self.__send_telemetry(data)

    def log(self, message, code = None, level = logging.INFO):
        self.__log_function(message, code, level)

    @abstractmethod
    def initialize(self, device_info):
        pass

    @abstractmethod
    def on_update(self, update_state, payload):
        pass

    @abstractmethod
    def run(self):
        pass

class SimulatorFactory:
    @staticmethod
    def create(full_class_name, *args):
        parts = full_class_name.split('.')
        module = '.'.join(parts[:-1])
        simple_class_name = parts[-1]
        module = importlib.import_module(module)
        simulator_class = getattr(module, simple_class_name)
        return simulator_class(*args)

if __name__ == '__main__':
    pass
