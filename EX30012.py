# ex300_device.py

import pyvisa
import time
import serial.tools.list_ports


class EX300_12:
    def __init__(self, baud_rate=9600, timeout=3000):
        self.rm = pyvisa.ResourceManager('@py')
        self.instrument = None
        self.port_name = None
        self.baud_rate = baud_rate
        self.timeout = timeout

        self._connect()

    def _connect(self):
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

                # Probe with voltage measurement
                inst.write('meas:volt?')
                time.sleep(0.1)
                response = inst.read().strip()
                if self._is_valid_voltage(response):
                    self.instrument = inst
                    self.port_name = port.device
                    print(f"✅ Connected to EX300-12 on {self.port_name}")
                    return
                else:
                    inst.close()
            except Exception:
                continue

        raise RuntimeError("❌ EX300-12 device not found on any COM port.")

    def _is_valid_voltage(self, response):
        try:
            float(response)
            return True
        except ValueError:
            return False

    def get_connection_info(self):
        return {"port": self.port_name, "baud_rate": self.baud_rate}

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
        if self.instrument:
            self.instrument.close()
