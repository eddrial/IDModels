'''
Created on 22 Oct 2025

@author: oqb
'''

import numpy as np
from wradia import wrad_obj as wrd
import apple2p5.model2 as id1
from idcomponents import parameters
from idanalysis import analysis_functions as af
from idanalysis.analysis_functions import Solution
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation,  CubicTriInterpolator
from shapely.geometry import LineString, point
import time


if __name__ == '__main__':
    #define parameter space
    #gaps = np.array([15,17,20,25,30,40,50])
    gaps = np.arange(4,7.1,1)
    shifts = np.arange(0,20.1,2500/4)
    
    #shifts = np.arange(0,3,4)
    #shiftmodes = ['circular', 'linear']
    shiftmodes = ['linear']
    #set up APPLE 2 device (UE56)
    #solve peakfield in parameter space
    print (gaps)
    print(shifts)
    
    min_gap = 15
    
    #parameter_Set Horizontal_polarisation
    UE40_params = parameters.model_parameters(Mova = 0,
                                        periods = 5, 
                                        periodlength =40.0,
                                        nominal_fmagnet_dimensions = [30.0,0.0,30.0], 
                                        #square_magnet = True,
                                        nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                        #nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                        #nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                        compappleseparation = 75,
                                        apple_clampcut = 5.0,
                                        comp_magnet_chamfer = [3.0,0.0,3.0],
                                        magnets_per_period = 4,
                                        rowtorowgap = 1.2,
                                        gap = 4, 
                                        rowshift = 0,
                                        shiftmode = 'linear',
                                        block_subdivision = [2,3,1],
                                        M = 1.31,
                                        type = 'Plain_APPLE'                                        
                                        )
    
    basescan = parameters.scan_parameters(40,gaprange = gaps,shiftrange = shifts, shiftmoderange = shiftmodes)
    
    UE40 = id1.plainAPPLE(UE40_params)
    
    UE40.cont.wradSolve()
    
    case = af.CaseSolution(UE40)
    case.calculate_B_field()
    
    print ("Peak Field for ID {} is {}".format('UE51', np.max(case.bmax)))
    print('placeholder')
    
    sol = Solution(UE40_params,basescan,property = ['B'])
    
    sol.solve('B')
    
    print('pause')