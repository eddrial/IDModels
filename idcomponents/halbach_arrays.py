'''
Created on 23 Oct 2020

@author: oqb
'''
import numpy as np
import radia as rd
import matplotlib.pyplot as plt

from wradia import wrad_obj as wrd
from wradia import wrad_mat as wrdm

from idcomponents import parameters
from idcomponents import magnet_shapes as ms
from wradia.wrad_obj import wradObjCnt

class HalbachArray():
    '''
    classdocs
    '''


    def __init__(self, model_hyper_parameters = parameters.model_parameters(), magnet = ms.appleMagnet, array_number = 1):
        '''
        Constructor
        '''
        #switch to find out which array order is required, for multi period undulators
        if array_number == 1:
            per_length = model_hyper_parameters.periodlength
            model_hyper_parameters.nominal_fmagnet_dimensions[1] = (model_hyper_parameters.periodlength-model_hyper_parameters.magnets_per_period * model_hyper_parameters.shim) / model_hyper_parameters.magnets_per_period
        
        elif array_number == 2:
            per_length = model_hyper_parameters.secondperiodlength
            model_hyper_parameters.nominal_fmagnet_dimensions[1] = (model_hyper_parameters.secondperiodlength-model_hyper_parameters.magnets_per_period * model_hyper_parameters.shim) / model_hyper_parameters.magnets_per_period
        
            
        elif array_number == 3:
            per_length = model_hyper_parameters.thirdperiodlength
            model_hyper_parameters.nominal_fmagnet_dimensions[1] = (model_hyper_parameters.thirdperiodlength-model_hyper_parameters.magnets_per_period * model_hyper_parameters.shim) / model_hyper_parameters.magnets_per_period
        

        
        #def appleArray(model_hyper_parameters, loc_offset, halbach_direction = -1):
        self.cont = wrd.wradObjCnt([])
        
        loc_offset = [0,0,0]
        
        #define the location offset in S of the magnet
        loc_offset[1] = -((model_hyper_parameters.totalmagnets-1)/2.0) * (model_hyper_parameters.nominal_fmagnet_dimensions[1] + model_hyper_parameters.shim)
        
        
        #functionally efined offset in x and z based on s. Function can be passed in.
        loc_offset[0:3:2] = model_hyper_parameters.perturbation_fn(loc_offset[1])
        
        M = []
        mat = []
        for i in range(model_hyper_parameters.magnets_per_period):
            #M.append([halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M*np.sin(2*np.pi*model_hyper_parameters.Mova/360.0),halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M * np.cos(2*np.pi*model_hyper_parameters.Mova/360.0), np.cos(i*np.pi/2.0)*model_hyper_parameters.M])
            M.append([np.cos(i*2*np.pi/model_hyper_parameters.magnets_per_period)*model_hyper_parameters.M*np.sin(2*np.pi*model_hyper_parameters.Mova/360.0),-1 * np.sin(i*2*np.pi/model_hyper_parameters.magnets_per_period)*model_hyper_parameters.M, np.cos(i*2*np.pi/model_hyper_parameters.magnets_per_period)*model_hyper_parameters.M * np.cos(2*np.pi*model_hyper_parameters.Mova/360.0)])
            
            mat.append(wrdm.wradMatLin(model_hyper_parameters.ksi,M[i]))
        
        for x in range(-int((model_hyper_parameters.totalmagnets-1)/2),int(1+(model_hyper_parameters.totalmagnets-1)/2)):#0,model_hyper_parameters.appleMagnets
            
            mag = magnet(model_hyper_parameters, loc_offset,mat[(x)%model_hyper_parameters.magnets_per_period]) 
            loc_offset[1] += model_hyper_parameters.nominal_fmagnet_dimensions[1] + model_hyper_parameters.shim
            loc_offset[0:3:2] = model_hyper_parameters.perturbation_fn(loc_offset[1])
            self.cont.wradObjAddToCnt([mag.cont])
            
        #return a
        
    #mag = appleMagnet(AII,4,materiald,[z,y,x])
    #mag apply magnetisation and colour
    #add to container
    
