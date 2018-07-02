""" 
Reads NVS stream and stores data in numpy files for easy processing

Hardie Pienaar
Pelham Ct
July 2018
"""

import binr
import time
import numpy as np
import pandas as pd

# Parameters
filename = "recording.dat"

# Open file for reading
reader = open("pelham_shed_1_July_2018.dat",'rb')

# Create some data structures for logging
# Every data structure has rows for every GPS and GLONASS sat
# indexes GPS: 0-31 for GPS or 32-55 for GLONASS
timesteps = 1325
step = 0
columns = list(["Time", "Signal Type", "Sat Number", "SNR", "Phase", 
                "Pseudorange","Doppler", "Signal Present",
                "Pseudorange and Doppler Present","Pseudorange Smoothed", 
                "Phase Present", "Signal Time Available","Preamble Not Detected"])
df = pd.DataFrame(columns=columns)

# Count messages
buffer = []
try:
    while True:
        # Get some bytes
        read = list(reader.read(100))
        # Append it to the buffer
        buffer = buffer + read
        # Exit the loop when reaching the end of the file
        if len(read) == 0:
            reader.close()
            print("Done")
            break
        try:
            # Try and process the buffer
            valid_message = False
            data, buffer = binr.process_msg(buffer) 
            valid_message = True
        except ValueError:
            #print("Buffer length: "+str(len(buffer))) 
            l = 1 
                    # If a message is available, save it to the data structures
        if valid_message:
            #print("Msg: "+str(data["ID"])+" buffer length: "+str(len(buffer)))
            
            # If we received raw data, save it
            if data["ID"]== 0xF5:
                print("Processing raw data")
                # Process the message
                raw_data = binr.process_raw_data(data["data"])
                # Get the number of channels
                num_channels = len(raw_data["Signal Type"])
                # Loop through every channel to find valid measurements
                for i in range(num_channels):
                    if raw_data["Signal Type"][i] == 1 or raw_data["Signal Type"][i] == 2:
                        # Process flags
                        signal_present = 0b00000001&raw_data["Flags"][i] > 0
                        pseudo_doppler_present = 0b00000010&raw_data["Flags"][i] > 0
                        pseudo_smoothed = 0b00000100&raw_data["Flags"][i] > 0
                        carrier_present = 0b00001000&raw_data["Flags"][i] > 0
                        time_available = 0b00010000&raw_data["Flags"][i] > 0
                        preamble_not_detected = 0b00100000&raw_data["Flags"][i] > 0
                        dataset = [[raw_data["Time"], 
                                raw_data["Signal Type"][i],
                                raw_data["Sat Number"][i],
                                raw_data["SNR"][i],
                                raw_data["Carrier Phase"][i],
                                raw_data["Pseudo Range"][i],
                                raw_data["Doppler Freq"][i],
                                signal_present,
                                pseudo_doppler_present,
                                pseudo_smoothed,
                                carrier_present,
                                time_available,
                                preamble_not_detected]]
                        df_step = pd.DataFrame(dataset, columns=columns)   
                        df = df.append(df_step)
            if data["ID"]== 0xF7:
                print("Processing extended ephemeres data")
                # TODO: Read ephemeris into a dataframe
                # TODO: Calculate and plot satellite positions
                # TODO: Calculate own position
            #time.sleep(0.1)
except KeyboardInterrupt:
    reader.close()
finally:
    print(df.tail(10))
    df.to_pickle("data/raw_data.pkl")  
