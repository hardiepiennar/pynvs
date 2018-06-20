"""
NVS BINR protocol functions.

Hardie Pienaar
Bosmans Crossing
June 2018
"""

import struct

WGS84 = 0
PZ90 = 1
SK42 = 2
SK95 = 3
PZ90_2 = 4
GPS = 1
GLONASS = 2

def process_msg(buffer):
    """
    Process a BINR message and return a dictionary with 
    # the message ID and data.

    <DLE><ID>[data]<DLE><ETX>
    
    arguments:
        buffer - byte buffer containing BINR data
    returns:
        {message_ID, data}
            data - array of data bytes contained in the message
        remaining_buffer - buffer with processed msg removed
    raises:
        ValueError - If no message could be found
    """

    # Check that message has valid start and stop bytes
    # and grab the message string from the buffer
    try:
        start_id = buffer.index(0x10)
        searching = True
        stop_id_offset = 0
        while searching:
            stop_id = buffer[start_id+1+stop_id_offset:].index(0x10)+start_id+1+stop_id_offset
            if buffer[stop_id + 1]== 0x03:
                searching = False
            else:
                stop_id_offset = stop_id+1
        msg = buffer[start_id:stop_id+2]
    except ValueError:
        raise ValueError("Buffer did not contain message")

    # Grab the message id and data segments
    message_id = int(msg[1])
    data = msg[2:-2]

    # Return the message and rest of the buffer
    return {"ID":message_id,"data":data}, buffer[stop_id+2:]

def reboot(erase=False):
    """
    Reboot device packet

    arguments:
        erase - False - erase saved system data and user settings
                True  - without erasing all saved parameters
    """
    erase_value = 0x01
    if erase:
        erase_value = 0x00
        
    # Generate packet
    packet = [0x10,0x01,
              0x00, 0x01, 0x21, 0x01, 0x00, erase_value,
              0x10, 0x03]
    return packet

def set_coordinate_system(coordinate_system):
    """
    Sets the coordinate system used in the system.

    argument:
        coordinate_system - 00 WGS-84
                            01 PZ-90
                            02 Pulkovo 42 Coordinate System (SK42)
                            03 Pulkovo 95 Coordinate System (SK95)
                            04 PZ-90.02
    """
    # Check for valid input
    if coordinate_system > 4 or coordinate_system < 0:
        raise ValueError("Not a valid coordinate system: "+str(coordinate_system))

    # Generate packet
    packet = [0x10, 0x0D,
              0x01, coordinate_system,
              0x10, 0x03]
    return packet

def set_navigation_system(navigation_system):
    """
    Set the constellation used for navigation

    arguments:
        navigation_system = 0 GPS,GLONASS
                            1 GPS
                            2 GLONASS
                            3 GALILEO
                            10 GPS, GLONASS, SBAS
                            11 GPS, SBAS
                            12 GLONASS, SBAS                            
    """
    if (navigation_system < 0 or \
        (navigation_system > 3 and navigation_system < 10) or\
        navigation_system > 12):
        raise ValueError("Ïnvalid navigation system: "+str(navigation_system))
    # Generate packet
    packet = [0x10, 0x0D,
              0x02, navigation_system,
              0x10, 0x03]
    return packet

def set_pvt_setting(min_sat_elev_mask, min_snr, max_rms_error):
    """
    Set the PVT settings

    arguments:
        min_sat_elev_mask - Value of the minimum satellite elevation mask for 
                            navigation use [deg] [0-90]
        min_snr - The minimum signal to noise ratio for use in navigation [0-39]                       
        max_rms_error - The maximum rms error at which the navigation task shall
                        be deemed valid. [meters]
    """
    # Test elevation mask input
    if min_sat_elev_mask < 0 or min_sat_elev_mask > 90:
        raise ValueError("Invalid elevation mask: "+str(min_sat_elev_mask))
    if min_snr < 0 or min_snr > 39:
        raise ValueError("Invalid min snr: "+str(min_snr))
    if max_rms_error < 0:
        raise ValueError("Invalid max rms error: "+str(max_rms_error))
    # Generate packet
    packet = [0x10, 0x0D,
              0x03, min_sat_elev_mask, min_snr, max_rms_error&0x00FF,(max_rms_error&0xFF00)/256,
              0x10, 0x03]
    return packet

def set_filtration_factor(factor):
    """
    Sets the filtration factor of the coordinates.

    arguments:
        factor - filtration factor [0-10]
    """
    if factor < 0 or factor > 10:
        raise ValueError("Invalid filtration factor: "+str(factor))
    packet = [0x10, 0x0D,
              0x04, 0x00, 0x00, 0x00, factor*2*16,
              0x10, 0x03]
    return packet

