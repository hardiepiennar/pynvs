"""
General plotting
"""

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd

# TODO:
# Create calc_sat_pos(time, ephemeris)
# Try and calculate position using visible sats


# Load ephemeris data
df_eph = pd.read_pickle("data/ext_ephemeris.pkl")
print(df_eph["PRN"])
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import numpy as np

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# u = np.linspace(0, 2 * np.pi, 100)
# v = np.linspace(0, np.pi, 100)

# earth_radius = 6371000
# x = earth_radius/2 * np.outer(np.cos(u), np.sin(v))
# y = earth_radius/2 * np.outer(np.sin(u), np.sin(v))
# z = earth_radius/2 * np.outer(np.ones(np.size(u)), np.cos(v))
# ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')
plt.figure()


for i in range(10):
    
    
    # ax.scatter(x_k,y_k,z_k)
    # ax.set_xlim(-3e7,3e7)
    # ax.set_ylim(-3e7,3e7)
    # ax.set_zlim(-3e7,3e7)
    # ax.set_aspect('equal')
    # ax.set_xlabel("X")
    # ax.set_ylabel("Y")
    # ax.set_zlabel("Z")
    plt.scatter(x_k,y_k)
plt.xlabel("W-E")
plt.xlabel("N-S")
plt.xlim(-4e7,4e7)
plt.ylim(-4e7,4e7)
plt.axes().set_aspect('equal')
plt.legend()
plt.show()





# Load and Filter all GPS data
raw_data = pd.read_pickle("data/raw_data.pkl")
df_gps = raw_data[raw_data["Signal Type"]==2]
df_gps = df_gps[df_gps["Pseudorange and Doppler Present"]]
df_gps = df_gps[df_gps["Phase Present"]]
df_gps = df_gps[df_gps["Signal Present"]]

assert(False)
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


