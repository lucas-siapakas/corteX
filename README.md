# DAQ Control Software

A Python-based application for controlling NI USB-6212 DAQ card with waveform generation and real-time monitoring capabilities.

## Features

- Generate various waveforms (sine, square, triangle, sawtooth)
- Real-time waveform preview
- Analog output control
- Real-time analog input monitoring
- User-friendly GUI interface

## Requirements

- Python 3.11+
- NI-DAQmx drivers installed
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cortex.git
cd cortex
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

4. Install requirements:
```bash
pip install -r requirements.txt
```

## Usage

1. Activate your virtual environment (if not already activated)
2. Run the application:
```bash
python main.py
```

3. Use the GUI to:
   - Select waveform type (sine, square, triangle, sawtooth)
   - Set frequency, amplitude, and duration
   - Preview the waveform before output
   - Monitor analog input in real-time

## Project Structure

```
cortex/
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
└── src/
    ├── daq/            # DAQ interface module
    ├── gui/            # GUI components
    ├── utils/          # Utility functions
    └── waveforms/      # Waveform generation module
```
