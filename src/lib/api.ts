const API_BASE = 'http://localhost:8000';

export async function getMeterData(): Promise<PowerMeterData> {
  const response = await fetch(`${API_BASE}/meter-data`);
  return response.json();
}

export async function setVoltage(values: [number, number, number]): Promise<void> {
  await fetch(`${API_BASE}/voltage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ values }),
  });
}

export async function setCurrent(values: [number, number, number]): Promise<void> {
  await fetch(`${API_BASE}/current`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ values }),
  });
}

export async function setPower(values: [number, number, number]): Promise<void> {
  await fetch(`${API_BASE}/power`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ values }),
  });
}

export async function setSerialNumber(serialNumber: string): Promise<void> {
  await fetch(`${API_BASE}/serial-number`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ serialNumber }),
  });
}

export async function setBrand(brand: 'Brand1' | 'Brand2'): Promise<void> {
  await fetch(`${API_BASE}/brand`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ brand }),
  });
}