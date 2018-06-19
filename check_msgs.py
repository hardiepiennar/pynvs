"""
Check and request messages from device

Hardie Pienaar
Bosmans Crossing
June 2018
"""

import binr
import serial

# Parameters
port = "COM5"

# Switch device to BINR
print("Switching serial protocol to BINR")
ser = serial.Serial(port, 115200)
ser.write("$PORZA,0,115200,3*7E\r\n".encode())
ser.close()

# Connect to device
print("Connecting to serial port [BINR 115200]")
ser = serial.Serial(port, 115200, parity=serial.PARITY_ODD, timeout=1)

# Request current receiver channels status
print("Requesting receiver channels status")
ser.write(binr.request_status_of_receiver_channels())
buffer = ser.read(1000)
data, buffer = binr.process_msg(buffer)
channel_status = binr.process_status_of_receiver_channels(data["data"])

for i in range(len(channel_status)):
    if channel_status[i]["System"] == 1:
        sys = "GPS"
    elif channel_status[i]["System"] == 2:
        sys = "GLO"
    elif channel_status[i]["System"] == 4:
        sys = "SBAS"
    elif channel_status[i]["System"] == 8:
        sys = "Galileo E1b"
    else:
        sys = "None"
    
    if channel_status[i]["Status"] == 0:
        stat = "Auto"
    elif channel_status[i]["Status"] == 1:
        stat = "Manual"
    elif channel_status[i]["Status"] == 2:
        stat = "Testing"
    elif channel_status[i]["Status"] == 3:
        stat = "Error"
    else:
        stat = "None"

    if channel_status[i]["Pseudorange Sign"] == 0:
        pseudo = "Pseudorange Digitization and Measurement"
    elif channel_status[i]["Pseudorange Sign"] == 1:
        pseudo = "Failure"
    elif channel_status[i]["Pseudorange Sign"] == 2:
        pseudo = "Pseudorange Measurement"
    else:
        pseudo = "None"

    print("Channel: "+str(i)+": "+str(sys)+"("\
          +str(channel_status[i]["Number"])+")\tSNR: "\
          +str(channel_status[i]["SNR"])+"\t"\
          +str(stat)+"\t"\
          +str(pseudo))

# # Show output
# print("Waiting for replies")
# buffer = []
# try:
#     while True:
#         # Read buffer
#         buffer = buffer + list(ser.read(10))
#         print("Buffer length: "+str(len(buffer)))
        
#         if len(buffer)>50:
#             # Process buffer
#             data, buffer = binr.process_msg(buffer)
#             # Display messages
            
        
# except KeyboardInterrupt:
#     print("Exiting...")
ser.close() 