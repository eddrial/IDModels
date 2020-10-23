'''
Created on 24 Sep 2020

@author: oqb
'''

from wRadia import wradMat
from wRadia import wradObj as wrd

import numpy as np
import radia as rd


class model_parameters():
    
    def __init__(self, **kwargs):
        #general
        prop_defaults = {
            "origin": np.zeros(3), #set the origin of the device. Default is array([0., 0., 0.])
            
            ######  Undulator Parameters  ######
            
            "periods" : 3, # Number of Periods of the APPLE Undulator
            "minimumgap" : 2, # Gap used in calculation in mm
            "shim" : 0.05, # The gap between each magnet in a row / magnet array.
            "periodlength" : 15, # The period length of the undulator
            "halbach_direction" : 1,  # a value to determine the sense of magnet rotation along the axis. 1 = Field BELOW array. -1 Field ABOVE array 
            "magnets_per_period" : 4, # This number is almost exclusively 4 in undulator Halbach arrays. But it doesn't *have* to be.
            
            #####  APPLE Undulator Parameters  #####
            "rowtorowgap": 0.5, # for APPLE devices the distance between functional rows on the same jaw
            "circlin" : 1, # Polarisation mode of the undulator -1 is circ (parallel), 1 is linear (antiparallel)
            "shift" : 0, # distance of row shift in mm
            
            #####  Compensated APPLE Undulator Parameters  #####
            "compappleseparation" : 15.0, # The gap between functional magnets and compenation magnets
            
            #####  Magnet Shape  #####
            
            "nominal_fmagnet_dimensions" : [30.0,0.0,30.0], # The nominal maximal magnet dimension for the functional magnets [mm]
            "apple_clampcut" : 5.0, # The size of the square removed for clamping an APPLE magnet [mm]
            "magnet_chamfer" : [5.0,0.0,5.0], # Dimensions of chamfer for a rectangular magnet (to make it octagonal) [mm]
            "direction" : 'y', # The direction of extrusion - along the direction of travel of the electrons. Dimensions propogate in the order [z,y,x]
        
            #####  Compensation Magnets #####
            
            "nominal_cmagnet_dimensions" : [15.0,0.0,30.0], # dimensions of the compensation magnets [mm]
            
            #####  Magnet Material #####
            
            "ksi" : [.019, .06], # Permeability - anisotropic
            "M" : 1.21*1.344, # Block Remanence [T]
            "Mova" : 0.0 # Off Vertical Angle of Vertical type magnet blocks [degrees]
        }
        
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))
        
        ###Derived Attributes###
        
        #Undulator
        self.totalmagnets = int(self.periods*self.magnets_per_period + 1);
        
        #magnet shape
        self.mainmagthick = (self.periodlength-self.magnets_per_period * self.shim) / self.magnets_per_period

        
        #compensation magnets
        self.compmagdimensions = [15.0,self.mainmagthick,30.0]
        
        #magnetmaterial
        self.magnet_material = wradMat.wradMatLin(self.ksi,[0,0,self.M])
        

class appleMagnet():
    '''
    classdocs
    '''


    def __init__(self, model_parameters = model_parameters(),magnet_centre  = [0,0,0]):
        
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
        