# Integrated IGBT System

The **Integrated IGBT System** is a modular, Python-based control platform for managing and monitoring industrial-grade devices including DC power supplies, function generators (DAQ), and temperature controllers. It provides a responsive and user-friendly interface built with PyQt5, enabling users to operate two independent systems in parallel.

---

## 🚀 Key Features

### ✅ Device Integration

- **Supported Devices**:
  - **DC Power Supplies**:
    - `DC61802F` (Custom Serial Protocol)
    - `EX300-12` (VISA-based)
  - **Function Generator**:
    - `MCCDAQ` (via InstaCal)
  - **Temperature Controller**:
    - `LKLabController` (Modbus RTU)
- **Automatic MCCDAQ Discovery**
- Visual device status and connection feedback in the UI.

### ⚙️ System Control

- Dual independent systems (System 1 and System 2)
- Set and monitor:
  - Frequency & Duty Cycle (via MCCDAQ)
  - Voltage (via EX300-12 / DC61802F)
  - Temperature (via LKLab)
  - Runtime with real-time progress
- Start, Pause, and Stop control per system

### 🖥️ GUI (Built with PyQt5)

- **Main Tab**:
  - Control panels for both systems
  - Parameter inputs and progress display
- **Port Settings Tab**:
  - Device connection controls
  - COM port and baudrate selection
- **Console**:
  - Logs device status, actions, and errors

---

## 🛠 Installation

### Prerequisites

- Python 3.10 or higher
- InstaCal (for MCCDAQ devices): Download and install `incalsetup.exe` from [Measurement Computing](https://www.mccdaq.com/Software-Downloads)

### Install Dependencies

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

## 🧪 Usage

### Start the Application

Run:

```bash
python main.py
```

### Operating Instructions

1. **Connect Devices**:
   - Select and connect power supply, DAQ, and temperature controller via the Port Settings tab.
2. **Initialize System**:
   - Press `Start_System_1` or `Start_System_2` to create a system controller once all devices are connected.
3. **Start Operation**:
   - Set desired parameters (frequency, voltage, temperature, runtime)
   - Press `Start`, `Pause`, or `Stop` per system

---

## 📁 Project Structure

```plaintext
├── main.py                  # Application entry point
├── controllers/
│   ├── device_controller.py # Manages connection to all devices
│   └── system_controller.py # Handles runtime and system logic
├── devices/
│   ├── DC61802F.py          # Custom serial protocol for 61802F
│   ├── EX30012.py           # VISA-based control for EX300-12
│   ├── LKLAB.py             # Modbus controller for temperature unit
│   └── MCCDAQ.py            # DAQ device control via mcculw
├── view/
│   ├── main_window.py       # PyQt MainWindow class
│   └── port_settings.ui     # QtDesigner UI layout
├── requirements.txt         # Required Python packages
```

---

## ⚠️ Troubleshooting

### 🔌 No Devices Found

- Ensure cables are properly connected
- Run `instacal` if using MCCDAQ devices

### ⚙️ Connection Fails

- Double-check COM ports and baudrates
- Use the LED flash feature to test MCCDAQ board detection

### ❗ Runtime Errors

- Review the console output for detailed error messages
- Ensure all parameter fields are filled with valid values

---

## 🔧 Development Notes

- Use the `.spec` file if building with `pyinstaller` to bundle dependencies.
- MCCDAQ frequency output is unstable above 5 MHz. Use lower frequencies for reliable voltage.

---

## 📜 License

This project is licensed under the **Chungnam National University License**.  
All rights reserved by the Agri-Food Engineering Laboratory, Chungnam National University.

Use of this software is permitted for academic and research purposes only.  
For commercial use or broader distribution rights, please contact the lab.

See the [LICENSE](./LICENSE) file for full terms.

---

## 👨‍💻 Contributors

**Owner**: [Agri-Food Engineering Laboratory, Chungnam National University]  
**GitHub**: [Kakon02]
