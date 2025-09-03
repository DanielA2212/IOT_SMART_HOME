# IoT Smart Home Control System

A Python-based IoT Smart Home Control System using MQTT protocol for communication between different components. The system includes temperature/humidity monitoring, light control, and relay management through an interactive GUI.

## Project Components

### 1. Main GUI (`MyGUI/DanielGUI.py`)
- Central control interface with detachable tabs
- MQTT client management
- Publish and subscribe functionality
- Dynamic tab management for multiple controls

### 2. Temperature and Humidity Control (`DHT.py`)
- Temperature monitoring and control
- Manual temperature adjustment (Hot/Cold)
- Real-time temperature and humidity display
- Automatic temperature regulation

### 3. Light Control System (`LDR.py`)
- Light level monitoring
- Manual light control (Bright/Dark)
- Automatic light adjustment
- Real-time light status display

### 4. Button Interface (`BUTTON.py`)
- Multi-click functionality:
  - Single click: Manual control
  - Double click: Temperature auto mode
  - Triple click: Light auto mode
- Interactive button feedback
- Click counter with timer

### 5. Relay Control (`RELAY.py`)
- Central control unit
- Multiple operation modes:
  - Manual control
  - Auto temperature control
  - Auto light control
- Status monitoring and display

## Prerequisites

- Python 3.x
- PyQt5
- paho-mqtt
- MQTT broker (e.g., Mosquitto)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DanielA2212/IOT_SMART_HOME.git
```

2. Install required Python packages:
```bash
pip install PyQt5 paho-mqtt
```

3. Configure MQTT broker settings in `mqtt_init.py`

## Usage

1. Start the MQTT broker service

2. Launch the components in separate terminals:

```bash
python MyGUI/DanielGUI.py  # Main control interface
python DHT.py              # Temperature/Humidity control
python LDR.py             # Light control
python BUTTON.py          # Button interface
python RELAY.py           # Relay control
```

## Features

- **Interactive GUI**: User-friendly interface with detachable tabs
- **Real-time Monitoring**: Temperature, humidity, and light levels
- **Multiple Control Modes**: Manual and automatic control options
- **MQTT Communication**: Reliable message handling between components
- **Multi-click Functionality**: Different actions based on click patterns
- **Status Display**: Real-time status updates for all components

## Project Structure

```
IOT_SMART_HOME/
│
├── MyGUI/
│   ├── DanielGUI.py         # Main GUI application
│   └── DeInitialization.py  # GUI initialization
│
├── BUTTON.py               # Button control interface
├── DHT.py                 # Temperature/Humidity control
├── LDR.py                # Light control system
├── RELAY.py             # Relay control unit
└── mqtt_init.py        # MQTT initialization settings
```

## Communication Protocol

The system uses MQTT protocol with the following topics:
- `home/daniel/DHT` - Temperature/Humidity data
- `home/daniel/LDR` - Light control data
- `home/daniel/BUTTON` - Button interface data
- `home/daniel/RELAY` - Relay control data
- `MY_SMART_HOME` - General system topic

## Contributing

Feel free to fork the project and submit pull requests for any improvements.

## License

This project is available under the MIT License. See the LICENSE file for more details.
