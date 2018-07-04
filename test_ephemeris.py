import unittest
import ephemeris

class Tests(unittest.TestCase):
    def test_calc_sat_xyz(self):
        # Create test data
        eph = {"System":1,"PRN":1,"C_rs":-8.78125,
                "C_us":5.539506673812866e-06,
               "dn":4.7037673235605926e-12,
               "M_0":1.5947882798474748,
               "C_uc":-3.7066638469696045e-07,
               "e":0.00791448203381151,
               "sqrtA":5153.666282653809,
               "t_0e":331200000.0,
               "C_ic":-1.6391277313232422e-07,
               "Omega_0":-3.124808765627783,
               "C_is":1.30385160446167e-07,
               "I_0":0.9718718749131658,
               "C_rc":280.96875,
               "w":0.6442693415469705,
               "Omega_dot":-8.322846679971361e-12,
               "IDOT":9.643258823294288e-14,
               "T_GD":5.587935447692871e-06,
               "t_0c":331200000.0,"a_f2":0.0,
               "a_f1":-3.524291969370097e-12,
               "a_f0":-0.05814945325255394,
               "URA":1,"IODE":54}
        t = 59000000/1000

        # Run function
        pos, sat_clk_bias = ephemeris.calc_sat_xyz(t,eph)
        
        # Check output of function
        self.assertEquals(pos[0],16073629.349016881)
        self.assertEquals(pos[1],-19771030.940108538)
        self.assertEquals(pos[2],16712811.164981617)
        self.assertEquals(sat_clk_bias,-0.056982420860378198)

        
        