import time
import random
from typing import Tuple
from abstract_simulation import AbstractSimulation

# Concrete Simulation Class for Dummy Protocol
class DummyPowerMeterSimulation(AbstractSimulation):
    def __init__(self, protocol: str):
        super().__init__(protocol)
        #if protocol != "dummy":
        #    raise ValueError(f"DummyPowerMeterSimulation only supports 'dummy' protocol, not '{protocol}'")

    def run_simulation(self):
        while self.is_running:
            if self.simulation_type == "steady":
                pass
            elif self.simulation_type == "fluctuating":
                for i in range(3):
                    self.voltage[i] = self.voltage[i] * random.uniform(0.95, 1.05)
                    self.current[i] = self.current[i] * random.uniform(0.95, 1.05)
                    self.power[i] = self.voltage[i] * self.current[i]
            elif self.simulation_type == "overload":
                for i in range(3):
                    self.current[i] *= 1.01
                    self.power[i] = self.voltage[i] * self.current[i]
            elif self.simulation_type == "brownout":
                for i in range(3):
                    self.voltage[i] *= 0.99
                    self.power[i] = self.voltage[i] * self.current[i]

            time.sleep(1)