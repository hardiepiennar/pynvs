import serial

def parse_nmea(line):
    """
    Check the message type and run the correct switch 
    function.

    Raises a ValueError if the message bounds are missing
    """
    # Check that the message is valid
    if not line[0] == "$":
        raise ValueError
    if not line[-2:] == "\r\n":
        raise ValueError

    talker_id = line[1:3]
    message_id = line[3:6]

    if message_id == "GGA":
        data = parse_gga(line)

    return {"Talker ID":talker_id,
            "Message ID":message_id}

def parse_gga(line):
    """
    Parse global positioning system fix data
    """
    data = line.split(',')
    time_of_position_fix = data[1] 

# Create serial connection
ser = serial.Serial('COM5', 115200)
message = parse_nmea("$GPGGA,143728.00,3334.4680,S,01918.2387,E,1,08,01.5,282.1,M,33.0,M,,*4D\r\n")

print(message)
assert(False)
# Show output
try:
    while True:
        print(ser.readline())
except KeyboardInterrupt:
    print("Exiting...")
    ser.close() 

# chksumdata = "PORZA,0,115200,3" # 7D
# # Initializing our first XOR value
# csum = 0 

# for c in chksumdata:
#     # XOR'ing value of csum against the next char in line
#     # and storing the new XOR value in csum
#     csum ^= ord(c)