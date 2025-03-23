# ex300_multi.py
import pyvisa
import time
import serial.tools.list_ports


class EX300_12_Device:
    def __init__(self, instrument, port_name):
        self.instrument = instrument
        self.port_name = port_name

    def send_command(self, cmd, delay=0.1):
        self.instrument.write(cmd)
        time.sleep(delay)

    def query(self, cmd, delay=1):
        time.sleep(delay)
        return self.instrument.query(cmd).strip()

    def turn_on(self):
        self.send_command('outp on')

    def turn_off(self):
        self.send_command('outp off')

    def set_voltage(self, value):
        self.send_command(f'volt {value}')

    def measure_voltage(self):
        return self.query('meas:volt?')

    def close(self):
        self.instrument.close()


class EX300_12_Manager:
    def __init__(self, baud_rate=9600, timeout=3000):
        self.rm = pyvisa.ResourceManager('@py')
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.devices = self._detect_devices()

    def _detect_devices(self):
        found_devices = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            try:
                com_str = port.device.replace("COM", "")
                resource_str = f'ASRL{com_str}::INSTR'
                inst = self.rm.open_resource(resource_str)
                inst.baud_rate = self.baud_rate
                inst.data_bits = 8
                inst.stop_bits = pyvisa.constants.StopBits.one
                inst.parity = pyvisa.constants.Parity.none
                inst.timeout = self.timeout
                inst.set_visa_attribute(pyvisa.constants.VI_ATTR_ASRL_FLOW_CNTRL, 0)
                inst.write_termination = '\n'
                inst.read_termination = '\n'

                # Probe
                inst.write('meas:volt?')
                time.sleep(0.1)
                response = inst.read().strip()
                if self._is_valid_voltage(response):
                    device = EX300_12_Device(inst, port.device)
                    found_devices.append(device)
                    print(f"✅ Connected to EX300-12 on {port.device}")
                else:
                    inst.close()
            except Exception:
                continue
        return found_devices

    def _is_valid_voltage(self, response):
        try:
            float(response)
            return True
        except ValueError:
            return False

    def close_all(self):
        for dev in self.devices:
            dev.close()
        self.devices.clear()
