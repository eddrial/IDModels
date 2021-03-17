'''
Created on 17 Feb 2021

@author: oqb

'''

#creation of indivudual compensated APPLE, quick case solution
#also a hyperparamaterspace search and solution
#parallel axes plotting at the very end, which is broken
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
        ### developing Case Solution ###
    
    test_hyper_params = parameters.model_parameters(Mova = 20, 
                                             periods = 3, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 6,
                                             gap = 2, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [2,3,1]
                                             )
    a = id.compensatedAPPLEv2(test_hyper_params)
#    
    case1 = af.CaseSolution(a)
    case1.calculate_B_field()
    case1.calculate_force_per_magnet()
    print(case1.bmax)
    print(1)
    
    
    ### Developing Model Solution ### Range of gap. rowshift and shiftmode ###
    gaprange = np.arange(2,10.1,40)
    shiftrange = np.arange(-7.5,7.51, 1.875)
    shiftmoderange = ['circular']
    
    #scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange)
    
    sol1 = af.Solution(test_hyper_params, scan_parameters,property = ['B','Forces'])
    sol1.solve(property = ['B','Forces'])
    
    
    rootname = 'mag_forces_4per210226'
    
    with open('M:\Work\Athena_APPLEIII\Python\Results\\{}.dat'.format(rootname),'wb') as fp:
        pickle.dump(sol1,fp,protocol=pickle.HIGHEST_PROTOCOL)
    
    with open('M:\Work\Athena_APPLEIII\Python\Results\\{}.dat'.format(rootname),'rb') as fp:
        sol1 = pickle.load(fp)
    
    
    
    sol1.save('M:\Work\Athena_APPLEIII\Python\Results\\{}.h5'.format(rootname))
    
    print('end')