class HalbachTermination_APPLE():
    
    def __init__(self, model_hyper_parameters = parameters.model_parameters(), magnet = ms.appleMagnet):
        self.cont = wrd.wradObjCnt([])
            
        loc_offset = [0,0,0]
        
        loc_offset[1] = -(((model_hyper_parameters.totalmagnets-1)/2.0) * 
                          (model_hyper_parameters.nominal_fmagnet_dimensions[1] + 
                           model_hyper_parameters.shim) + 
                          model_hyper_parameters.nominal_fmagnet_dimensions[1]/2.0 + 2 *model_hyper_parameters.shim +
                          model_hyper_parameters.end_magnet_thickness[0] * 2.5 +
                          model_hyper_parameters.end_separation
                          )
        M = []
        mat = []
        
        for i in range(model_hyper_parameters.magnets_per_period):
            #M.append([halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M*np.sin(2*np.pi*model_hyper_parameters.Mova/360.0),halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M * np.cos(2*np.pi*model_hyper_parameters.Mova/360.0), np.cos(i*np.pi/2.0)*model_hyper_parameters.M])
            M.append([np.cos(i*2*np.pi/model_hyper_parameters.magnets_per_period)*model_hyper_parameters.M*np.sin(2*np.pi*model_hyper_parameters.Mova/360.0),
                      -1 * np.sin(i*2*np.pi/model_hyper_parameters.magnets_per_period)*model_hyper_parameters.M, 
                      np.cos(i*2*np.pi/model_hyper_parameters.magnets_per_period)*model_hyper_parameters.M * np.cos(2*np.pi*model_hyper_parameters.Mova/360.0)])
            
            mat.append(wrdm.wradMatLin(model_hyper_parameters.ksi,M[i]))
        
        Mus = -int((model_hyper_parameters.totalmagnets-1)/2)#1st full magnet Upstream in row
        Mds = int((model_hyper_parameters.totalmagnets-1)/2)#1st full magnet Downstreamin row
        
        mag1 = magnet(model_hyper_parameters, loc_offset,mat[(Mus-3)%model_hyper_parameters.magnets_per_period], magnet_thickness = model_hyper_parameters.end_magnet_thickness[0]) 
        loc_offset[1] += model_hyper_parameters.end_magnet_thickness[0] + model_hyper_parameters.end_separation
        
        mag2 = magnet(model_hyper_parameters, loc_offset,mat[(Mus-2)%model_hyper_parameters.magnets_per_period], magnet_thickness = model_hyper_parameters.end_magnet_thickness[0]) 
        
        loc_offset[1] += model_hyper_parameters.end_magnet_thickness[0] + model_hyper_parameters.shim
        
        mag3 = magnet(model_hyper_parameters, loc_offset,mat[(Mus-1)%model_hyper_parameters.magnets_per_period], magnet_thickness = model_hyper_parameters.end_magnet_thickness[0]) 
        
        
        loc_offset[1] = (((model_hyper_parameters.totalmagnets-1)/2.0) * 
                          (model_hyper_parameters.nominal_fmagnet_dimensions[1] + 
                           model_hyper_parameters.shim) + 
                          model_hyper_parameters.nominal_fmagnet_dimensions[1]/2.0 + 
                          model_hyper_parameters.shim +
                          model_hyper_parameters.end_magnet_thickness[0]/2.0
                          )
        
        mag4 = magnet(model_hyper_parameters, loc_offset,mat[(Mds+1)%model_hyper_parameters.magnets_per_period], magnet_thickness = model_hyper_parameters.end_magnet_thickness[0]) 
        loc_offset[1] += model_hyper_parameters.end_magnet_thickness[0] + model_hyper_parameters.shim
        
        mag5 = magnet(model_hyper_parameters, loc_offset,mat[(Mds+2)%model_hyper_parameters.magnets_per_period], magnet_thickness = model_hyper_parameters.end_magnet_thickness[0]) 
        loc_offset[1] += model_hyper_parameters.end_magnet_thickness[0] + model_hyper_parameters.end_separation
        
        mag6 = magnet(model_hyper_parameters, loc_offset,mat[(Mds+3)%model_hyper_parameters.magnets_per_period], magnet_thickness = model_hyper_parameters.end_magnet_thickness[0]) 
        
        
        self.cont.wradObjAddToCnt([mag1.cont, mag2.cont, mag3.cont, mag4.cont, mag5.cont, mag6.cont])
            
    
class MagnetRow():
    def __init__(self,name = 'default_name', Body = HalbachArray(), Termination = HalbachTermination_APPLE(),beam = 0, quadrant = 0, row = 0):
        self.cont = wrd.wradObjCnt([])
        self.cont.wradObjAddToCnt([Body.cont, Termination.cont])
        self.beam = beam
        self.quadrant = quadrant
        self.row = row
        self.name = name

    
if __name__ == '__main__':
    mymodelparams = parameters.model_parameters(magnets_per_period = 6, periods = 1)
    
    a = HalbachArray(mymodelparams)
    b = HalbachTermination_APPLE(mymodelparams)
    
    c = MagnetRow(a,b)
    
    a.cont.wradSolve(0.001, 1000)
    
    print('{}{}'.format(a.cont.radobj,b))
#    rd.ObjDrwOpenGL(a.cont.radobj)
    rd.ObjDrwOpenGL(b.cont.radobj)
    rd.ObjDrwOpenGL(c.cont.radobj)
    
    
    
    z = 17.5; x1 = 15.25; x2 = 0; ymax = 400; nump = 2001
    
    Bz1 = rd.FldLst(a.cont.radobj, 'bz', [x1,-ymax,z], [x1,ymax,z], nump, 'arg', 0)
    Bz2 = rd.FldLst(a.cont.radobj, 'bz', [x2,-ymax,z], [x2,ymax,z], nump, 'arg',0 )
    
    Bx1 = rd.FldLst(a.cont.radobj, 'bx', [x1,-ymax,z], [x1,ymax,z], nump, 'arg', 0)
    Bx2 = rd.FldLst(a.cont.radobj, 'bx', [x2,-ymax,z], [x2,ymax,z], nump, 'arg',0 )
    
    Bz1 = np.array(Bz1)
    Bz2 = np.array(Bz2)

    Bx1 = np.array(Bx1)
    Bx2 = np.array(Bx2)
    
    #set up plot
    # set width and height
    width = 7
    height = 9
    
    #create the figure with nice margins
    fig, axs = plt.subplots(2,1, sharex = False, sharey = False)
    fig.subplots_adjust(left=.15, bottom=.16, right=.85, top= 0.9, wspace = 0.7, hspace = 0.6)
    fig.set_size_inches(width, height)
    
    
    axs[0].plot(Bz1[:,0],Bz1[:,1])
    axs[0].plot(Bx1[:,0],Bx1[:,1])
    axs[1].plot(Bz2[:,0],Bz2[:,1])
    axs[1].plot(Bx2[:,0],Bx2[:,1])
    
    #plt.show()
    
    input("Press Enter to continue...")