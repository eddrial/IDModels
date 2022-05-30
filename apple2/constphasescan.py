'''
Created on 4 Jan 2022

@author: oqb
'''
import numpy as np
from wradia import wrad_obj as wrd
from apple2p5 import model2 as id
from idcomponents import parameters
from idanalysis import analysis_functions as af
from idanalysis.analysis_functions import Solution
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation,  CubicTriInterpolator
from shapely.geometry import LineString, point
import time

if __name__ == '__main__':
    #define parameter space
    gaps = np.array([15,17,20,25,30,40,50])
    shifts = np.arange(-24,25,4)
    shiftmodes = ['circular', 'linear']
    #set up APPLE 2 device (UE48)
    #solve peakfield in parameter space
    print (gaps)
    print(shifts)
    
    min_gap = 13
    
    #parameter_Set Horizontal_polarisation
    UE48_params = parameters.model_parameters(Mova = 0,
                                        periods = 5, 
                                        periodlength =48,
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
                                        rowshift = 0,
                                        shiftmode = 'circular',
                                        block_subdivision = [2,3,1],
                                        M = 1.3                                        
                                        )
    
    basescan = parameters.scan_parameters(48.0,gaprange = gaps,shiftrange = shifts, shiftmoderange = shiftmodes)
    
    UE48 = id.plainAPPLE(UE48_params)
    
    UE48.cont.wradSolve()
    
    case = af.CaseSolution(UE48)
    case.calculate_B_field()
    
    print ("Peak Field for ID {} is {}".format('UE48', np.max(case.bmax)))
    print('placeholder')
    
    sol = Solution(UE48_params,basescan,property = ['B'])
    
    #sol.solve('B')
    
    #babs = np.linalg.norm(sol.results['Bmax'], axis = 3)
    #np.save('C:/Users/oqb/git/IDModels/apple2/babs_demo.npy',babs)
    
    #bphi = np.sign(shifts[:]) * (180 / np.pi) * np.arctan(sol.results['Bmax'][:,:,:,0]/sol.results['Bmax'][:,:,:,2])
    #np.save('C:/Users/oqb/git/IDModels/apple2/bphi_demo.npy',bphi)
    
    #or load
    bphi=np.load('C:/Users/oqb/git/IDModels/apple2/bphi_demo.npy')
    babs=np.load('C:/Users/oqb/git/IDModels/apple2/babs_demo.npy')
    
    
    K = 0.0934 * 48 * babs

    lamb = 48/(2*3400*3400)*(1 + (K*K/2)/2) 
    
    E = 6.64e-34 * 3e8/(1e-3 * lamb*1.6e-19)

    X,Y =  np.meshgrid(shifts,gaps)
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    
    ax.plot_surface(X,Y,babs[0])
    
    fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
    
    ax1.plot_surface(X,Y,bphi[0])
    
    fig11, ax11 = plt.subplots(subplot_kw={"projection": "3d"})
    
    ax11.plot_surface(X,Y,E[0])
    
    
    #creating triangular grid, and interpolating (shift, gap)
    #grid creation
    triObj = Triangulation(X.flatten(),Y.flatten())
    
    #cubic interpolation of abs B
    babs_fzc = CubicTriInterpolator(triObj,babs[0].flatten())
    
    #cubic interpolation of E
    E_fzc = CubicTriInterpolator(triObj,E[0].flatten())
    
    #cubic interpolation of phi
    bphi_fzc = CubicTriInterpolator(triObj,bphi[0].flatten())
    
    #export 100 random values
    
    rands = np.zeros([1000,4])
    for i in range(1000):
        gaprand = 15 + 35* np.random.random()
        shiftrand = -24 + 48 * np.random.random()
        rands[i] = [gaprand, shiftrand, E_fzc(shiftrand,gaprand),bphi_fzc(shiftrand,gaprand)]
    
    #plot rands
    figrand, axrand = plt.subplots()
    
    axrand.tricontour(rands[:,1],rands[:,0],rands[:,2])
    axrand.tricontour(rands[:,1],rands[:,0],rands[:,3])
    
    
    #plot on plane
    fig2, ax2 = plt.subplots()
    
    t0 = time.time()
    
    ax2.tricontour(X.flatten(),Y.flatten(),bphi[0].flatten(), [30])
    ax2.tricontour(X.flatten(),Y.flatten(),E[0].flatten(), [400])

    #ax2.tricontour(X.flatten(),Y.flatten(),bphi[0].flatten())
    #ax2.tricontour(X.flatten(),Y.flatten(),babs[0].flatten())
    
    if ax2.collections[0].get_paths().__len__() >= 1:
        bphi_contour = ax2.collections[0]._paths[0].vertices
        l1 = LineString(bphi_contour)
    
    if ax2.collections[1].get_paths().__len__() >= 1:
        E_contour = ax2.collections[1]._paths[0].vertices
        l2 = LineString(E_contour)
        
    if 'l1' in globals() and 'l2' in globals():
        p = l1.intersection(l2)
    
        if isinstance(p,point.Point):
            ax2.plot(p.coords.xy[0],p.coords.xy[1],'ro')
    t1 = time.time()
    print(t1-t0)
    plt.show()
    print(1)
    