'''
Created on 19 Mar 2026

@author: oqb


NOTE on ORIENTATION.

Dimensions given as three element list relative to direction of extrusion:
[z,y,x] when extrusion direction is y,
[y,x,z] when extrusion direction is x,
[x,z,y] when extrusion direction is z.

Holds for 2d coordinates in perpendicular plane.

For This Model, y is electron direction, x is transverse, z is vertical
View from Upstream

Upper Beam (U)
          ^z
           |
            __> x

Lower Beam (L)



'''

from wradia import wrad_obj as wrd
from wradia import wrad_mat as wrdm
import radia as rd
import numpy as np
import matplotlib.pyplot as plt
from idcomponents import parameters
from idcomponents import magnet_shapes as ms
from idcomponents import halbach_arrays as ha

import matplotlib.gridspec as gridspec
from wradia.wrad_obj import wradObjCnt

class cpmu_HZB():
    def __init__(self, 
         model_parameters = parameters.model_parameters(),
         magnet = ms.appleMagnet,
         pole = ms.tribsAppleMiddleMagnet):
        
        rd.UtiDelAll()
        self.cont = wrd.wradObjCnt([])
        
        if model_parameters.termination_style == 'HZB':
            termination = ha.HalbachTermination_APPLE_HZB(model_parameters,magnet)
            
        else:
            termination = ha.HalbachTermination_APPLE(model_parameters,magnet)
        
        self.model_parameters = model_parameters
        mp = self.model_parameters
                
        self.rownames = ['upper','lower']
        
        self.allarraytabs = np.array([ha.MagnetRow(self.rownames[0], ha.Halbach2Array(model_parameters,magnet,pole),
                                                       ha.Halbach2ArrayTermination()) for _ in range(2)])
            
        for r in range(2):
            self.allarraytabs[r] = ha.MagnetRow(self.rownames[r], ha.Halbach2Array(model_parameters,magnet,pole),
                                              ha.Halbach2ArrayTermination(), beam = int((r//2)),  row = r)
        
        #lower
        self.allarraytabs[0].cont.wradTranslate([0.0,
                                                 0.0,
                                                 -(mp.nominal_fmagnet_dimensions[0] + mp.gap)/2.0])
        
        #upper
        self.allarraytabs[1].cont.wradTranslate([0.0,
                                                 0.0,
                                                 (mp.nominal_fmagnet_dimensions[0] + mp.gap)/2.0])
        
        self.allarraytabs[1].cont.wradFieldInvert()
        
        for row in range(len(self.allarraytabs)):
            self.cont.wradObjAddToCnt([self.allarraytabs[row].cont])
        
if __name__ == '__main__':
    testparams = parameters.model_parameters(Mova = 0, 
                                             periods = 5, 
                                             periodlength = 20,
                                             block_subdivision = [1,1,1],
                                             nominal_fmagnet_dimensions = [9.75,0.0,9.75], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,7.5], 
                                             #compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             #comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period =2,
                                             gap = 13,
                                             rowshift = 10,
                                             shiftmode = 'circular')
    #CPMU test
    

    b = cpmu_HZB(testparams)
    
    rd.ObjDrwOpenGL(b.cont.radobj)
    
    print(1)
