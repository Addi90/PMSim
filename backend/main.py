from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from typing import List, Tuple
import urllib.parse

class PowerMeterSimulation:
    def __init__(self):
        self.voltage = [230.0, 230.0, 230.0]
        self.current = [1.0, 1.0, 1.0]
        self.power = [230.0, 230.0, 230.0]
        self.serial_number = "1234567"
        self.brand = "Brand1"

    def get_voltage(self) -> Tuple[float, float, float]:
        return tuple(self.voltage)

    def set_voltage(self, v1: float, v2: float, v3: float):
        self.voltage = [v1, v2, v3]

    def get_current(self) -> Tuple[float, float, float]:
        return tuple(self.current)

    def set_current(self, i1: float, i2: float, i3: float):
        self.current = [i1, i2, i3]

    def get_power(self) -> Tuple[float, float, float]:
        return tuple(self.power)

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

simulation = PowerMeterSimulation()

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/meter-data':
            self.send_response(200)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            data = {
                "voltage": simulation.get_voltage(),
                "current": simulation.get_current(),
                "power": simulation.get_power(),
                "serialNumber": simulation.get_serial_number(),
                "brand": simulation.get_brand()
            }
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        try:
            if self.path == '/voltage':
                simulation.set_voltage(*data['values'])
            elif self.path == '/current':
                simulation.set_current(*data['values'])
            elif self.path == '/power':
                simulation.set_power(*data['values'])
            elif self.path == '/serial-number':
                simulation.set_serial_number(data['serialNumber'])
            elif self.path == '/brand':
                simulation.set_brand(data['brand'])
            else:
                self.send_error(404)
                return

            self.send_response(200)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
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
        server.server_close()
        print("Server stopped.")