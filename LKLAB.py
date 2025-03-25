import serial
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from serial.tools import list_ports


class LKLabController:
    def __init__(self, port, baudrate=9600, slave_id=1, timeout=1):
        self.client = None
        self.port = port
        self.baudrate = baudrate
        self.slave_id = slave_id
        self.timeout = timeout
        self.operation_value = False

        # Automatically connect to the device on initialization
        # self._auto_connect()

    def _connect(self):
        try:
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
                result = client.read_holding_registers(0, 1, unit=self.slave_id)
                if not result.isError():
                    self.client = client
                    self._update_operation_state()
                    print(f"✅ Connected to LKLAB device on {self.port}")
                    return
                else:
                    client.close()
                    raise IOError("Failed to read holding register.")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to LKLAB device on {self.port}") from e

    def _auto_connect(self):
        """Automatically connect to the LKLAB device by scanning available ports."""
        ports = [p.device for p in list_ports.comports()]  # Get a list of available ports
        for port_name in ports:
            try:
                # Attempt to connect to the port
                client = ModbusClient(
                    method='rtu',
                    port=port_name,
                    baudrate=self.baudrate,
                    parity=serial.PARITY_EVEN,
                    bytesize=8,
                    stopbits=1,
                    timeout=self.timeout
                )
                if client.connect():
                    # Verify the connection by reading a known register
                    result = client.read_holding_registers(9, 1, unit=self.slave_id)
                    if not result.isError():
                        # Successfully connected
                        self.client = client
                        self.port = port_name
                        self._update_operation_state()
                        print(f"✅ Connected to LKLAB device on {port_name}")
                        return
                    else:
                        client.close()
            except Exception as e:
                raise ConnectionError(f"Failed to connect on {port_name}") from e

        raise RuntimeError("No compatible LKLAB device found on available ports.")

    def _update_operation_state(self):
        """Update the operation state of the device."""
        result = self.client.read_holding_registers(9, 1, unit=self.slave_id)
        if result.isError():
            raise IOError("Failed to read operation state.")
        self.operation_value = result.registers[0] != 0

    def get_temperatures(self):
        """Get the current and setpoint temperatures."""
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
        val = int(temp_celsius * 100)
        if val < 0:
            val += 65536
        self.client.write_register(21, val, unit=self.slave_id)

    def adjust_temperature(self, delta):
        """Adjust the temperature by a delta value."""
        nsv = self.client.read_holding_registers(2, 1, unit=self.slave_id)
        current_val = nsv.registers[0]
        adjusted_val = (current_val + int(delta * 100)) % 65536
        self.client.write_register(21, adjusted_val, unit=self.slave_id)

    def turn_on_operation(self):
        """Turn on the operation."""
        self.client.write_register(25, 1, unit=self.slave_id)
        self.operation_value = True

    def turn_off_operation(self):
        """Turn off the operation."""
        self.client.write_register(25, 0, unit=self.slave_id)
        self.operation_value = False

    def close(self):
        """Close the Modbus connection."""
        if self.client:
            self.client.close()


# Example usage
if __name__ == "__main__":

    try:
        lk = LKLabController('COM4')
        # lk.port = 'COM4'
        # lk.baudrate = 9600
        # lk._connect()

        # Get current & setpoint temperatures
        temps = lk.get_temperatures()
        print("Current Temp:", temps["current"], "Setpoint Temp:", temps["setpoint"])

        # Set a new temperature
        lk.set_temperature(25.0)
        print("Set temperature to 25.0°C")

        # Turn on operation
        lk.turn_on_operation()
        print("Operation turned on")

        # Turn off operation
        lk.turn_off_operation()
        print("Operation turned off")

        # Close the connection
        lk.close()
    except RuntimeError as e:
        print(e)