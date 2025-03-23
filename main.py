# from EX30012 import EX300_12

# ex = EX300_12()

# info = ex.get_connection_info()
# print("Connected on:", info["port"])
# print("Baud rate:", info["baud_rate"])

# ex.set_voltage(5.0)
# print("Voltage set. Measuring...")
# print("Voltage:", ex.measure_voltage(), "V")

# ex.turn_off()
# ex.close()

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

# from DC61802F import DCPowerController

# dc = DCPowerController()

# info = dc.get_connection_info()
# print(f"Connected to {info['model']} on {info['port']}")

# dc.run_voltage_sequence(150)  # Set 150V and start
# time.sleep(3)
# dc.stop()
# dc.close()
