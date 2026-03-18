'''
Created on Jul 2, 2025

@author: oqb
'''
#imports
import numpy as np


from idanalysis import analysis_functions as af
from idcomponents import parameters
import datetime as dt

if __name__ == '__main__':
    #folder/filename
    my_path = 'E:\Sim_Outputs\CUE\Test'
    
    timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    rootname = 'hypersoln_{}'.format(timestamp)
    
    ### Developing Model Solution 
    
    #Base Hyperparameters
    base_hyper_params = parameters.model_parameters(#type = 'Anti-symmetrically Compensated APPLE',
                                                    type = 'Symmetrically Compensated APPLE',
                                                    #type = 'Plain_APPLE',
                                            Mova = 0, 
                                             periods = 4, 
                                             periodlength = 17,
                                             nominal_fmagnet_dimensions = [15,0.0,15], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,15.0],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut_non_symmetric = [3.0, 0.0, 3.0],
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             rowtorowgap = 1.0,
                                             gap = 5.0, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [1,1,1]
                                             )
    
    base_hyper_params_dict = {'type': 'Symmetrically Compensated APPLE',
                              'Mova': 20,
                              'Mova_comp' : 0,
                              'periods' : 4,
                              'periodlength' : 17,
                              'nominal_fmagnet_dimensions' : [15.0,0.0,15.0], #obsoleted by 'square_magnet'
                              'nominal_cmagnet_dimensions' : [7.5,0.0,15.0], #obsoleted by 'square_magnet'
                              'nominal_vcmagnet_dimensions' : [7.5,0.0,15.0], #obsoleted by 'square_magnet'
                              'nominal_hcmagnet_dimensions' : [7.5,0.0,15.0], #obsoleted by 'square_magnet'
                              'compappleseparation' : 7.5,
                              'apple_clampcut' : 3.0,
                              'comp_magnet_chamfer' : [3.0,0.0,3.0],
                              'magnets_per_period' :4,
                              'magnets_per_period_comp' : 2,
                              'gap' : 5, 
                              'rowshift' : 4,
                              'shiftmode' : 'circular',
                              'shim' : 0.25,
                              'square_magnet' : 15.0,
                              'block_subdivision' : [1,1,1]
                              }
    
    
    ### Range of gap. rowshift and shiftmode ###
    gaprange = np.arange(5.0, 7.1, 10.0)
    shiftrange = np.arange(0,8.6, 2.125)
    shiftmoderange = ['circular']
    
    scan_parameters = parameters.scan_parameters(periodlength = base_hyper_params_dict['periodlength'], gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    #define hyper_parameters to be varied
    
    hyper_solution_variables = {
        #"block_subdivision" : [np.array([2]),np.arange(2,4),np.arange(3,4)],
        #"Mova" : np.arange(15,25.1,5),
        "nominal_vcmagnet_dimensions": [np.arange(7.5,8.1,5),np.arange(0.0,1.0,10.0),np.arange(10.1,40.1,45.0)],
        "nominal_hcmagnet_dimensions": [np.arange(7.5,8.1,5),np.arange(0.0,1.0,10.0),np.arange(10,20.1,5.0)]
        #"square_magnet" : np.arange(10,20.1,2.5),
        #"magnets_per_period" : np.arange(4,8,2)
        }
    
    
    
    force_scan = af.HyperSolution(base_hyper_params_dict, hyper_solution_variables,scan_parameters, ['B','Forces'], 'systematic')
    
    force_scan.solve()
    
    force_scan.save('{}\{}.h5'.format(my_path, rootname))
    
    print('end')