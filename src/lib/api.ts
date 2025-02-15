const API_BASE = 'http://localhost:8000';

export async function getMeterData(simulatorId: string): Promise<PowerMeterData> {
  const response = await fetch(`${API_BASE}/simulator/${simulatorId}`);
  return response.json();
}

export async function getSimulatorConfig(): Promise<SimulatorConfig> {
  const response = await fetch(`${API_BASE}/config`);
  return response.json();
}

export async function addSimulator(protocol: SimulatorProtocol): Promise<void> {
  await fetch(`${API_BASE}/simulator`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ protocol }),
  });
}

export async function removeSimulator(id: string): Promise<void> {
  await fetch(`${API_BASE}/simulator/${id}`, {
    method: 'DELETE',
  });
}

export async function resetConfig(): Promise<void> {
  await fetch(`${API_BASE}/config/reset`, {
    method: 'POST',
  });
}

export async function setVoltage(simulatorId: string, values: [number, number, number]): Promise<void> {
  await fetch(`${API_BASE}/simulator/${simulatorId}/voltage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ values }),
  });
}

export async function setCurrent(simulatorId: string, values: [number, number, number]): Promise<void> {
  await fetch(`${API_BASE}/simulator/${simulatorId}/current`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ values }),
  });
}

export async function setPower(simulatorId: string, values: [number, number, number]): Promise<void> {
  await fetch(`${API_BASE}/simulator/${simulatorId}/power`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ values }),
  });
}

export async function setSerialNumber(simulatorId: string, serialNumber: string): Promise<void> {
  await fetch(`${API_BASE}/simulator/${simulatorId}/serial-number`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ serialNumber }),
  });
}

export async function setBrand(simulatorId: string, brand: 'Brand1' | 'Brand2'): Promise<void> {
  await fetch(`${API_BASE}/simulator/${simulatorId}/brand`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ brand }),
  });
}

export async function setSimulationType(simulatorId: string, type: SimulationType): Promise<void> {
  await fetch(`${API_BASE}/simulator/${simulatorId}/simulation-type`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type }),
  });
}

export async function setSimulationState(simulatorId: string, isRunning: boolean): Promise<void> {
  await fetch(`${API_BASE}/simulator/${simulatorId}/simulation-state`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ isRunning }),
  });
}