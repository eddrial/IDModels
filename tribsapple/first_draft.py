'''
Created on 3 Jun 2026

@author: oqb
'''

from wradia import wrad_obj as wrd
from wradia import wrad_mat as wrdm
import radia as rd
import numpy as np
import matplotlib.pyplot as plt
from idcomponents import parameters
from idcomponents import magnet_shapes as ms
from idcomponents import halbach_arrays as ha
from apple2p5 import model2 as id
from idcomponents import parameters
from idanalysis import analysis_functions as af

import matplotlib.gridspec as gridspec
from wradia.wrad_obj import wradObjCnt
from plotly.validators.layout.geo import lonaxis

if __name__ == '__main__':
    test_hyper_params = parameters.model_parameters(Mova = 0, 
                                         periods = 8, 
                                         periodlength = 20,
                                         nominal_fmagnet_dimensions = [20.0,0.0,10.0],
                                         nominal_tmagnet_dimensions = [20.0,0.0,10.0],
                                         M = 1.32, 
                                         #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                         nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                         nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                         compappleseparation = 15,
                                         apple_clampcut = 2.0,
                                         comp_magnet_chamfer = [3.0,0.0,3.0],
                                         magnets_per_period = 4,
                                         gap = 6, 
                                         rowshift = 9,
                                         shiftmode = 'linear',
                                         rowtorowgap = 1.0,
                                         )
    
    #create device
    ta = id.tribsAPPLE(test_hyper_params)
    
    #draw device
    rd.ObjDrwOpenGL(ta.cont.radobj)
    
    case1 = af.CaseSolution(ta)
    
    #magnetic fields
    negax = np.array(rd.FldLst(ta.cont.radobj,'bxbybz',[-10.5,-150,0],[-10.5,150,0],1001, 'arg',-150))
    onax = np.array(rd.FldLst(ta.cont.radobj,'bxbybz',[0,-150,0],[0,150,0],1001, 'arg',-150))
    posax = np.array(rd.FldLst(ta.cont.radobj,'bxbybz',[10.5,-150,0],[10.5,150,0],1001, 'arg',-150))
    
    plt.plot(negax[:,0],negax[:,1])
    plt.plot(negax[:,0],negax[:,3])
    plt.plot(negax[:,0],posax[:,1])
    
    plt.show()
    

    
    print(negax)