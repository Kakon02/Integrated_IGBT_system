from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QComboBox

def handle_button_click(combo_box: QComboBox):
    selected_value = combo_box.currentText()
    print(f"Selected value from FG_Device_Number_1: {selected_value}")

def read_combo_box_value(combo_box: QComboBox):
    return combo_box.currentText()

def populate_combo_box():
    # Load the UI file
    ui_file = "port_settings.ui"
    app = QApplication([])
    window = uic.loadUi(ui_file)
    
    # Reference the ComboBox object
    combo_box: QComboBox = window.FG_Device_Number_1
    
    # Example list of values to populate the ComboBox
    port_values = ["COM1", "COM2", "COM3", "COM4"]
    
    # Add values to the ComboBox
    combo_box.addItems(port_values)

    # Read the value of the ComboBox after populating it
    

    # Connect the button to the handler
    button = window.FG_Find_Device_1
    button.clicked.connect(lambda: handle_button_click(combo_box))
    
    # Show the UI (for testing purposes)
    window.show()
    app.exec_()

# Call the function to populate the ComboBox
if __name__ == "__main__":
    populate_combo_box()
