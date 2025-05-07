from datetime import datetime, timedelta
from PyQt5.QtCore import QTimer

class SystemController:
    def __init__(self, daq, power, cooler, ui, console):
        self.daq = daq
        self.power = power
        self.cooler = cooler
        self.ui = ui
        self.console = console

        self.runtime = 0
        self.start_time = None

        # Setup timer for progress update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    def start_system(self, freq, duty, voltage, temp, runtime):
        try:
            self.console.append("🚀 Starting system...")

            self.daq.start_pulse(freq, duty)
            self.console.append(f"✅ Pulse started at {freq} Hz, {duty*100}% duty.")

            self.power.run_voltage_sequence(voltage)
            self.console.append(f"✅ Voltage set to {voltage} V.")

            self.cooler.set_temperature(temp)
            self.console.append(f"✅ Cooler set to {temp} °C.")

            self.runtime = runtime
            self.start_time = datetime.now()

            self.timer.start(1000)
            self.console.append("🕒 Progress timer started.")

        except Exception as e:
            self.console.append(f"❌ Error starting system: {e}")

    def stop_system(self):
        try:
            self.daq.stop_all()
            self.console.append("✅ Pulse output stopped.")

            self.power.stop()
            self.console.append("✅ DC Power stopped.")

            self.cooler.turn_off_operation()
            self.console.append("✅ Cooler operation stopped.")

            self.timer.stop()
            self.console.append("🛑 Timer stopped.")

        except Exception as e:
            self.console.append(f"❌ Error stopping system: {e}")

    def update_progress(self):
        if not self.start_time:
            return
        elapsed = (datetime.now() - self.start_time).total_seconds()
        percentage = (elapsed / self.runtime) * 100
        self.ui.System_1_Progress.setValue(min(percentage, 100))

        if percentage >= 100:
            self.console.append("✅ System completed.")
            self.stop_system()