def cancel_requests():
    """
    Clears the list of output messages
    """
    return [0x10,0x0E,0x10,0x03]
    
def set_ref_coordinates(lat, lon, height):
    """
    Set the reference antenna coodinates for fixed coordinate operating mode
    
    arguments:
        lat - latitude [rad]
        lon - longitude [rad]
        height - height [m]
    """
   
    # Convert the inputs to byte arrays
    lat_hex = struct.pack('<d',lat)
    lon_hex = struct.pack('<d',lon)
    height = struct.pack('<d',height)
    
    # Create packet
    packet = [0x10, 0x0F, 0x03]
    packet = packet + list(lat_hex)
    packet = packet + list(lon_hex)
    packet = packet + list(height)
    packet = packet + [0x10, 0x03]
    return packet

def enable_sat(sat_system, sat_no, state=True):
    """
    Enabling or disabling the use of specific satellites for navigation.

    arguments:
        sat_system - GPS or GLONASS
        sat_no     - satellite ID (1-32 for GPS or 1-24 for GLONASS)
        state      - True to enable the satellite, False to disable
    """ 
    # Test for bad arguments
    if sat_system != GPS and sat_system != GLONASS:
        raise ValueError("Satellite system invalid: "+str(sat_system))
    if sat_system == GPS:
        if sat_no < 1 or sat_no > 32:
            raise ValueError("SPS satellite number not valid: "+str(sat_no))
    else:
        if sat_no < 1 or sat_no > 24:
            raise ValueError("Glonass satellite number not valid: "+str(sat_no))

    # Create packet
    if state:
        state_packet = 1
    else:
        state_packet = 2
    packet = [0x10,0x12,
              sat_system, sat_no, state_packet, 
              0x10, 0x03]
    return packet

def request_status_of_receiver_channels():
    """
    Generates a packet to request the current status of the receiver channels

    Responds with message 42
    """
    return [0x10, 0x17, 0x10, 0x03]

def process_status_of_receiver_channels(data):
    """
    Process the response of the status of receiver channel request.

    arguments:
        data - data portion of response message
    
    returns:
        A dictionary is returned with the following format:
        list[{System, Number, SNR, Status, Pseudorange Sign}]

        Every list item reperesents a single channel.

        System - 1 GPS, 2 GLONASS, 4, SBAS, 8 - Galileo E1b
        Number - 1-32 GPS, 120-138 SBAS, -7-6 GLONASS
        SNR - Signal to noise ratio
        Status - 0-Automatic, 1-Manual, 2-Being Tested, 3-Error
        Pseudorange sign - 0-Digitization and measurement of pseudorange, 
                           1-Failure,
                           2-Pseudorange measurement available, digitization not 
    """
    # Test if packet is valid using num channels not a float property

    # Get the number of channels from the length of the data
    num_channels = int(len(data)/6)
    
    # Parse receiver data
    receiver_channels = []
    for i in range(num_channels):
        system = data[0+i*5]
        number = data[1+i*5]
        if system == 2: # If GLONASS, convert to signed int
            if number > 128:
                number = (256-number)*-1        
        snr = data[2+i*5]
        ch_status = data[3+i*5]
        pseudo_status = data[4+i*5]
        receiver_channels.append({"System":system,
                                  "Number":number,
                                  "SNR":snr,
                                  "Status":ch_status,
                                  "Pseudorange Sign":pseudo_status})
    return receiver_channels

def print_status_of_receiver_channels(channel_status):
    """
    Print the processed result of the status of receiver channel request.
    """
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

def request_sv_ephemeris(sat_system, sat_no, carrier=None):
    """
    Requests the ephemerides of the specified satellite.

    arguments:
        sat_system - 1-GPS, 2-GLONASS
        sat_no - 1-32(GPS), 1-24(GLONASS)
        carrier - GLONASS Carrier frequency number
    """
    # Test input values
    if sat_system != GPS and sat_system != GLONASS:
        raise ValueError("Satellite system invalid: "+str(sat_system))
    if sat_system == GPS:
        if sat_no < 1 or sat_no > 32:
            raise ValueError("SPS satellite number not valid: "+str(sat_no))
    else:
        if sat_no < 1 or sat_no > 24:
            raise ValueError("Glonass satellite number not valid: "+str(sat_no))
    # TODO: create carrier check

    # Create package
    packet = [0x10, 0x19, sat_system, sat_no]
    if carrier != None:
        packet = packet + [(256-(carrier*-1))]
    packet = packet + [0x10, 0x03]

    return packet