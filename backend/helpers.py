import serial.tools.list_ports

def list_serial_interfaces():
    """List available serial interfaces."""
    return [port.device for port in serial.tools.list_ports.comports()]
