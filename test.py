import pyvisa
import time

# pip install pyvisa-py
# pip install mcculw

# Use pyvisa-py backend
rm = pyvisa.ResourceManager('@py')

# Replace with your actual COM port
COM_PORT = '4'
BAUD_RATE = 9600

# Open serial resource
instrument = rm.open_resource(f'ASRL{COM_PORT}::INSTR')

# Configure serial parameters
instrument.baud_rate = BAUD_RATE
instrument.data_bits = 8
instrument.stop_bits = pyvisa.constants.StopBits.one
instrument.parity = pyvisa.constants.Parity.none
instrument.timeout = 3000  # in milliseconds

# Flow control = None (as per manual)
instrument.set_visa_attribute(pyvisa.constants.VI_ATTR_ASRL_FLOW_CNTRL, 0)

# ✅ Set termination characters (based on manual: LF)
instrument.write_termination = '\n'
instrument.read_termination = '\n'

# Helper function
def send_command(cmd, delay=0.1):
    instrument.write(cmd)
    time.sleep(delay)

# --- SCPI Sequence ---
send_command('outp on') # Turn power on
send_command('volt 5') # Set voltage
time.sleep(1)
voltage = instrument.query('meas:volt?')
print(f"Measured Voltage: {voltage.strip()} V")

instrument.close()
