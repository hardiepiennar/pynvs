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
        self.assertEquals(sv_ephemeris["dn"], 4.7037673235605926e-12)
        self.assertEquals(sv_ephemeris["M_0"], 1.5947882798474748)
        self.assertEquals(sv_ephemeris["C_uc"], -3.7066638469696045e-07)
        self.assertEquals(sv_ephemeris["e"], 0.00791448203381151)
        self.assertEquals(sv_ephemeris["sqrtA"], 5153.666282653809)
        self.assertEquals(sv_ephemeris["t_oe"], 331200000.0)
        self.assertEquals(sv_ephemeris["C_ic"], -1.6391277313232422e-07)
        self.assertEquals(sv_ephemeris["Omega_0"], -3.124808765627783)
        self.assertEquals(sv_ephemeris["C_is"], 1.30385160446167e-07)
        self.assertEquals(sv_ephemeris["I_0"], 0.9718718749131658)
        self.assertEquals(sv_ephemeris["C_rc"], 280.96875)
        self.assertEquals(sv_ephemeris["w"], 0.6442693415469705)
        self.assertEquals(sv_ephemeris["Omega_dot"], -8.322846679971361e-12)
        self.assertEquals(sv_ephemeris["IDOT"], 9.643258823294288e-14)
        self.assertEquals(sv_ephemeris["T_GD"], 5.587935447692871e-06)
        self.assertEquals(sv_ephemeris["t_oc"], 331200000.0)
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
        self.assertEquals(sv_ephemeris["Ë_n"], 0) 

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
        # Test data
        data = b'qE\xad\x00\r\xee\xb3A\xd7\x03k_\xbd\x00\x00\x94\xd1@\x00\x00\x00\x00p\x99dA\x00\x02\x1f\x1f$\x00\xb8\x88\xf1\x87Y\xe2@\x00H\xe5\xfdN\xcdS@\x00\x000\xe9c[\x8d\xc0{\x00\x02\t\t0\x00\xfaD7@w\x01\xc1\x00H\xe5\x91\x07iR@\x00\x00XG\x80\xfc\xaa@;\x00\x01\x1a\xfb$R\xa8R&\xaa\\\xd4@\x00P\x9aeFHP@\x00\x00\xc0\x86pZ\x81\xc0;\x00\x01\x13\x03*\x932\xfd\xfcO\x9a\x03A\x00\xd0\xb5q\x97kR@\x00\x00,\x1e7F\xaf\xc0{\x00\x01\x06\xfc"\xc5(XY\x8e\xc5\x02\xc1\x00\x80\x1a\xc3\xed\xa1S@\x00\x00pMD\xc5\xaf@{\x00\x02\x03\x03#\x00p\xaf\x8d\x9b\xac\xe8@\x00H\xa5\xdc\xa4GQ@\x00\x00\x98{\x0e.\x94\xc0;\x00\x02\x17\x170\x00\xc0\x16a\xd5\xcb\xea\xc0\x00H%\xa5V}Q@\x00\x00\x00-\x9b\x12\x96@{\x00\x02\x06\x06%\x00t\xa0M\xc1r\xfa\xc0\x00H\xe5\xc7\x95MR@\x00\x00\x80\xf88#\xa7@;\x00\x02\x01\x01/\x00\xac\xf5*\xa4\xce\xfc@\x00H\xe5FeXS@\x00\x00\x8c\xfb\n\xa5\xa8\xc0{\x00\x02\x0c\x0c-\x00\xe0\xb3>zw\xe3@\x00H\xa5\x12U\xd1T@\x00\x000\xff\xf6(\x8f\xc0{\x00\x02\x11\x11*\x00\xd8\xdaX\xe9A\xec@\x00H\xa5\xbe\xdd\x7fR@\x00\x00h[\xa4\x12\x97\xc0{\x00'

        # Process data
        raw = binr.process_raw_data(data)

        # Check raw data response
        self.assertEquals(raw["Time"],334368000.67684084)
        self.assertEquals(raw["Week Number"],983)
        self.assertEquals(raw["GPS time shift"],18000.000045149976 )
        self.assertEquals(raw["GLO time shift"],10800000.0 )
        self.assertEquals(raw["Rec Time Scale Correction"],0 )
        self.assertEquals(len(raw["Signal Type"]),10)
        self.assertEquals(raw["Signal Type"][0],2)
        self.assertEquals(raw["Sat Number"][0],31)
        self.assertEquals(raw["Carrier Number"][0],31)
        self.assertEquals(raw["Carrier Phase"][0],37580.24823413789)
        self.assertEquals(raw["Pseudo Range"][0],79.20794627562282)
        self.assertEquals(raw["Doppler Freq"][0],-939.4237846136093)
        self.assertEquals(raw["Flags"][0],123)
        self.assertEquals(raw["Sat Number"][2],26)
    
    def test_process_software_version(self):
        # Test data
        data = b' CSM54 05.04 18/10/16\x00\xbc\x8f\xec\x1cNV08C 07.03 30/03/12\x00\xbc\x8f\xec\x1c                    \x00\x00\x00\x00\x00'

        # Process software version data
        version = binr.process_software_version(data)

        # Check data
        self.assertEquals(version["No of Channels"], 32)
        #self.assertEquals(version["Version"], 32) # TODO: implement if you want
        self.assertEquals(version["Serial Number"], 485265340)

    def test_process_ionosphere_parameters(self):
        # Test data
        data = b'\x00\x00\xa01\x00\x00\x802\x00\x00\x80\xb3\x00\x00\x00\xb4\x00\x00\xa0G\x00\x00\xc0G\x00\x00\x80\xc7\x00\x00\x00\xc9\xff'
        raise NotImplementedError()

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
        # Test data
        data = b'\x01\x01\x00\x80\xd8\xc2\xfa>\x8d,\xc5cl\xe1l!\x07@\x00\xe0\xbc\xb6\x00\x00\x00\x98\x9a?\x80?\x00\xf0:7\x00\x00\xe0+\xad!\xb4@\x00\x00\x00\x00\x93+\xb4A'
        
        # Process packet
        ext_ephemeris = binr.process_extended_ephemeris_of_satellites(data)

        # Check that data is correct
        self.assertEquals(ext_ephemeris["System"], 0)
        # TODO: we need a valid dataset here
        # TODO: we need to check our msg lengths when processing