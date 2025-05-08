from devices.MCCDAQ import MCCDAQ, MCCDAQManager
from devices.EX30012 import EX300_12
from devices.LKLAB import LKLabController
from devices.DC61802F import DC61802F

class DeviceController:
    def __init__(self):
        self.daq_manager = None
        self.daq_devices = None
        self.dc_power = None
        self.cooler = None

    def get_daq(self):
        return self.daq_devices[0]

    def get_power(self):
        return self.dc_power

    def get_cooler(self):
        return self.cooler


    def refresh_FG_devices(self, combo_box, console):
    # Initialize the manager if it doesn't exist
        if self.daq_manager is None:
            self.daq_manager = MCCDAQManager()
        # Discover devices
        else:
            self.daq_manager.discover_devices()
        
        daq_device_list = self.daq_manager.list_devices()

        # Clear any previous MCCDAQ instances
        self.daq_devices = []

        if not daq_device_list:
            console.append("❌ No devices found.")
            return

        # Update combo box and create MCCDAQ instances
        combo_box.clear()
        for device in daq_device_list:
            board_num = device["board_num"]
            unique_id = device["unique_id"]
            combo_box.addItem(f"{board_num}-{unique_id}")
            self.daq_devices.append(MCCDAQ(board_num))

        console.append(f"✅ {len(self.daq_devices)} DAQ device(s) found and ready.")

    
    def connect_fg_device(self, combo_box, status_label, console):
        selected_device = combo_box.currentText()
        if not selected_device:
            console.append("❌ No device selected.")
            return

        if self.flash_led_on_device(combo_box, console):
            status_label.setText(f"✅ Connected to {selected_device}.")
            console.append(f"✅ Connected to device {selected_device}.")
        else:
            status_label.setText("❌ Disconnected")
            status_label.setStyleSheet("color: red; font-family: Arial; font-size: 20px;")
            console.append(f"❌ Failed to connect to device {selected_device}.")
    
    def flash_led_on_device(self, combo_box, console):
        selected_device = combo_box.currentText()
        if not selected_device:
            console.append("❌ No device selected.")
            return False

        board_num = int(selected_device.split('-')[0])
        if self.daq_manager.flash_led(board_num):
            console.append(f"✅ LED flashed on device {selected_device}.")
            return True
        else:
            console.append(f"❌ Failed to flash LED on device {selected_device}.")
            return False
    
    def connect_dc_power(self, device_selection, port, baudrate, status_label, console):
        port = port.currentText()
        device_selection = device_selection.currentText()
        baudrate = baudrate.text()

        try:
            baudrate = int(baudrate)
        except ValueError:
            
            console.append("❌ Invalid type for baud rate.")
            status_label.setText("❌ Disconnected")
            status_label.setStyleSheet("color: red; font-family: Arial; font-size: 20px;")
            return
        if device_selection == "EX300-12":
            self.dc_power = EX300_12(port, baudrate)
            self.dc_power.connect_to_port(port)
            if self.dc_power.connected:
                console.append(f"✅ Connected to {device_selection}.")
                status_label.setText(f"✅ Connected to {device_selection}.")
                status_label.setStyleSheet("color: green; font-family: Arial; font-size: 20px;")
            else:
                console.append(f"❌ Failed to connect to {device_selection}.")
                status_label.setText("❌ Disconnected")
                status_label.setStyleSheet("color: red; font-family: Arial; font-size: 20px;")

        elif device_selection == "DC61802F":
            self.dc_power = DC61802F(port, baudrate)
            self.dc_power.connect_to_port(port)

            if self.dc_power.connected:        
                console.append(f"✅ Connected to {device_selection}.")
                status_label.setText(f"✅ Connected to {device_selection}.")
                status_label.setStyleSheet("color: green; font-family: Arial; font-size: 20px;")
            else:
                console.append(f"❌ Failed to connect to {device_selection}.")
                status_label.setText("❌ Disconnected")
                status_label.setStyleSheet("color: red; font-family: Arial; font-size: 20px;")


    def connect_cooler(self, port, baudrate, status_label, console):
        port = port.currentText()
        baudrate = baudrate.text()

        try:
            baudrate = int(baudrate)
        except ValueError:
            console.append("❌ Invalid type for baud rate.")
            status_label.setText("❌ Disconnected")
            status_label.setStyleSheet("color: red; font-family: Arial; font-size: 20px;")
            return
        
        self.cooler = LKLabController(port, baudrate)
        self.cooler._connect()
        
        if self.cooler._connection:
            console.append(f"✅ Connected to Cooler on {port}.")
            status_label.setText(f"✅ Connected to Cooler on {port}.")
            status_label.setStyleSheet("color: green; font-family: Arial; font-size: 20px;")
        else:
            console.append(f"❌ Failed to connect to Cooler on {port}.")
            status_label.setText("❌ Disconnected")
            status_label.setStyleSheet("color: red; font-family: Arial; font-size: 20px;")
    
    def has_all_devices_connected(self):
        return all([self.daq_devices, self.dc_power, self.cooler])
