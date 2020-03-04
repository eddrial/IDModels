'''
Created on 3 Mar 2020

@author: oqb
'''
from wRadia import wradObj as wrd
import numpy as np

def parameters():
    pass

def appleMagnet():
    pass

def appleArray():
    pass

def appleTotal():
    pass

if __name__ == '__main__':
    
    #my parameter list
    origin = np.zeros(3)
    mainmagthick = 5
    mainmagdimension = 30
    clamput = 5
    direction = 'y'
    
    #my magnet model
    basemagnet = wrd.wradObjThckPgn(0, mainmagthick, [[-5,-5],[-5,5],[5,5],[5,-5]], direction)
    
    #my beam model
    
    #my apple model
    print(basemagnet.radobj)
    print(origin)
    
    pass