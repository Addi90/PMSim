from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from typing import List, Tuple, Dict
import urllib.parse
import random
import threading
import time
import uuid
import os

CONFIG_FILE = "simulator_config.json"

class PowerMeterSimulation:
    def __init__(self, protocol: str):
        self.id = str(uuid.uuid4())
        self.protocol = protocol
        self.voltage = [230.0, 230.0, 230.0]
        self.current = [1.0, 1.0, 1.0]
        self.power = [230.0, 230.0, 230.0]
        self.serial_number = "1234567"
        self.brand = "Brand1"
        self.is_running = False
        self.simulation_type = "steady"
        self.simulation_thread = None

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
        print(p1, p2, p3)
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

    def set_simulation_type(self, sim_type: str):
        if sim_type not in ["steady", "fluctuating", "overload", "brownout"]:
            raise ValueError("Invalid simulation type")
        self.simulation_type = sim_type

    def set_simulation_state(self, is_running: bool):
        self.is_running = is_running
        if is_running and not self.simulation_thread:
            self.simulation_thread = threading.Thread(target=self.run_simulation)
            self.simulation_thread.daemon = True
            self.simulation_thread.start()

    def run_simulation(self):
        while True:
            if not self.is_running:
                self.simulation_thread = None
                break

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

    def get_data(self):
        return {
            "voltage": self.get_voltage(),
            "current": self.get_current(),
            "power": self.get_power(),
            "serialNumber": self.get_serial_number(),
            "brand": self.get_brand(),
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
            "brand": self.brand,
            "isRunning": self.is_running,
            "simulationType": self.simulation_type
        }

class SimulatorManager:
    def __init__(self):
        self.simulators: Dict[str, PowerMeterSimulation] = {}
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                for instance in config['instances']:
                    simulator = PowerMeterSimulation(instance['protocol'])
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
        simulator = PowerMeterSimulation(protocol)
        self.simulators[simulator.id] = simulator
        self.save_config()
        return simulator.id

    def remove_simulator(self, simulator_id: str):
        if simulator_id in self.simulators:
            simulator = self.simulators[simulator_id]
            simulator.set_simulation_state(False)
            del self.simulators[simulator_id]
            self.save_config()

    def get_simulator(self, simulator_id: str) -> PowerMeterSimulation:
        return self.simulators.get(simulator_id)

    def reset(self):
        for simulator in list(self.simulators.values()):
            simulator.set_simulation_state(False)
        self.simulators.clear()
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)

simulator_manager = SimulatorManager()

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/config':
            self.send_response(200)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            config = {
                'instances': [sim.to_dict() for sim in simulator_manager.simulators.values()]
            }
            self.wfile.write(json.dumps(config).encode())
        elif self.path.startswith('/simulator/'):
            simulator_id = self.path.split('/')[-1]
            simulator = simulator_manager.get_simulator(simulator_id)
            if simulator:
                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(simulator.get_data()).encode())
            else:
                self.send_error(404)
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            
            if self.path == '/simulator':
                simulator_id = simulator_manager.add_simulator(data['protocol'])
                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"id": simulator_id}).encode())
            elif self.path == '/config/reset':
                simulator_manager.reset()
                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            elif self.path.startswith('/simulator/'):
                parts = self.path.split('/')
                simulator_id = parts[2]
                action = parts[3] if len(parts) > 3 else None
                
                simulator = simulator_manager.get_simulator(simulator_id)
                if not simulator:
                    self.send_error(404)
                    return

                if action == 'voltage':
                    simulator.set_voltage(*data['values'])
                elif action == 'current':
                    simulator.set_current(*data['values'])
                elif action == 'power':
                    simulator.set_power(*data['values'])
                elif action == 'serial-number':
                    simulator.set_serial_number(data['serialNumber'])
                elif action == 'brand':
                    simulator.set_brand(data['brand'])
                elif action == 'simulation-type':
                    simulator.set_simulation_type(data['type'])
                elif action == 'simulation-state':
                    simulator.set_simulation_state(data['isRunning'])
                else:
                    self.send_error(400)
                    return

                simulator_manager.save_config()
                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            else:
                self.send_error(404)
        except Exception as e:
            self.send_response(400)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_DELETE(self):
        try:
            if self.path.startswith('/simulator/'):
                simulator_id = self.path.split('/')[-1]
                simulator_manager.remove_simulator(simulator_id)
                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            else:
                self.send_error(404)
        except Exception as e:
            self.send_response(400)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:5173')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Credentials', 'true')

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print("Server started at http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        simulator_manager.reset()
        server.server_close()
        print("Server stopped.")