export interface PowerMeterData {
  voltage: [number, number, number];
  current: [number, number, number];
  power: [number, number, number];
  serialNumber: string;
  brand: 'Brand1' | 'Brand2';
}

export interface Phase {
  voltage: number;
  current: number;
  power: number;
}

export type Domain = 'power' | 'voltage' | 'current';