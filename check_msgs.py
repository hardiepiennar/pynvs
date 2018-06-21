"""
Check and request messages from device

Hardie Pienaar
Bosmans Crossing
June 2018
"""

import binr
import serial
import os
import time

# Parameters
port = "COM5"

# Switch device to BINR
print("Switching serial protocol to BINR")
ser = serial.Serial(port, 115200)
ser.write("$PORZA,0,115200,3*7E\r\n".encode())
ser.close()

# Connect to device
print("Connecting to serial port [BINR 115200]")
ser = serial.Serial(port, 115200, parity=serial.PARITY_ODD, timeout=0.2)

# Request current receiver channels status
print("Requesting receiver channels status")
ser.write(binr.request_status_of_receiver_channels())
buffer = ser.read(1000)
data, buffer = binr.process_msg(buffer)
channel_status = binr.process_status_of_receiver_channels(data["data"])
binr.print_status_of_receiver_channels(channel_status)

print("Requesting satellite ephemeris")
ser.write(binr.request_sv_ephemeris(binr.GLONASS, 0,-3))
buffer = ser.read(1000)
data, buffer = binr.process_msg(buffer)
print(data)
print(len(data["data"]))

try:
    while True:

        time.sleep(0.1)
except:
    ser.close() 