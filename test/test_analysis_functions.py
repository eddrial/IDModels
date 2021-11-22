'''
Created on 11 Nov 2021

@author: oqb
'''
import unittest
import numpy as np
import radia as rd
import wradia as wrd
from idanalysis import analysis_functions as af
from idcomponents import parameters
from apple2p5 import model2 as id


class Test(unittest.TestCase):


    def SetUp(self):
        rd.UtiDelAll()
        self.ax = wrd.wrad_obj.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[1,2,3])
    
    def testCaseFullSolution(self):
        a = 1
        pass
    
    def testCaseSolution(self):
        rd.UtiDelAll()
        test_hyper_params = parameters.model_parameters(Mova = 20, 
                                             periods = 1, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 6,
                                             gap = 2, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [1,1,1]
                                             )
        a = id.compensatedAPPLEv2(test_hyper_params)
#    
        case1 = af.CaseSolution(a)
        
        
        np.testing.assert_equal(case1.model.cont.radobj,1)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCaseFullSolution']
    unittest.main()