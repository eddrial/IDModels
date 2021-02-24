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
                                             periodlength = 65,
                                             nominal_fmagnet_dimensions = [30.0,0.0,30.0],
                                             M = 1.3, 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 15,
                                             apple_clampcut = 5.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 10, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             rowtorowgap = 1.0,
                                             )
    id_10eV = id.compensatedAPPLEv2(test_hyper_params)
#    
    case1 = af.CaseSolution(id_10eV)
    case1.calculate_B_field()
    print(case1.bmax)
    rd.ObjDrwOpenGL(id_10eV.cont.radobj)
    plt.plot(case1.bfield[:,0],case1.bfield[:,1],case1.bfield[:,3])
    plt.show()
    print(1)
