from http.server import HTTPServer, BaseHTTPRequestHandler
from simulation_manager import SimulationManager
from request_handler import RequestHandler

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print("Server started at http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped.")