# 🏠 IoT Smart Home Control System

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)](https://pypi.org/project/PyQt5/)
[![MQTT](https://img.shields.io/badge/protocol-MQTT-orange.svg)](https://mqtt.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> A modern, intuitive IoT Smart Home Control System built with Python and MQTT protocol. Monitor temperature, control lighting, and manage your home automation through an elegant interactive GUI.

## ✨ Key Features

- 🌡️ Real-time temperature and humidity monitoring
- 💡 Intelligent light control system
- 🔌 Smart relay management
- 🖥️ User-friendly GUI with detachable tabs
- 🔄 Automatic and manual control modes
- 🔗 Reliable MQTT communication

## 🔧 System Components

### 🖥️ Main Control Interface
`MyGUI/DanielGUI.py`
```
✓ Intuitive control interface with detachable tabs
✓ Comprehensive MQTT client management
✓ Real-time publish and subscribe functionality
✓ Smart tab management for multiple controls
```

### 🌡️ Temperature & Humidity Module
`DHT.py`
```
✓ Precision temperature monitoring
✓ Hot/Cold manual temperature controls
✓ Live temperature and humidity readings
✓ Smart automatic temperature regulation
✓ 5-second update interval
```

### 💡 Light Control Module
`LDR.py`
```
✓ Accurate light level monitoring
✓ Bright/Dark manual controls
✓ Smart automatic light adjustment
✓ Real-time status indicators
✓ 5-second update interval
```

### 🔘 Smart Button Interface
`BUTTON.py`
```
✓ Advanced multi-click detection:
  • Single Click → Manual Control
  • Double Click → Temperature Auto Mode
  • Triple Click → Light Auto Mode
✓ Visual button feedback
✓ Intelligent click pattern recognition
```

### ⚡ Relay Control Center
`RELAY.py`
```
✓ Centralized control system
✓ Multiple operation modes:
  • Manual Override
  • Temperature Auto Control
  • Light Auto Control
✓ Real-time status monitoring
✓ Intelligent mode switching
```

## Prerequisites

- Python 3.13 or higher
- PyQt5
- paho-mqtt
- MQTT broker (e.g., Mosquitto)

## 📥 Quick Start Guide

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/DanielA2212/IOT_SMART_HOME.git
   cd IOT_SMART_HOME
   ```

2. **Set Up Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install PyQt5 paho-mqtt
   ```

4. **Configure MQTT Settings**
   - Open `mqtt_init.py`
   - Update broker settings with your MQTT server details

## 🚀 Getting Started

1. **Start MQTT Broker**
   - Ensure your MQTT broker service is running
   - Verify broker connection settings in `mqtt_init.py`

2. **Launch System Components**
   ```bash
   # Open separate terminals for each component:

   # Terminal 1 - Main Control Interface
   python MyGUI/DanielGUI.py

   # Terminal 2 - Temperature & Humidity Module
   python DHT.py

   # Terminal 3 - Light Control System
   python LDR.py

   # Terminal 4 - Smart Button Interface
   python BUTTON.py

   # Terminal 5 - Relay Control Center
   python RELAY.py
   ```

> 💡 **Pro Tip**: Use a terminal multiplexer like `tmux` or `screen` to manage multiple components easily

## Features

- **Interactive GUI**: User-friendly interface with detachable tabs
- **Real-time Monitoring**: Temperature, humidity, and light levels
- **Multiple Control Modes**: Manual and automatic control options
- **MQTT Communication**: Reliable message handling between components
- **Multi-click Functionality**: Different actions based on click patterns
- **Status Display**: Real-time status updates for all components

## 📁 Project Structure

```
IOT_SMART_HOME/
│
├── 🖥️ MyGUI/
│   ├── DanielGUI.py         # Main GUI application
│   └── DeInitialization.py  # GUI initialization
│
├── 🔘 BUTTON.py            # Smart button interface
├── 🌡️ DHT.py              # Temperature/Humidity module
├── 💡 LDR.py              # Light control system
├── ⚡ RELAY.py            # Central relay control
└── ⚙️ mqtt_init.py        # MQTT configuration
```

> 💡 **Tip**: Each component can run independently while maintaining communication through MQTT

## 📡 Communication Protocol

### MQTT Topics Structure

| Topic | Description | Type |
|-------|-------------|------|
| `home/daniel/DHT` | Temperature/Humidity data | Publisher: DHT sensor |
| `home/daniel/LDR` | Light control data | Publisher: Light sensor |
| `home/daniel/BUTTON` | Button interface data | Publisher: Button interface |
| `home/daniel/RELAY` | Relay control data | Subscriber: DHT & LDR |
| `MY_SMART_HOME` | General system topic | System-wide messages |

### Update Intervals
| Component | Interval | Description |
|-----------|----------|-------------|
| Temperature/Humidity | 5 seconds | Regular sensor readings |
| Light Level | 5 seconds | Ambient light monitoring |

## Contributing

Feel free to fork the project and submit pull requests for any improvements.
