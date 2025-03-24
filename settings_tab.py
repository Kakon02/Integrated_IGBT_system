import tkinter as tk
from tkinter import ttk

# pip install -r requirements.txt

class SettingsTabApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Settings Tab Test")

        # Automatically adjust geometry to 80% of screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

        # Create a tab control
        tab_control = ttk.Notebook(self)
        self.settings_tab = ttk.Frame(tab_control)
        tab_control.add(self.settings_tab, text="Port Settings")
        tab_control.grid(row=0, column=0, sticky="nsew")  # Use grid instead of pack

        # Configure row and column weights for the settings_tab
        self.settings_tab.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
        self.settings_tab.grid_rowconfigure(1, weight=1)  # Allow row 1 to expand
        self.settings_tab.grid_rowconfigure(2, weight=1)  # Allow row 2 to expand
        self.settings_tab.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand
        self.settings_tab.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand
        
        # Setup the settings tab
        self.setup_settings_tab()

    def setup_settings_tab(self):
        # Define a custom style for the LabelFrame
        style = ttk.Style()
        style.configure("Custom.TLabelframe", font=("Arial", 14))
        style.configure("Custom.TLabelframe.Label", font=("Arial", 14))

        # Main Settings Label
        ttk.Label(self.settings_tab, text="Port Settings", font=("Arial", 18)).grid(row=0, column=0, columnspan=4, padx=10, pady=20)

        # Create a labeled box (LabelFrame) for "System 1"
        system1_frame = ttk.LabelFrame(self.settings_tab, text="System 1", style="Custom.TLabelframe")
        system1_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Add Pulse widgets inside the "System 1" box
        ttk.Label(system1_frame, text="Pulse Port", font=("Arial", 12)).grid(row=0, column=0, rowspan=2,sticky="e", padx=10, pady=5)

        ttk.Label(system1_frame, text="COM Port:", font=("Arial", 12)).grid(row=0, column=1, sticky="e", padx=10, pady=5)
        self.com_port_combobox = ttk.Combobox(system1_frame, width=15, font=("Arial", 12), state="readonly")
        self.com_port_combobox['values'] = ["COM1", "COM2", "COM3", "COM4", "COM5"]
        self.com_port_combobox.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.com_port_combobox.current(0)

        ttk.Label(system1_frame, text="Baud Rate:", font=("Arial", 12)).grid(row=1, column=1, sticky="e", padx=10, pady=5)
        self.baud_rate_entry = ttk.Entry(system1_frame, width=15, font=("Arial", 12))
        self.baud_rate_entry.grid(row=1, column=2, sticky="w", padx=10, pady=5)
        self.baud_rate_entry.insert(0, "9600")

        # Add a separator between the Pulse and Voltage sections
        ttk.Separator(system1_frame, orient="horizontal").grid(row=2, column=0, columnspan=3, sticky="ew", pady=20)


        # Add Voltage widgets inside the "System 1" box

        ttk.Label(system1_frame, text="Voltage Port", font=("Arial", 12)).grid(row=3, column=0, rowspan=2, sticky="e", padx=10, pady=5)

        ttk.Label(system1_frame, text="COM Port:", font=("Arial", 12)).grid(row=3, column=1, sticky="e", padx=10, pady=5)
        self.voltage_com_port_combobox = ttk.Combobox(system1_frame, width=15, font=("Arial", 12), state="readonly")
        self.voltage_com_port_combobox['values'] = ["COM1", "COM2", "COM3", "COM4", "COM5"]
        self.voltage_com_port_combobox.grid(row=3, column=2, sticky="w", padx=10, pady=5)
        self.voltage_com_port_combobox.current(0)

        ttk.Label(system1_frame, text="Baud Rate:", font=("Arial", 12)).grid(row=4, column=1, sticky="e", padx=10, pady=5)
        self.voltage_baud_rate_entry = ttk.Entry(system1_frame, width=15, font=("Arial", 12))
        self.voltage_baud_rate_entry.grid(row=4, column=2, sticky="w", padx=10, pady=5)
        self.voltage_baud_rate_entry.insert(0, "9600")

        ttk.Separator(system1_frame, orient="horizontal").grid(row=5, column=0, columnspan=3, sticky="ew", pady=20)

        # Add Coolr widgets insdie the "System 1" box
        ttk.Label(system1_frame, text="Cooler Port", font=("Arial", 12)).grid(row=6, column=0, rowspan=2, sticky="e", padx=10, pady=5)

        ttk.Label(system1_frame, text="COM Port:", font=("Arial", 12)).grid(row=6, column=1, sticky="e", padx=10, pady=5)
        self.cooler_com_port_combobox = ttk.Combobox(system1_frame, width=15, font=("Arial", 12), state="readonly")
        self.cooler_com_port_combobox['values'] = ["COM1", "COM2", "COM3", "COM4", "COM5"]
        self.cooler_com_port_combobox.grid(row=6, column=2, sticky="w", padx=10, pady=5)
        self.cooler_com_port_combobox.current(0)

        ttk.Label(system1_frame, text="Baud Rate:", font=("Arial", 12)).grid(row=7, column=1, sticky="e", padx=10, pady=5)
        self.cooler_baud_rate_entry = ttk.Entry(system1_frame, width=15, font=("Arial", 12))
        self.cooler_baud_rate_entry.grid(row=7, column=2, sticky="w", padx=10, pady=5)
        self.cooler_baud_rate_entry.insert(0, "9600")

        # Create a labeled box (LabelFrame) for "System 2"
        system2_frame = ttk.LabelFrame(self.settings_tab, text="System 2", style="Custom.TLabelframe")
        system2_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Add Pulse widgets inside the "System 2" box
        ttk.Label(system2_frame, text="Pulse Port", font=("Arial", 12)).grid(row=0, column=0, rowspan=2, sticky="e", padx=10, pady=5)

        ttk.Label(system2_frame, text="COM Port:", font=("Arial", 12)).grid(row=0, column=1, sticky="e", padx=10, pady=5)
        self.system2_com_port_combobox = ttk.Combobox(system2_frame, width=15, font=("Arial", 12), state="readonly")
        self.system2_com_port_combobox['values'] = ["COM1", "COM2", "COM3", "COM4", "COM5"]
        self.system2_com_port_combobox.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.system2_com_port_combobox.current(0)

        ttk.Label(system2_frame, text="Baud Rate:", font=("Arial", 12)).grid(row=1, column=1, sticky="e", padx=10, pady=5)
        self.system2_baud_rate_entry = ttk.Entry(system2_frame, width=15, font=("Arial", 12))
        self.system2_baud_rate_entry.grid(row=1, column=2, sticky="w", padx=10, pady=5)
        self.system2_baud_rate_entry.insert(0, "9600")

        # Add a separator between the Pulse and Voltage sections
        ttk.Separator(system2_frame, orient="horizontal").grid(row=2, column=0, columnspan=3, sticky="ew", pady=20)

        # Add Voltage widgets inside the "System 2" box
        ttk.Label(system2_frame, text="Voltage Port", font=("Arial", 12)).grid(row=3, column=0, rowspan=2, sticky="e", padx=10, pady=5)

        ttk.Label(system2_frame, text="COM Port:", font=("Arial", 12)).grid(row=3, column=1, sticky="e", padx=10, pady=5)
        self.system2_voltage_com_port_combobox = ttk.Combobox(system2_frame, width=15, font=("Arial", 12), state="readonly")
        self.system2_voltage_com_port_combobox['values'] = ["COM1", "COM2", "COM3", "COM4", "COM5"]
        self.system2_voltage_com_port_combobox.grid(row=3, column=2, sticky="w", padx=10, pady=5)
        self.system2_voltage_com_port_combobox.current(0)

        ttk.Label(system2_frame, text="Baud Rate:", font=("Arial", 12)).grid(row=4, column=1, sticky="e", padx=10, pady=5)
        self.system2_voltage_baud_rate_entry = ttk.Entry(system2_frame, width=15, font=("Arial", 12))
        self.system2_voltage_baud_rate_entry.grid(row=4, column=2, sticky="w", padx=10, pady=5)
        self.system2_voltage_baud_rate_entry.insert(0, "9600")

        # Add a separator between the Voltage and Cooler sections
        ttk.Separator(system2_frame, orient="horizontal").grid(row=5, column=0, columnspan=3, sticky="ew", pady=20)

        # Add Cooler widgets insdie the "System 2" box
        ttk.Label(system2_frame, text="Cooler Port", font=("Arial", 12)).grid(row=6, column=0, rowspan=2, sticky="e", padx=10, pady=5)

        ttk.Label(system2_frame, text="COM Port:", font=("Arial", 12)).grid(row=6, column=1, sticky="e", padx=10, pady=5)
        self.system2_cooler_com_port_combobox = ttk.Combobox(system2_frame, width=15, font=("Arial", 12), state="readonly")
        self.system2_cooler_com_port_combobox['values'] = ["COM1", "COM2", "COM3", "COM4", "COM5"]
        self.system2_cooler_com_port_combobox.grid(row=6, column=2, sticky="w", padx=10, pady=5)
        self.system2_cooler_com_port_combobox.current(0)

        ttk.Label(system2_frame, text="Baud Rate:", font=("Arial", 12)).grid(row=7, column=1, sticky="e", padx=10, pady=5)
        self.system2_cooler_baud_rate_entry = ttk.Entry(system2_frame, width=15, font=("Arial", 12))
        self.system2_cooler_baud_rate_entry.grid(row=7, column=2, sticky="w", padx=10, pady=5)
        self.system2_cooler_baud_rate_entry.insert(0, "9600")


        # Apply Button (outside the box)
        ttk.Button(self.settings_tab, text="Apply Settings", command=self.apply_settings).grid(row=2, column=0, columnspan=4, pady=20)

    def apply_settings(self):
        # Retrieve the selected COM Port from the drop-down menu
        com_port = self.com_port_combobox.get()
        baud_rate = self.baud_rate_entry.get()

        # Print the settings to the console (or handle them as needed)
        print(f"COM Port: {int(com_port[-1])}, Baud Rate: {int(baud_rate)}")
    

if __name__ == "__main__":
    app = SettingsTabApp()
    app.mainloop()