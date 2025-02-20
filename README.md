# PMSim

PMSim is a simulation tool that provides a web interface and a backend to run simulations of three-phase power meters as well as provides a modbus tcp or rtu interface (dependent on how the power meter that is simulated is set up). It allows users to adjust values such as Power, Voltage, and Current through the web UI. Additionally, it provides an API for direct control of the simulated power meter, offering flexibility for various use cases. A python backend provides the API and runs the simulations, while the Frontend accessing the API is provided by vite. The configurated simulation(s) are stored in a file persistently.

## Features

- Easy to use web UI for monitoring, configuring, and modifying simulations.
- For each simulation, modify power, voltage, current phase-wise, and modify the serial number.
- Selection of serial interface of available interfaces per simulation (for Modbus RTU only)
- Start/Stop/Remove simulations individually.
- Ability to add/run multiple simulations.
- API to access and modify without a graphical user interface.

## Setup

Install python requirements from `requirements.txt`:
```sh
pip install -r requirements.txt
```

Install node.js packages:
```sh
npm install
```

Run Python backend:
```sh
python ./backend/main.py
```

Run frontend dev server:
```sh
npm run dev
```
