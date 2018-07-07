import unittest
import ephemeris

class Tests(unittest.TestCase):
    def test_calc_sat_xyz(self):
        # Create test data
        eph = {"System":1,"PRN":1,"C_rs":-8.78125,
                "C_us":5.757436156272888e-06,
               "dn":4.394468729879142e-12,
               "M_0":0.9302223777587179,
               "C_uc":-4.811212420463562e-06,
               "e":0.00794832909014076,
               "sqrtA":5153.671276092529,
               "t_0e":64800000.0,
               "C_ic":-3.725290298461914e-09,
               "Omega_0":2.910170226716813,
               "C_is":8.568167686462402e-08,
               "I_0":0.9720403650400273,
               "C_rc": 274.09375,
               "w":0.652247015654833,
               "Omega_dot":-8.148910863417868e-12,
               "IDOT":-3.3679974334690787e-13,
               "T_GD":5.587935447692871e-06 ,
               "t_0c":64800000.0,"a_f2": 0.0,
               "a_f1":-3.637978807091713e-12,
               "a_f0":-0.061552971601486206 ,
               "URA":0,"IODE":68}
        t = 58374000.14730411/1000

        # Run function
        pos, sat_clk_bias, dt_r = ephemeris.calc_sat_xyz(t,eph)
        
        # Check output of function
        self.assertEquals(pos[0],12609667.744728811)
        self.assertEquals(pos[1],-20496207.098995764)
        self.assertEquals(pos[2],11337473.897957033
        )
        self.assertEquals(sat_clk_bias,-6.1549414555349904e-05)
        self.assertEquals(dt_r,3.5336684847128199e-09)      
    