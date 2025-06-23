'''
Created on 22 Aug 2023

@author: oqb

'''
#12.05.25 This is a hyperparameter scan of
#lambda u - 15mm, 17mm
#functional cross section - 15mm, 20mm
#M 1.32, 1.64

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
    cross_sec = 15
    for lam_u in [15,17]:
        for phi in [20]:
            for M in [1.62]:
                rd.UtiDelAll()
                
                
                test_hyper_params = parameters.model_parameters(#type = 'Anti-symmetrically Compensated APPLE',
                                                                #type = 'Symmetrically Compensated APPLE',
                                                                type = 'Plain_APPLE',
                                                         Mova = phi, 
                                                         M = M,
                                                         periodlength = lam_u,
            
                                                         periods = 5, 
                                                         #periodlength = 15,
                                                         nominal_fmagnet_dimensions = [cross_sec,0.0, cross_sec], 
                                                         #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                                         nominal_vcmagnet_dimensions = [cross_sec/2,0.0,cross_sec],
                                                         nominal_hcmagnet_dimensions = [cross_sec/2,0.0,cross_sec], 
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
                #case1.calculate_force_per_magnet()
                print(case1.bmax)
                print(1)
                
                
                ### Developing Model Solution ### Range of gap. rowshift and shiftmode ###
                gaprange = np.arange(5.0, 5.1, 0.5)
                shiftrange = np.arange(-lam_u/2,0.1+lam_u/2, lam_u/16)
                shiftmoderange = ['circular', 'linear']
                
                #scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
                scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
                
                sol1 = af.Solution(test_hyper_params, scan_parameters,property = ['B', 'Forces'])
                sol1.solve(property = ['B', 'Forces'])
                
                my_path = 'D:\Work - Laptop\CryoAPPLE\Results'
                rootname = 'cryoAPPLE_M_{}_cs_{}_lam_{}_tilt_{}_20250524'.format(M, cross_sec, lam_u, phi)
                
            #    with open('{}\{}.dat'.format(my_path, rootname),'wb') as fp:
            #        pickle.dump(sol1,fp,protocol=pickle.HIGHEST_PROTOCOL)
                
            #    with open('{}\{}.dat'.format(my_path,rootname),'rb') as fp:
            #        sol1 = pickle.load(fp)
                
                
                
                sol1.save('{}\{}.h5'.format(my_path, rootname))
                
    print('end')