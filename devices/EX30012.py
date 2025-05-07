import pyvisa
import time
import serial.tools.list_ports
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class EX300_12:
    def __init__(self, port: Optional[str] = None, baud_rate: int = 9600, timeout: int = 3000):
        self.rm = pyvisa.ResourceManager('@py')
        self.instrument = None
        self.port_name = port
        self.baud_rate = baud_rate
        self.timeout = timeout


    def _configure_instrument(self, inst):
        """Configure the instrument with standard settings."""
        inst.baud_rate = self.baud_rate
        inst.data_bits = 8
        inst.stop_bits = pyvisa.constants.StopBits.one
        inst.parity = pyvisa.constants.Parity.none
        inst.timeout = self.timeout
        inst.set_visa_attribute(pyvisa.constants.VI_ATTR_ASRL_FLOW_CNTRL, 0)
        inst.write_termination = '\n'
        inst.read_termination = '\n'

    def _probe_device(self, inst):
        """Probe the device to check if it's a valid EX300-12."""
        try:
            response = inst.query('meas:volt?').strip()
            return self._is_valid_voltage(response)
        except Exception:
            return False

    def _connect_to_port(self, port: str):
        """Attempt to connect to a specific port."""
        try:
            com_str = port.replace("COM", "")
            resource_str = f'ASRL{com_str}::INSTR'
            inst = self.rm.open_resource(resource_str)
            self._configure_instrument(inst)
            if self._probe_device(inst):
                self.instrument = inst
                self.port_name = port
                logging.info(f"✅ Connected to EX300-12 on {self.port_name}")
            else:
                inst.close()
                raise RuntimeError(f"❌ Device on {port} is not a valid EX300-12.")
        except Exception as e:
            raise RuntimeError(f"❌ Failed to connect to {port}: {e}")

    # def _auto_connect(self):
    #     """Automatically scan and connect to an available port."""
    #     ports = serial.tools.list_ports.comports()
    #     for port in ports:
    #         try:
    #             time.sleep(0.2)
    #             self._connect_to_port(port.device)
    #             return
    #         except RuntimeError:
    #             continue
        # raise RuntimeError("❌ EX300-12 device not found on any COM port.")

    def _is_valid_voltage(self, response: str) -> bool:
        """Check if the response is a valid voltage."""
        try:
            float(response)
            return True
        except ValueError:
            return False

    def get_connection_info(self):
        return {"port": self.port_name, "baud_rate": self.baud_rate}

    def send_command(self, cmd: str, delay: float = 0.1):
        self.instrument.write(cmd)
        time.sleep(delay)

    def query(self, cmd: str, delay: float = 1.0) -> str:
        time.sleep(delay)
        return self.instrument.query(cmd).strip()

    def turn_on(self):
        self.send_command('outp on')

    def turn_off(self):
        self.send_command('outp off')

    def set_voltage(self, value: float):
        self.send_command(f'volt {value}')

    def measure_voltage(self) -> str:
        return self.query('meas:volt?')

    def close(self):
        if self.instrument:
            self.instrument.close()
            logging.info("✅ Instrument connection closed.")


if __name__ == '__main__':
    ex300_12 = EX300_12()
    ex300_12._auto_connect()
    ex300_12.turn_on()
    ex300_12.set_voltage(10)
    print(ex300_12.measure_voltage())
    ex300_12.close()

