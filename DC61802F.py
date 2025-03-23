# dc_power_controller.py

import serial
import time


class DCPowerController:
    def __init__(self, baudrate=38400, timeout=1):
        self.serial = None
        self.port = None
        self.baudrate = baudrate
        self.timeout = timeout
        self.connected = False
        self.model = None  # "61802(F)" or "61804(F)"

        self._connect()

    def _connect(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        for port_name in ports:
            try:
                ser = serial.Serial(
                    port=port_name,
                    baudrate=self.baudrate,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=self.timeout
                )
                self.serial = ser
                self.port = port_name
                if self._identify_model():
                    self.connected = True
                    print(f"✅ Connected to DC Power Supply: {self.model} on {port_name}")
                    return
                else:
                    ser.close()
            except Exception:
                continue
        raise RuntimeError("❌ No compatible DC power supply found.")

    def _identify_model(self):
        self._send_bytes([0x7B, 0x00, 0x08, 0x01, 0xF0, 0x0C, 0x05, 0x7D])
        time.sleep(0.05)
        response = self.serial.read_all().decode(errors="ignore")
        if "61802(F)" in response:
            self.model = "61802(F)"
            return True
        elif "61804(F)" in response:
            self.model = "61804(F)"
            return True
        return False

    def _send_bytes(self, byte_list):
        if self.serial and self.serial.is_open:
            self.serial.write(bytearray(byte_list))

    def _checksum(self, bytes_list):
        return sum(bytes_list[1:bytes_list[2] - 1]) & 0xFF

    def stop(self):
        self._send_bytes([0x7B, 0x00, 0x08, 0x01, 0x0F, 0x00, 0x18, 0x7D])

    def reset(self):
        self._send_bytes([0x7B, 0x00, 0x08, 0x01, 0x0F, 0x01, 0x19, 0x7D])

    def start(self):
        self._send_bytes([0x7B, 0x00, 0x08, 0x01, 0x0F, 0xFF, 0x17, 0x7D])

    def enter_normal_mode(self):
        self._send_bytes([0x7B, 0x00, 0x08, 0x01, 0x0F, 0x0D, 0x25, 0x7D])

    def set_dc_mode(self):
        self._send_bytes([0x7B, 0x00, 0x09, 0x01, 0x5A, 0x04, 0x01, 0x69, 0x7D])

    def set_voltage(self, voltage):
        val = int(voltage * 10)
        high = (val >> 8) & 0xFF
        low = val & 0xFF
        msg = [0x7B, 0x00, 0x0A, 0x01, 0x5A, 0x02, high, low]
        msg.append(self._checksum(msg))
        msg.append(0x7D)
        self._send_bytes(msg)

    def run_voltage_sequence(self, voltage):
        if not self.connected:
            raise RuntimeError("Device not connected.")
        self.stop()
        time.sleep(0.05)
        self.set_dc_mode()
        time.sleep(0.05)
        self.set_voltage(voltage)
        time.sleep(0.05)
        self.start()

    def get_connection_info(self):
        return {"port": self.port, "baudrate": self.baudrate, "model": self.model}

    def close(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
