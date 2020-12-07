'''
Created on 23 Oct 2020

@author: oqb
'''

from wradia import wrad_mat as wrdm
from wradia import wrad_obj as wrd

import numpy as np
import radia as rd


class model_parameters():
    
    def __init__(self, **kwargs):
        #general
        prop_defaults = {
            "origin": np.zeros(3), #set the origin of the device. Default is array([0., 0., 0.])
            "pointsperperiod" : 20,
            "block_subdivision" : [2,3,1],
            
            ######  Undulator Parameters  ######
            
            "periods" : 3, # Number of Periods of the APPLE Undulator
            "minimumgap" : 2, # Minimum designed gap in mm
            "gap" : 5, #Default Gap to calculate at
            "shim" : 0.05, # The gap between each magnet in a row / magnet array.
            "periodlength" : 15, # The period length of the undulator
            "halbach_direction" : 1,  # a value to determine the sense of magnet rotation along the axis. 1 = Field BELOW array. -1 Field ABOVE array 
            "magnets_per_period" : 4, # This number is almost exclusively 4 in undulator Halbach arrays. But it doesn't *have* to be.
            
            #####  APPLE Undulator Parameters  #####
            "rowtorowgap": 0.5, # for APPLE devices the distance between functional rows on the same jaw
            "shiftmode" : 'circular', # Polarisation mode of the undulator ; 'circular' (parallel) or 'linear' (antiparallel)
            "rowshift" : 0, # distance of row shift in mm
            "jawshift" : 0, #distance of jawshift in mm
            "end_separation" : 2.5, #separation of end magnet in usual APPLE end constellation
            
            #####  Compensated APPLE Undulator Parameters  #####
            "compappleseparation" : 15.0, # The gap between functional magnets and compenation magnets
            
            #####  Magnet Shape  #####
            
            "nominal_fmagnet_dimensions" : [30.0,0.0,30.0], # The nominal maximal magnet dimension for the functional magnets [mm]
            "apple_clampcut" : 5.0, # The size of the square removed for clamping an APPLE magnet [mm]
            "magnet_chamfer" : [5.0,0.0,5.0], # Dimensions of chamfer for a rectangular magnet (to make it octagonal) [mm]
            "direction" : 'y', # The direction of extrusion - along the direction of travel of the electrons. Dimensions propogate in the order [z,y,x]
        
            #####  Compensation Magnets #####
            
            "nominal_cmagnet_dimensions" : [15.0,0.0,30.0], # dimensions of the compensation magnets [mm]
            "comp_magnet_chamfer" : [5.0,0.0,5.0],
            
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
        
        #magnet thicknesses
        self.nominal_fmagnet_dimensions[1] = (self.periodlength-self.magnets_per_period * self.shim) / self.magnets_per_period
        self.nominal_cmagnet_dimensions[1] = self.nominal_fmagnet_dimensions[1]
        
        #end_magnet_thicknesses
        self.end_magnet_thickness = [(self.periodlength / 8.0) - self.shim]
        
        #magnetmaterial
        self.magnet_material = wrdm.wradMatLin(self.ksi,[0,0,self.M])
        
#TODO
    #def read json
    #def write json
    #def write to h5
    #def read h5