"""
Read and count the messages stored in the recorded dat file.

Hardie Pienaar
Makespace Cambridge
July 2018
"""

import binr
import os
import time

# Parameters
filename = "pelham_shed_1_July_2018.dat"

# Open file for reading
reader = open(filename, 'rb')

# Count messages
print("Starting read loop")
buffer = []
try:
    while True:
        read = list(reader.read(100))
        buffer = buffer + read
        if len(read) == 0:
            reader.close()
            print("Done")
            break
        try:
            data, buffer = binr.process_msg(buffer)
            print("Msg: "+str(data["ID"])+" buffer length: "+str(len(buffer)))
            if data["ID"] == 0xF5:
                print(bytearray(data["data"]))
        except ValueError:
            print("Buffer length: "+str(len(buffer)))  
        time.sleep(0.01)
except KeyboardInterrupt:
    reader.close()

        

