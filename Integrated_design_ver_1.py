import tkinter as tk
from tkinter import ttk

class IntegratedControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Integrated IGBT Control Panel")
        screen_width = int(self.winfo_screenwidth()*0.8)
        screen_height = int(self.winfo_screenheight()*0.8)
        self.geometry(f"{screen_width}x{screen_height}")

        self.resizable(True, True)

        # Setup tabs
        tab_control = ttk.Notebook(self)
        self.real_time_tab = ttk.Frame(tab_control)
        self.loop_tab = ttk.Frame(tab_control)
        self.settings_tab = ttk.Frame(tab_control)

        tab_control.add(self.real_time_tab, text="Real-Time Control") # Add tab
        tab_control.add(self.loop_tab, text="Loop Control")
        tab_control.add(self.settings_tab, text="Settings")
        tab_control.pack(expand=1, fill="both")

        self.setup_real_time_tab()
        self.setup_loop_tab()
        self.setup_settings_tab()

    def setup_real_time_tab(self):
        ttk.Label(self.real_time_tab, text="Current Temp:", font=("Arial", 20)).grid(row=0, column=0, padx=10, pady=20)
        self.current_temp = ttk.Entry(self.real_time_tab, font=("Arial", 20), width=10)
        self.current_temp.grid(row=0, column=1)

        ttk.Label(self.real_time_tab, text="Set Temp:", font=("Arial", 20)).grid(row=1, column=0, padx=10, pady=10)
        self.set_temp = ttk.Entry(self.real_time_tab, font=("Arial", 20), width=10)
        self.set_temp.grid(row=1, column=1)

        # Instant buttons
        ttk.Button(self.real_time_tab, text="+1", command=lambda: self.change_temp(1)).grid(row=2, column=0, padx=10)
        ttk.Button(self.real_time_tab, text="+0.1", command=lambda: self.change_temp(0.1)).grid(row=2, column=1)
        ttk.Button(self.real_time_tab, text="-1", command=lambda: self.change_temp(-1)).grid(row=3, column=0)
        ttk.Button(self.real_time_tab, text="-0.1", command=lambda: self.change_temp(-0.1)).grid(row=3, column=1)

        # Run/Stop
        self.run_btn = ttk.Button(self.real_time_tab, text="Run", command=self.toggle_run)
        self.run_btn.grid(row=4, column=0, columnspan=2, pady=20)

    def setup_loop_tab(self):
        ttk.Label(self.loop_tab, text="Loop Configuration", font=("Arial", 18, "bold")).pack(pady=10)

        self.loop_display = tk.Text(self.loop_tab, height=10, width=80, font=("Arial", 12))
        self.loop_display.pack(pady=10)

        add_btn = ttk.Button(self.loop_tab, text="Add Loop Step")
        add_btn.pack(pady=5)

        run_loop_btn = ttk.Button(self.loop_tab, text="Run Loop")
        run_loop_btn.pack(pady=5)

    def setup_settings_tab(self):
        ttk.Label(self.settings_tab, text="Settings", font=("Arial", 18)).pack(pady=20)

        ttk.Label(self.settings_tab, text="COM Port:").pack()
        self.com_port_entry = ttk.Entry(self.settings_tab, width=10)
        self.com_port_entry.pack()

        ttk.Label(self.settings_tab, text="Baud Rate:").pack()
        self.baud_rate_entry = ttk.Entry(self.settings_tab, width=10)
        self.baud_rate_entry.pack()

        ttk.Button(self.settings_tab, text="Apply").pack(pady=10)

    def toggle_run(self):
        if self.run_btn["text"] == "Run":
            self.run_btn.config(text="Stop")
        else:
            self.run_btn.config(text="Run")

    def change_temp(self, delta):
        try:
            value = float(self.set_temp.get())
        except ValueError:
            value = 0.0
        value += delta
        self.set_temp.delete(0, tk.END)
        self.set_temp.insert(0, f"{value:.1f}")

    def read_entry_data(self):
        current_temp_value = self.current_temp.get()  # Read value from current_temp entry
        set_temp_value = self.set_temp.get()  # Read value from set_temp entry
        print(f"Current Temp: {current_temp_value}, Set Temp: {set_temp_value}")
        return current_temp_value, set_temp_value


if __name__ == "__main__":
    app = IntegratedControlPanel()
    app.mainloop()
