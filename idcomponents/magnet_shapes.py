'''
Created on 24 Sep 2020

@author: oqb
'''

from wradia import wrad_obj as wrd
import radia as rd
import numpy as np
import matplotlib.pyplot as plt

from idcomponents import parameters

class appleMagnet():
    '''
    classdocs
    '''
    def __init__(self, model_parameters = parameters.model_parameters(), magnet_centre  = [0,0,0], this_magnet_material = 0):
        
        '''
        Constructor
        '''
        
        mp = model_parameters
        self.magnet_centre = magnet_centre
        
        if this_magnet_material == 0:
            this_magnet_material = mp.magnet_material
        
        '''orientation order z,y,x'''
        self.cont = wrd.wradObjCnt([])  # Container
    #    a.magnet_material = magnet_material
        p1 = wrd.wradObjThckPgn(magnet_centre[1], mp.nominal_fmagnet_dimensions[1], [[magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2 + mp.apple_clampcut,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2 + mp.apple_clampcut,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2 - mp.apple_clampcut,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2 - mp.apple_clampcut,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2]], 
                                                                  mp.direction)
        p2 = wrd.wradObjThckPgn(magnet_centre[1], mp.nominal_fmagnet_dimensions[1], [[magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2 - mp.apple_clampcut],
                                                                  [magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2 + mp.apple_clampcut,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2 - mp.apple_clampcut],
                                                                  [magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2 + mp.apple_clampcut,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2]], 
                                                                  mp.direction)
        p3 = wrd.wradObjThckPgn(magnet_centre[1], mp.nominal_fmagnet_dimensions[1], [[magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2 + mp.apple_clampcut],
                                                                  [magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2 - mp.apple_clampcut,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2 - mp.apple_clampcut,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2 + mp.apple_clampcut]], 
                                                                  mp.direction)
        
        self.cont.wradObjAddToCnt([p1,p2,p3])
        self.cont.wradMatAppl(this_magnet_material)
        
class compMagnet():
    '''
    classdocs
    '''
    def __init__(self, model_parameters = parameters.model_parameters(), magnet_centre  = [0,0,0], this_magnet_material = 0):
                
        '''
        Constructor
        '''
        
        mp = model_parameters
        self.magnet_centre = magnet_centre
        if this_magnet_material == 0:
            this_magnet_material = mp.magnet_material
        '''orientation order z,y,x'''
        self.cont = wrd.wradObjCnt([])
        
        p1 = wrd.wradObjThckPgn(magnet_centre[1], model_parameters.nominal_cmagnet_dimensions[1], [[magnet_centre[0]-model_parameters.nominal_cmagnet_dimensions[0]/2.0,magnet_centre[2]-model_parameters.nominal_cmagnet_dimensions[2]/2.0],
                                                                  [magnet_centre[0]-model_parameters.nominal_cmagnet_dimensions[0]/2.0,magnet_centre[2]+model_parameters.nominal_cmagnet_dimensions[2]/2.0],
                                                                  [magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2.0 - model_parameters.comp_magnet_chamfer[0],magnet_centre[2]+model_parameters.nominal_cmagnet_dimensions[2]/2.0],
                                                                  [magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2.0 - model_parameters.comp_magnet_chamfer[0],magnet_centre[2]-model_parameters.nominal_cmagnet_dimensions[2]/2.0]], 
                                                                  model_parameters.direction)
        p2 = wrd.wradObjThckPgn(magnet_centre[1], model_parameters.nominal_cmagnet_dimensions[1], [[magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2,magnet_centre[2]-model_parameters.nominal_cmagnet_dimensions[2]/2 + model_parameters.comp_magnet_chamfer[2]/2.0],
                                                                  [magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2,magnet_centre[2]+model_parameters.nominal_cmagnet_dimensions[2]/2.0 - model_parameters.comp_magnet_chamfer[2]/2.0],
                                                                  [magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2.0 - model_parameters.comp_magnet_chamfer[0],magnet_centre[2]+model_parameters.nominal_cmagnet_dimensions[2]/2 - model_parameters.comp_magnet_chamfer[2]/2.0],
                                                                  [magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2.0 - model_parameters.comp_magnet_chamfer[0],magnet_centre[2]-model_parameters.nominal_cmagnet_dimensions[2]/2 + model_parameters.comp_magnet_chamfer[2]/2.0]], 
                                                                  model_parameters.direction)
        
        self.cont.wradObjAddToCnt([p1,p2])
        self.cont.wradMatAppl(this_magnet_material)
        
        
if __name__ == '__main__':
    a = appleMagnet()
    b = compMagnet()
    
    a.cont.wradSolve(.001, 1000)
    
    z = 20; x1 = -15; x2 = 0; ymax = 400; nump = 2001
    
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
    
    plt.show()
    
    print('{}{}'.format(a.cont.radobj,b.cont.radobj))
    
        