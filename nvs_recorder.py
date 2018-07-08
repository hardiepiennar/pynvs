"""
We need to be able to test this thing without putting on sunscreen every time.
So this file is soley to record the serial stream to a file for later readback 
testing.

Hardie Pienaar
Makespace Cambridge
July 2018
"""

import binr
import serial
import os
import time

# Parameters
port = "COM5"
filename = "recording.dat"

# Switch device to BINR
print("Switching serial protocol to BINR")
ser = serial.Serial(port, 115200)
ser.write("$PORZA,0,115200,3*7E\r\n".encode())
ser.close()

time.sleep(1)
assert(False)
# Connect to device
print("Connecting to serial port [BINR 115200]")
ser = serial.Serial(port, 115200, parity=serial.PARITY_ODD, timeout=1)

# Create file
record_file  = open(filename, "wb")

# Send commands (this is up to you!)
ser.write(binr.request_raw_data(10))

# Start recording
total = 0
try:
    while True:
        buffer = ser.read(100)
        total = total + len(buffer)
        print("Received: "+str(len(buffer))+" bytes. Total: "+str(total))
        record_file.write(buffer)
        time.sleep(0.1)
except KeyboardInterrupt:
    # Close file
    record_file.close()
    ser.close()