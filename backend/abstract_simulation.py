from typing import Tuple
import threading
import uuid
from abc import ABC, abstractmethod

# Abstract Base Class for Simulations
class AbstractSimulation(ABC):
    def __init__(self, protocol: str):
        self.id = str(uuid.uuid4())
        self.protocol = protocol
        self.voltage = [230.0, 230.0, 230.0]
        self.current = [1.0, 1.0, 1.0]
        self.power = [230.0, 230.0, 230.0]
        self.serial_number = "1234567"
        self.brand = "Brand1"
        self.port = ""
        self.is_running = False
        self.simulation_type = "steady"
        self.simulation_thread = None

    @abstractmethod
    def run_simulation(self):
        """Abstract method to define the simulation logic."""
        pass

    def get_voltage(self) -> Tuple[float, float, float]:
        return tuple([round(i, 2) for i in self.voltage])

    def set_voltage(self, v1: float, v2: float, v3: float):
        self.voltage = [v1, v2, v3]

    def get_current(self) -> Tuple[float, float, float]:
        return tuple([round(i, 2) for i in self.current])

    def set_current(self, i1: float, i2: float, i3: float):
        self.current = [i1, i2, i3]

    def get_power(self) -> Tuple[float, float, float]:
        return tuple([round(i, 2) for i in self.power])

    def set_power(self, p1: float, p2: float, p3: float):
        self.power = [p1, p2, p3]

    def get_serial_number(self) -> str:
        return self.serial_number

    def set_serial_number(self, serial: str):
        if len(serial) > 7 or not serial.isdigit():
            raise ValueError("Serial number must be 7 digits")
        self.serial_number = serial

    def get_brand(self) -> str:
        return self.brand
    
    def set_brand(self, brand: str):
        if brand not in ["Brand1", "Brand2"]:
            raise ValueError("Invalid brand")
        self.brand = brand

    def get_port(self) -> str:
        return self.port
    
    def set_port(self, port: str):
        self.port = port
        # restart the simulation if it is running
        if self.is_running:
            self.set_simulation_state(False)
            self.set_simulation_state(True)

    def set_simulation_type(self, sim_type: str):
        if sim_type not in ["steady", "fluctuating", "overload", "brownout"]:
            raise ValueError("Invalid simulation type")
        self.simulation_type = sim_type

    def set_simulation_state(self, is_running: bool):
        self.is_running = is_running
        if is_running and not self.simulation_thread:
            self.simulation_thread = threading.Thread(target=self.run_simulation_wrapper)
            self.simulation_thread.daemon = True
            self.simulation_thread.start()
        elif not is_running and self.simulation_thread:
            self.is_running = False # Ensure the thread loop terminates

    def run_simulation_wrapper(self):
        """Wrapper to handle thread lifecycle and call abstract run_simulation."""
        self.run_simulation()
        self.simulation_thread = None # Reset thread after loop finishes (when is_running is set to False)


    def get_data(self):
        return {
            "voltage": self.get_voltage(),
            "current": self.get_current(),
            "power": self.get_power(),
            "serialNumber": self.get_serial_number(),
            "brand": self.get_brand(),
            "port": self.get_port(),
            "isRunning": self.is_running,
            "simulationType": self.simulation_type,
            "id": self.id,
            "protocol": self.protocol
        }

    def to_dict(self):
        return {
            "id": self.id,
            "protocol": self.protocol,
            "serialNumber": self.serial_number,
            "port": self.get_port(),
            "isRunning": self.is_running,
            "simulationType": self.simulation_type
        }