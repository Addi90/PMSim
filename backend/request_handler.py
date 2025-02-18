import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict
from dummy_power_meter_simulation import DummyPowerMeterSimulation
from simulation_manager import SimulationManager
from abstract_simulation import AbstractSimulation

simulation_manager = SimulationManager()

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
                'instances': [sim.to_dict() for sim in simulation_manager.simulators.values()]
            }
            self.wfile.write(json.dumps(config).encode())
        elif self.path.startswith('/simulator/'):
            simulator_id = self.path.split('/')[-1]
            simulator = simulation_manager.get_simulator(simulator_id)
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
                simulator_id = simulation_manager.add_simulator(data['protocol'])
                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"id": simulator_id}).encode())
            elif self.path == '/config/reset':
                simulation_manager.reset()
                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            elif self.path.startswith('/simulator/'):
                parts = self.path.split('/')
                simulator_id = parts[2]
                action = parts[3] if len(parts) > 3 else None

                simulator = simulation_manager.get_simulator(simulator_id)
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

                simulation_manager.save_config()
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
                simulation_manager.remove_simulator(simulator_id)
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
