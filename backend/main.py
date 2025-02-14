from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is where you would import your actual power meter simulation
# For now, we'll create a mock class
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

# Initialize simulation
simulation = PowerMeterSimulation()

class ValuesPayload(BaseModel):
    values: List[float]

class SerialNumberPayload(BaseModel):
    serialNumber: str

class BrandPayload(BaseModel):
    brand: str

@app.get("/meter-data")
async def get_meter_data():
    return {
        "voltage": simulation.get_voltage(),
        "current": simulation.get_current(),
        "power": simulation.get_power(),
        "serialNumber": simulation.get_serial_number(),
        "brand": simulation.get_brand()
    }

@app.post("/voltage")
async def update_voltage(payload: ValuesPayload):
    try:
        simulation.set_voltage(*payload.values)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/current")
async def update_current(payload: ValuesPayload):
    try:
        simulation.set_current(*payload.values)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/power")
async def update_power(payload: ValuesPayload):
    try:
        simulation.set_power(*payload.values)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/serial-number")
async def update_serial_number(payload: SerialNumberPayload):
    try:
        simulation.set_serial_number(payload.serialNumber)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/brand")
async def update_brand(payload: BrandPayload):
    try:
        simulation.set_brand(payload.brand)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)