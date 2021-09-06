'''
Created on 17 Feb 2021

@author: oqb
'''

import numpy as np
import radia as rd
import h5py as h5
import random
import itertools
import copy
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tracemalloc
import time

from wradia import wrad_obj as wrd
from apple2p5 import model2 as id
from idcomponents import parameters
from idanalysis import analysis_functions as af
from ipywidgets.widgets.interaction import fixed
from wradia.wrad_obj import wradObjCnt

if __name__ == '__main__':
   
    test_hyper_params = parameters.model_parameters(Mova = 0, 
                                             periods = 8, 
                                             periodlength = 20,
                                             nominal_fmagnet_dimensions = [40.0,0.0,40.0],
                                             M = 1.32, 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 15,
                                             apple_clampcut = 5.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 4.1, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             rowtorowgap = 1.5,
                                             )
    
    test_hyper_params2 = parameters.model_parameters(Mova = 0, 
                                             periods = 8, 
                                             periodlength = 40,
                                             nominal_fmagnet_dimensions = [40.0,0.0,40.0],
                                             M = 1.15, 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 15,
                                             apple_clampcut = 5.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 15.0, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             rowtorowgap = 1.5,
                                             )
    id_10eV = id.plainAPPLE(test_hyper_params)
    
#    

    x = np.linspace(-30,30,41)
    case1 = af.CaseSolution(id_10eV)
    case1.calculate_B_field([[-50,0,0],[50,0,0]])
    print(case1.bmax)
    rd.ObjDrwOpenGL(id_10eV.cont.radobj)
    plt.plot(x,case1.bfield[:,3], label = 'H Mode: Peak Vertical Field (T)')
    plt.xlabel ("X (mm)")
    plt.ylabel ("Peak Field (T)")
    plt.title("Peak Field Variation across X")
    plt.xlim(-10,10)
    
    #plt.show()
    
    id2 = id.compensatedAPPLEv2(test_hyper_params2)
    case2= af.CaseSolution(id2)
    case2.calculate_B_field([[-30,0,0],[30,0,0]])
    print(case2.bmax)
    rd.ObjDrwOpenGL(id2.cont.radobj)
    plt.plot(x,-case2.bfield[:,1], label = 'V Mode: Peak Horizontal Field (T)')
    plt.legend()
    plt.show()
    print(1)
