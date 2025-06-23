'''
Created on 22 Aug 2023

@author: oqb

'''
#07.05.25 Need to create forces etc for CryoAPPLE, 15mm period. down to 3mm
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
from idcomponents import magnet_shapes as ms
from idanalysis import analysis_functions as af
from wradia.wrad_obj import wradObjCnt

if __name__ == '__main__':
        ### developing Case Solution ###
    
    test_hyper_params = parameters.model_parameters(#type = 'Anti-symmetrically Compensated APPLE',
                                                    type = 'Symmetrically Compensated APPLE',
                                                    #type = 'Plain_APPLE',
                                            Mova = 0, 
                                             periods = 4, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15,0.0,15], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,15.0],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut_non_symmetric = [3.0, 0.0, 3.0],
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             rowtorowgap = 1.0,
                                             gap = 3.0, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [2,2,1]
                                             )
    a = id.compensatedAPPLEv2_Sym(test_hyper_params, fmagnet=ms.appleMagnetNonSymmetric)
    
    #a = id.plainAPPLE(test_hyper_params, fmagnet=ms.appleMagnetNonSymmetric)#    


    rd.ObjDrwOpenGL(a.cont.radobj)
    case1 = af.CaseSolution(a)
    case1.calculate_B_field()
    case1.calculate_force_per_magnet()
    print(case1.bmax)
    print(1)
    
    
    ### Developing Model Solution ### Range of gap. rowshift and shiftmode ###
    gaprange = np.arange(3.0, 10.1, 1.0)
    shiftrange = np.arange(0,7.6, 0.5)
    shiftmoderange = ['circular', 'linear']
    
    #scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    sol1 = af.Solution(test_hyper_params, scan_parameters,property = ['B','Forces'])
    sol1.solve(property = ['B','Forces'])
    
    my_path = 'D:\Work - Laptop\CryoAPPLE\Results'
    rootname = 'ivue32_comp_hv_asym_221_20250507'
    
#    with open('{}\{}.dat'.format(my_path, rootname),'wb') as fp:
#        pickle.dump(sol1,fp,protocol=pickle.HIGHEST_PROTOCOL)
    
#    with open('{}\{}.dat'.format(my_path,rootname),'rb') as fp:
#        sol1 = pickle.load(fp)
    
    
    
    sol1.save('{}\{}.h5'.format(my_path, rootname))
    
    print('end')