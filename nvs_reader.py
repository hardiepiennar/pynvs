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
filename = "recording.dat"

# Open file for reading
reader = open(filename, 'rb')

# Count messages
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
        except ValueError:
            print("Buffer length: "+str(len(buffer)))  
        time.sleep(0.5)
except KeyboardInterrupt:
    reader.close()

        

