# Function Generator Controller
from mcculw import ul
from mcculw.enums import CounterChannelType, InterfaceType
from mcculw.device_info import DaqDeviceInfo
from mcculw.ul import ULError
import logging

logging.getLogger(__name__)

class MCCDAQManager:
    # Scanning all devices
    # Managing multiple boards
    # Device discovery and release

    def __init__(self):
        ul.ignore_instacal()
        self.devices = []
        self.board_map = {}  # Maps board_num to descriptor
        self.discover_devices()

    def discover_devices(self):
        self.devices = ul.get_daq_device_inventory(InterfaceType.ANY)
        for i, descriptor in enumerate(self.devices):
            try:
                ul.create_daq_device(i, descriptor)
                self.board_map[i] = descriptor
            except ULError as e:
                print(f"Error creating device {descriptor}: {e}")

    def list_devices(self):
        return [
            {
                "board_num": i,
                "product_name": desc.product_name,
                "unique_id": desc.unique_id,
                "dev_string": str(desc)
            }
            for i, desc in self.board_map.items()
        ]

    def flash_led(self, board_num):
        try:
            ul.flash_led(board_num)
            print(f"Flashed LED on board {board_num}")
            return True
        except ULError as e:
            print(f"Error flashing LED on board {board_num}: {e}")
            return False

    def release_all(self):
        for board_num in self.board_map:
            try:
                ul.release_daq_device(board_num)
            except ULError as e:
                print(f"Error releasing device {board_num}: {e}")
        self.board_map.clear()


class MCCDAQ:
    # Controlling a specific board number (pulse output, stop, etc.)
    
    def __init__(self, board_num=0, auto_detect=False):
        self.board_num = board_num
        self.first_chan_num = -1
        self.last_chan_num = -1
        self.device_info = None

        if auto_detect:
            self._configure_first_detected_device()

        self._detect_pulse_channels()
        if self.first_chan_num == -1:
            raise RuntimeError("No CTRPULSE-capable channels found on the device.")

    def _configure_first_detected_device(self):
        ul.ignore_instacal()
        devices = ul.get_daq_device_inventory(InterfaceType.ANY)  # Use InterfaceType.ANY
        if not devices:
            raise RuntimeError("No MCC devices found.")
        ul.create_daq_device(self.board_num, devices[0])

    def _detect_pulse_channels(self):
        self.device_info = DaqDeviceInfo(self.board_num)
        ctr_info = self.device_info.get_ctr_info()

        pulse_channels = [
            ch.channel_num for ch in ctr_info.chan_info
            if ch.type == CounterChannelType.CTRPULSE
        ]

        if pulse_channels:
            self.first_chan_num = min(pulse_channels)
            self.last_chan_num = max(pulse_channels)

    def start_pulse(self, frequency=100000, duty_cycle=0.5, timer_channel=None):
        if timer_channel is None:
            timer_channel = self.first_chan_num
        try:
            actual_freq, actual_duty, _ = ul.pulse_out_start(
                self.board_num, timer_channel, frequency, duty_cycle)
            return actual_freq, actual_duty
        except ULError as e:
            raise RuntimeError(f"Failed to start pulse output: {e}")

    def stop_all(self):
        if self.first_chan_num != -1:
            for chan in range(self.first_chan_num, self.last_chan_num + 1):
                try:
                    ul.pulse_out_stop(self.board_num, chan)
                except ULError as e:
                    print(f"Error stopping channel {chan}: {e}")

    def stop(self, timer_channel):
        try:
            ul.pulse_out_stop(self.board_num, timer_channel)
        except ULError as e:
            raise RuntimeError(f"Failed to stop pulse output: {e}")


if __name__ == "__main__":
    daq_manager = MCCDAQManager()
    # List all detected devices
    print("Detected Devices:")
    devices = daq_manager.list_devices()
    if not devices:
        print("No devices detected.")
        exit(1)

    for dev in devices:
        print(dev)

    # Flash LED on all detected devices
    print("\nFlashing LEDs on all devices...")
    for dev in devices:
        daq_manager.flash_led(dev["board_num"])

    # Select the first detected device for pulse output
    board_num = devices[0]["board_num"]
    print(f"\nUsing board {board_num} for pulse output.")

    # Initialize the MCCDAQ class for pulse output
    mcc_daq = MCCDAQ(board_num=board_num)

    # Start a pulse output on the first available channel
    print("\nStarting pulse output...")
    frequency = 5000000  # 1 kHz
    duty_cycle = 0.5  # 50%
    actual_freq, actual_duty = mcc_daq.start_pulse(frequency=frequency, duty_cycle=duty_cycle)
    print(f"Pulse output started with frequency: {actual_freq} Hz, duty cycle: {actual_duty * 100}%")

    # Wait for 5 seconds to observe the pulse output
    import time
    time.sleep(30)

    # Stop all pulse outputs
    print("\nStopping all pulse outputs...")
    mcc_daq.stop_all()


# Frequency unstable after 5Mhz; Causing the voltage to be unstable
# Would recommend to use a frequency lower than 5Mhz for stable voltage output