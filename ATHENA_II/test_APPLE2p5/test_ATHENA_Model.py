'''
Created on 3 Mar 2020

@author: oqb
'''
import unittest
import wRadia as wrd


class Test(unittest.TestCase):

    def testone(self, a =2):
        assert a==2

    def wradiaimports(self):
        a = wrd.wradObj.wradObjCnt()
        print(a)
        self.assertFalse(False, 'msg')
        

    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()