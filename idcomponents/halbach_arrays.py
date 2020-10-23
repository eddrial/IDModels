'''
Created on 23 Oct 2020

@author: oqb
'''
import numpy as np
import radia as rd

from wradia import wrad_obj as wrd
from wradia import wrad_mat as wrdm

from idcomponents import parameters
from idcomponents import magnet_shapes as ms

class HalbachArray():
    '''
    classdocs
    '''


    def __init__(self, model_parameters = parameters.model_parameters(), magnet = ms.appleMagnet):
        '''
        Constructor
        '''
        #def appleArray(model_parameters, loc_offset, halbach_direction = -1):
        self.cont = wrd.wradObjCnt([])
        
        loc_offset = [0,0,0]
        
        loc_offset[1] = -((model_parameters.totalmagnets-1)/2.0) * (model_parameters.nominal_fmagnet_dimensions[1] + model_parameters.shim)
        M = []
        mat = []
        for i in range(model_parameters.magnets_per_period):
            #M.append([halbach_direction * np.sin(i*np.pi/2.0)*model_parameters.M*np.sin(2*np.pi*model_parameters.Mova/360.0),halbach_direction * np.sin(i*np.pi/2.0)*model_parameters.M * np.cos(2*np.pi*model_parameters.Mova/360.0), np.cos(i*np.pi/2.0)*model_parameters.M])
            M.append([np.cos(i*2*np.pi/model_parameters.magnets_per_period)*model_parameters.M*np.sin(2*np.pi*model_parameters.Mova/360.0),-1 * np.sin(i*2*np.pi/model_parameters.magnets_per_period)*model_parameters.M, np.cos(i*2*np.pi/model_parameters.magnets_per_period)*model_parameters.M * np.cos(2*np.pi*model_parameters.Mova/360.0)])
            
            mat.append(wrdm.wradMatLin(model_parameters.ksi,M[i]))
        
        for x in range(-int((model_parameters.totalmagnets-1)/2),int(1+(model_parameters.totalmagnets-1)/2)):#0,model_parameters.appleMagnets
            
            mag = magnet(model_parameters, loc_offset) 
            loc_offset[1] += model_parameters.nominal_fmagnet_dimensions[1] + model_parameters.shim
            magcol = [(2 + y) / 4.0 for y in M[(x)%model_parameters.magnets_per_period]]
            mag.cont.wradObjDrwAtr(magcol, 2) # [x / myInt for x in myList]
            mag.cont.wradObjDivMag([2,3,1])
            self.cont.wradObjAddToCnt([mag.cont])
            
        #return a
        
    #mag = appleMagnet(AII,4,materiald,[z,y,x])
    #mag apply magnetisation and colour
    #add to container
        
if __name__ == '__main__':
    mymodelparams = parameters.model_parameters(magnets_per_period = 20)
    
    a = HalbachArray(mymodelparams)
    b = 2
    
    print('{}{}'.format(a.cont.radobj,b))
    rd.ObjDrwOpenGL(a.cont.radobj)
    
    input("Press Enter to continue...")