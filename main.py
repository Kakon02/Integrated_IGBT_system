from DC61802F import DCPowerController
from EX30012 import EX300_12
from LKLAB import LKLabController
from MCCDAQ import MCCDAQManager, MCCDAQ
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import serial
from datetime import datetime, timedelta


# Load the UI file
port_settings_ui = uic.loadUiType("port_settings.ui")[0]

class PortSettingsApp(QMainWindow, port_settings_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

def refresh_FG_devices(combo_box, console):
    devices = daq_manager.list_devices()
    if not devices:
        console.append("❌ No devices found.")
    else:
        combo_box.clear()
        combo_box.addItems([device["unique_id"] for device in devices])

def connect_fg_device(combo_box, connection_status_label, console):
    if not combo_box.currentText():
        console.append("❌ No board selected.")
        return

    connection_status_label.setText("Connecting...")
    connection_status_label.setStyleSheet("color: orange; font-family: Arial; font-size: 20px;")
    matching_devices = [
        device["board_num"] for device in daq_manager.list_devices()
        if device["unique_id"] == combo_box.currentText()
    ]
    board_num = matching_devices[0] if matching_devices else None
    if board_num is not None and daq_manager.flash_led(board_num):
        connection_status_label.setText("Connected")
        connection_status_label.setStyleSheet("color: green; font-family: Arial; font-size: 20px;")
        console.append(f"✅ Connected to {combo_box.currentText()}")
    else:
        connection_status_label.setText("Disconnected")
        connection_status_label.setStyleSheet("color: red; font-family: Arial; font-size: 20px;")
        console.append(f"❌ Failed to connect to {combo_box.currentText()}")

def flash_led_on_device(combo_box, console):
    matching_devices = [
        device["board_num"] for device in daq_manager.list_devices()
        if device["unique_id"] == combo_box.currentText()
    ]
    if not matching_devices:
        console.append("❌ No matching device found.")
    else:
        daq_manager.flash_led(matching_devices[0])

def connect_dc_power_controller(combo_box, baud_rate_line_edit, connection_status_label, console):
    port = combo_box.currentText()
    try:
        baudrate = int(baud_rate_line_edit.text())
    except ValueError:
        console.append("❌ Invalid baud rate. Please enter a valid number.")
        connection_status_label.setText("Disconnected")
        connection_status_label.setStyleSheet("color: red; font-family: Arial; font-size: 20px;")
        return

    # Try connecting to EX30012
    try:
        dc_power_controller = EX300_12(port, baudrate)
        dc_power_controller._connect_to_port(port)
        connection_info = dc_power_controller.get_auto_connection_info()
        connection_status_label.setText(f"Connected (EX30012) on {connection_info['port']}")
        connection_status_label.setStyleSheet("color: green; font-family: Arial; font-size: 20px;")
        console.append(f"✅ Connected to EX30012 on {connection_info['port']}")
        return
    except RuntimeError as e:
        console.append(str(e))

    # If EX30012 fails, try connecting to DC61802F
    dc_power_controller = DCPowerController(port, baudrate)
    try:
        if dc_power_controller._connect():
            connection_status_label.setText("Connected (DC61802F)")
            connection_status_label.setStyleSheet("color: green; font-family: Arial; font-size: 20px;")
            console.append(f"✅ Connected to DC61802F on {port}")
        else:
            raise RuntimeError("Connection failed.")
    except Exception as e:
        connection_status_label.setText("Disconnected")
        connection_status_label.setStyleSheet("color: red; font-family: Arial; font-size: 20px;")
        console.append(f"❌ Failed to connect to any DC Power Controller on {port}: {e}")

def auto_connect_dc_power_controller(DCDC_COM_Port_1, DCDC_COM_Port_2, baud_rate_line_edit, connection_status_label_1, connection_status_label_2, console):
    ports = [p.device for p in serial.tools.list_ports.comports()]
    usable_ports = []

    # Find usable ports
    for port in ports:
        try:
            # Try connecting to DC61802F
            dc_power_controller = DCPowerController(port)
            dc_power_controller._connect()
            usable_ports.append(port)
            dc_power_controller.close()
        except RuntimeError:
            # If DC61802F fails, try connecting to EX30012
            try:
                ex30012 = EX300_12(port)
                ex30012._connect_to_port(port)
                usable_ports.append(port)
                ex30012.close()
            except RuntimeError:
                continue

    if not usable_ports:
        console.append("❌ No usable DC power supply found.")
        return

    # Select the available ports without clearing the combo boxes
    if usable_ports:
        DCDC_COM_Port_1.setCurrentText(usable_ports[0])
    if len(usable_ports) > 1:
        DCDC_COM_Port_2.setCurrentText(usable_ports[1])

    # Connect to the first available device
    try:
        DCDC_COM_Port_1.setCurrentText(usable_ports[0])
        connect_dc_power_controller(DCDC_COM_Port_1, baud_rate_line_edit, connection_status_label_1, console)
    except RuntimeError as e:
        console.append(str(e))

    # Connect to the second available device if present
    if len(usable_ports) > 1:
        try:
            DCDC_COM_Port_2.setCurrentText(usable_ports[1])
            connect_dc_power_controller(DCDC_COM_Port_2, baud_rate_line_edit, connection_status_label_2, console)
        except RuntimeError as e:
            console.append(str(e))

def connect_cooler(combo_box, baud_rate_line_edit, connection_status_label, console):
    port = combo_box.currentText()
    try:
        baudrate = int(baud_rate_line_edit.text())
    except ValueError:
        console.append("❌ Invalid baud rate. Please enter a valid number.")
        connection_status_label.setText("Disconnected")
        connection_status_label.setStyleSheet("color: red; font-family: Arial; font-size: 20px;")
        return

    # Try connecting to LKLab
    try:
        cooler = LKLabController(port, baudrate)
        cooler._connect()
        connection_status_label.setText("Connected (LKLab)")
        connection_status_label.setStyleSheet("color: green; font-family: Arial; font-size: 20px;")
        console.append(f"✅ Connected to LKLab on {port}")
    except Exception as e:
        console.append(f"❌ Failed to connect to LKLab on {port}: {e}")
        connection_status_label.setText("Disconnected")
        connection_status_label.setStyleSheet("color: red; font-family: Arial; font-size: 20px;")

def auto_connect_cooler(Cooler_COM_Port_1, Cooler_COM_Port_2, baud_rate_line_edit, connection_status_label_1, connection_status_label_2, console):
    ports = [p.device for p in serial.tools.list_ports.comports()]
    usable_ports = []

    # Find usable ports
    for port in ports:
        try:
            cooler = LKLabController(port)
            cooler._connect()
            usable_ports.append(port)
            cooler.close()
        except Exception:
            continue

    if not usable_ports:
        console.append("❌ No usable cooler found.")
        return

    # Select the available ports without clearing the combo boxes
    if usable_ports:
        Cooler_COM_Port_1.setCurrentText(usable_ports[0])
    if len(usable_ports) > 1:
        Cooler_COM_Port_2.setCurrentText(usable_ports[1])

    # Connect to the first available device
    try:
        Cooler_COM_Port_1.setCurrentText(usable_ports[0])
        connect_cooler(Cooler_COM_Port_1, baud_rate_line_edit, connection_status_label_1, console)
    except Exception as e:
        console.append(str(e))

    # Connect to the second available device if present
    if len(usable_ports) > 1:
        try:
            Cooler_COM_Port_2.setCurrentText(usable_ports[1])
            connect_cooler(Cooler_COM_Port_2, baud_rate_line_edit, connection_status_label_2, console)
        except Exception as e:
            console.append(str(e))

# Check if FG_Connection_Status_1, DCDC_Connection_Status_1, Cooler_Connection_Status_1 are connected
def check_system_1_connection_status(FG_Connection_Status_1, DCDC_Connection_Status_1, Cooler_Connection_Status_1):
    return FG_Connection_Status_1.text() == "Connected" and DCDC_Connection_Status_1.text() == "Connected" and Cooler_Connection_Status_1.text() == "Connected"

# Check if FG_Connection_Status_2, DCDC_Connection_Status_2, Cooler_Connection_Status_2 are connected
def check_system_2_connection_status(FG_Connection_Status_2, DCDC_Connection_Status_2, Cooler_Connection_Status_2):
    return FG_Connection_Status_2.text() == "Connected" and DCDC_Connection_Status_2.text() == "Connected" and Cooler_Connection_Status_2.text() == "Connected"


def system_1_start(Console):
    if not check_system_1_connection_status(FG_Connection_Status_1, DCDC_Connection_Status_1, Cooler_Connection_Status_1):
        Console.append("❌ Please connect all devices before starting the system.")
        return

    System_1_Loading.setText("System 1 Connection Status: Connected")
    System_1_Loading.setStyleSheet("color: green; font-family: Arial; font-size: 12px;")
    
    try:
        freq = float(System_1_Freq.text())
        duty = float(System_1_Duty.text())
        voltage = float(System_1_Voltage.text())
        temp = float(System_1_Temp.text())
        runtime = int(System_1_RunTime.text())
    except ValueError:
        Console.append("❌ Invalid input values. Please check the fields.")
        return

    Console.append("🚀 System 1 started.")
    daq_manager.start_pulse(freq, duty)
    dc_power_controller = DCPowerController(DCDC_COM_Port_1.currentText())
    dc_power_controller._connect()
    dc_power_controller.run_voltage_sequence(voltage)
    cooler = LKLabController(Cooler_COM_Port_1.currentText())
    cooler._connect()
    cooler.set_temperature(temp)

    # Calculate and update System_1_ACTime
    finish_time = datetime.now() + timedelta(seconds=runtime)
    System_1_ACTime.setText(finish_time.strftime("%H:%M:%S"))

    # Start progress timer
    System_1_Progress.setValue(0)
    global progress_timer_1
    progress_timer_1 = QtCore.QTimer()
    progress_timer_1.timeout.connect(lambda: update_progress(System_1_Progress, runtime, progress_timer_1, Console))
    progress_timer_1.start(1000)

def system_2_start(Console):
    if not check_system_2_connection_status(FG_Connection_Status_2, DCDC_Connection_Status_2, Cooler_Connection_Status_2):
        Console.append("❌ Please connect all devices before starting the system.")
        return

    System_2_Loading.setText("System 2 Connection Status: Connected")
    System_2_Loading.setStyleSheet("color: green; font-family: Arial; font-size: 12px;")

    try:
        freq = float(System_2_Freq.text())
        duty = float(System_2_Duty.text())
        voltage = float(System_2_Voltage.text())
        temp = float(System_2_Temp.text())
        runtime = int(System_2_RunTime.text())
    except ValueError:
        Console.append("❌ Invalid input values. Please check the fields.")
        return

    Console.append("🚀 System 2 started.")
    daq_manager.start_pulse(freq, duty)
    dc_power_controller = DCPowerController(DCDC_COM_Port_2.currentText())
    dc_power_controller._connect()
    dc_power_controller.run_voltage_sequence(voltage)
    cooler = LKLabController(Cooler_COM_Port_2.currentText())
    cooler._connect()
    cooler.set_temperature(temp)

    # Calculate and update System_2_ACTime
    finish_time = datetime.now() + timedelta(seconds=runtime)
    System_2_ACTime.setText(finish_time.strftime("%H:%M:%S"))

    # Start progress timer
    System_2_Progress.setValue(0)
    global progress_timer_2
    progress_timer_2 = QtCore.QTimer()
    progress_timer_2.timeout.connect(lambda: update_progress(System_2_Progress, runtime, progress_timer_2, Console))
    progress_timer_2.start(1000)

def update_progress(progress_bar, runtime, timer, Console):
    elapsed_time = progress_bar.value() * runtime / 100
    elapsed_time += 1
    progress_bar.setValue((elapsed_time / runtime) * 100)
    if elapsed_time >= runtime:
        timer.stop()
        Console.append("✅ System completed.")

def system_1_pause(progress_timer, runtime, elapsed_time):
    if not check_system_1_connection_status(FG_Connection_Status_1, DCDC_Connection_Status_1, Cooler_Connection_Status_1):
        Console.append("❌ System 1 is not running. Please start the system before pausing.")
        return

    Console.append("⏸ System 1 paused.")
    # Stop the timer for System_1_Progress
    if progress_timer.isActive():
        progress_timer.stop()
    # Calculate and save the remaining time to System_1_RunTime
    remaining_time = runtime - elapsed_time
    System_1_RunTime.setText(str(remaining_time))

def system_2_pause(progress_timer, runtime, elapsed_time):
    if not check_system_2_connection_status(FG_Connection_Status_2, DCDC_Connection_Status_2, Cooler_Connection_Status_2):
        Console.append("❌ System 2 is not running. Please start the system before pausing.")
        return

    Console.append("⏸ System 2 paused.")
    # Stop the timer for System_2_Progress
    if progress_timer.isActive():
        progress_timer.stop()
    # Calculate and save the remaining time to System_2_RunTime
    remaining_time = runtime - elapsed_time
    System_2_RunTime.setText(str(remaining_time))

def system_1_stop(combo_box, Console):
    
    # Get the unique_id from FG_Device_Number_1
    unique_id = combo_box.currentText()
    if not unique_id:
        Console.append("❌ No device selected in FG_Device_Number_1.")
        return

    # Find the board_num associated with the unique_id
    matching_devices = [
        device for device in daq_manager.list_devices()
        if device["unique_id"] == unique_id
    ]
    if not matching_devices:
        Console.append(f"❌ No matching device found for unique_id: {unique_id}")
        return

    board_num = matching_devices[0]["board_num"]

    # Initialize the MCCDAQ instance for the specific board_num
    mcc_daq = MCCDAQ(board_num=board_num)

    # Stop the pulse output on the specific timer_channel
    try:
        timer_channel = mcc_daq.first_chan_num  # Use the first available channel
        mcc_daq.stop(timer_channel=timer_channel)
        Console.append(f"✅ Stopped pulse output on DAQ device with unique_id: {unique_id} (Board {board_num}, Channel {timer_channel})")
    except Exception as e:
        Console.append(f"❌ Failed to stop pulse output on DAQ device with unique_id: {unique_id}: {e}")

    # Stop the DC Power Controller
    dc_power_controller = DCPowerController(DCDC_COM_Port_1.currentText())
    try:
        dc_power_controller._connect()
        dc_power_controller.stop()
        Console.append(f"✅ Stopped DC Power Controller on {DCDC_COM_Port_1.currentText()}")
    except Exception as e:
        Console.append(f"❌ Failed to stop DC Power Controller: {e}")

    # Stop the Cooler
    cooler = LKLabController(Cooler_COM_Port_1.currentText())
    try:
        cooler._connect()
        cooler.turn_off_operation()
        Console.append(f"✅ Stopped Cooler on {Cooler_COM_Port_1.currentText()}")
    except Exception as e:
        Console.append(f"❌ Failed to stop Cooler: {e}")

    # Reset System_1_RunTime and System_1_Progress
    System_1_RunTime.setText("0")
    System_1_Progress.setValue(0)
    Console.append("⛔ System 1 stopped.")

def system_2_stop():
    
    # Get the unique_id from FG_Device_Number_2
    unique_id = FG_Device_Number_2.currentText()
    if not unique_id:
        Console.append("❌ No device selected in FG_Device_Number_2.")
        return

    # Find the board_num associated with the unique_id
    matching_devices = [
        device for device in daq_manager.list_devices()
        if device["unique_id"] == unique_id
    ]
    if not matching_devices:
        Console.append(f"❌ No matching device found for unique_id: {unique_id}")
        return

    board_num = matching_devices[0]["board_num"]

    # Initialize the MCCDAQ instance for the specific board_num
    mcc_daq = MCCDAQ(board_num=board_num)

    # Stop the pulse output on the specific timer_channel
    try:
        timer_channel = mcc_daq.first_chan_num  # Use the first available channel
        mcc_daq.stop(timer_channel=timer_channel)
        Console.append(f"✅ Stopped pulse output on DAQ device with unique_id: {unique_id} (Board {board_num}, Channel {timer_channel})")
    except Exception as e:
        Console.append(f"❌ Failed to stop pulse output on DAQ device with unique_id: {unique_id}: {e}")

    # Stop the DC Power Controller
    dc_power_controller = DCPowerController(DCDC_COM_Port_2.currentText())
    try:
        dc_power_controller._connect()
        dc_power_controller.stop()
        Console.append(f"✅ Stopped DC Power Controller on {DCDC_COM_Port_2.currentText()}")
    except Exception as e:
        Console.append(f"❌ Failed to stop DC Power Controller: {e}")

    # Stop the Cooler
    cooler = LKLabController(Cooler_COM_Port_2.currentText())
    try:
        cooler._connect()
        cooler.turn_off_operation()
        Console.append(f"✅ Stopped Cooler on {Cooler_COM_Port_2.currentText()}")
    except Exception as e:
        Console.append(f"❌ Failed to stop Cooler: {e}")

    # Reset System_2_RunTime and System_2_Progress
    System_2_RunTime.setText("0")
    System_2_Progress.setValue(0)
    Console.append("⛔ System 2 stopped.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PortSettingsApp()

    FG_Device_Number_1 = window.FG_Device_Number_1
    FG_Device_Number_2 = window.FG_Device_Number_2
    FG_Find_Device_1 = window.FG_Find_Device_1
    FG_Find_Device_2 = window.FG_Find_Device_2

    FG_Connect_1 = window.FG_Connect_1
    FG_Connect_2 = window.FG_Connect_2
    FG_Refresh_1 = window.FG_Refresh_1
    FG_Refresh_2 = window.FG_Refresh_2

    FG_Connection_Status_1 = window.FG_Connection_Status_1
    FG_Connection_Status_2 = window.FG_Connection_Status_2

    DCDC_COM_Port_1 = window.DCDC_COM_Port_1
    DCDC_COM_Port_2 = window.DCDC_COM_Port_2
    DCDC_BaudRate_1 = window.DCDC_BaudRate_1
    DCDC_BaudRate_2 = window.DCDC_BaudRate_2

    DCDC_Connect_1 = window.DCDC_Connect_1
    DCDC_Connect_2 = window.DCDC_Connect_2
    DCDC_AutoConnect_1 = window.DCDC_AutoConnect_1
    DCDC_AutoConnect_2 = window.DCDC_AutoConnect_2

    DCDC_Connection_Status_1 = window.DCDC_Connection_Status_1
    DCDC_Connection_Status_2 = window.DCDC_Connection_Status_2

    Cooler_COM_Port_1 = window.Cooler_COM_Port_1
    Cooler_COM_Port_2 = window.Cooler_COM_Port_2
    Cooler_BaudRate_1 = window.Cooler_BaudRate_1
    Cooler_BaudRate_2 = window.Cooler_BaudRate_2

    Cooler_Connect_1 = window.Cooler_Connect_1
    Cooler_Connect_2 = window.Cooler_Connect_2
    Cooler_AutoConnect_1 = window.Cooler_AutoConnect_1
    Cooler_AutoConnect_2 = window.Cooler_AutoConnect_2

    Cooler_Connection_Status_1 = window.Cooler_Connection_Status_1
    Cooler_Connection_Status_2 = window.Cooler_Connection_Status_2

    System_1_Freq = window.System_1_Freq
    System_1_Freq_unit = window.System_1_Freq_unit
    System_1_Duty = window.System_1_Duty
    System_1_Voltage = window.System_1_Voltage
    System_1_Voltage_unit = window.System_1_Voltage_unit
    System_1_Temp = window.System_1_Temp
    System_1_RunTime = window.System_1_RunTime
    System_1_ACTime = window.System_1_ACTime
    System_1_Progress = window.System_1_Progress
    System_1_Loading = window.System_1_Loading

    System_2_Freq = window.System_2_Freq
    System_2_Freq_unit = window.System_2_Freq_unit
    System_2_Duty = window.System_2_Duty
    System_2_Voltage = window.System_2_Voltage
    System_2_Voltage_unit = window.System_2_Voltage_unit
    System_2_Temp = window.System_2_Temp
    System_2_RunTime = window.System_2_RunTime
    System_2_ACTime = window.System_2_ACTime
    System_2_Progress = window.System_2_Progress
    System_2_Loading = window.System_2_Loading

    System_1_Start = window.System_1_Start
    System_1_Pause = window.System_1_Pause
    System_1_Stop = window.System_1_Stop

    System_2_Start = window.System_2_Start
    System_2_Pause = window.System_2_Pause
    System_2_Stop = window.System_2_Stop


    Console = window.Console

    


    FG_Refresh_1.clicked.connect(lambda: refresh_FG_devices(FG_Device_Number_1, Console))
    FG_Refresh_2.clicked.connect(lambda: refresh_FG_devices(FG_Device_Number_2, Console))

    FG_Connect_1.clicked.connect(lambda: connect_fg_device(FG_Device_Number_1, FG_Connection_Status_1, Console))
    FG_Connect_2.clicked.connect(lambda: connect_fg_device(FG_Device_Number_2, FG_Connection_Status_2, Console))

    FG_Find_Device_1.clicked.connect(lambda: flash_led_on_device(FG_Device_Number_1, Console))
    FG_Find_Device_2.clicked.connect(lambda: flash_led_on_device(FG_Device_Number_2, Console))

    DCDC_Connect_1.clicked.connect(lambda: connect_dc_power_controller(DCDC_COM_Port_1, DCDC_BaudRate_1, DCDC_Connection_Status_1, Console))
    DCDC_Connect_2.clicked.connect(lambda: connect_dc_power_controller(DCDC_COM_Port_2, DCDC_BaudRate_2, DCDC_Connection_Status_2, Console))

    DCDC_AutoConnect_1.clicked.connect(lambda: auto_connect_dc_power_controller(DCDC_COM_Port_1, DCDC_COM_Port_2, DCDC_BaudRate_1, DCDC_Connection_Status_1, DCDC_Connection_Status_2, Console))
    DCDC_AutoConnect_2.clicked.connect(lambda: auto_connect_dc_power_controller(DCDC_COM_Port_2, DCDC_COM_Port_1, DCDC_BaudRate_2, DCDC_Connection_Status_2, DCDC_Connection_Status_1, Console))

    Cooler_Connect_1.clicked.connect(lambda: connect_cooler(Cooler_COM_Port_1, Cooler_BaudRate_1, Cooler_Connection_Status_1, Console))
    Cooler_Connect_2.clicked.connect(lambda: connect_cooler(Cooler_COM_Port_2, Cooler_BaudRate_2, Cooler_Connection_Status_2, Console))

    Cooler_AutoConnect_1.clicked.connect(lambda: auto_connect_cooler(Cooler_COM_Port_1, Cooler_COM_Port_2, Cooler_BaudRate_1, Cooler_Connection_Status_1, Cooler_Connection_Status_2, Console))
    Cooler_AutoConnect_2.clicked.connect(lambda: auto_connect_cooler(Cooler_COM_Port_2, Cooler_COM_Port_1, Cooler_BaudRate_2, Cooler_Connection_Status_2, Cooler_Connection_Status_1, Console))

    System_1_Start.clicked.connect(lambda: system_1_start(Console))
    System_2_Start.clicked.connect(lambda: system_2_start(Console))

    System_1_Pause.clicked.connect(lambda: system_1_pause(
        System_1_Progress, 
        int(System_1_RunTime.text()) if System_1_RunTime.text().isdigit() else 0, 
        System_1_Progress.value()
    ))
    System_2_Pause.clicked.connect(lambda: system_2_pause(
        System_2_Progress, 
        int(System_2_RunTime.text()) if System_2_RunTime.text().isdigit() else 0, 
        System_2_Progress.value()
    ))

    System_1_Stop.clicked.connect(lambda: system_1_stop(FG_Device_Number_1, Console))
    System_2_Stop.clicked.connect(lambda: system_2_stop())

    daq_manager = MCCDAQManager()

    window.show()
    sys.exit(app.exec_())
