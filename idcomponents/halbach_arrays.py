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
from apple2p5.model1 import model_hyper_parameters

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
        
        #assign locally functional or compensation magnet quantities
        if magnet == ms.appleMagnet:
            magnet_length = model_hyper_parameters.nominal_fmagnet_dimensions[1]
            total_magnets = model_hyper_parameters.totalmagnets
            magnets_per_period = model_hyper_parameters.magnets_per_period
            Mova = model_hyper_parameters.Mova
            
            
        else:
            magnet_length = model_hyper_parameters.nominal_cmagnet_dimensions[1]
            total_magnets = int(model_hyper_parameters.periods*model_hyper_parameters.magnets_per_period_comp + 1)
            magnets_per_period = model_hyper_parameters.magnets_per_period_comp 
            Mova = model_hyper_parameters.Mova_comp

        
        #def appleArray(model_hyper_parameters, loc_offset, halbach_direction = -1):
        self.cont = wrd.wradObjCnt([])
        
        loc_offset = [0,0,0]
        
        #define the location offset in S of the magnet
        loc_offset[1] = -((total_magnets-1)/2.0) * (magnet_length + model_hyper_parameters.shim)
        
        
        #functionally efined offset in x and z based on s. Function can be passed in.
        loc_offset[0:3:2] = model_hyper_parameters.perturbation_fn(loc_offset[1])
        
        M = []
        mat = []
        for i in range(magnets_per_period):
            #M.append([halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M*np.sin(2*np.pi*model_hyper_parameters.Mova/360.0),halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M * np.cos(2*np.pi*model_hyper_parameters.Mova/360.0), np.cos(i*np.pi/2.0)*model_hyper_parameters.M])
            M.append([np.cos(i*2*np.pi/magnets_per_period)*model_hyper_parameters.M*np.sin(2*np.pi*Mova/360.0),-1 * np.sin(i*2*np.pi/magnets_per_period)*model_hyper_parameters.M, np.cos(i*2*np.pi/magnets_per_period)*model_hyper_parameters.M * np.cos(2*np.pi*Mova/360.0)])
            
            mat.append(wrdm.wradMatLin(model_hyper_parameters.ksi,M[i]))
        
        for x in range(-int((total_magnets-1)/2),int(1+(total_magnets-1)/2)):#0,model_hyper_parameters.appleMagnets
            
            mag = magnet(model_hyper_parameters, loc_offset,mat[(x)%magnets_per_period]) 
            loc_offset[1] += magnet_length + model_hyper_parameters.shim
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
        
