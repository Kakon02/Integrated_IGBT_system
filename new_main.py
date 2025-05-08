# main.py
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow
from controllers.system_controller import SystemController
from controllers.device_controller import DeviceController
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = QApplication(sys.argv)
window = MainWindow()

def create_system_controller(device_controller, window, system_number):
    if device_controller.has_all_devices_connected() and system_number == 1:
        daq = device_controller.get_daq()
        power = device_controller.get_power()
        cooler = device_controller.get_cooler()
        window.system_controller_1 = SystemController(daq, power, cooler, window.System_1_RunTime, window.System_1_Progress, window.System_1_TimeLeft, window.console)
        window.console.append("✅ System Controller 1 created.")
        window.Start_System_1.setText("Connected!")
        window.Start_System_1.setStyleSheet("font-family: Arial; font-size: 36px; color: green;")
    
    elif not device_controller.has_all_devices_connected() and system_number == 1:
        window.console.append("❌ System Controller 1 not created. Please connect all devices.")
        window.Start_System_1.setText("Disconnected!")
        window.Start_System_1.setStyleSheet("font-family: Arial; font-size: 36px; color: red;")

    elif device_controller.has_all_devices_connected() and system_number == 2:
        daq = device_controller.get_daq()
        power = device_controller.get_power()
        cooler = device_controller.get_cooler()
        window.system_controller_2 = SystemController(daq, power, cooler, window.System_2_RunTime, window.System_2_Progress, window.System_2_TimeLeft, window.console)
        window.console.append("✅ System Controller 2 created.")
        window.Start_System_2.setText("Connected!")
        window.Start_System_2.setStyleSheet("font-family: Arial; font-size: 36px; color: green;")

    elif not device_controller.has_all_devices_connected() and system_number == 2:
        window.console.append("❌ System Controller 2 not created. Please connect all devices.")
        window.Start_System_2.setText("Disconnected!")
        window.Start_System_2.setStyleSheet("font-family: Arial; font-size: 36px; color: red;")


def start_system(system_number, system_controller, window):
    if system_controller:
        if system_number == 1:
            system_controller.start_system(
                freq=float(window.System_1_Freq.text()),
                duty=float(window.System_1_Duty.text()),
                voltage=float(window.System_1_Voltage.text()),
                temp=float(window.System_1_Temp.text()),
                runtime=int(window.System_1_RunTime.text()) * 60
            )
        elif system_number == 2:
            system_controller.start_system(
                freq=float(window.System_2_Freq.text()),
                duty=float(window.System_2_Duty.text()),
                voltage=float(window.System_2_Voltage.text()),
                temp=float(window.System_2_Temp.text()),
                runtime=int(window.System_2_RunTime.text()) * 60
            )
    else:
        if system_number == 1:
            window.console.append("❌ System Controller 1 not created. Please connect all devices.")
        elif system_number == 2:
            window.console.append("❌ System Controller 2 not created. Please connect all devices.")

def stop_system(system_number, system_controller, window):
    if system_controller:
        if system_number == 1:
            system_controller.stop_system(window.System_1_RunTime)
        elif system_number == 2:
            system_controller.stop_system(window.System_2_RunTime)
    else:
        if system_number == 1:
            window.console.append("❌ System Controller 1 not created. Please connect all devices.")
        elif system_number == 2:
            window.console.append("❌ System Controller 2 not created. Please connect all devices.")

def pause_system(system_number, system_controller, window):
    if system_controller:
        if system_number == 1:
            system_controller.pause_system(window.System_1_RunTime)
        elif system_number == 2:
            system_controller.pause_system(window.System_2_RunTime)
    else:
        if system_number == 1:
            window.console.append("❌ System Controller 1 not created. Please connect all devices.")
        elif system_number == 2:
            window.console.append("❌ System Controller 2 not created. Please connect all devices.")


# DEVICE CONTROLLER
device_controller_1 = DeviceController()
device_controller_2 = DeviceController()

window.system_controller_1 = None
window.system_controller_2 = None

window.FG_Refresh_1.clicked.connect(lambda: device_controller_1.refresh_FG_devices(window.FG_Device_Number_1, window.console))
window.FG_Refresh_2.clicked.connect(lambda: device_controller_2.refresh_FG_devices(window.FG_Device_Number_2, window.console))

window.FG_Connect_1.clicked.connect(lambda: device_controller_1.connect_fg_device(window.FG_Device_Number_1, window.FG_Connection_Status_1, window.console))
window.FG_Connect_2.clicked.connect(lambda: device_controller_2.connect_fg_device(window.FG_Device_Number_2, window.FG_Connection_Status_2, window.console))

window.FG_Find_Device_1.clicked.connect(lambda: device_controller_1.flash_led_on_device(window.FG_Device_Number_1, window.console))
window.FG_Find_Device_2.clicked.connect(lambda: device_controller_2.flash_led_on_device(window.FG_Device_Number_2, window.console))

window.DCDC_Connect_1.clicked.connect(lambda: device_controller_1.connect_dc_power(window.DCDC_Devices_1, window.DCDC_COM_Port_1, window.DCDC_BaudRate_1, window.DCDC_Connection_Status_1, window.console))
window.DCDC_Connect_2.clicked.connect(lambda: device_controller_2.connect_dc_power(window.DCDC_Devices_2, window.DCDC_COM_Port_2, window.DCDC_BaudRate_2, window.DCDC_Connection_Status_2, window.console))

window.Cooler_Connect_1.clicked.connect(lambda: device_controller_1.connect_cooler(window.Cooler_COM_Port_1, window.Cooler_BaudRate_1, window.Cooler_Connection_Status_1, window.console))
window.Cooler_Connect_2.clicked.connect(lambda: device_controller_2.connect_cooler(window.Cooler_COM_Port_2, window.Cooler_BaudRate_2, window.Cooler_Connection_Status_2, window.console))

window.Start_System_1.clicked.connect(lambda: create_system_controller(device_controller_1, window, 1))
window.Start_System_2.clicked.connect(lambda: create_system_controller(device_controller_2, window, 2))


window.System_1_Start.clicked.connect(
    lambda: start_system(
        system_number=1,
        system_controller=window.system_controller_1,
        window=window)
)

window.System_2_Start.clicked.connect(
    lambda: start_system(
        system_number=2,
        system_controller=window.system_controller_2,
        window=window)
)


window.System_1_Stop.clicked.connect(lambda: stop_system(system_number=1, system_controller=window.system_controller_1, window=window))
window.System_2_Stop.clicked.connect(lambda: stop_system(system_number=2, system_controller=window.system_controller_2, window=window))

window.System_1_Pause.clicked.connect(lambda: pause_system(system_number=1, system_controller=window.system_controller_1, window=window))
window.System_2_Pause.clicked.connect(lambda: pause_system(system_number=2, system_controller=window.system_controller_2, window=window))

window.show()
sys.exit(app.exec_())
