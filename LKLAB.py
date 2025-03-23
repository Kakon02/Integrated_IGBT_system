# lklab_controller.py

import serial
from pymodbus.client import ModbusSerialClient as ModbusClient


class LKLabController:
    def __init__(self, port='COM4', baudrate=9600, slave_id=1, timeout=1):
        self.client = ModbusClient(
            method='rtu',
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_EVEN,
            bytesize=8,
            stopbits=1,
            timeout=timeout
        )
        self.slave_id = slave_id
        self.operation_value = False
        if not self.client.connect():
            raise ConnectionError(f"Failed to connect to LKLAB on {port}")
        self._update_operation_state()

    def _update_operation_state(self):
        result = self.client.read_holding_registers(9, 1, unit=self.slave_id)
        if result.isError():
            raise IOError("Failed to read operation state.")
        self.operation_value = result.registers[0] != 0

    def get_temperatures(self):
        npv = self.client.read_holding_registers(1, 1, unit=self.slave_id)
        nsv = self.client.read_holding_registers(2, 1, unit=self.slave_id)
        npv_value = self._convert_temp(npv.registers[0])
        nsv_value = self._convert_temp(nsv.registers[0])
        return {"current": npv_value, "setpoint": nsv_value}

    def _convert_temp(self, raw):
        if raw > 32767:
            return (raw - 65536) / 100
        return raw / 100

    def set_temperature(self, temp_celsius):
        val = int(temp_celsius * 100)
        if val < 0:
            val += 65536
        self.client.write_register(21, val, unit=self.slave_id)

    def adjust_temperature(self, delta):
        nsv = self.client.read_holding_registers(2, 1, unit=self.slave_id)
        current_val = nsv.registers[0]
        adjusted_val = (current_val + int(delta * 100)) % 65536
        self.client.write_register(21, adjusted_val, unit=self.slave_id)

    def turn_on_operation(self):
        self.client.write_register(25, 1, unit=self.slave_id)
        self.operation_value = True

    def turn_off_operation(self):
        self.client.write_register(25, 0, unit=self.slave_id)
        self.operation_value = False

    def run_loop(self, loop_list):
        if not loop_list or not isinstance(loop_list, list):
            return
        self.turn_on_operation()
        for i in range(0, len(loop_list), 4):
            temp = float(loop_list[i])
            hour = int(loop_list[i + 1])
            minute = int(loop_list[i + 2])
            second = int(loop_list[i + 3])
            duration_ms = (hour * 3600 + minute * 60 + second) * 1000
            self.set_temperature(temp)
            self.client.sleep(duration_ms / 1000)
        self.turn_off_operation()

    def close(self):
        self.client.close()
