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
ser = serial.Serial(port, 115200, parity=serial.PARITY_ODD, timeout=0.5)
#ser = open("pelham_shed_1_July_2018.dat",'rb')

# Request current receiver channels status
# print("Requesting receiver channels status")
# ser.write(binr.request_status_of_receiver_channels())
# buffer = ser.read(1000)
# data, buffer = binr.process_msg(buffer)
# channel_status = binr.process_status_of_receiver_channels(data["data"])
# binr.print_status_of_receiver_channels(channel_status)

# print("Requesting satellite ephemeris")
ser.write(binr.cancel_requests())
time.sleep(0.5)
ser.write(binr.request_sv_ephemeris(binr.GPS, 3,-3))
# buffer = ser.read(1000)
# data, buffer = binr.process_msg(buffer) 

print("Requesting raw data stream")
ser.write(binr.request_raw_data(10))
buffer = []
try:
    while True:
        try:
            
            buffer = list(ser.read_until(terminator='\x10\x03'))
            if len(buffer) > 0:               
                data, buffer = binr.process_msg(list(buffer))
                print(len(buffer))
                print("Msg: "+str(hex(data["ID"]))+": "+
                      str(len(data["data"]))+" bytes : "+
                      str(bytearray(data["data"][0:50])))
                if data["ID"] == 0xF5:
                   raw_data = binr.process_raw_data(data["data"])
                   binr.print_raw_data(raw_data)
            time.sleep(0.1)
        except ValueError:
                s = 1
        time.sleep(0.1)
except KeyboardInterrupt:
    ser.close() 