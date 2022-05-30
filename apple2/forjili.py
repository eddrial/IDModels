'''
Created on 13 May 2022

@author: oqb

A one period of an APPLE Undulator for Ji Li for a paper
'''

import numpy as np
from wradia import wrad_obj as wrd
from apple2p5 import model2 as id
from idcomponents import parameters
from idanalysis import analysis_functions as af
from idanalysis.analysis_functions import Solution
import matplotlib.pyplot as plt
import radia as rd
from matplotlib import cm
import json

if __name__ == '__main__':
    gaps = np.array([25])#,17,20,25,30,40,50])
    shifts = np.arange(-33,0,49)
    shiftmodes = ['circular']#, 'linear']
    #set up APPLE 2 device (UE48)
    #solve peakfield in parameter space
    print (gaps)
    print(shifts)
    
    min_gap = 25
    
    #parameter_Set Horizontal_polarisation
    UE100_params = parameters.model_parameters(Mova = 0,
                                        periods = 5, 
                                        periodlength =100,
                                        nominal_fmagnet_dimensions = [40.0,0.0,40.0], 
                                        #square_magnet = True,
                                        nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                        #nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                        #nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                        compappleseparation = 75,
                                        apple_clampcut = 5.0,
                                        comp_magnet_chamfer = [3.0,0.0,3.0],
                                        magnets_per_period = 4,
                                        gap = min_gap, 
                                        rowshift = 30,
                                        shiftmode = 'circular',
                                        block_subdivision = [5,5,5],
                                        M = 1.3                                        
                                        )
    
    basescan = parameters.scan_parameters(100.0,gaprange = gaps,shiftrange = shifts, shiftmoderange = shiftmodes)
    
    UE100 = id.plainAPPLE(UE100_params)
    
    UE100.cont.wradSolve()
    
    case = af.CaseSolution(UE100)
    case.calculate_B_field()
    
    print ("Peak Field for ID {} is {}".format('UE48', np.max(case.bmax)))
    print('placeholder')
    
    Barray= np.zeros([101,101,25,3])
    pos= np.zeros([101,101,25,3])
    
    xrange = np.arange(-50,51)
    srange = np.arange(-50,51)
    zrange = np.arange(-12,13)
    
    for x in range(101):
        for s in range(101):
            for z in range(25):
                pos[x,s,z] = [xrange[x],srange[s],zrange[z]]
                Barray[x,s,z] = rd.Fld(UE100.cont.radobj,'bxbybz',[list(pos[x,s,z])])
                
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    Xx,Ss = np.meshgrid(xrange,srange)
    surf = ax.plot_surface(Xx, Ss, Barray[:,:,13,2], cmap=cm.coolwarm, linewidth=0, antialiased=False)

    with open('M:\\Work\\JiliAPPLE\\Bfield_x_s_z_Bxsz_fine_25mm.json','w') as fp:
        json.dump(Barray.tolist(),fp)
        
    #with open('M:\\Work\\JiliAPPLE\\Location_x_s_z.json','w') as fp:
    #    json.dump(pos.tolist(),fp)
    
    sol = Solution(UE100_params,basescan,property = ['B'])
    
    sol.solve('B')
    
    babs = np.linalg.norm(sol.results['Bmax'], axis = 3)
    #np.save('C:/Users/oqb/git/IDModels/apple2/babs_demo.npy',babs)
    
    #bphi = np.sign(shifts[:]) * (180 / np.pi) * np.arctan(sol.results['Bmax'][:,:,:,0]/sol.results['Bmax'][:,:,:,2])
    #np.save('C:/Users/oqb/git/IDModels/apple2/bphi_demo.npy',bphi)