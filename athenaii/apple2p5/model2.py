'''
Created on 23 Oct 2020

@author: oqb


NOTE on ORIENTATION.

Dimensions given as three element list relative to direction of extrusion:
[z,y,x] when extrusion direction is y,
[y,x,z] when extrusion direction is x,
[x,z,y] when extrusion direction is z.

Holds for 2d coordinates in perpendicular plane.

For This Model, y is electron direction, x is transverse, z is vertical
View from Downstream

~~~~~~~~C1v~C2v~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~            ^z
~~C1h~~~~Q1~Q2~~~~C2h~~            |
~~~~~~~~~~~~~~~~~~~~~~~            __> x
~~C3h~~~~Q3~Q4~~~~C4h~~
~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~C3v~C4v~~~~~~~~


'''

from wradia import wrad_obj as wrd
from wradia import wrad_mat as wrdm
import radia as rd
import numpy as np
import matplotlib.pyplot as plt
from idcomponents import parameters
from idcomponents import magnet_shapes as ms
from idcomponents import halbach_arrays as ha

class compensatedAPPLE():
    '''
    classdocs
    '''


    def __init__(self, 
                 model_parameters = parameters.model_parameters(),
                 fmagnet = ms.appleMagnet, 
                 cmagnet = ms.compMagnet, 
                 gap = 50, 
                 rowshift = 0,
                 jawshift = 0, 
                 shiftmode = 'circular'):
        
        self.cont = wrd.wradObjCnt([])
        
        mp = model_parameters
        
        if shiftmode == 'circular':
            shiftmodesign = 1
        elif shiftmode == 'linear':
            shiftmodesign = -1
        else:
            shiftmodesign = 0
        
        self.allarrays = {'q1' : ha.HalbachArray(model_parameters,fmagnet),
                          'q2' : ha.HalbachArray(model_parameters,fmagnet),
                          'q3' : ha.HalbachArray(model_parameters,fmagnet),
                          'q4' : ha.HalbachArray(model_parameters,fmagnet),
                          'c1v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c1h' : ha.HalbachArray(model_parameters,cmagnet),
                          'c2v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c2h' : ha.HalbachArray(model_parameters,cmagnet),
                          'c3v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c3h' : ha.HalbachArray(model_parameters,cmagnet),
                          'c4v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c4h' : ha.HalbachArray(model_parameters,cmagnet),
                          }
        
        ### Q1 ###
        self.allarrays['q1'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[0] + mp.rowtorowgap)/2.0,
                                                 rowshift*shiftmodesign,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q1'].cont.wradFieldInvert()
        self.allarrays['q1'].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        
        
        ### Q2 ###
        self.allarrays['q2'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[0] + mp.rowtorowgap)/2.0,
                                                 rowshift*shiftmodesign,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q2'].cont.wradFieldInvert()
        self.allarrays['q2'].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        self.allarrays['q2'].cont.wradReflect([0,0,0],[1,0,0])
        
        ### Q3 ###
        self.allarrays['q3'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[0] + mp.rowtorowgap)/2.0,
                                                 rowshift*shiftmodesign,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q3'].cont.wradReflect([0,0,0],[1,0,0])
        
        ### Q4 ###
        self.allarrays['q4'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[0] + mp.rowtorowgap)/2.0,
                                                 rowshift*shiftmodesign,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        
        for key in self.allarrays:
            self.cont.wradObjAddToCnt([self.allarrays[key].cont])
        
        print('my compensated APPLE calculated at a gap of {}mm'.format(gap))
        '''
        Constructor
        '''


if __name__ == '__main__':
    testparams = parameters.model_parameters(Mova = 20)
    a = compensatedAPPLE(testparams)
    
    rd.ObjDrwOpenGL(a.cont.radobj)
    
    
        
    input("Press Enter to continue...")
    print('{}'.format(a.cont.radobj))