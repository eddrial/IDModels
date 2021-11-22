'''
Created on 24 Sep 2020

@author: oqb
'''
import unittest
import wRadia as wrd
import radia as rd
import MagnetsAndArrays as ma

class Test(unittest.TestCase):
    def setUp(self):
        rd.UtiDelAll()
        #ATHENA_II Parameters
        AII = ma.model_hyper_parameters(applePeriods = 3, Mova = 0.0)


    def test_appleMagnet(self):
        a = ma.appleMagnets(self.AII)
        self.assertEqual(a.model_hyper_parameters.applePeriods, 3, 'hello, error')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_appleMagnet']
    unittest.main()