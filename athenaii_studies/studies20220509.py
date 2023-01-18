'''
Created on 14 Jul 2021

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
from datetime import datetime

from wradia import wrad_obj as wrd
from apple2p5 import model2 as id
from idcomponents import magnet_shapes as ms
from idcomponents import parameters
from idanalysis import analysis_functions as af
from ipywidgets.widgets.interaction import fixed
from wradia.wrad_obj import wradObjCnt

if __name__ == '__main__':
        ### developing Case Solution ###
    lam_u = 15
    
    test_hyper_params = parameters.model_parameters(Mova = 45, 
                                             periods = 4, 
                                             periodlength = lam_u,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,15.0],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 0,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 6,
                                             gap = 0.5, 
                                             rowshift = 0,#lam_u*21.55/64.0,
                                             shiftmode = 'circular',
                                             block_subdivision = [1,1,1]
                                             )
    #a = id.compensatedAPPLEv2(test_hyper_params)
    #a = id.plainAPPLE(test_hyper_params, fmagnet=ms.appleMagnetFELr4)
    a = id.plainAPPLE(test_hyper_params, fmagnet=ms.appleMagnetvarProfile)
    #a = id.plainAPPLE(test_hyper_params, fmagnet=ms.appleMagnet)
#    

        #add stayclear
    stayclear = rd.ObjCylMag([0,0,0],2,150,24,'y')
    stayclearcnt = rd.ObjCnt([stayclear])
    rd.ObjDrwAtr(stayclearcnt,[1,0,0],1)
    rd.ObjDrwOpenGL(stayclearcnt)
    
    case1 = af.CaseSolution(a)
    case1.calculate_B_field()
    #case1.calculate_force_per_magnet()
    rd.ObjDrwOpenGL(a.cont.radobj, 'Axes->False')
    
    rd.ObjAddToCnt(stayclearcnt,[a.cont.radobj])
    rd.ObjDrwOpenGL(stayclearcnt)


    print(case1.bmax)
    print(1)
    
    
    ### Developing Model Solution ### Range of gap. rowshift and shiftmode ###
    gaprange = np.array([2.2,5,10,30])
    shiftrange = np.arange(0,7.51, 7.5)
    shiftmoderange = ['linear']
    
    #scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    sol1 = af.Solution(test_hyper_params, scan_parameters,property = ['B'])
    sol1.solve(property = ['B'])
    
    timestamp = datetime.now()
    rootname = 'dev_{}'.format(timestamp.strftime("%Y%m%d_%H%M%S"))
    
    print('files with root {} are bing saved'.format(timestamp.strftime("%Y%m%d_%H%M%S")))
    
    with open('M:\Work\Athena_APPLEIII\Python\Results\\{}.dat'.format(rootname),'wb') as fp:
        pickle.dump(sol1,fp,protocol=pickle.HIGHEST_PROTOCOL)
    
    with open('M:\Work\Athena_APPLEIII\Python\Results\\{}.dat'.format(rootname),'rb') as fp:
        sol1 = pickle.load(fp)
    
    
    
    sol1.save('M:\Work\Athena_APPLEIII\Python\Results\\{}.h5'.format(rootname))
    
    print('end')