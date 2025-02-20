import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict
from dummy_power_meter_simulation import DummyPowerMeterSimulation
from abstract_simulation import AbstractSimulation

CONFIG_FILE = "simulator_config.json"

class SimulationManager:
    def __init__(self):
        self.simulators: Dict[str, AbstractSimulation] = {} # Store AbstractSimulation instances
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                for instance in config['instances']:
                    protocol = instance['protocol']
                    if protocol == 'ModbusMTU' or 'ModbusTCP': # Select simulation class based on protocol
                        simulator = DummyPowerMeterSimulation(protocol)
                    else:
                        # Default to dummy if protocol is unknown, or handle error as needed
                        simulator = DummyPowerMeterSimulation("dummy") # Or raise an error
                        print(f"Warning: Unknown protocol '{protocol}' in config, defaulting to dummy simulation.")

                    simulator.id = instance['id']
                    simulator.serial_number = instance['serialNumber']
                    simulator.brand = instance['brand']
                    simulator.simulation_type = instance['simulationType']
                    self.simulators[simulator.id] = simulator

    def save_config(self):
        config = {
            'instances': [sim.to_dict() for sim in self.simulators.values()]
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)

    def add_simulator(self, protocol: str) -> str:
        if protocol == 'ModbusMTU' or 'ModbusTCP': # Select simulation class based on protocol
            simulator = DummyPowerMeterSimulation(protocol)
        else:
            # Default to dummy if protocol is unknown, or handle error as needed
            simulator = DummyPowerMeterSimulation("dummy") # Or raise an error
            print(f"Warning: Unknown protocol '{protocol}' in config, defaulting to dummy simulation.")

        self.simulators[simulator.id] = simulator
        self.save_config()
        return simulator.id

    def remove_simulator(self, simulator_id: str):
        if simulator_id in self.simulators:
            simulator = self.simulators[simulator_id]
            simulator.set_simulation_state(False)
            del self.simulators[simulator_id]
            self.save_config()

    def get_simulator(self, simulator_id: str) -> AbstractSimulation: # Return type is AbstractSimulation
        return self.simulators.get(simulator_id)

    def reset(self):
        for simulator in list(self.simulators.values()):
            simulator.set_simulation_state(False)
        self.simulators.clear()
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)