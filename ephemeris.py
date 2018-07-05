"""
Ephemerides calculation functions. 

Structure inspired by RTkLIB from tomajatso

Hardie Pienaar
Makespace Cambridge
July 2018
"""

import numpy as np

# Constants
C = 299792458.0 # Speed of light
OMGE = 7.2921151467E-5 # earth angular velocity
GM = 3.986005E14 # Product of gravitational constant G and mass of the earth M [m^3/s^2]
Omega_dot_e = 7.292115E-5 # Earth rotation rate [rad/s]

PI = 3.1415926535897932  # PI
MU_GPS = 3.9860050E14 # Gravitational constant for GPS
MU_GLONASS = 3.9860044E14 # Gravitational constant for GLONASS

RTOL_KEPLER = 1E-14 # Relative tolerance for Kepler equation
MAX_ITER_KEPLER = 30 # Maximum number of iteration of Kepler


def calc_sat_xyz(t, eph):
    """
    Calculate satellite position in ECEF coordinates using the given
    ephemerides and time.

    Currently only handles GPS
    
    arguments:
        eph - dictionary with the ephemeris data
        t - time of raw data transmission [s]

    returns:
        pos - [x, y, z] ECEF coordinates of satellite [m]
        sat_clk_bias - satellite clock bias [s]
    """

    # Get time difference between transmission and ephemeris 
    # reference time

    t_k = t-eph["t_0e"]/1000
    if t_k >= 302400:
        t_k = t_k - 604800
    elif t_k < -302400:
        t_k = t_k + 604800

    # Compute the mean anommally for tk
    # TODO: for GLONASS, MU will need to be selected according
    #       to system
    A = eph["sqrtA"]**2
    n_0 = np.sqrt(MU_GPS/(A**3))# Computed mean motion
    n = n_0 + eph["dn"] # Corrected mean motion
    M_k = eph["M_0"] + n*t_k # Mean anomaly

    # Keplers equation of eccentricity. Iteratively solved.
    e = eph["e"]
    E_k = 0
    E = M_k
    kepler_cnt = 0
    while (np.abs(E-E_k) > RTOL_KEPLER and 
           kepler_cnt < MAX_ITER_KEPLER):
        E_k = E
        E = E - (e*np.sin(E)-M_k)/(1-e*np.cos(E))
        kepler_cnt = kepler_cnt + 1
        if kepler_cnt > MAX_ITER_KEPLER:
            raise OverflowError("Kepler iteration overflow. Sat: "
                                +str(eph["PRN"]))
    

    # True anomaly
    sinE = np.sin(E)
    cosE = np.sin(E)
    v = np.arcsin((np.sqrt(1-e**2)*sinE))/np.arccos((cosE-e))

    # Argument of latitude
    u = v + eph["w"]

    # Second harmonic pertubations
    sin2u = np.sin(2*u)
    cos2u = np.cos(2*u)
    su = eph["C_us"]*sin2u + eph["C_uc"]*cos2u # latitude correction
    sr = eph["C_rc"]*cos2u + eph["C_rs"]*sin2u # radius correction
    si = eph["C_ic"]*cos2u + eph["C_is"]*sin2u # inclination correction

    u = u + su # Corrected argument of latitude
    r = A*(1-e*cosE) + sr # Corrected  radius
    i = eph["I_0"] + eph["IDOT"]*t_k + si  # Corrected inclination

    # Positions in orbital plane
    xa = r*np.cos(u)
    ya = r*np.sin(u)
    cosi = np.cos(i)

    # Corrected longitudinal ascending node
    Omega = (eph["Omega_0"] + (eph["Omega_dot"]
            -OMGE)*t_k  
            -OMGE*eph["t_0e"]/1000)

    # Earth Centered, Earth Fixed coordinates (ECEF)
    sinO = np.sin(Omega)
    cosO = np.cos(Omega)
    x_k = xa*cosO - ya*cosi*sinO
    y_k = xa*sinO + ya*cosi*cosO
    z_k = ya*np.sin(i)

    # Calculate clock correction
    # TODO: MU needs to be switched for GLONASS
    t_k = t-eph["t_0c"]/1000
    sat_clk_bias = eph["a_f0"]/1000 + eph["a_f1"]/1000*t_k + eph["a_f2"]/1000*t_k**2
    sat_clk_bias = sat_clk_bias - 2*np.sqrt(MU_GPS*A)*e*sinE/(C**2)

    # Calculate relativistic effects
    # TODO: implement this and return it
    F = -4.442807633E-10
    dt_r = F*e*eph["sqrtA"]*sinE

    return [x_k, y_k, z_k], sat_clk_bias, dt_r


def calc_tx_time(rx_time, prng):
    """
    Calculate the transit time given the given pseudornage.

    arguments:
        rx_time - the raw data receive time [s]
        prng - pseudorange [ms]
    
    returns:
        tx_time - time at which the message was transmitted
    """
    #return rx_time - prng/C
    return rx_time - prng/1000 # This is my own interpretation
    # TODO:test this function
    

# TODO:
# Next
# Calculate multiple sat positions (store in position, pseudorange array)
# Solve ECEF position

# After next:
# Use new range data to calculate time inputs
# See if position converges

# Future
# Investigate single difference solution using phase
# Create data structure with single differenced values
# Gather single differenced datasets at same time
# Calculate RTK position