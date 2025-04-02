'''
Created on Apr 2, 2025

@author: oqb
'''
import time
import random

import numpy as np

import apple2p5.model2 as id1

import radia as rd
from idcomponents import parameters

if __name__ == '__main__':
    rd.UtiDelAll()
    a_param = parameters.model_parameters(
        periods = 10,
        periodlength = 40,
        minimumgap = 15,
        M = 1.32,
        block_subdivision = [1,1,1])
    #a_param.block_subdivision = [1,1,1]
    #a_param.periods = 20
    #a_param.periodlength = 40
    #a_param.minimumgap = 15
    
    #a_param.M = 1.32
    
    t0 = time.time()
    
    for i in range(len(a_param.M_list[:])):
        ang = random.random()*2*np.pi
        
        
        a_param.M_list[i,0:3:2] = np.array([a_param.M*np.sin(ang), a_param.M*np.cos(ang)])
    
    
    #a = ArbAPPLE(model_parameters = a_param)
    
    a = id1.plainAPPLE(model_parameters = a_param)
    
    rd.ObjDrwOpenGL(a.cont.radobj)
    
    pass