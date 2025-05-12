import time
from uldaq import (
    get_daq_device_inventory, InterfaceType, DaqDevice, PulseOutOption,
    TmrIdleState, ULException
)

class MCCDAQManager:
    def __init__(self):
        self.devices = get_daq_device_inventory(InterfaceType.ANY)
        self.device_map = {}
        self._init_devices()

    def _init_devices(self):
        for idx, descriptor in enumerate(self.devices):
            try:
                device = DaqDevice(descriptor)
                device.connect()
                self.device_map[idx] = device
            except ULException as e:
                print(f"Error initializing device {descriptor}: {e}")

    def list_devices(self):
        return [
            {
                "board_num": i,
                "product_name": dev.get_descriptor().product_name,
                "unique_id": dev.get_descriptor().unique_id,
                "dev_string": str(dev.get_descriptor())
            }
            for i, dev in self.device_map.items()
        ]

    def flash_led(self, board_num, flashes=3):
        try:
            self.device_map[board_num].flash_led(flashes)
            print(f"Flashed LED on board {board_num}")
        except ULException as e:
            print(f"Error flashing LED: {e}")

    def release_all(self):
        for dev in self.device_map.values():
            try:
                dev.disconnect()
                dev.release()
            except ULException as e:
                print(f"Error releasing device: {e}")
        self.device_map.clear()


class MCCDAQ:
    def __init__(self, device: DaqDevice):
        self.device = device
        self.timer_device = self.device.get_tmr_device()
        self.timer_info = self.timer_device.get_info()
        self.timer_index = self._find_timer_channel()

    def _find_timer_channel(self):
        num_timers = self.timer_info.get_num_tmrs()
        if num_timers > 0:
            return 0  # Use the first available timer
        else:
            raise RuntimeError("No timer channels available on this device.")

    def start_pulse(self, frequency=1000.0, duty_cycle=0.5, pulse_count=0,
                    initial_delay=0.0, idle_state=TmrIdleState.LOW,
                    options=PulseOutOption.DEFAULT):
        try:
            actual_freq, actual_duty, actual_delay = self.timer_device.pulse_out_start(
                self.timer_index, frequency, duty_cycle, pulse_count,
                initial_delay, idle_state, options
            )
            print(f"Pulse started on timer {self.timer_index} with frequency: {actual_freq} Hz, duty cycle: {actual_duty * 100}%, initial delay: {actual_delay} s")
        except ULException as e:
            raise RuntimeError(f"Failed to start pulse: {e}")

    def stop_pulse(self):
        try:
            self.timer_device.pulse_out_stop(self.timer_index)
            print(f"Pulse stopped on timer {self.timer_index}.")
        except ULException as e:
            raise RuntimeError(f"Failed to stop pulse: {e}")


if __name__ == "__main__":
    manager = MCCDAQManager()
    devices = manager.list_devices()
    if not devices:
        print("No devices found.")
        exit(1)

    print("Detected devices:")
    for dev in devices:
        print(dev)

    print("\nFlashing LEDs...")
    for dev in devices:
        manager.flash_led(dev["board_num"])

    # Use first device
    device = manager.device_map[0]
    mcc_daq = MCCDAQ(device)

    print("\nStarting pulse output...")
    mcc_daq.start_pulse(frequency=5000.0, duty_cycle=0.5)

    time.sleep(5)

    print("\nStopping pulse...")
    mcc_daq.stop_pulse()

    manager.release_all()
