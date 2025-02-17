# PMSin

PMSin is a simulation tool with a web interface that simulates three-phase power meters. It allows users to adjust values such as Power, Voltage, and Current through the web UI. Additionally, it provides a FastAPI for direct control of the simulated power meter, offering flexibility for various use cases. A python backend provides the API and runs the simulations, while the Frontend accessing the API is provided by vite. The configurated simulation(s) are stored in a file persistently.

## Features

- Easy to use web UI for monitoring, configuring, and modifying simulations.
- For each simulation, modify power, voltage, current phase-wise, and modify the serial number.
- Start/Stop/Remove simulations individually.
- Ability to add/run multiple simulations.
- API to access without a graphical user interface.

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
