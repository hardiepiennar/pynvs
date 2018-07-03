"""
General plotting
"""

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd

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
    # Constants
    GM = 3.986005E14 # Product of gravitational constant G and mass of the earth M [m^3/s^2]
    Omega_dot_e = 7.292115E-5 # Earth rotation rate [rad/s]
    pi = 3.1415926535898 



    sqrtA = df_eph.iloc[i]["sqrtA"] # Sqrt of the semi major axis m
    dn =  df_eph.iloc[i]["dn"] # rad/ms
    M_0 =  df_eph.iloc[i]["M_0"] # rad
    t_0e = df_eph.iloc[i]["t_oe"] # Reference time ephemeris
    t_0c = df_eph.iloc[i]["t_oc"] # Reference time clock
    a_0 = df_eph.iloc[i]["a_f0"] # Clock corrections 
    a_1 = df_eph.iloc[i]["a_f1"]
    a_2 = df_eph.iloc[i]["a_f2"]
    e = df_eph.iloc[i]["e"] # eccentricity #TODO: check this, should be less than 0.001
    w = df_eph.iloc[i]["w"] # Argument of perigee (semicircles)
    C_us = df_eph.iloc[i]["C_us"] # Corrections
    C_uc = df_eph.iloc[i]["C_uc"]
    C_rc = df_eph.iloc[i]["C_rc"]
    C_rs = df_eph.iloc[i]["C_rs"]
    C_ic = df_eph.iloc[i]["C_ic"] 
    C_is = df_eph.iloc[i]["C_is"] 
    I_0 = df_eph.iloc[i]["I_0"] 
    IDOT = df_eph.iloc[i]["IDOT"] 
    Omega_0 = df_eph.iloc[i]["Omega_0"]
    Omega_dot = df_eph.iloc[i]["Omega_dot"]

    # Get the measurement time
    t = 59000000 # 5:30 Sunday 1 July 2018 [ms] comes from raw data
    
    T = (2*pi)/(np.sqrt(GM)*(1/(sqrtA**3))) # Satellite orbital period

    # Calculate the time from the epheremides epoch
    t_k = (t - t_0e)/1000 # [s]
    if t_k >= 302400:
        t_k = t_k - 604800
    elif t_k < -302400:
        t_k = t_k + 604800

    # Compute the mean anommally for tk
    n_0 = np.sqrt(GM)*(1/sqrtA**3) # Computed mean motion
    n = n_0 + dn # Corrected mean motion
    M_k = M_0 + n*t_k # Mean anomaly

    # Keplers equation of eccentricit. Iteratively solved
    E_k = M_k
    for i in range(5):
        E_k = M_k + e*np.sin(E_k) 
    # True anomaly
    v_k = np.arccos((np.cos(E_k)-e)/(1-e*np.cos(E_k)))
    v_k = np.arcsin((np.sqrt(1-e**2)*np.sin(E_k))/(1-e*np.cos(E_k)))

    Phi_k = v_k + w # Argument of latitude

    # Second harmonic pertubations
    su_k = C_us*np.sin(2*Phi_k) + C_uc*np.cos(2*Phi_k) # latitude correction
    sr_k = C_rc*np.cos(2*Phi_k) + C_rs*np.sin(2*Phi_k) # radius correction
    si_k = C_ic*np.cos(2*Phi_k) + C_is*np.sin(2*Phi_k) # inclination correction

    u_k = Phi_k + su_k # Corrected argument of latitude
    r_k = (sqrtA**2)*(1-e*np.cos(E_k)) + sr_k # Corrected  radius
    i_k = I_0 + si_k + IDOT*t_k # Corrected inclination

    # Positions in orbital plane
    xa_k = r_k*np.cos(u_k)
    ya_k = r_k*np.sin(u_k)

    # Corrected longitudinal ascending node
    Omega_k = Omega_0 + (Omega_dot-Omega_dot_e)*t_k - Omega_dot_e*t_0e

    # Earth Centered, Earth Fixed coordinates (ECEF)
    x_k = xa_k*np.cos(Omega_k) - ya_k*np.cos(i_k)*np.sin(Omega_k)
    y_k = xa_k*np.sin(Omega_k) - ya_k*np.cos(i_k)*np.cos(Omega_k)
    z_k = ya_k*np.sin(i_k)
    
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


