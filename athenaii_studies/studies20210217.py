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
        ### developing Case Solution ###
    
    test_hyper_params = parameters.model_parameters(Mova = 20, 
                                             periods = 1, 
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
                                             block_subdivision = [1,1,1]
                                             )
    a = id.compensatedAPPLEv2(test_hyper_params)
#    
    case1 = af.CaseSolution(a)
    case1.calculate_B_field()
    print(case1.bmax)
    print(1)
#    case1.calculate_force_per_beam()
#    case1.calculate_force_per_quadrant()
#    case1.calculate_force_per_row()
    
#    case1.case_save(False, 'Single_Case', fname = 'M:\Work\Athena_APPLEIII\Python\Results\\casedev210210.h5')
#    
    #draw object
#    rd.ObjDrwOpenGL(a.cont.radobj)
    
#    plt.plot(case1.bfield[:,0],case1.bfield[:,1:4])
#    plt.legend(['bx','by','bz'])
    
    #show it
#    plt.show()
    
    ### Developing Model Solution ### Range of gap. rowshift and shiftmode ###
    gaprange = np.arange(2,10.1,40)
    shiftrange = np.arange(-7.5,7.51, 3.75)
    shiftmoderange = ['linear','circular']
    
    #scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange)
    
#    sol1 = Solution(test_hyper_params, scan_parameters)
#    sol1.solve()
#    sol1.save(hf = None, solstring = 'Sol1', fname = 'M:\Work\Athena_APPLEIII\Python\Results\\Solution.h5')
    
    ### Developing model Hypersolution
    
    #test_hyper_params is a params object
    #solution_parameters is a list of two iterators and a list
    
    #create test hyper params as dict
    test_hyper_params_dict = {'Mova': 20,
                              'periods' : 5,
                              'periodlength' : 15,
                              'nominal_fmagnet_dimensions' : [15.0,0.0,15.0], #obsoleted by 'square_magnet'
                              'nominal_cmagnet_dimensions' : [7.5,0.0,15.0], #obsoleted by 'square_magnet'
                              'nominal_vcmagnet_dimensions' : [7.5,0.0,15.0], #obsoleted by 'square_magnet'
                              'nominal_hcmagnet_dimensions' : [7.5,0.0,15.0], #obsoleted by 'square_magnet'
                              'compappleseparation' : 7.5,
                              'apple_clampcut' : 3.0,
                              'comp_magnet_chamfer' : [3.0,0.0,3.0],
                              'magnets_per_period' :6,
                              'gap' : 2, 
                              'rowshift' : 4,
                              'shiftmode' : 'circular',
                              #'square_magnet' : 15.0,
                              #'block_subdivision' : [1,1,1]
                              }
    
    #hypersolution_variables a dict of ranges. Can only be ranges of existing parameters in test_hyper_params
    hyper_solution_variables = {
        #"block_subdivision" : [np.array([2]),np.arange(2,4),np.arange(3,4)],
        #"Mova" : np.arange(15,25.1,5),
        #"nominal_vcmagnet_dimensions": [np.arange(7.5,8,10),np.arange(0.0,1.0,10.0),np.arange(10,25.1,2.5)],
        #"nominal_hcmagnet_dimensions": [np.arange(7.5,8.1,2),np.arange(0.0,1.0,10.0),np.arange(10,15.1,1)],
        #"square_magnet" : np.arange(10,20.1,5),
        #"rowtorowgap" : np.arange(0.4,0.51,0.1),
        "magnets_per_period" : np.arange(4,11,2)
        }
    
    hyper_solution_properties = ['B']
    
    #create hypersolution object
    hypersol1 = af.HyperSolution(base_hyper_parameters = test_hyper_params_dict, 
                              hyper_solution_variables = hyper_solution_variables, 
                              hyper_solution_properties = hyper_solution_properties,
                              scan_parameters = scan_parameters,
                              method = 'systematic',
                              iterations = 60)
    
#    hypersol1.solve()
    
    rootname = 'nper210216'
    
#    with open('M:\Work\Athena_APPLEIII\Python\Results\\{}.dat'.format(rootname),'wb') as fp:
#        pickle.dump(hypersol1,fp,protocol=pickle.HIGHEST_PROTOCOL)
    
    with open('M:\Work\Athena_APPLEIII\Python\Results\\{}.dat'.format(rootname),'rb') as fp:
        hypersol1 = pickle.load(fp)
    
    hypersol1.save('M:\Work\Athena_APPLEIII\Python\Results\\{}.h5'.format(rootname))
    
    mynumpyarray = np.zeros([len(hypersol1.hyper_results),2])
    
    for i in range(len(hypersol1.hyper_results)):
        mynumpyarray[i] = [hypersol1.hyper_inputs[i].square_magnet,
                           hypersol1.hyper_results[i]['Bmax'][0,0,0,0]]
        
    plt.plot(mynumpyarray[:,0],mynumpyarray[:,1])
    
    mynumpyarray = np.zeros([60,4])
    
    for i in range(60):
        mynumpyarray[i] = [hypersol1.hyper_inputs[i].block_subdivision[0],
                           hypersol1.hyper_inputs[i].block_subdivision[1],
                           hypersol1.hyper_inputs[i].block_subdivision[2],
                           hypersol1.hyper_results[i]['Bmax'][0,0,0,2]]
        
    eddf = pd.DataFrame(data = mynumpyarray, index = range(60), columns = ['Slice X', 'Slice Y', 'Slice Z', 'Bmax'])

    fig = px.parallel_coordinates(eddf, color="Bmax", labels={"Bmax": "Bmax",
            "Slice X": "Slice X", "Slice Y": "Slice Y",
            "Slice Z": "Slice Z", },
                         color_continuous_scale=px.colors.diverging.Tealrose,
                         color_continuous_midpoint=1.58)
        
    fig.show()
        
    
    print(1)