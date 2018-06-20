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
    
        # # Create test message
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