'''
Created on 3 Mar 2020

@author: oqb
'''
from wRadia import wradObj as wrd
import radia as rd
import numpy as np

class model_parameters():
    
    def __init__(self):
        self.origin = np.zeros(3)
        self.mainmagthick = 5
        self.mainmagdimension = 30
        self.clampcut = 5
        self.direction = 'y'
    


def appleMagnet(parameter_class, mag_center):
    a = wrd.wradObjCnt([])
    p1 = wrd.wradObjThckPgn(0, parameter_class.mainmagthick, [[-5,-5],[-5,5],[5,5],[5,-5]], parameter_class.direction)
    p2 = wrd.wradObjThckPgn(10, parameter_class.mainmagthick, [[-5,-5],[-5,5],[5,5],[5,-5]], parameter_class.direction)
    p3 = wrd.wradObjThckPgn(20, parameter_class.mainmagthick, [[-5,-5],[-5,5],[5,5],[5,-5]], parameter_class.direction)
    
    a = wrd.wradObjAddToCnt(a.radobj, [p1.radobj,p2.radobj,p3.radobj])
    return a

def appleArray():
    pass

def appleTotal():
    pass

if __name__ == '__main__':
    
    #my parameter list
    '''    origin = np.zeros(3)
    mainmagthick = 5
    mainmagdimension = 30
    clamput = 5
    direction = 'y'
    '''
    #ATHENA_II Parameters
    AII = model_parameters()
    
    #my magnet model
    basemagnet = wrd.wradObjThckPgn(0, AII.mainmagthick, [[-5,-5],[-5,5],[5,5],[5,-5]], AII.direction)
    
    a = appleMagnet(AII,4)
    #my beam model
    
    #my apple model
    print(basemagnet.radobj)
    print(AII.origin)
    print(a.objectlist)
    
    rd.ObjDrwOpenGL(a.radobj)
    
    print(a.objectlist)
    pass