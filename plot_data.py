"""
General plotting
"""

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd

# Filter all GPS data
raw_data = pd.read_pickle("data/raw_data.pkl")
df_gps = raw_data[raw_data["Signal Type"]==2]
df_gps = df_gps[df_gps["Pseudorange and Doppler Present"]]
df_gps = df_gps[df_gps["Phase Present"]]
df_gps = df_gps[df_gps["Signal Present"]]

# Get a list of satellites observed
sats = df_gps["Sat Number"].unique()
print("GPS Sats: "+str(sats))

# For every satellite in the list plot its data
plt.figure()
for i in range(len(sats)):
    df_sat = df_gps[df_gps["Sat Number"]==sats[i]]
    plt.plot(df_sat["Time"],df_sat["SNR"],label=sats[i], alpha=0.75, linewidth=1)
    plt.xlabel("Time")
    plt.ylabel("SNR")
    plt.ylim(0,60)
    plt.legend()
plt.savefig("plots/snr.png")

plt.figure()
for i in range(len(sats)):
    df_sat = df_gps[df_gps["Sat Number"]==sats[i]]
    plt.plot(df_sat["Time"],df_sat["Phase"],label=sats[i], alpha=0.75, linewidth=1)
    plt.xlabel("Time")
    plt.ylabel("Phase")
    plt.legend()
plt.savefig("plots/phase.png")

plt.figure()
for i in range(len(sats)):
    df_sat = df_gps[df_gps["Sat Number"]==sats[i]]
    plt.plot(df_sat["Time"],df_sat["Pseudorange"],label=sats[i], alpha=0.75, linewidth=1)
    plt.xlabel("Time")
    plt.ylabel("Pseudorange")
    plt.legend()
plt.savefig("plots/pseudorange.png")

plt.figure()
for i in range(len(sats)):
    df_sat = df_gps[df_gps["Sat Number"]==sats[i]]
    plt.plot(df_sat["Time"],df_sat["Doppler"],label=sats[i], alpha=0.75, linewidth=1)
    plt.xlabel("Time")
    plt.ylabel("Doppler")
    plt.legend()
plt.savefig("plots/doppler.png")
