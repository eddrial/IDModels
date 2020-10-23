'''
Created on 24 Sep 2020

@author: oqb
'''

from wradia import wrad_mat as wrdm
from wradia import wrad_obj as wrd

import numpy as np
import radia as rd
from idcomponents import parameters

class appleMagnet():
    '''
    classdocs
    '''


    def __init__(self, model_parameters = parameters.model_parameters(),magnet_centre  = [0,0,0]):
        
        '''
        Constructor
        '''
        
        self.mp = model_parameters
        self.magnet_centre = magnet_centre
        
        '''orientation order z,y,x'''
        self.a = wrd.wradObjCnt([])
    #    a.magnet_material = magnet_material
        p1 = wrd.wradObjThckPgn(magnet_centre[1], self.mp.mainmagthick, [[magnet_centre[0]-self.mp.nominal_fmagnet_dimensions[0]/2 + self.mp.apple_clampcut,magnet_centre[2]-self.mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]-self.mp.nominal_fmagnet_dimensions[0]/2 + self.mp.apple_clampcut,magnet_centre[2]+self.mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+self.mp.nominal_fmagnet_dimensions[0]/2 - self.mp.apple_clampcut,magnet_centre[2]+self.mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+self.mp.nominal_fmagnet_dimensions[0]/2 - self.mp.apple_clampcut,magnet_centre[2]-self.mp.nominal_fmagnet_dimensions[2]/2]], 
                                                                  self.mp.direction)
        p2 = wrd.wradObjThckPgn(magnet_centre[1], self.mp.mainmagthick, [[magnet_centre[0]-self.mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]-self.mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]-self.mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]+self.mp.nominal_fmagnet_dimensions[2]/2 - self.mp.apple_clampcut],
                                                                  [magnet_centre[0]-self.mp.nominal_fmagnet_dimensions[0]/2 + self.mp.apple_clampcut,magnet_centre[2]+self.mp.nominal_fmagnet_dimensions[2]/2 - self.mp.apple_clampcut],
                                                                  [magnet_centre[0]-self.mp.nominal_fmagnet_dimensions[0]/2 + self.mp.apple_clampcut,magnet_centre[2]-self.mp.nominal_fmagnet_dimensions[2]/2]], 
                                                                  self.mp.direction)
        p3 = wrd.wradObjThckPgn(magnet_centre[1], self.mp.mainmagthick, [[magnet_centre[0]+self.mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]-self.mp.nominal_fmagnet_dimensions[2]/2 + self.mp.apple_clampcut],
                                                                  [magnet_centre[0]+self.mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]+self.mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+self.mp.nominal_fmagnet_dimensions[0]/2 - self.mp.apple_clampcut,magnet_centre[2]+self.mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+self.mp.nominal_fmagnet_dimensions[0]/2 - self.mp.apple_clampcut,magnet_centre[2]-self.mp.nominal_fmagnet_dimensions[2]/2 + self.mp.apple_clampcut]], 
                                                                  self.mp.direction)
        
        self.a.wradObjAddToCnt([p1,p2,p3])
        self.a.wradMatAppl(self.mp.magnet_material)
        
        
        
if __name__ == '__main__':
    a = appleMagnet()
    
    print(a)
        