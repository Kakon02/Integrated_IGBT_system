from PyQt5 import QtWidgets, uic, QtCore
import sys

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("port_settings.ui", self)
        
        self.messages = ["Connected", "Connecting", "Disconnected"]
        self.colors = ["green", "orange", "red"]
        self.current_index = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_label)
        self.Console.append("🚀 Hello from console!")

        self.timer.start(2000)

    def update_status_label(self, label, text, color="black", bold=False, size=10):
        """Update the label with text and style."""
        style = f"color: {color}; font-size: {size}px; font-family: Arial;"
        if bold:
            style += " font-weight: bold;"
        label.setStyleSheet(style)
        label.setText(text)

    def update_label(self):
        msg = self.messages[self.current_index]
        color = self.colors[self.current_index]

        self.update_status_label(self.label_8, msg, color=color, bold=False, size=20)

        self.current_index = (self.current_index + 1) % len(self.messages)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