class HalbachTermination_APPLE_HZB():
    
    def __init__(self, model_hyper_parameters = parameters.model_parameters(), magnet = ms.appleMagnet):
        self.cont = wrd.wradObjCnt([])
            
        loc_offset = [0,0,0]
        
        loc_offset[1] = -(((model_hyper_parameters.totalmagnets-1)/2.0) * 
                          (model_hyper_parameters.nominal_fmagnet_dimensions[1] + 
                           model_hyper_parameters.shim) + 
                          31*model_hyper_parameters.periodlength/32 + model_hyper_parameters.shim/2
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
        
        mag1 = magnet(model_hyper_parameters, loc_offset,mat[(Mus-4)%model_hyper_parameters.magnets_per_period], magnet_thickness = (0.25*model_hyper_parameters.periodlength/4)) 
        loc_offset[1] += 7*model_hyper_parameters.periodlength/32
        
        mag2 = magnet(model_hyper_parameters, loc_offset,mat[(Mus-3)%model_hyper_parameters.magnets_per_period], magnet_thickness = (0.5*model_hyper_parameters.periodlength/4)) 
        
        loc_offset[1] += 9*model_hyper_parameters.periodlength/32
        
        mag3 = magnet(model_hyper_parameters, loc_offset,mat[(Mus-2)%model_hyper_parameters.magnets_per_period], magnet_thickness =(0.75*model_hyper_parameters.periodlength/4)) 
        
        loc_offset[1] += 3*model_hyper_parameters.periodlength/32 + model_hyper_parameters.shim+(model_hyper_parameters.nominal_fmagnet_dimensions[1])/2
        
        mag4 = magnet(model_hyper_parameters, loc_offset,mat[(Mus-1)%model_hyper_parameters.magnets_per_period], magnet_thickness =model_hyper_parameters.nominal_fmagnet_dimensions[1]) 
        
        
        loc_offset[1] = (((model_hyper_parameters.totalmagnets-1)/2.0) * 
                          (model_hyper_parameters.nominal_fmagnet_dimensions[1] + 
                           model_hyper_parameters.shim) + 
                          model_hyper_parameters.nominal_fmagnet_dimensions[1]/2.0 + model_hyper_parameters.shim +
                          3*model_hyper_parameters.periodlength/32
                          )
        
        mag5 = magnet(model_hyper_parameters, loc_offset,mat[(Mds+1)%model_hyper_parameters.magnets_per_period], magnet_thickness =model_hyper_parameters.nominal_fmagnet_dimensions[1]) 
        loc_offset[1] += 3*model_hyper_parameters.periodlength/32 + model_hyper_parameters.shim+(model_hyper_parameters.nominal_fmagnet_dimensions[1])/2
        
        mag6 = magnet(model_hyper_parameters, loc_offset,mat[(Mds+2)%model_hyper_parameters.magnets_per_period], magnet_thickness =(0.75*model_hyper_parameters.periodlength/4)) 
        loc_offset[1] += 9*model_hyper_parameters.periodlength/32
        
        mag7 = magnet(model_hyper_parameters, loc_offset,mat[(Mds+3)%model_hyper_parameters.magnets_per_period], magnet_thickness = (0.5*model_hyper_parameters.periodlength/4)) 
        loc_offset[1] += 7*model_hyper_parameters.periodlength/32
        
        mag8 = magnet(model_hyper_parameters, loc_offset,mat[(Mds+4)%model_hyper_parameters.magnets_per_period], magnet_thickness = (0.25*model_hyper_parameters.periodlength/4)) 
        
        
        self.cont.wradObjAddToCnt([mag1.cont, mag2.cont, mag3.cont, mag4.cont, mag5.cont, mag6.cont, mag7.cont, mag8.cont])
        
class Halbach2ArrayTermination():
    
    def __init__(self):
        self.cont = wrd.wradObjCnt([])
        
class HalbachArrayCompensation():
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
        
        #assign locally functional or compensation magnet quantities
    
        magnet_length = model_hyper_parameters.nominal_cmagnet_dimensions[1]
        total_magnets = int(model_hyper_parameters.periods*model_hyper_parameters.magnets_per_period_comp + 1)
        magnets_per_period = model_hyper_parameters.magnets_per_period_comp 
        Mova = model_hyper_parameters.Mova_comp

        
        #def appleArray(model_hyper_parameters, loc_offset, halbach_direction = -1):
        self.cont = wrd.wradObjCnt([])
        
        loc_offset = [0,0,0]
        
        #define the location offset in S of the magnet
        loc_offset[1] = -((total_magnets-1)/2.0) * (magnet_length + model_hyper_parameters.shim)+magnet_length/2.0-model_hyper_parameters.nominal_fmagnet_dimensions[1]/2
        
        
        #functionally efined offset in x and z based on s. Function can be passed in.
        loc_offset[0:3:2] = model_hyper_parameters.perturbation_fn(loc_offset[1])
        
        M = []
        mat = []
        for i in range(magnets_per_period):
            #M.append([halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M*np.sin(2*np.pi*model_hyper_parameters.Mova/360.0),halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M * np.cos(2*np.pi*model_hyper_parameters.Mova/360.0), np.cos(i*np.pi/2.0)*model_hyper_parameters.M])
            M.append([np.cos(i*2*np.pi/magnets_per_period)*model_hyper_parameters.M*np.sin(2*np.pi*Mova/360.0),-1 * np.sin(i*2*np.pi/magnets_per_period)*model_hyper_parameters.M, np.cos(i*2*np.pi/magnets_per_period)*model_hyper_parameters.M * np.cos(2*np.pi*Mova/360.0)])
            
            mat.append(wrdm.wradMatLin(model_hyper_parameters.ksi,M[i]))
        
        for x in range(-int((total_magnets-1)/2),int(1+(total_magnets-1)/2)-1):#0,model_hyper_parameters.appleMagnets
            
            mag = magnet(model_hyper_parameters, loc_offset,mat[(x)%magnets_per_period]) 
            loc_offset[1] += magnet_length + model_hyper_parameters.shim
            loc_offset[0:3:2] = model_hyper_parameters.perturbation_fn(loc_offset[1])
            self.cont.wradObjAddToCnt([mag.cont])
            
        #return a
        
    #mag = appleMagnet(AII,4,materiald,[z,y,x])
    #mag apply magnetisation and colour
    #add to container

class Halbach2Array():
    '''
    classdocs
    Hybrid array
    '''


    def __init__(self, model_hyper_parameters = parameters.model_parameters(), magnet = ms.appleMagnet, array_number = 1):
        '''
        Constructor
        '''
        
        per_length = model_hyper_parameters.periodlength
        model_hyper_parameters.nominal_fmagnet_dimensions[1] = model_hyper_parameters.magnet_length
        model_hyper_parameters.nominal_pole_dimensions[1] = model_hyper_parameters.pole_length
        
        #assign magnet quantities
        magnet_length = model_hyper_parameters.nominal_fmagnet_dimensions[1]
        total_magnets = model_hyper_parameters.totalmagnets - 1
        magnets_per_period = model_hyper_parameters.magnets_per_period
        Mova = model_hyper_parameters.Mova
            
            
        pole_length = model_hyper_parameters.nominal_pole_dimensions[1]
        total_poles = model_hyper_parameters.totalmagnets
        poles_per_period = model_hyper_parameters.magnets_per_period

        
        #def appleArray(model_hyper_parameters, loc_offset, halbach_direction = -1):
        self.cont = wrd.wradObjCnt([])
        
        loc_offset = [0,0,0]
        
        #define the location offset in S of the magnet
        loc_offset[1] = -((magnet_length+pole_length)/2 +
                          (magnet_length+pole_length+model_hyper_parameters.shim)*(total_magnets-2)/2)
        
        
        #functionally defined offset in x and z based on s. Function can be passed in.
        loc_offset[0:3:2] = model_hyper_parameters.perturbation_fn(loc_offset[1])
        
        M = []
        mat = []
        for i in range(magnets_per_period):
            #M.append([halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M*np.sin(2*np.pi*model_hyper_parameters.Mova/360.0),halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M * np.cos(2*np.pi*model_hyper_parameters.Mova/360.0), np.cos(i*np.pi/2.0)*model_hyper_parameters.M])
            M.append([0,
                      np.cos(i*2*np.pi/magnets_per_period)*model_hyper_parameters.M, 
                      0])
            
            mat.append(wrdm.wradMatLin(model_hyper_parameters.ksi,M[i]))
        
        for x in range(total_magnets):#0,model_hyper_parameters.appleMagnets
            
            mag = magnet(model_hyper_parameters, loc_offset,mat[(x)%magnets_per_period]) 
            loc_offset[1] += magnet_length + model_hyper_parameters.shim + pole_length
            loc_offset[0:3:2] = model_hyper_parameters.perturbation_fn(loc_offset[1])
            self.cont.wradObjAddToCnt([mag.cont])
            
        loc_offset[1] = -((magnet_length+pole_length) +
                          (magnet_length+pole_length+model_hyper_parameters.shim)*(total_magnets-2)/2 +
                          model_hyper_parameters.shim)
        
        polmat = wrdm.wradMatLin(model_hyper_parameters.ksi,[0.1,0,0])
        
        for x in range(total_poles):
            
            
            
            pol = magnet(model_hyper_parameters, loc_offset,polmat,magnet_thickness = pole_length)
            loc_offset[1] += magnet_length + model_hyper_parameters.shim + pole_length
            loc_offset[0:3:2] = model_hyper_parameters.perturbation_fn(loc_offset[1])
            self.cont.wradObjAddToCnt([pol.cont])  
                
    
class MagnetRow():
    def __init__(self,name = 'default_name', Body = HalbachArray(), Termination = HalbachTermination_APPLE(),beam = 0, quadrant = 0, row = 0):
        self.cont = wrd.wradObjCnt([])
        self.cont.wradObjAddToCnt([Body.cont, Termination.cont])
        self.beam = beam
        self.quadrant = quadrant
        self.row = row
        self.name = name

    
if __name__ == '__main__':
    mymodelparams = parameters.model_parameters(periodlength = 51.3, magnets_per_period = 4, periods = 1)
    
    a = HalbachArray(mymodelparams)
    b = HalbachTermination_APPLE(mymodelparams)
    
    c = MagnetRow(a,b)
    
    d = HalbachTermination_APPLE_HZB(mymodelparams)
    
    a.cont.wradSolve(0.001, 1000)
    
    print('{}{}'.format(a.cont.radobj,b))
#    rd.ObjDrwOpenGL(a.cont.radobj)
    rd.ObjDrwOpenGL(b.cont.radobj)
    rd.ObjDrwOpenGL(c.cont.radobj)
    rd.ObjDrwOpenGL(d.cont.radobj)
    
    
    
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