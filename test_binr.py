import unittest
import binr

class Tests(unittest.TestCase):
    def test_process_msg(self):
        # Create test message
        raw_msg = bytearray([0x10,0x21,0x01,0x10,0x03])

        # Process message 1
        msg, bufffer = binr.process_msg(raw_msg)
        
        # Test return data
        self.assertEqual(msg["ID"], 0x21)
        self.assertEqual(len(msg["data"]),1)
        self.assertEqual(msg["data"][0],0x01)
    
        ## Create test message
        raw_msg = bytearray([0x10,0x60,0x0B,0x09,0x3E,0x4E,
                              0x12,0x3F,0x11,0x39,0x60,0x3F,
                              0x10,0x03])
        
        # Process message 2
        msg, buffer = binr.process_msg(raw_msg)
        
        # Test return data
        self.assertEqual(msg["ID"], 0x60)
        self.assertEqual(len(msg["data"]),10)
        self.assertEqual(msg["data"][4],0x12)

        # Create bad message
        raw_msg = bytearray([0x11,0x21,0x01,0x10,0x03])
        
        # Process bad message
        with self.assertRaises(ValueError):
            binr.process_msg(raw_msg)

        # Process message where last character is not yet sent
        raw_msg = bytearray([0x10,0x21,0x01,0x10])

        # Process message
        with self.assertRaises(ValueError):
            binr.process_msg(raw_msg)
    
    def test_process_msg_in_buffer(self):
        # Create msg contained in buffer
        raw_msg = bytearray([0x11,0x21,0x10,0x21,0x01,0x10,0x03,0x23, 0x12])
        msg, buffer = binr.process_msg(raw_msg)

        # Test return data
        self.assertEqual(msg["ID"], 0x21)
        self.assertEqual(len(msg["data"]),1)
        self.assertEqual(msg["data"][0],0x01)

        # Test buffer
        self.assertEqual(len(buffer), 2)
        self.assertEqual(buffer[0], 0x23)
        
        # Test for proper ending (no ending)
        raw_msg = bytearray([0x11,0x21,0x10,0x21,0x01,0x10,0x00,0x23, 0x12])
        with self.assertRaises(ValueError):
            binr.process_msg(raw_msg)
    
    def test_reboot(self):
        # Generate normal packet
        packet = binr.reboot()
        self.assertEqual(packet,[0x10,0x01,0x00, 0x01, 0x21, 0x01, 0x00, 
                                  0x01,0x10, 0x03])
        # Generate erasing packet
        packet = binr.reboot(erase=True)
        self.assertEqual(packet,[0x10,0x01,0x00, 0x01, 0x21, 0x01, 0x00, 
                                 0x00,0x10, 0x03])
    
    def test_set_coordinate_system(self):
        # Generate normal packet
        packet = binr.set_coordinate_system(binr.WGS84)
        self.assertEqual(packet,[0x10,0x0D,0x01, 0x00, 0x10, 0x03])
        # Check different packet
        packet = binr.set_coordinate_system(binr.PZ90)
        self.assertEqual(packet,[0x10,0x0D,0x01, 0x01, 0x10, 0x03])
        # Check invalid argument
        with self.assertRaises(ValueError):
            packet = binr.set_coordinate_system(5)
        with self.assertRaises(ValueError):
            packet = binr.set_coordinate_system(-1)
    
    def test_set_navigation_system(self):
        # Generate normal packet
        packet = binr.set_navigation_system(0)
        self.assertEqual(packet,[0x10,0x0D,0x02, 0x00, 0x10, 0x03])
        # Check for bad packets
        with self.assertRaises(ValueError):
            packet = binr.set_navigation_system(-1)
    
    def test_set_pvt_setting(self):
        # Generate normal packet
        packet = binr.set_pvt_setting(5, 30, 20001)
        self.assertEqual(packet,[0x10,0x0D,0x03, 0x05, 0x1E, 0x21, 0x4E, 0x10, 0x03])
        # Generate bad inputs
        with self.assertRaises(ValueError):
             binr.set_pvt_setting(-1, 30, 20001)
        with self.assertRaises(ValueError):
             binr.set_pvt_setting(91, 30, 20001)
        with self.assertRaises(ValueError):
             binr.set_pvt_setting(5, -1, 20001)
        with self.assertRaises(ValueError):
             binr.set_pvt_setting(5, 40, 20001)
        with self.assertRaises(ValueError):
             binr.set_pvt_setting(5, 30, -1)

    def test_set_filtration_factor(self):
        # Generate normal packet
        packet = binr.set_filtration_factor(2)
        self.assertEqual(packet,[0x10,0x0D,0x04, 0x00, 0x00, 0x00, 0x40, 0x10, 0x03])
        # Generate bad inputs        
        with self.assertRaises(ValueError):
             binr.set_filtration_factor(-1)
        with self.assertRaises(ValueError):
             binr.set_filtration_factor(11)

    def test_cancel_requests(self):
         # Generate normal packet
        packet = binr.cancel_requests()
        self.assertEqual(packet,[0x10,0x0E,0x10,0x03])

    def test_set_ref_coordinates(self):
        # Generate normal packet
        packet = binr.set_ref_coordinates(0.530870980814942, 1.061741961629884, 180.6)
        self.assertEqual(packet,[0x10, 0x0F, 0x03, 0x1D, 0xDC, 0x9F, 0x23,
                                 0xE5, 0xFC, 0xE0, 0x3F, 0x1D, 0xDC, 0x9F,
                                 0x23, 0xE5, 0xFC, 0xF0, 0x3F, 0x33, 0x33,
                                 0x33, 0x33, 0x33, 0x93, 0x66, 0x40, 0x10,
                                 0x03])

    def test_enable_sat(self):
        # Generate normal packet
        packet = binr.enable_sat(binr.GPS, 10, False)
        self.assertEqual(packet,[0x10, 0x12, 0x01, 0x0A, 0x02, 0x10, 0x03])
        # Generate bad packages
        with self.assertRaises(ValueError):
            binr.enable_sat(3, 0x0A, False)
        with self.assertRaises(ValueError):
            binr.enable_sat(binr.GPS, 33, False)
        with self.assertRaises(ValueError):
            binr.enable_sat(binr.GLONASS, 25, False)

    def test_request_status_of_receiver_channels(self):
        # Generate normal packet
        packet = binr.request_status_of_receiver_channels()
        self.assertEqual(packet,[0x10, 0x17, 0x10, 0x03])

    def test_process_status_of_receiver_channels(self):
        # Given test data, return results
        data = b'\x02\xf9\x00\x00\x01\x02\x06\x00\x00\x01\x02\x05\x00\x00\x01\x02\x03\x00\x00\x01\x02\x02\x00\x00\x01\x02\x04\x00\x00\x01\x02\x00\x00\x00\x01\x02\x01\x00\x00\x01\x02\xff\x03\x00\x01\x02\xfc\x00\x00\x01\x02\xfe\x18\x00\x02\x02\xfd\x00\x00\x01\x02\xfb\x00\x00\x01\x02\xfa\x00\x00\x01\x01\n\x03\x00\x01\x01\x12\x10\x10\x00\x00\x01\x0c\x00\x00\x01\x01\x0b\x1d\x00\x00\x01\x0e\x00\x00\x01\x01\x0f\x00\x00\x01\x01\x13\x00\x00\x01\x01\x03\x1b\x00\x02\x01\x10\x10\x00\x00\x01\x01\x11\x00\x00\x01\x01\x14\x00\x00\x01\x01\x15\x00\x00\x01\x01\x16\x00\x00\x01\x01\x08\r\x00\x01\x01\t\x01\x00\x01\x01\r\x00\x00\x01\x05\xfa\x1e\x03\x01\x12\x00"\x03\x01'
        receiver_status = binr.process_status_of_receiver_channels(data)
        
        self.assertEquals(len(receiver_status),27)
        self.assertEquals(receiver_status[0]["System"],2)
        self.assertEquals(receiver_status[0]["Number"],-7)
        self.assertEquals(receiver_status[0]["SNR"],0)
        self.assertEquals(receiver_status[0]["Status"],0)
        self.assertEquals(receiver_status[0]["Pseudorange Sign"],1)
        self.assertEquals(receiver_status[5]["System"],2)

        # TODO: Check if packet contains multiple of 5 bytes

    def test_request_sv_ephemeris(self):
        # Generate packet
        packet = binr.request_sv_ephemeris(binr.GPS, 2)
        self.assertEquals(packet, [0x10, 0x19,0x01,0x02,0x10,0x03])
        packet = binr.request_sv_ephemeris(binr.GLONASS, 0,-2)
        self.assertEquals(packet, [0x10, 0x19,0x02, 0x00, 0xFE, 0x10,0x03])

        # Generate bad packets
        with self.assertRaises(ValueError):
            packet = binr.request_sv_ephemeris(-1, 2)
        with self.assertRaises(ValueError):
            packet = binr.request_sv_ephemeris(3, 2)
        with self.assertRaises(ValueError):
            packet = binr.request_sv_ephemeris(binr.GPS, -1)
        #TODO: specifying carrier for GPSs

    def test_process_sv_ephemeris(self):
        # Given GPS test data return results
        data = b'\x01\x01\x00\x80\x0c\xc1\xc5\x7f\xa5,\xf2\xd2\x1f\xb7@\x84\xf9?\x00\x00\xc7\xb4\x00\x00\x00\xccw5\x80?\x00\xe0\xb96\x00\x00\x80\x91\xaa!\xb4@\x00\x00\x00\x00\xb6\xbd\xb3A\x00\x000\xb4\xf0\x00\xf5\xbc\x9b\xff\x08\xc0\x00\x00\x0c4\x9e\xef\xd4\x0b\x93\x19\xef?\x00|\x8cCfO\xf8\xbc\xda\x9d\xe4?\x8c\x1eW\x9dXM\xa2\xbd\r\x12\x87F\xb3$;=\x00\x80\xbb6\x00\x00\x00\x00\xb6\xbd\xb3A\x00\x00\x00\x00\x00\x00x\xac\x1f.n\xbd\x01\x006\x00'
        sv_ephemeris = binr.process_sv_ephemeris(data)
        self.assertEquals(sv_ephemeris["System"], binr.GPS)
        self.assertEquals(sv_ephemeris["PRN"], 1)
        self.assertEquals(sv_ephemeris["C_rs"], -8.78125)
        self.assertEquals(sv_ephemeris["C_us"],5.539506673812866e-06)
        self.assertEquals(sv_ephemeris["dn"], 4.7037673235605926e-12)
        self.assertEquals(sv_ephemeris["M_0"], 1.5947882798474748)
        self.assertEquals(sv_ephemeris["C_uc"], -3.7066638469696045e-07)
        self.assertEquals(sv_ephemeris["e"], 0.00791448203381151)
        self.assertEquals(sv_ephemeris["sqrtA"], 5153.666282653809)
        self.assertEquals(sv_ephemeris["t_0e"], 331200000.0)
        self.assertEquals(sv_ephemeris["C_ic"], -1.6391277313232422e-07)
        self.assertEquals(sv_ephemeris["Omega_0"], -3.124808765627783)
        self.assertEquals(sv_ephemeris["C_is"], 1.30385160446167e-07)
        self.assertEquals(sv_ephemeris["I_0"], 0.9718718749131658)
        self.assertEquals(sv_ephemeris["C_rc"], 280.96875)
        self.assertEquals(sv_ephemeris["w"], 0.6442693415469705)
        self.assertEquals(sv_ephemeris["Omega_dot"], -8.322846679971361e-12)
        self.assertEquals(sv_ephemeris["IDOT"], 9.643258823294288e-14)
        self.assertEquals(sv_ephemeris["T_GD"], 5.587935447692871e-06)
        self.assertEquals(sv_ephemeris["t_0c"], 331200000.0)
        self.assertEquals(sv_ephemeris["a_f2"], 0.0)
        self.assertEquals(sv_ephemeris["a_f1"], -3.524291969370097e-12)
        self.assertEquals(sv_ephemeris["a_f0"], -0.05814945325255394)
        self.assertEquals(sv_ephemeris["URA"], 1)
        self.assertEquals(sv_ephemeris["IODE"], 54)

        # Given GPS test data return results
        data = b'\x02\x16\xfd\x00\x00\x90\x12\xdf\xa3vA\x00\x00@\x9e\xcf\xa9a\xc1\x00\x00\x80\x1d\x11\xe1@A\x00\x00\x00\x00p\xb7\xca?\x00\x00\x00\x008\x9b\xd4\xbf\x00\x00\x00\x00\xec\x97\x0c\xc0\xfc\xa9\xf1\xd2Mb\x80=\xfa~j\xbct\x93\x88\xbd\xfc\xa9\xf1\xd2Mbp\xbd\x00\x00\x00\x00X\x08XA\x00\x00\x00\xacH=Y=\x00\x00'
        sv_ephemeris = binr.process_sv_ephemeris(data)
        self.assertEquals(sv_ephemeris["System"], binr.GLONASS)
        self.assertEquals(sv_ephemeris["n^A"], 22)
        self.assertEquals(sv_ephemeris["H_n^A"], -3)
        self.assertEquals(sv_ephemeris["x_n"], 23739889.16015625) 
        self.assertEquals(sv_ephemeris["y_n"], -9260668.9453125) 
        self.assertEquals(sv_ephemeris["z_n"], 2212386.23046875) 
        self.assertEquals(sv_ephemeris["x_nv"], 0.2087230682373047) 
        self.assertEquals(sv_ephemeris["y_nv"], -0.3219738006591797) 
        self.assertEquals(sv_ephemeris["z_nv"], -3.5741806030273438) 
        self.assertEquals(sv_ephemeris["x_na"], 1.862645149230957e-12) 
        self.assertEquals(sv_ephemeris["y_na"], -2.7939677238464356e-12) 
        self.assertEquals(sv_ephemeris["z_na"], -9.313225746154785e-13) 
        self.assertEquals(sv_ephemeris["t_b"], 6300000) 
        self.assertEquals(sv_ephemeris["gamma_n"], -1.8189894035458565e-12)
        self.assertEquals(sv_ephemeris["tau_n"], 0.05303695797920227) 
        self.assertEquals(sv_ephemeris["E_n"], 0) 

    def test_request_raw_data(self):
        # Generate packet
        packet = binr.request_raw_data(20)
        self.assertEquals(packet, [0x10, 0xF4, 0x14, 0x10, 0x03])
        
        # Test bad packet
        with self.assertRaises(ValueError):
            binr.request_raw_data(-1)
        with self.assertRaises(ValueError):
            binr.request_raw_data(0)

    def test_process_raw_data(self):
        # TODO: Suspect something is wrong with channel 0
        # Test data
        data = b'\xc7\xad-\x81\xbb\xd5\x8bA\xd8\x03\x0e\xabW\x00\x00\x94\xd1@\x00\x00\x00\x00p\x99dA\x00\x01\x15\x04*\x89\xf5\xec=m\xea\xff@\x00\x90+,\xc8\x8fP@\x00\x00\x88\x13\x8f\xfc\x94\xc0{\x00\x01\r\xfe \xc5x\x03\xf2\x04\xb9\xf1\xc0\x00\x10\x10\x02\xa2\xf4\x98R@\x00\x00`\x12w\xee\x88@{\x00\x01\x05\x01*\x19\xbbc\xd5(\\\x11A\x00`\nL\x0fWR@\x00\x00\xa8\x10\x10\x02\xac\xa6\xc0{\x00\x01\x16\xfd+\x93d_8?-\r\xc1\x00\xa0\xe8\xd5\xd9\xc1P@\x00\x00\xc4!M\xbf\xa2@;\x00\x02\x01\x01\x1c\x00\x01\xc0\xb7\xa3P\x13\xc1\x00H\xfd\xad\x1b\xa2R@\x00\x00<\xb7\x8f\xf0\xa8@3\x00\x02\x12\x120\x00nX|\x93z\n\xc1\x00H\x85\xa4\x93\x1bQ@\x00\x00X\t\xb0\x0f\xa1@{\x00\x02\x1b\x1b.\x00\xae\xed"\xfe\xd5\x0bA\x00H\xa5\x00\x1b\xf7Q@\x00\x00\xf8\xda\xd8s\xa2\xc0{\x00\x02\x14\x14.\x00\xf9d \x05\xeb\x11A\x00H5$\xcd\x9eS@\x00\x004`\xe1h\xa7\xc0{\x00\x02\x08\x082\x00\x00\xd5\x83\x90\xb1\x97@\x00H\xbdl&\xf9P@\x00\x00\x00\xb7\x9c\x9dC\xc0;\x00\x02  $\x00\x96\xe8\xda\xcdo\x0e\xc1\x00H\x1d\x16E\xc9S@\x00\x00H)\xce,\xa6@{\x00\x02\n\n1\x00\x0eJJ\xb5B\x03A\x00H-\x83\xac\tR@\x00\x00\xe8\xed\xb6T\x99\xc0;\x00\x02\x0b\x0b/\x00E\xf4\xa7\xba;\x12\xc1\x00H\x05g\xbf\xf9Q@\x00\x00\xb8zl\x8f\xa7@{\x00\x02\x1c\x1c"\x00p\xfc\x1d\xe1\'\x0c\xc1\x00H\x05n\xb3\xd0S@\x00\x00\\F4\x1f\xa4@;\x00'

        # Process data
        raw = binr.process_raw_data(data)

        # Check raw data response
        self.assertEquals(raw["Time"],58374000.14730411)
        self.assertEquals(raw["Week Number"],984)
        self.assertEquals(raw["GPS time shift"],18000.000020901723)
        self.assertEquals(raw["GLO time shift"],10800000.0 )
        self.assertEquals(raw["Rec Time Scale Correction"],0 )
        self.assertEquals(len(raw["Signal Type"]),13)
        self.assertEquals(raw["Signal Type"][2],1)
        self.assertEquals(raw["Sat Number"][2],5)
        self.assertEquals(raw["Carrier Number"][2],1)
        self.assertEquals(raw["Carrier Phase"][2],284426.2083882555)
        self.assertEquals(raw["Pseudo Range"][2],73.36030865681823)
        self.assertEquals(raw["Doppler Freq"][2],-2.1184331551132058e-122)
        self.assertEquals(raw["Flags"][2],192)
    
    def test_process_software_version(self):
        # Test data
        data = b' CSM54 05.04 18/10/16\x00\xbc\x8f\xec\x1cNV08C 07.03 30/03/12\x00\xbc\x8f\xec\x1c                    \x00\x00\x00\x00\x00'

        # Process software version data
        version = binr.process_software_version(data)

        # Check data
        self.assertEquals(version["No of Channels"], 32)
        #self.assertEquals(version["Version"], 32) # TODO: implement if you want
        self.assertEquals(version["Serial Number"], 485265340)

    # def test_process_ionosphere_parameters(self):
    #     # Test data
    #     data = b'\x00\x00\xa01\x00\x00\x802\x00\x00\x80\xb3\x00\x00\x00\xb4\x00\x00\xa0G\x00\x00\xc0G\x00\x00\x80\xc7\x00\x00\x00\xc9\xff'
    #     raise NotImplementedError()

    def test_process_time_scales_parameters(self):
        # Test data
        data = b'\x00\x00\x00\x00\x00\x00\xf8<\x00\x00\x00\x00\x00\x00(>\x00\xb0\x07\x00\xd7\x00\x12\x00\x89\x00\x07\x00\x12\x00\xff\x8d\x03\x00\x00\x00\x00\x00\x00 >\xff'

        # Process packet
        param = binr.process_time_scales_parameters(data)

        # Check data
        self.assertEquals(param["A_1"],5.329070518200751e-15)
        self.assertEquals(param["A_0"],2.7939677238464355e-09)
        self.assertEquals(param["t_ot"],7.059853767145574e-40)
        self.assertEquals(param["WN_t"],215)
        self.assertEquals(param["dt_LS"],18)
        self.assertEquals(param["WN_LSF"],137)
        self.assertEquals(param["DN"],7)
        self.assertEquals(param["dt_LSF"],18)
        self.assertEquals(param["GPS Reliability"],255)
        self.assertEquals(param["N^A"],909)
        self.assertEquals(param["tau_c"],1.862645149230957e-09)
        self.assertEquals(param["GLONASS Reliability"],255)

    def test_process_geocentric_coordinates_of_antenna(self):
        # Test data
        data = b'\xebaFF\x0f\xe0MA\xdf\x10\x10\xb3\t\xb4\x1e\xb7@Gi\xb8a5$SA\x00\x00\x00`\x9d\xde\x1a@\x00\x00\x00\xc0jd\x13@\x00\x00\x00 \xbe=\x1c@\x00'

        # Process antenna
        geo_coords = binr.process_geocentric_coordinates_of_antenna(data)

        # Check returned values
        self.assertEquals(geo_coords["X"],3915806.549022903)
        self.assertEquals(geo_coords["Y"],-3.4419559446041095e-43) # TODO: something looks wrong here
        self.assertEquals(geo_coords["Z"],3.2932389635128064e+92)
        self.assertEquals(geo_coords["X error"],2.9511633910563842e-179)
        self.assertEquals(geo_coords["Y error"],2.9613168073097877e-215)
        self.assertEquals(geo_coords["Z error"],1.2025483161027633e-172)
        self.assertEquals(geo_coords["Flag"],64)

      
    def test_process_extended_ephemeris_of_satellites(self):
        # Test GPS processing
        # Test data
        data = b'\x01\x01\x000\xc1\xc2\xdb\x9d\x9a,\xc5dO\xb8a\xc4\xed?\x00p\xa1\xb6\x00\x00\x00\xac6G\x80?\x000\xc16\x00\x00\xc0\xd8\xab!\xb4@\x00\x00\x00\x00(\xe6\x8eA\x00\x00\x80\xb1;U\xecS\x07H\x07@\x00\x00\xb83h\xa4Ge\xf4\x1a\xef?\x00\x0c\x89C\xe0\xd5$"5\xdf\xe4?\x01\x98Z\xd2m\xeb\xa1\xbd\x12\xea\xda\xaa>\xb3W\xbd\x00\x80\xbb6\x00\x00\x00\x00(\xe6\x8eA\x00\x00\x00\x00\x00\x00\x80\xac\xf8\x1e|\xbd\x00\x00D\x00D\x00\x01\x00\x00\x00\xd8\x03'
        
        # Process packet
        ext_ephemeris = binr.process_extended_ephemeris_of_satellites(data)

        # Check that data is correct
        self.assertEquals(ext_ephemeris["System"], 1)
        self.assertEquals(ext_ephemeris["PRN"], 1)
        self.assertEquals(ext_ephemeris["C_rs"], -96.59375)
        self.assertEquals(ext_ephemeris["dn"],  4.394468729879142e-12 )
        self.assertEquals(ext_ephemeris["M_0"], 0.9302223777587179)
        self.assertEquals(ext_ephemeris["C_uc"], -4.811212420463562e-06)
        self.assertEquals(ext_ephemeris["e"], 0.00794832909014076)
        self.assertEquals(ext_ephemeris["C_us"], 5.757436156272888e-06)
        self.assertEquals(ext_ephemeris["sqrtA"], 5153.671276092529)
        self.assertEquals(ext_ephemeris["t_0e"],  64800000.0)
        self.assertEquals(ext_ephemeris["C_ic"],  -3.725290298461914e-09)
        self.assertEquals(ext_ephemeris["Omega_0"],  2.910170226716813)
        self.assertEquals(ext_ephemeris["C_is"],  8.568167686462402e-08)
        self.assertEquals(ext_ephemeris["I_0"],  0.9720403650400273)
        self.assertEquals(ext_ephemeris["C_rc"],  274.09375)
        self.assertEquals(ext_ephemeris["w"],  0.652247015654833)
        self.assertEquals(ext_ephemeris["Omega_dot"], -8.148910863417868e-12)
        self.assertEquals(ext_ephemeris["IDOT"],  -3.3679974334690787e-13)
        self.assertEquals(ext_ephemeris["T_GD"],  5.587935447692871e-06 )
        self.assertEquals(ext_ephemeris["t_0c"],  64800000.0)
        self.assertEquals(ext_ephemeris["a_f2"],  0.0)
        self.assertEquals(ext_ephemeris["a_f1"],  -3.637978807091713e-12)
        self.assertEquals(ext_ephemeris["a_f0"],  -0.061552971601486206 )
        self.assertEquals(ext_ephemeris["URA"],  0)
        self.assertEquals(ext_ephemeris["IODE"],  68)
        self.assertEquals(ext_ephemeris["IODC"],  68)
        self.assertEquals(ext_ephemeris["CODEL2"],  1)
        self.assertEquals(ext_ephemeris["L2 P Data Flag"],  0)
        self.assertEquals(ext_ephemeris["WN"],  984)

        # Test GLONASS processing
        # Create packet
        data = b'\x02\x0c\xff\x00\x00@\xb7\xb6\x91eA\x00\x00\xd0\x85\x00@t\xc1\x00\x00\xe0\x81\x16Y`A\x00\x00\x00\x00\xa6z\xe2?\x00\x00\x00\x00\xe8\x95\xf0\xbf\x00\x00\x00\x00_\x90\n\xc0\xfc\xa9\xf1\xd2Mb\x90=\xfc\xa9\xf1\xd2Mb\x80\xbd\xfc\xa9\xf1\xd2Mbp=\x00\x00\x00\x80\xbc\x85\x90A\x00\x00\x00\x004\\\x08=\x00\x00'
        
        # Process packet
        ext_ephemeris = binr.process_extended_ephemeris_of_satellites(data)

        # Check data
        self.assertEquals(ext_ephemeris["System"], 2)
        self.assertEquals(ext_ephemeris["PRN"], 12)
        self.assertEquals(ext_ephemeris["H_n^A"], -1)
        self.assertEquals(ext_ephemeris["x_n"], 11308469.7265625)
        self.assertEquals(ext_ephemeris["y_n"], -21233672.36328125)
        self.assertEquals(ext_ephemeris["z_n"], 8571060.05859375)
        self.assertEquals(ext_ephemeris["x_nv"], 0.5774717330932617)
        self.assertEquals(ext_ephemeris["y_nv"], -1.0365982055664062)
        self.assertEquals(ext_ephemeris["z_nv"], -3.320493698120117)
        self.assertEquals(ext_ephemeris["x_na"], 3.725290298461914e-12)
        self.assertEquals(ext_ephemeris["y_na"], -1.862645149230957e-12)
        self.assertEquals(ext_ephemeris["z_na"], 9.313225746154785e-13)
        self.assertEquals(ext_ephemeris["t_b"], 69300000.0)
        self.assertEquals(ext_ephemeris["gamma_n"], 0)
        self.assertEquals(ext_ephemeris["tau_n"], 0.033291056752204895)
        self.assertEquals(ext_ephemeris["E_n"], 0)