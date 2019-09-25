"""
Check and request gps receiver status 

Hardie Pienaar
Bosmans Crossing
September 2019
"""

import binr
import serial
import os
import time

# Parameters
port = "/dev/ttyAMA0"

# Switch device to BINR
print("Switching serial protocol to BINR")
ser = serial.Serial(port, 115200)
ser.write("$PORZA,0,115200,3*7E\r\n".encode())
ser.close()

# Connect to device
print("Connecting to serial port [BINR 115200]")
ser = serial.Serial(port, 115200, parity=serial.PARITY_ODD, timeout=0.5)

# Cancel all previous requests
print("Cancelling old requests")
ser.write(binr.cancel_requests())
time.sleep(1)

try:
    while True:
        try:
            # Clear screen
            # Request current receiver channels status
            print("Requesting receiver channels status")
            ser.write(binr.request_status_of_receiver_channels())
            buffer = ser.read(1000)
            data, buffer = binr.process_msg(buffer)
            channel_status = binr.process_status_of_receiver_channels(data["data"])
            os.system('cls' if os.name== 'nt' else 'clear')
            binr.print_status_of_receiver_channels(channel_status)
            time.sleep(1)
        except ValueError:
                s = 1
        time.sleep(0.1)
except KeyboardInterrupt:
    ser.close() 
