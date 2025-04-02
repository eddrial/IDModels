'''
Created on 23 Oct 2020

@author: oqb
'''

from wradia import wrad_mat as wrdm
from wradia import wrad_obj as wrd


import json
import numpy as np
import radia as rd
import h5py as h5



class model_parameters():

    def __init__(self, **kwargs):
        #h5py string type
        h5str = h5.special_dtype(vlen=str) 
        #general
        
        prop_defaults = {
            "origin": np.zeros(3), #set the origin of the device. Default is array([0., 0., 0.])
            "coordinate_names" :np.array(['X','S','Z'], dtype = h5str),
            "pointsperperiod" : 20,
            "block_subdivision" : [2,3,1],
            
            ######  Undulator Parameters  ######
            
            "type" : "Compensated_APPLE", #Or "Plain_APPLE"
            "beams" : 2,
            "quadrants" : 4,
            "rows_per_quadrant" : 3,
            #"rows" : 12, 
            "periods" : 3, # Number of Periods of the APPLE Undulator
            "minimumgap" : 2, # Minimum designed gap in mm
            "gap" : 5, #Default Gap to calculate at
            "shim" : 0.1, # The gap between each magnet in a row / magnet array.
            "periodlength" : 15, # The period length of the undulator
            "secondperiodlength" : 15, #The period length of a second array (for multiperiod array models or APPLE KNOTs etc)
            "thirdperiodlength" : 15, #The period length of a third array, for multi period arrays for eg TRIBs exploitation
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
            
            "square_magnet" : False,
            "nominal_fmagnet_dimensions" : [30.0,0.0,30.0], # The nominal maximal magnet dimension for the functional magnets [mm]
            "apple_clampcut" : 5.0, # The size of the square removed for clamping an APPLE magnet [mm]
            "apple_clampcut_non_symmetric": [5.0, 0.0, 3.0],
            "magnet_chamfer" : [5.0,0.0,5.0], # Dimensions of chamfer for a rectangular magnet (to make it octagonal) [mm]
            "direction" : 'y', # The direction of extrusion - along the direction of travel of the electrons. Dimensions propogate in the order [z,y,x]
        
            #####  Compensation Magnets #####
            
            "nominal_cmagnet_dimensions" : [15.0,0.0,30.0], # dimensions of the compensation magnets [mm]
            "comp_magnet_chamfer" : [5.0,0.0,5.0],
            "nominal_hcmagnet_dimensions" : [15.0,0.0,30.0], # dimensions of the compensation magnets [mm]
            "hcomp_magnet_chamfer" : [5.0,0.0,5.0],
            "nominal_vcmagnet_dimensions" : [15.0,0.0,30.0], # dimensions of the compensation magnets [mm]
            "vcomp_magnet_chamfer" : [5.0,0.0,5.0],
            
            #####  Magnet Material #####
            
            "ksi" : [.019, .06], # Permeability - anisotropic
            "M" : 1.21*1.344, # Block Remanence [T] Default Cryogenic Grade
            "Mova" : 0.0, # Off Vertical Angle of Vertical type magnet blocks [degrees]
            
            #####  Perturbation #####
            
            "perturbation_fn" : self.perturbation_fn
            
        }
        
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))
        
        ###Derived Attributes###
        
        #Undulator
        self.totalmagnets = int(self.periods*self.magnets_per_period + 1)
        
        self.perturbation_list = np.zeros([self.totalmagnets,2])
        
        #magnet thicknesses
        self.nominal_fmagnet_dimensions[1] = (self.periodlength-self.magnets_per_period * self.shim) / self.magnets_per_period
        self.nominal_cmagnet_dimensions[1] = self.nominal_fmagnet_dimensions[1]
        self.nominal_hcmagnet_dimensions[1] = self.nominal_fmagnet_dimensions[1]
        self.nominal_vcmagnet_dimensions[1] = self.nominal_fmagnet_dimensions[1]
        
        
        #square magnet dimensions
        if self.square_magnet is not False:
            self.nominal_fmagnet_dimensions[0] = self.square_magnet
            self.nominal_fmagnet_dimensions[2] = self.square_magnet
            self.nominal_cmagnet_dimensions[0] = self.square_magnet/2.0
            self.nominal_cmagnet_dimensions[2] = self.square_magnet+self.comp_magnet_chamfer[2]
                    
        #end_magnet_thicknesses
        self.end_magnet_thickness = [(self.periodlength / 8.0) - self.shim]
        
        #default magnet profile
        self.magnet_profile = np.random.rand(int(self.nominal_fmagnet_dimensions[0]+1))
        
        #magnetisation list
        self.M_list = np.zeros([self.totalmagnets,3])
        
        #magnetmaterial
        self.magnet_material = wrdm.wradMatLin(self.ksi,[0,0,self.M])
        
        
        
        
        #core undulator parameters
        if self.type == 'Compensated_APPLE':
            self.magnet_rows = 12
            self.rows = 12
            
        if self.type == 'Plain_APPLE':
            self.magnet_rows = 4
            self.rows = 4
        
    def perturbation_fn(self, s=0.0):
        return np.array([s*0.0,s*0.0])
        
    def resize_square_blocks(self, square):
        self.nominal_fmagnet_dimensions[0] = square
        self.nominal_fmagnet_dimensions[2] = square
        self.nominal_cmagnet_dimensions[0] = square
        self.nominal_cmagnet_dimensions[2] = square/2.0
        
        self.square_magnet = square
        
        return True

#TODO
    #def read json
    #def write json
    #def write to h5
    #def read h5
    
    def save(self, file_loc):
        
        tmp_dict = vars(self)
        
        for key in tmp_dict:
            #print (tmp_dict[key])
            if type(tmp_dict[key]) == np.ndarray:
                tmp_dict[key] = tmp_dict[key].tolist()
            if type(tmp_dict[key]) == wrdm.wradMatLin:
                tmp_dict[key] = [self.ksi,self.M]
        
        with open(file_loc, 'w') as f:
            json.dump(vars(self), f,sort_keys = True, indent = 4)
    
    
    def load(self,f):
        h5str = h5.special_dtype(vlen=str)
        with open(f) as jj:
            jsondict = json.load(jj)
        
        #print (jsondict)
        
        for key in jsondict:
            setattr(self, key, jsondict[key])
            
        
        self.origin = np.array(self.origin)
        self.coordinate_names = np.array(['X','S','Z'], dtype = h5str)
        
        self.magnet_material = wrdm.wradMatLin(self.ksi,[0,0,self.M])
        

    
class scan_parameters():
    
    def __init__(self, periodlength, **kwargs):
        #general
        prop_defaults = {
            "gaprange" : np.arange(2,3,4),
            "shiftrange" : np.arange(-periodlength/2.0,periodlength/2.0 +0.1,periodlength/2.0),
            "shiftmoderange" : ['circular']
            }
            
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))
            
        # shape is [#modes, #gaps, #shifts, 3 (= Bx, By, Bz)
        self.shape = [len(self.shiftmoderange),len(self.gaprange),len(self.shiftrange),3]