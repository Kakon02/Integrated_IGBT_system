from datetime import datetime, timedelta
from PyQt5.QtCore import QTimer

class SystemController:
    def __init__(self, daq, power, cooler, runtime_object, progress_bar_object, remaining_time_object, console):
        self.daq = daq
        self.power = power
        self.cooler = cooler
        self.original_runtime = None
        self.runtime = None
        self.console = console
        self.start_time = None

        # Setup timer for progress update
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_progress(progress_bar_object, remaining_time_object, runtime_object))

    def start_system(self, freq, duty, voltage, temp, runtime):
        try:
            self.console.append("🚀 Starting system...")

            self.daq.start_pulse(freq, duty)
            self.console.append(f"✅ Pulse started at {freq} Hz, {duty*100}% duty.")

            self.power.run_voltage_sequence(voltage)
            self.console.append(f"✅ Voltage set to {voltage} V.")

            self.cooler.set_temperature(temp)
            self.console.append(f"✅ Cooler set to {temp} °C.")

            self.runtime = runtime * 60  # Convert minutes to seconds
            self.original_runtime = runtime * 60  # Store original runtime for stopping
            self.start_time = datetime.now()

            self.timer.start(1000)
            self.console.append("🕒 Progress timer started.")

        except Exception as e:
            self.console.append(f"❌ Error starting system: {e}")

    def stop_system(self, runtime_object=None):
        try:
            self.daq.stop_all()
            self.console.append("✅ Pulse output stopped.")

            self.power.stop()
            self.console.append("✅ DC Power stopped.")

            self.cooler.turn_off_operation()
            self.console.append("✅ Cooler operation stopped.")

            self.timer.stop()
            self.console.append("🛑 Timer stopped.")

            runtime_object.setText(self.original_runtime / 60)


        except Exception as e:
            self.console.append(f"❌ Error stopping system: {e}")

    def pause_system(self, runtime_object=None):
        try:
            self.daq.stop_all()
            self.console.append("⏸️ System paused.")

            self.timer.stop()
            self.console.append("🛑 Timer paused.")

            elapsed = (datetime.now() - self.start_time).total_seconds()
            self.runtime -= elapsed
            runtime_object.setText(str(self.runtime / 60))
            self.start_time = None
            self.console.append("Paused system")
            self.console.append(f"⏳ Remaining runtime: {self.runtime / 60:.2f} minutes.")
            

        except Exception as e:
            self.console.append(f"❌ Error pausing system: {e}")

    def update_progress(self, progress_bar=None, remaining_time=None):
        if not self.start_time:
            return
        elapsed = (datetime.now() - self.start_time).total_seconds()
        percentage = (elapsed / self.runtime) * 100
        progress_bar.setValue(min(percentage, 100))
        # Show elaped time in HH:MM:SS format
        remaining_time.setText(str(timedelta(seconds=int(self.runtime - elapsed))))

        if percentage >= 100:
            self.console.append("✅ System completed.")
            self.stop_system()