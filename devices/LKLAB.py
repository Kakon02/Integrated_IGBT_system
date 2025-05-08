import serial
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
import logging

logging.getLogger(__name__)

class LKLabController:
    def __init__(self, port: str = None, baudrate=9600, slave_id=1, timeout=1):
        self.client = None
        self.port = port
        self.baudrate = baudrate
        self.slave_id = slave_id
        self.timeout = timeout
        self._connection = False
        self._operation = False

    def _connect(self):

        client = ModbusClient(
                method='rtu',
                port=self.port,
                baudrate=self.baudrate,
                parity=serial.PARITY_EVEN,
                bytesize=8,
                stopbits=1,
                timeout=self.timeout
        )
        if client.connect():
                result = client.read_holding_registers(9, 1, unit=self.slave_id)
                if not result.isError():
                    self.client = client
                    self._connection = True
                else:
                    client.close()
                    self._connection = False
        

    def get_temperatures(self):
        """Get the current and setpoint temperatures."""
                
        if self._connection:
            npv = self.client.read_holding_registers(1, 1, unit=self.slave_id)
            nsv = self.client.read_holding_registers(2, 1, unit=self.slave_id)
            npv_value = self._convert_temp(npv.registers[0])
            nsv_value = self._convert_temp(nsv.registers[0])
            return {"current": npv_value, "setpoint": nsv_value}        
        

    def _convert_temp(self, raw):
        """Convert raw temperature data to Celsius."""
        if raw > 32767:
            return (raw - 65536) / 100
        return raw / 100

    def set_temperature(self, temp_celsius):
        """Set the target temperature."""
        if self._connection:
            val = int(temp_celsius * 100)
            if val < 0:
                val += 65536
            self.client.write_register(21, val, unit=self.slave_id)


    def adjust_temperature(self, delta):
        """Adjust the temperature by a delta value."""
        if self._connection:
            nsv = self.client.read_holding_registers(2, 1, unit=self.slave_id)
            current_val = nsv.registers[0]
            adjusted_val = (current_val + int(delta * 100)) % 65536
            self.client.write_register(21, adjusted_val, unit=self.slave_id)
            
    def turn_on_operation(self):
        """Turn on the operation."""
        if not self._operation:
            self.client.write_register(25, 1, unit=self.slave_id)
            self._operation = True

    def turn_off_operation(self):
        """Turn off the operation."""
        if self._operation:
            self.client.write_register(25, 1, unit=self.slave_id)
            self._operation = False

    def close(self):
        """Close the Modbus connection."""
        if self.client:
            self.client.close()


# Example usage
if __name__ == "__main__":

    try:
        lk = LKLabController('COM3')
        # lk.port = 'COM4'
        # lk.baudrate = 9600
        lk._connect()

        # Get current & setpoint temperatures

        # Set a new temperature
        lk.set_temperature(25.0)
        print("Set temperature to 25.0°C")

        # Turn on operation
        lk.turn_on_operation()
        print("Operation turned on")

        temps = lk.get_temperatures()
        print("Current Temp:", temps["current"], "Setpoint Temp:", temps["setpoint"])

        time.sleep(5)

        # Turn off operation
        lk.turn_off_operation()
        print("Operation turned off")

        # Close the connection
        lk.close()
    except RuntimeError as e:
        print(e)