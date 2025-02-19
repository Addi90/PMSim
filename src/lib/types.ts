export interface PowerMeterData {
  voltage: [number, number, number];
  current: [number, number, number];
  power: [number, number, number];
  serialNumber: string;
  brand: 'Brand1' | 'Brand2';
  port: string;
  isRunning: boolean;
}

export interface Phase {
  voltage: number;
  current: number;
  power: number;
}

export type Domain = 'power' | 'voltage' | 'current';

export type SimulationType = 'steady' | 'fluctuating' | 'overload' | 'brownout';

export type SimulatorProtocol = 'ModbusRTU' | 'ModbusTCP';

export interface SimulatorInstance {
  id: string;
  protocol: SimulatorProtocol;
  serialNumber: string;
  brand: 'Brand1' | 'Brand2';
  port: string
  isRunning: boolean;
  simulationType: SimulationType;
}

export interface SimulatorConfig {
  instances: SimulatorInstance[];
}