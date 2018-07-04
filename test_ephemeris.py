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
        pos, sat_clk_bias = ephemeris.calc_sat_xyz(t,eph)
        
        # Check output of function
        self.assertEquals(pos[0],22541255.091432475)
        self.assertEquals(pos[1],13680697.110073447)
        self.assertEquals(pos[2],4578677.2463169703)
        self.assertEquals(sat_clk_bias,-0.061317425526771774)

        
        