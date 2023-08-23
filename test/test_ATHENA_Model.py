'''
Created on 3 Mar 2020

@author: oqb
'''
import unittest
import radia as rd
import wradia as wrd

import apple2p5.model1 as am


class Test(unittest.TestCase):

    def testone(self, a =2):
        assert a==2

    def wradiaimports(self):
        a = wrd.wrad_obj.wradObjCnt()
        print(a)
        self.assertFalse(False, 'msg')


    def testName(self):
        pass
    
class Test_appleUpperBeam_magnetOrientation_VerticalField(unittest.TestCase):
    #magnet directions x,s,z
    def setUp(self):
        rd.UtiDelAll()
        #ATHENA_II Parameters
        AII = am.model_hyper_parameters(applePeriods = 3, Mova = 0.0)
        self.tc = am.appleUpperBeam(AII) #tc test_container
        
#q1 is upper quadrant structure side
        
    def test_q1_centre_magnet_vertical_up(self):
        '''Test to check central magnet upper structure side is a vertical magnet
        '''
        self.assertAlmostEqual(self.tc.objectlist[0].objectlist[int((self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[2], 1.62624, 14)
        
    def test_q1_ds_neighbourcentre_magnet_horizontal_ds(self):
        '''Test to check magnet downstream of central magnet upper structure side is a pointing downstream (increasing s) magnet
        '''
        self.assertAlmostEqual(self.tc.objectlist[0].objectlist[int(1+(self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[1], 1.62624, 8)
        
    def test_q1_us_neighbourcentre_magnet_horizontal_ds(self):
        '''Test to check magnet upstream of central magnet upper structure bench side is a pointing upstream (decreasing s) magnet
        '''
        self.assertAlmostEqual(self.tc.objectlist[0].objectlist[int(-1+(self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[1], -1.62624, 8)
        
    def test_q1_2xus_neighbourcentre_magnet_vertical_down(self):
        '''Test to check magnet twice upstream of central magnet upper structure bench side is a pointing down magnet
        '''
        self.assertAlmostEqual(self.tc.objectlist[0].objectlist[int(-2+(self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[2], -1.62624, 8)
        
    def test_q2_centre_magnet_vertical_up(self):
        '''Test to check central magnet upper bench side is a vertical magnet
        '''
        self.assertAlmostEqual(self.tc.objectlist[1].objectlist[int((self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[2], 1.62624, 14)
        
    

class Test_appleUpperBeam_magnetOrientation_TiltedField(unittest.TestCase):
    #magnet directions x,s,z
    def setUp(self):
        rd.UtiDelAll()
        #ATHENA_II Parameters
        AII = am.model_hyper_parameters(applePeriods = 3, Mova = 10.0)
        self.tc = am.appleUpperBeam(AII) #tc test_container
        
#q1 is upper quadrant bench side q2 is upper structure side, q2 is structure side
        
    def test_q1_centre_magnet_vertical_10deg(self):
        '''Test to check central magnet upper structure side is a vertical magnet
        '''
        self.assertAlmostEqual(self.tc.objectlist[0].objectlist[int((self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[2], 1.60153376025857, 14)
        
    def test_q1_ds_neighbourcentre_magnet_horizontal_ds(self):
        '''Test to check magnet downstream of central magnet upper structure side is a pointing downstream (increasing s) magnet
        '''
        self.assertAlmostEqual(self.tc.objectlist[0].objectlist[int(1+(self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[1], 1.62624, 8)
        
    def test_q1_us_neighbourcentre_magnet_horizontal_ds(self):
        '''Test to check magnet upstream of central magnet upper structure side is a pointing upstream (decreasing s) magnet
        '''
        self.assertAlmostEqual(self.tc.objectlist[0].objectlist[int(-1+(self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[1], -1.62624, 8)
        
    def test_q1_2xus_neighbourcentre_magnet_vertical_down(self):

        self.assertAlmostEqual(self.tc.objectlist[0].objectlist[int(-2+(self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[2], -1.60153376025857, 8)
        
    def test_q2_centre_magnet_vertical_10deg(self):
        '''Test to check central magnet upper bench side is a vertical magnet
        '''
        self.assertAlmostEqual(self.tc.objectlist[1].objectlist[int((self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[2], 1.60153376025857, 14)

    def test_q1_centre_magnet_transverse_10deg(self):
        '''Test to check central magnet upper structure side transverse component is negative (points to structure)
        '''
        self.assertAlmostEqual(self.tc.objectlist[0].objectlist[int((self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[0], -0.2823936124490688, 14)
        
    def test_q2_centre_magnet_transverse_10deg_neg_q1(self):
        ''''Test to check central magnet upper structure side transverse component is opposite to the bench side
        '''
        self.assertAlmostEqual(self.tc.objectlist[0].objectlist[int((self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[0],
                                -self.tc.objectlist[1].objectlist[int((self.tc.objectlist[0].objectlist.__len__()-1)/2)].objectlist[0].magnetisation[0], 14)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()