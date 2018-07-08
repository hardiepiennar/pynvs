"""
Attempt to do RTK with a base and rover input stream

Hardie Pienaar
Makespace Cambridge
July 2018
"""

import serial
import binr
import time
import numpy as np 

Nc = 28 # Number of raw data channels
T_IDX = 0 # Time index
C_IDX = 1 # Carrier index
P_IDX = 2 # Pseudorange index
SNR_IDX = 3 # Signal to noise index

rover_obs = np.zeros((Nc, 4))
base_obs = np.zeros((Nc, 4))

# Define input streams
rover_stream = serial.Serial("COM5", 115200, parity=serial.PARITY_ODD, timeout=0.5)
base_stream = serial.Serial("COM6", 115200, parity=serial.PARITY_ODD, timeout=0.5)

# Main loop
while True:
    rover_obs = np.zeros((Nc, 4))
    base_obs = np.zeros((Nc, 4))

    # Get messages from base and rover
    print("Checking for messages")
    if rover_stream.in_waiting > 0:
        # Read and process the messages
        try:
            rover_buffer = list(rover_stream.read_until(terminator='\x10\x03'))
            rover_msg, rover_buffer = binr.process_msg(rover_buffer)
            print("Rover message received. Unread buffer size: "+str(len(rover_buffer)))

            # We are only interrested in observation and navigation messages
            if rover_msg['ID'] == 0xF5: # observation message
                rover_data = binr.process_raw_data(rover_msg["data"])

                # Calculate obervable receiver time
                t_rx = (rover_data["Time"] + rover_data["GPS time shift"])/1000
                
                # Loop through all channels
                for i in range(len(rover_data["Carrier Phase"])):
                    # Check if raw data is valid
                    if (rover_data["Signal Type"][i] == binr.GPS and 
                        rover_data["Flags"][i]&0b00011011 == 0b00011011): # Only handle GPS for now
                        
                        # Start adding information 
                        sat_no = rover_data["Sat Number"][i]
                        phase = rover_data["Carrier Phase"][i]
                        prng = rover_data["Pseudo Range"][i]
                        snr = rover_data["SNR"][i]
                        rover_obs[sat_no,T_IDX] = t_rx
                        rover_obs[sat_no,P_IDX] = prng
                        rover_obs[sat_no,C_IDX] = phase  
                        rover_obs[sat_no,SNR_IDX] = snr        

            elif rover_msg['ID'] == 0xF7: # navigation message
                rover_data = binr.process_extended_ephemeris_of_satellites(rover_msg["data"])
            else:
                print("Discarding unused message: "+str(hex(rover_msg['ID'])))
        except ValueError:
            print("No message found in rover buffer.")
    if base_stream.in_waiting > 0:
        # Read and process the messages
        try:
            base_buffer = list(base_stream.read_until(terminator='\x10\x03'))
            base_msg, base_buffer = binr.process_msg(base_buffer)
            print("base message received. Unread buffer size: "+str(len(base_buffer)))

            # We are only interrested in observation and navigation messages
            if base_msg['ID'] == 0xF5: # observation message
                base_data = binr.process_raw_data(base_msg["data"])

                # Calculate obervable receiver time
                t_rx = (base_data["Time"] + base_data["GPS time shift"])/1000
                
                # Loop through all channels
                for i in range(len(base_data["Carrier Phase"])):
                    # Check if raw data is valid
                    if (base_data["Signal Type"][i] == binr.GPS and 
                        base_data["Flags"][i]&0b00011011 == 0b00011011): # Only handle GPS for now
                        
                        # Start adding information 
                        sat_no = base_data["Sat Number"][i]
                        phase = base_data["Carrier Phase"][i]
                        prng = base_data["Pseudo Range"][i]
                        snr = base_data["SNR"][i]
                        base_obs[sat_no,T_IDX] = t_rx
                        base_obs[sat_no,P_IDX] = prng
                        base_obs[sat_no,C_IDX] = phase   
                        base_obs[sat_no,SNR_IDX] = snr      

            elif base_msg['ID'] == 0xF7: # navigation message
                base_data = binr.process_extended_ephemeris_of_satellites(base_msg["data"])
            else:
                print("Discarding unused message: "+str(hex(base_msg['ID'])))
        except ValueError:
            print("No message found in base buffer.")

    print("Observables Rover: ")  
    for i in range(28):
        if base_obs[i][0] != 0:
            print(str(i)+" "+str(base_obs[i]))
    print("Observables Base: ") 
    for i in range(28):
        if rover_obs[i][0] != 0:
            print(str(i)+" "+str(rover_obs[i]))
    time.sleep(0.5)

    # Calculate single differentials

    # Check common satellites

    # Calculate double differentials

    # Calculate float position

    # Calculate residuals

    # Try and solve integer ambiguity