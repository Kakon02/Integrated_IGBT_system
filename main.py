# from test import EX300_12

# try:
#     device = EX300_12()
#     device.turn_on()
#     device.set_voltage(5)
#     voltage = device.measure_voltage()
#     print(f"Measured Voltage: {voltage} V")
#     device.turn_off()
#     device.close()
# except RuntimeError as e:
#     print(e)

# from LKLAB import LKLabController

# lk = LKLabController(port='COM4')

# # Get current & setpoint temps
# temps = lk.get_temperatures()
# print("Current:", temps["current"], "Setpoint:", temps["setpoint"])

# # Set new temperature
# lk.set_temperature(42.5)

# # Increase temp by +1.0°C
# lk.adjust_temperature(+1.0)

# # Turn on/off operation
# lk.turn_on_operation()
# lk.turn_off_operation()

# # Run a simple loop (e.g., [temp, hr, min, sec] * n)
# lk.run_loop([30, 0, 0, 10, 40, 0, 0, 5])

# lk.close()


# from MCCDAQ import MCCDAQManager

# daq = MCCDAQManager()

# print("Detected Devices:")
# for dev in daq.list_devices():
#     print(dev)

# # Flash LED on all devices
# for dev in daq.list_devices():
#     daq.flash_led(dev["board_num"])

# # Release devices when done
# daq.release_all()
