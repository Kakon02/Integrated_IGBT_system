from PyQt5 import QtWidgets, uic
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = uic.loadUi("port_settings.ui")  # Make sure this path is correct
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()