# main.py
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow
from controllers.system_controller import SystemController
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = QApplication(sys.argv)
window = MainWindow()

# DEVICE INSTANCES (singletons for the session)
daq = MCCDAQ(board_num=0)
power = DCPowerController(port='COM3', baudrate=38400)
cooler = LKLabController(port='COM4', baudrate=9600)

# SYSTEM CONTROLLER
system_controller = SystemController(daq, power, cooler, window, window.console)


window.FG_Refresh_1.clicked.connect(lambda: refresh_FG_devices(FG_Device_Number_1, Console))
# window.FG_Refresh_2.clicked.connect(lambda: refresh_FG_devices(FG_Device_Number_2, Console))

window.FG_Connect_1.clicked.connect(lambda: connect_fg_device(FG_Device_Number_1, FG_Connection_Status_1, Console))
# window.FG_Connect_2.clicked.connect(lambda: connect_fg_device(FG_Device_Number_2, FG_Connection_Status_2, Console))

window.FG_Find_Device_1.clicked.connect(lambda: flash_led_on_device(FG_Device_Number_1, Console))
# window.FG_Find_Device_2.clicked.connect(lambda: flash_led_on_device(FG_Device_Number_2, Console))

window.DCDC_Connect_1.clicked.connect(lambda: connect_dc_power_controller(DCDC_Device_1, DCDC_COM_Port_1, DCDC_BaudRate_1, DCDC_Connection_Status_1, Console))
# window.DCDC_Connect_2.clicked.connect(lambda: connect_dc_power_controller(DCDC_Device_2, DCDC_COM_Port_2, DCDC_BaudRate_2, DCDC_Connection_Status_2, Console))

window.Cooler_Connect_1.clicked.connect(lambda: connect_cooler(Cooler_COM_Port_1, Cooler_BaudRate_1, Cooler_Connection_Status_1, Console))
# window.Cooler_Connect_2.clicked.connect(lambda: connect_cooler(Cooler_COM_Port_2, Cooler_BaudRate_2, Cooler_Connection_Status_2, Console))

window.System_1_Start.clicked.connect(lambda: system_1_start(Console))
# window.System_2_Start.clicked.connect(lambda: system_2_start(Console))

window.System_1_Pause.clicked.connect(lambda: system_1_pause())
# window.System_2_Pause.clicked.connect(lambda: system_2_pause())

window.System_1_Stop.clicked.connect(lambda: system_1_stop(FG_Device_Number_1, Console))
# window.System_2_Stop.clicked.connect(lambda: system_2_stop())



# CONNECT BUTTONS
window.System_1_Start.clicked.connect(
    lambda: system_controller.start_system(
        freq=float(window.System_1_Freq.text()),
        duty=float(window.System_1_Duty.text()),
        voltage=float(window.System_1_Voltage.text()),
        temp=float(window.System_1_Temp.text()),
        runtime=int(window.System_1_RunTime.text()) * 60
    )
)
window.System_1_Stop.clicked.connect(system_controller.stop_system)

window.show()
sys.exit(app.exec_())
