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
            
            "applePeriods" : 3, # Number of Periods of the APPLE Undulator
            "minimumgap" : 2, # Gap used in calculation in mm
            "rowtorowgap": 0.5, # for APPLE devices the distance between functional rows on the same jaw
            "shim" : 0.05, # The gap between each magnet in a row / magnet array.
            "compappleseparation" : 15.0, # The gap between functional magnets and compenation magnets
            "periodlength" : 15, # The period length of the undulator
            "circlin" : 1, # Polarisation mode of the undulator -1 is circ (parallel), 1 is linear (antiparallel)
            "shift" : 0, # distance of row shift in mm
            "halbach_direction" : 1,  # a value to determine the sense of magnet rotation along the axis. 1 = Field BELOW array. -1 Field ABOVE array 
            
            #####  Magnet Shape  #####
            
            "mainmagdimension" : 30, # The primary magnet dimension for the functional magnets [mm]
            "clampcut" : 5, # The size of the square removed for clamping [mm]
            "direction" : 'y', # The direction of extrusion - along the direction of travel of the electrons. Dimensions propogate in the order [z,y,x]
        
            #####  Compensation Magnets #####
            
            # "compmagdimensions" : [15.0,self.mainmagthick,30.0] # dimensions of the compensation magnets [mm]
            
            #####  Magnet Material #####
            
            "ksi" : [.019, .06], # Permeability - anisotropic
            "M" : 1.21*1.344, # Block Remanence [T]
            "Mova" : 0.0 # Off Vertical Angle of Vertical type magnet blocks [degrees]
        }
        
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))
        
        ###Derived Attributes###
        
        #Undulator
        self.appleMagnets = int(self.applePeriods*4 + 1);
        
        #magnet shape
        self.mainmagthick = (self.periodlength-4 * self.shim) / 4.0

        
        #compensation magnets
        self.compmagdimensions = [15.0,self.mainmagthick,30.0]
        
        #magnetmaterial
        self.magnet_material = wradMat.wradMatLin(self.ksi,[0,0,self.M])
        

class appleMagnet():
    '''
    classdocs
    '''


    def __init__(self, model_parameters = model_parameters.__init__(self),magnet_centre  = [0,0,0]):
        
        self.mp = model_parameters
        
        '''
        Constructor
        '''
        