# views/main_window.py
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI
        uic.loadUi("port_settings.ui", self)

        # You can access all the widgets from the UI file directly
        # Example widgets:
        # self.System_1_Start
        # self.System_1_Stop
        # self.System_1_Freq
        # self.System_1_Duty
        # self.System_1_Voltage
        # self.System_1_Temp
        # self.System_1_RunTime
        # self.System_1_Progress
        # self.console

        # Optional: Set some default values or styles
        self.System_1_Progress.setValue(0)
        self.console.append("✅ UI loaded and ready.")

