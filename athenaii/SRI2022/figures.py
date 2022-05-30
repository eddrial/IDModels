'''
Created on 14 Mar 2022

@author: oqb

Code to generate figres for SRI2022 paper on Cr
'''
from matplotlib import pyplot as plt
from matplotlib import ticker as tk
import numpy as np
import pickle

from symfit import variables, sin, cos, Fit
from symfit import parameters as symparam
from wradia import wrad_obj as wrd
from apple2p5 import model2 as id
from idcomponents import parameters
from idanalysis import analysis_functions as af
from apple2p5.model2 import plainAPPLE


def fourier_series(x, f, n=0):
    """
    Returns a symbolic fourier series of order `n`.

    :param n: Order of the fourier series.
    :param x: Independent variable
    :param f: Frequency of the fourier series
    """
    # Make the parameter objects for all the terms
    a0, *cos_a = symparam(','.join(['a{}'.format(i) for i in range(0, n + 1)]))
    sin_b = symparam(','.join(['b{}'.format(i) for i in range(1, n + 1)]))
    # Construct the series
    series = a0 + sum(ai * cos(i * f * x) + bi * sin(i * f * x)
                     for i, (ai, bi) in enumerate(zip(cos_a, sin_b), start=1))
    return series

def figuresA(savepath):
    ''' Peak Bx/Bz with Gap for a nominal APPLEII structure, transverse profiles, longitudinal profiles'''
    #base parameters
    fig1params30x30 = parameters.model_parameters(M = 1.344,
                                             Mova = 0, 
                                             periods = 5, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [30.0,0.0,30.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 1, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [3,3,3],
                                             rowtorowgap = 0.5
                                             )
    
    fig1params15x15 = parameters.model_parameters(Mova = 0, 
                                             periods = 5, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 1, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [3,3,3],
                                             rowtorowgap = 0.5
                                             )
    
    fig1params15x15bow = parameters.model_parameters(Mova = 0, 
                                             periods = 5, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 1, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [3,3,3],
                                             rowtorowgap = 0.506
                                             )
    fig1paramsUE56 = parameters.model_parameters(M = 1.344,
                                             type = 'Plain_APPLE',
                                             Mova = 0, 
                                             periods = 3, 
                                             periodlength = 56,
                                             nominal_fmagnet_dimensions = [30.0,0.0,30.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 1, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [3,3,3],
                                             rowtorowgap = 0.5
                                             )
    #base scan range
    gaprange = np.arange(1.,6.01,1)
    gaprangeUE56 = np.array([2,4,6,13, 2.025, 13.025])
    bowgaprange = np.arange(2,3,5)
    shiftrange = np.arange(0,7.51, 7.5)
    shiftrangeUE56 = np.arange(0,28.1,28)
    #shiftmoderange = ['linear','circular']
    shiftmoderange = ['linear']
    
    scan_parameters = parameters.scan_parameters(periodlength = fig1params30x30.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    scan_parametersUE56 = parameters.scan_parameters(periodlength = fig1paramsUE56.periodlength, gaprange = gaprangeUE56, shiftrange = shiftrangeUE56, shiftmoderangeUE56 = shiftmoderange)
    scan_parametersbow = parameters.scan_parameters(periodlength = fig1params15x15bow.periodlength, gaprange = bowgaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    sol130x30 = af.Solution(fig1params30x30, scan_parameters)
    #sol130x30.solve('B')
    #with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresA30x30.dat','wb') as fp:
        #pickle.dump(sol130x30,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresA30x30.dat','rb') as fp:
        sol130x30 = pickle.load(fp)
    
    sol115x15 = af.Solution(fig1params15x15, scan_parameters)
    #sol115x15.solve('B')
    #with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresA15x15.dat','wb') as fp:
        #pickle.dump(sol115x15,fp,protocol=pickle.HIGHEST_PROTOCOL)
    
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresA15x15.dat','rb') as fp:
        sol115x15 = pickle.load(fp)
        
    #sol115x15bow = af.Solution(fig1params15x15bow, scan_parametersbow)
    #sol115x15bow.solve('B')
    #with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresA15x15bow.dat','wb') as fp:
    #    pickle.dump(sol115x15bow,fp,protocol=pickle.HIGHEST_PROTOCOL)
    
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresA15x15bow.dat','rb') as fp:
        sol115x15bow = pickle.load(fp)
        
    solUE56 = af.Solution(fig1paramsUE56, scan_parametersUE56)
    solUE56.solve('B')
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresAUE56.dat','wb') as fp:
        pickle.dump(solUE56,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresAUE56.dat','rb') as fp:
        solUE56 = pickle.load(fp)
        

    #plot peak field against gap
    #sol115x15.plot_Bpeak_vs_Gap()
    #sol130x30.plot_Bpeak_vs_Gap()
    #plt.title = ('APPLE II Peak field vs Gap')
    
    csfont = {'fontname':'Times New Roman'}    
        
    fig2,ax2 = plt.subplots()
    fig2.set_size_inches(2.1, 2.1)
    fig2.subplots_adjust(0.24, 0.17, 0.96, 0.84, 0.05, 0.05)
    ax2.plot(solUE56.case_solutions[0].bprofile[:,0],solUE56.case_solutions[0].bprofile[:,3], label = '2mm Gap')
    ax2.plot(solUE56.case_solutions[0].bprofile[:,0],solUE56.case_solutions[2].bprofile[:,3], label = '4mm Gap')
    ax2.plot(solUE56.case_solutions[0].bprofile[:,0],solUE56.case_solutions[4].bprofile[:,3], label = '6mm Gap')
    ax2.plot(solUE56.case_solutions[0].bprofile[:,0],solUE56.case_solutions[6].bprofile[:,3], label = '13mm Gap')
    
    ax2.set_xlim(-30,30)
    ax2.set_ylim(-1,2.5)
    ax2.set_title('UE56 Field Profile in\nHorizontal Mode', fontsize=8, **csfont)
    ax2.set_ylabel('Field $B_z$ (T)', fontsize = 7, **csfont)
    ax2.set_xlabel('Position $x$ (mm)', fontsize = 7, **csfont)
    ax2.tick_params('both', labelsize = 6)
    ax2.legend(fontsize = 6)
    fig2.savefig('{}UE56_Bz_vs_gap_mini.png'.format(savepath), dpi=fig2.dpi)
    
    
    fig3,ax3 = plt.subplots()
    fig3.set_size_inches(2.1, 2.1)
    fig3.subplots_adjust(0.24, 0.17, 0.96, 0.84, 0.05, 0.05)
    ax3.plot(solUE56.case_solutions[1].bprofile[:,0],-solUE56.case_solutions[1].bprofile[:,1], label = '2mm Gap')
    ax3.plot(solUE56.case_solutions[1].bprofile[:,0],-solUE56.case_solutions[3].bprofile[:,1], label = '4mm Gap')
    ax3.plot(solUE56.case_solutions[1].bprofile[:,0],-solUE56.case_solutions[5].bprofile[:,1], label = '6mm Gap')
    ax3.plot(solUE56.case_solutions[1].bprofile[:,0],-solUE56.case_solutions[7].bprofile[:,1], label = '13mm Gap')
    
    ax3.set_xlim(-30,30)
    ax3.set_ylim(-1,2.5)
    ax3.set_title('UE56 Field Profile in\nVertical Mode', fontsize=8, **csfont)
    ax3.set_ylabel('Field $B_x$ (T)', fontsize = 7, **csfont)
    ax3.set_xlabel('Position $x$ (mm)', fontsize = 7, **csfont)
    ax3.tick_params('both', labelsize = 6)
    
    fig3.savefig('{}UE56_Bx_vs_gap_mini.png'.format(savepath), dpi=fig3.dpi)
    
    fig4,ax4 = plt.subplots()
    fig4.set_size_inches(2.1, 2.1)
    fig4.subplots_adjust(0.24, 0.17, 0.96, 0.84, 0.05, 0.05)
    ax4.plot(solUE56.scan_parameters.gaprange[:4],solUE56.results['Bmax'][:,:4,0,2].flatten(), label = 'Peak $B_z$')
    ax4.plot(solUE56.scan_parameters.gaprange[:4],solUE56.results['Bmax'][:,:4,1,0].flatten(), label = 'Peak $B_x$')
    
    ax4.set_xlim(0,15)
    ax4.set_title('UE56 Peak Field', fontsize=8, **csfont)
    ax4.set_ylabel('Field $B_x,_z$ (T)', fontsize = 7, **csfont)
    ax4.set_xlabel('Gap $g$ (mm)', fontsize = 7, **csfont)
    ax4.tick_params('both', labelsize = 6)
    ax4.legend(fontsize = 6)
    
    fig4.savefig('{}UE56_B_vs_gap_mini.png'.format(savepath), dpi=fig4.dpi)
    print(1)
    #sol1.save(hf = None, solstring = 'Sol1', fname = 'M:\Work\Athena_APPLEIII\Python\Results\SRI2022\gap_scan.h5')
    
    #no hyperparameters

def figuresB(savepath):
    
    figBparams30x30 = parameters.model_parameters(M = 1.344,
                                             Mova = 20, 
                                             periods = 5, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [30.0,0.0,30.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 1, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [3,3,3],
                                             rowtorowgap = 0.5
                                             )
    
    
    #base scan range
    gaprange = np.arange(2.,6.01,2)
    shiftrange = np.arange(0,7.51, 7.5)
    shiftmoderange = ['linear']
    
    scan_parameters = parameters.scan_parameters(periodlength = figBparams30x30.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    solB30x30 = af.Solution(figBparams30x30, scan_parameters)
    #solB30x30.solve('B')
    #with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresB30x30.dat','wb') as fp:
        #pickle.dump(solB30x30,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresB30x30.dat','rb') as fp:
        solB30x30 = pickle.load(fp)
        
    
    csfont = {'fontname':'Times New Roman'}    
    
    fig2,ax2 = plt.subplots()
    fig2.set_size_inches(2.1, 2.1)
    fig2.subplots_adjust(0.24, 0.17, 0.96, 0.84, 0.05, 0.05)
    ax2.plot(solB30x30.case_solutions[0].bprofile[:,0],solB30x30.case_solutions[0].bprofile[:,3], label = '2mm Gap')
    ax2.plot(solB30x30.case_solutions[0].bprofile[:,0],solB30x30.case_solutions[2].bprofile[:,3], label = '4mm Gap')
    ax2.plot(solB30x30.case_solutions[0].bprofile[:,0],solB30x30.case_solutions[4].bprofile[:,3], label = '6mm Gap')
    
    ax2.set_xlim(-30,30)
    ax2.set_ylim(-0.6,1.6)
    ax2.set_title('UE15 field profile in\nHorizontal Mode: M$_\u03C6$ = 20\u00B0', fontsize=8, **csfont)
    ax2.set_ylabel('Field $B_x$ (T)', fontsize = 7, **csfont)
    ax2.set_xlabel('Position $x$ (mm)', fontsize = 7, **csfont)
    ax2.tick_params('both', labelsize = 6)
    ax2.legend(fontsize = 6)
    
    fig2.savefig('{}UE15_Mphi_Bz_mini.png'.format(savepath), dpi=fig2.dpi)
    
    fig3,ax3 = plt.subplots()
    fig3.set_size_inches(2.1, 2.1)
    fig3.subplots_adjust(0.24, 0.17, 0.96, 0.84, 0.05, 0.05)
    ax3.plot(solB30x30.case_solutions[1].bprofile[:,0],-solB30x30.case_solutions[1].bprofile[:,1], label = '2mm Gap')
    ax3.plot(solB30x30.case_solutions[1].bprofile[:,0],-solB30x30.case_solutions[3].bprofile[:,1], label = '4mm Gap')
    ax3.plot(solB30x30.case_solutions[1].bprofile[:,0],-solB30x30.case_solutions[5].bprofile[:,1], label = '6mm Gap')
    
    ax3.set_xlim(-30,30)
    ax3.set_ylim(-0.6,1.6)
    ax3.set_title('UE15 field profile in\nVertical Mode: M$_\u03C6$ = 20\u00B0', fontsize=8, **csfont)
    ax3.set_ylabel('Field $B_x$ (T)', fontsize = 7, **csfont)
    ax3.set_xlabel('Position $x$ (mm)', fontsize = 7, **csfont)
    ax3.tick_params('both', labelsize = 6)
    
    fig3.savefig('{}UE15_Mphi_Bx_mini.png'.format(savepath), dpi=fig3.dpi)
    
    print(1)

def figuresC(savepath):
    
    figBparams30x30 = parameters.model_parameters(M = 1.344,
                                             Mova = 20, 
                                             periods = 5, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [30.0,0.0,30.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 1, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [3,3,3],
                                             rowtorowgap = 0.5
                                             )
    
    
    #base scan range
    gaprange = np.array([15/16.0, 15/8.0,15.0/4 ,15.0/2])
    shiftrange = np.arange(0,7.51, 7.5)
    shiftmoderange = ['linear']
    
    scan_parameters = parameters.scan_parameters(periodlength = figBparams30x30.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    solB30x30 = af.Solution(figBparams30x30, scan_parameters)
    #solB30x30.solve('B')
    #with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresB30x30_long.dat','wb') as fp:
        #pickle.dump(solB30x30,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresB30x30_long.dat','rb') as fp:
        solB30x30 = pickle.load(fp)
        
    
    csfont = {'fontname':'Times New Roman'}
    
    fig2,ax2 = plt.subplots()
    fig2.set_size_inches(2.1, 2.1)
    fig2.subplots_adjust(0.24, 0.17, 0.96, 0.84, 0.05, 0.05)
    ax2.plot(solB30x30.case_solutions[0].bfield[:,0],solB30x30.case_solutions[0].bfield[:,3], label = '16:1')
    ax2.plot(solB30x30.case_solutions[0].bfield[:,0],solB30x30.case_solutions[2].bfield[:,3], label = '8:1')
    ax2.plot(solB30x30.case_solutions[0].bfield[:,0],solB30x30.case_solutions[4].bfield[:,3], label = '4:1')
    ax2.plot(solB30x30.case_solutions[0].bfield[:,0],solB30x30.case_solutions[6].bfield[:,3], label = '2:1')
    
    ax2.set_xlim(-15,15)
    ax2.set_ylim(-2,2)
    ax2.set_title('UE15 on-axis field profile in\nHorizontal Mode', fontsize=8, **csfont)
    ax2.set_ylabel('Field $B_x$ (T)', fontsize = 7, **csfont)
    ax2.set_xlabel('Position $s$ (mm)', fontsize = 7, **csfont)
    ax2.tick_params('both', labelsize = 6)
    ax2.legend(fontsize = 6)
    
    fig2.savefig('{}UE15_Gap_BzvsS_mini.png'.format(savepath), dpi=fig2.dpi)
    
    fig3,ax3 = plt.subplots()
    fig3.set_size_inches(2.1, 2.1)
    fig3.subplots_adjust(0.24, 0.17, 0.96, 0.84, 0.05, 0.05)
    ax3.plot(solB30x30.case_solutions[0].bfield[:,0],-solB30x30.case_solutions[1].bfield[:,1], label = '16:1')
    ax3.plot(solB30x30.case_solutions[0].bfield[:,0],-solB30x30.case_solutions[3].bfield[:,1], label = '8:1')
    ax3.plot(solB30x30.case_solutions[0].bfield[:,0],-solB30x30.case_solutions[5].bfield[:,1], label = '4:1')
    ax3.plot(solB30x30.case_solutions[0].bfield[:,0],-solB30x30.case_solutions[7].bfield[:,1], label = '2:1')
    
    ax3.set_xlim(-15,15)
    ax3.set_ylim(-2,2)
    ax3.set_title('UE15 on-axis field profile in\nVertical Mode', fontsize=8, **csfont)
    ax3.set_ylabel('Field $B_x$ (T)', fontsize = 7, **csfont)
    ax3.set_xlabel('Position $s$ (mm)', fontsize = 7, **csfont)
    ax3.tick_params('both', labelsize = 6)
    ax3.legend(fontsize = 6)
    fig3.savefig('{}UE15_Gap_BxvsS_mini.png'.format(savepath), dpi=fig3.dpi)
    
    print(1)    
    
def figuresD():
    #Radia pictures of array
    figDparams = parameters.model_parameters(M = 1.344,
                                             Mova = 20, 
                                             periods = 35, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 1, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [1,1,1],
                                             rowtorowgap = 0.5
                                             )
    
    figDparams1 = parameters.model_parameters(M = 1.344,
                                             Mova = 0, 
                                             periods = 35, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 1, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [1,1,1],
                                             rowtorowgap = 0.5
                                             )
    
    
    #base scan range
    gaprange = np.array([15/16.0, 15/8.0,15.0/4 ,15.0/2])
    shiftrange = np.arange(0,7.51, 7.5)
    shiftmoderange = ['linear']
    
    scan_parameters = parameters.scan_parameters(periodlength = figDparams.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    solD = af.Solution(figDparams, scan_parameters)
    #solD1 = af.Solution(figDparams1, scan_parameters)
    casemodel = id.compensatedAPPLEv2(figDparams)
    #casemodel1 = id.compensatedAPPLEv2(figDparams1)
    
    d = wrd.wradObjCnt()
    d.wradObjAddToCnt([casemodel.cont.objectlist[0].objectlist[0].objectlist[2], 
                     casemodel.cont.objectlist[1].objectlist[0].objectlist[2], 
                     casemodel.cont.objectlist[2].objectlist[0].objectlist[2], 
                     casemodel.cont.objectlist[3].objectlist[0].objectlist[2]])
    #d1 = wrd.wradObjCnt()
    #d1.wradObjAddToCnt([casemodel1.cont.objectlist[0].objectlist[0].objectlist[2], 
    #                 casemodel1.cont.objectlist[1].objectlist[0].objectlist[2], 
    #                 casemodel1.cont.objectlist[2].objectlist[0].objectlist[2], 
    #                 casemodel1.cont.objectlist[3].objectlist[0].objectlist[2]])
    import radia as rd
    
    rd.ObjDrwOpenGL(casemodel.cont.radobj,'Axes->False')
    print(1)
    
def figuresE():
    # I dunno
    figEparams = parameters.model_parameters(Mova = 0, 
                                             periods = 5, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 1, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [2,2,1],
                                             rowtorowgap = 0.5
                                             )
    
    gaprange = np.arange(2.,10.01,2)
    
    shiftrange = np.arange(-7.5,7.51, 1.875)
    shiftmoderange = ['linear','circular']
    
    scan_parameters = parameters.scan_parameters(periodlength = figEparams.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    solE = af.Solution(figEparams, scan_parameters)
    solE.solve('B')
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresE.dat','wb') as fp:
        pickle.dump(solE,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresE.dat','rb') as fp:
        solE = pickle.load(fp)
    
    
def figuresLEAPS():
    #figure for LEAPS, done in the middle of SRI work
    figLEAPSparams = parameters.model_parameters(Mova = 0,
                                             M = 1.3,
                                             periods = 5, 
                                             periodlength = 32,
                                             nominal_fmagnet_dimensions = [30.0,0.0,30.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 5.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 4,
                                             gap = 1, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [3,2,1],
                                             rowtorowgap = 1
                                             )
    
    gaprange = np.arange(7.,7.01,2)
    shiftrange = np.arange(0,16.01, 16)
    shiftmoderange = ['linear','circular']
    
    scan_parameters = parameters.scan_parameters(periodlength = figLEAPSparams.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    solLEAPS = af.Solution(figLEAPSparams, scan_parameters)
    solLEAPS.solve('B')
    
    print(1)
    
def figuresF():
    #figures for longitudinal field profile with gap. harmonic content
    figFparams = parameters.model_parameters(Mova = 0, 
                                         periods = 5, 
                                         periodlength = 15,
                                         nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                         #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                         nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                         nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                         compappleseparation = 7.5,
                                         apple_clampcut = 3.0,
                                         comp_magnet_chamfer = [3.0,0.0,3.0],
                                         magnets_per_period = 4,
                                         gap = 1, 
                                         rowshift = 0,
                                         shiftmode = 'circular',
                                         block_subdivision = [3,2,1],
                                         rowtorowgap = 0.5
                                         )
    
    #base scan range
    gaprange = np.array([15/8.,15/4.,15/2.])
    shiftrange = np.arange(0,7.51, 7.5)
    shiftmoderange = ['linear']
    
    scan_parameters = parameters.scan_parameters(periodlength = figFparams.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    solF = af.Solution(figFparams, scan_parameters)
#    solF.solve('B')
#    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresF.dat','wb') as fp:
#        pickle.dump(solF,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresF.dat','rb') as fp:
        solF = pickle.load(fp)
    
    csfont = {'fontname':'Times New Roman'}    
        
    fig2,ax2 = plt.subplots()
    fig2.set_size_inches(2.1, 2.1)
    fig2.subplots_adjust(0.24, 0.17, 0.96, 0.84, 0.05, 0.05)
    ax2.plot(solF.case_solutions[0].bfield[:,0],solF.case_solutions[0].bfield[:,3]/solF.case_solutions[0].bmax[2], label = '$\lambda_u/8$')
    ax2.plot(solF.case_solutions[0].bfield[:,0],solF.case_solutions[2].bfield[:,3]/solF.case_solutions[2].bmax[2], label = '$\lambda_u/4$')
    ax2.plot(solF.case_solutions[0].bfield[:,0],solF.case_solutions[4].bfield[:,3]/solF.case_solutions[4].bmax[2], label = '$\lambda_u/2$')
    
    
    ax2.set_xlim(-15,15)
    ax2.set_ylim(-1.1,1.1)
    ax2.set_title('Normalised On-axis Field in\nHorizontal Mode', fontsize=8, **csfont)
    ax2.set_ylabel('Field $B_z$ (T)', fontsize = 7, **csfont)
    ax2.set_xlabel('Position $s$ (mm)', fontsize = 7, **csfont)
    ax2.tick_params('both', labelsize = 6)
    ax2.legend(fontsize = 6)
    fig2.savefig('{}Aspect_Ratio_Bz.png'.format(savepath), dpi=fig2.dpi)
    
    fig3,ax3 = plt.subplots()
    fig3.set_size_inches(2.1, 2.1)
    fig3.subplots_adjust(0.24, 0.17, 0.96, 0.84, 0.05, 0.05)
    ax3.plot(solF.case_solutions[0].bfield[:,0],solF.case_solutions[1].bfield[:,1]/solF.case_solutions[1].bmax[0], label = '$\lambda_u/8$')
    ax3.plot(solF.case_solutions[0].bfield[:,0],solF.case_solutions[3].bfield[:,1]/solF.case_solutions[3].bmax[0], label = '$\lambda_u/4$')
    ax3.plot(solF.case_solutions[0].bfield[:,0],solF.case_solutions[5].bfield[:,1]/solF.case_solutions[5].bmax[0], label = '$\lambda_u/2$')
    
    
    ax3.set_xlim(-15,15)
    ax3.set_ylim(-1.1,1.1)
    ax3.set_title('Normalised On-axis Field in\nHorizontal Mode', fontsize=8, **csfont)
    ax3.set_ylabel('Field $B_z$ (T)', fontsize = 7, **csfont)
    ax3.set_xlabel('Position $s$ (mm)', fontsize = 7, **csfont)
    ax3.tick_params('both', labelsize = 6)
    ax3.legend(fontsize = 6)
    fig3.savefig('{}Aspect_Ratio_Bx.png'.format(savepath), dpi=fig3.dpi)
    
    print('!')
    
def figuresG(savepath):
    block_divis = [2,2,2]
    #4/period compensated parameters
    figG4cparams = parameters.model_parameters(type = 'Compensated_APPLE',
                                     Mova = 20, 
                                     periods = 3, 
                                     periodlength = 15,
                                     nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                     #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                     nominal_vcmagnet_dimensions = [7.5,0.0,15.0],
                                     nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                     compappleseparation = 7.5,
                                     apple_clampcut = 3.0,
                                     comp_magnet_chamfer = [3.0,0.0,3.0],
                                     magnets_per_period = 4,
                                     gap = 1, 
                                     rowshift = 0,
                                     shiftmode = 'circular',
                                     block_subdivision = block_divis,
                                     rowtorowgap = 0.5
                                     )
    
    #4/period uncompensated/plain APPLE
    figG4uparams = parameters.model_parameters(type = 'Plain_APPLE',
                                     Mova = 20, 
                                     periods = 3, 
                                     periodlength = 15,
                                     nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                     #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                     nominal_vcmagnet_dimensions = [7.5,0.0,15.0],
                                     nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                     compappleseparation = 7.5,
                                     apple_clampcut = 3.0,
                                     comp_magnet_chamfer = [3.0,0.0,3.0],
                                     magnets_per_period = 4,
                                     gap = 1, 
                                     rowshift = 0,
                                     shiftmode = 'circular',
                                     block_subdivision = block_divis,
                                     rowtorowgap = 0.5
                                     )
    
    #6/period compensated parameters
    
    figG6cparams = parameters.model_parameters(type = 'Compensated_APPLE',
                                     Mova = 20, 
                                     periods = 3, 
                                     periodlength = 15,
                                     nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                     #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                     nominal_vcmagnet_dimensions = [7.5,0.0,15.0],
                                     nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                     compappleseparation = 7.5,
                                     apple_clampcut = 3.0,
                                     comp_magnet_chamfer = [3.0,0.0,3.0],
                                     magnets_per_period = 6,
                                     gap = 1, 
                                     rowshift = 0,
                                     shiftmode = 'circular',
                                     block_subdivision = block_divis,
                                     rowtorowgap = 0.5
                                     )
    
    #6/period uncompensated/plain parameters
    
    figG6uparams = parameters.model_parameters(type = 'Plain_APPLE',
                                     Mova = 20, 
                                     periods = 3, 
                                     periodlength = 15,
                                     nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                     #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                     nominal_vcmagnet_dimensions = [7.5,0.0,15.0],
                                     nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                     compappleseparation = 7.5,
                                     apple_clampcut = 3.0,
                                     comp_magnet_chamfer = [3.0,0.0,3.0],
                                     magnets_per_period = 6,
                                     gap = 1, 
                                     rowshift = 0,
                                     shiftmode = 'circular',
                                     block_subdivision = block_divis,
                                     rowtorowgap = 0.5
                                     )
    #scan parameters
    gaprange = np.arange(2.,10.01,12)
    shiftrange = np.arange(-7.5,7.51, 1.875)
    #shiftmoderange = ['linear','circular']
    shiftmoderange = ['linear','circular']
    
    scan_parameters = parameters.scan_parameters(periodlength = figG4cparams.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    #4/period compensated
    
    #solG4c = af.Solution(figG4cparams, scan_parameters)
    #solG4c.solve('Forces')
    #with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresG4c.dat','wb') as fp:
    #    pickle.dump(solG4c,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresG4c.dat','rb') as fp:
        solG4c = pickle.load(fp)
    
    #4/period uncompensated
    #solG4u = af.Solution(figG4uparams, scan_parameters)
    #solG4u.solve('Forces')
    #with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresG4u.dat','wb') as fp:
    #    pickle.dump(solG4u,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresG4u.dat','rb') as fp:
        solG4u = pickle.load(fp)
    #6/period compensated
    
    #solG6c = af.Solution(figG6cparams, scan_parameters)
    #solG6c.solve('Forces')
    #with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresG6c.dat','wb') as fp:
    #    pickle.dump(solG6c,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresG6c.dat','rb') as fp:
        solG6c = pickle.load(fp)
    
    #6/period uncompensated
    #solG6u = af.Solution(figG6uparams, scan_parameters)
    #solG6u.solve('Forces')
    #with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresG6u.dat','wb') as fp:
    #    pickle.dump(solG6u,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresG6u.dat','rb') as fp:
        solG6u = pickle.load(fp)
        
    plt.plot(scan_parameters.shiftrange, solG6u.results['Force_Per_Magnet_Type'][0,0,:,0,0])
    
    csfont = {'fontname':'Times New Roman'}    
    ticker = tk.EngFormatter(unit='N')
        
    fig2,ax2 = plt.subplots(1,2, sharey = True)
    fig2.set_size_inches(4.2, 2.5)
    fig2.subplots_adjust(0.24, 0.3, 0.96, 0.84, 0.05, 0.05)
    ax2[0].plot(solG4c.scan_parameters.shiftrange,60*(np.sum(solG4c.results['Force_Per_Magnet_Type'][0,0,:,0,:,0],1) + np.sum(solG4c.results['Force_Per_Magnet_Type'][0,0,:,4,:,0],1)), color = '#1f77b4', label = 'Compensated $F_x$')
    ax2[0].plot(solG4c.scan_parameters.shiftrange,60*(np.sum(solG4c.results['Force_Per_Magnet_Type'][0,0,:,0,:,0],1)), color = '#1f77b4',linestyle = 'dashed', label = 'Uncompensated $F_x$')
    ax2[0].plot(solG4c.scan_parameters.shiftrange,60*(np.sum(solG4c.results['Force_Per_Magnet_Type'][0,0,:,0,:,1],1) + np.sum(solG4c.results['Force_Per_Magnet_Type'][0,0,:,4,:,1],1) + np.sum(solG4c.results['Force_Per_Magnet_Type'][0,0,:,5,:,1],1)), color = '#ff7f0e', label = 'Compensated $F_s$')
    ax2[0].plot(solG4c.scan_parameters.shiftrange,60*(np.sum(solG4c.results['Force_Per_Magnet_Type'][0,0,:,0,:,1],1)), color = '#ff7f0e',linestyle = 'dashed', label = 'Uncompensated $F_s$')
    ax2[0].plot(solG4c.scan_parameters.shiftrange,60*(np.sum(solG4c.results['Force_Per_Magnet_Type'][0,0,:,0,:,2],1) + np.sum(solG4c.results['Force_Per_Magnet_Type'][0,0,:,5,:,2],1)), color = '#2ca02c', label = 'Compensated $F_z$')
    ax2[0].plot(solG4c.scan_parameters.shiftrange,60*(np.sum(solG4c.results['Force_Per_Magnet_Type'][0,0,:,0,:,2],1)), color = '#2ca02c',linestyle = 'dashed', label = 'Uncompensated $F_z$')
    
    
    ax2[0].yaxis.set_major_formatter(ticker)
    
    ax2[0].set_xlim(-8,8)
    ax2[0].set_ylim(-11000,11000)
    ax2[0].set_title('Force on 60 Period CIVUE15\nHalbach N = 4', fontsize=8, **csfont)
    ax2[0].set_ylabel('Directional Force', fontsize = 7, **csfont)
    ax2[0].set_xlabel('Axis Shift $S$ (mm)', fontsize = 7, **csfont)
    ax2[0].tick_params('both', labelsize = 6)
    
    ax2[1].plot(solG6c.scan_parameters.shiftrange,60*(np.sum(solG6c.results['Force_Per_Magnet_Type'][0,0,:,0,:,0],1) + np.sum(solG6c.results['Force_Per_Magnet_Type'][0,0,:,4,:,0],1)), color = '#1f77b4', label = None)
    ax2[1].plot(solG6c.scan_parameters.shiftrange,60*(np.sum(solG6c.results['Force_Per_Magnet_Type'][0,0,:,0,:,0],1)), color = '#1f77b4',linestyle = 'dashed', label = None)
    ax2[1].plot(solG6c.scan_parameters.shiftrange,60*(np.sum(solG6c.results['Force_Per_Magnet_Type'][0,0,:,0,:,1],1) + np.sum(solG6c.results['Force_Per_Magnet_Type'][0,0,:,4,:,1],1) + np.sum(solG6c.results['Force_Per_Magnet_Type'][0,0,:,5,:,1],1)), color = '#ff7f0e', label = None)
    ax2[1].plot(solG6c.scan_parameters.shiftrange,60*(np.sum(solG6c.results['Force_Per_Magnet_Type'][0,0,:,0,:,1],1)), color = '#ff7f0e',linestyle = 'dashed', label = None)
    ax2[1].plot(solG6c.scan_parameters.shiftrange,60*(np.sum(solG6c.results['Force_Per_Magnet_Type'][0,0,:,0,:,2],1) + np.sum(solG6c.results['Force_Per_Magnet_Type'][0,0,:,5,:,2],1)), color = '#2ca02c', label = None)
    ax2[1].plot(solG6c.scan_parameters.shiftrange,60*(np.sum(solG6c.results['Force_Per_Magnet_Type'][0,0,:,0,:,2],1)), color = '#2ca02c',linestyle = 'dashed', label = None)
    
    
    ax2[1].yaxis.set_major_formatter(ticker)
    
    ax2[1].set_xlim(-8,8)
    ax2[1].set_ylim(-11000,11000)
    ax2[1].set_title('Force on 60 Period CIVUE15\nHalbach N = 6', fontsize=8, **csfont)
    ax2[1].set_xlabel('Axis Shift $S$ (mm)', fontsize = 7, **csfont)
    ax2[1].tick_params('both', labelsize = 6)
    
    fig2.legend(loc="lower right", borderaxespad=0, ncol=3, fontsize = 6)
    
    fig2.savefig('{}Force_Comp.png'.format(savepath), dpi=3*fig2.dpi)
    
    print('FiguresG completed')
    
def figuresH(savepath):
    #plot of peak field for magnet width
    block_divis = [2,2,2]
        
    #4/period uncompensated/plain APPLE
    figHparams = parameters.model_parameters(type = 'Plain_APPLE',
                                     Mova = 20, 
                                     periods = 3, 
                                     periodlength = 15,
                                     nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                     #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                     nominal_vcmagnet_dimensions = [7.5,0.0,15.0],
                                     nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                     compappleseparation = 7.5,
                                     apple_clampcut = 3.0,
                                     comp_magnet_chamfer = [3.0,0.0,3.0],
                                     magnets_per_period = 6,
                                     gap = 1, 
                                     rowshift = 0,
                                     shiftmode = 'circular',
                                     block_subdivision = block_divis,
                                     rowtorowgap = 0.5
                                     )
    
        #create test hyper params as dict
    test_hyper_params_dict = {'type': 'Plain_APPLE',
                              'Mova': 20,
                              'periods' : 3,
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
                              'shim' : 0.25,
                              'square_magnet' : 15.0,
                              'block_subdivision' : [2,2,2]
                              }
    
    hyper_solution_variables = {
        #"block_subdivision" : [np.array([2]),np.arange(2,4),np.arange(3,4)],
        #"Mova" : np.arange(15,25.1,5),
        #"nominal_vcmagnet_dimensions": [np.arange(7.5,8,0.25),np.arange(0.0,1.0,10.0),np.arange(10,40.1,5.0)],
        #"nominal_hcmagnet_dimensions": [np.arange(7.5,8.1,2),np.arange(0.0,1.0,10.0),np.arange(10,15.1,1)],
        "square_magnet" : np.arange(10,20.1,2.5),
        "magnets_per_period" : np.arange(4,8,2)
        }
    
    #hyper_solution_properties = ['B', 'Forces']
    hyper_solution_properties = ['B']
    
    #scan parameters
    gaprange = np.arange(2.,10.01,2)
    shiftrange = np.arange(0.0,7.51, 7.5)
    #shiftmoderange = ['linear','circular']
    shiftmoderange = ['linear']
    
    scan_parameters = parameters.scan_parameters(periodlength = figHparams.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    #create hypersolution object
    hypersolH = af.HyperSolution(base_hyper_parameters = test_hyper_params_dict, 
                              hyper_solution_variables = hyper_solution_variables, 
                              hyper_solution_properties = hyper_solution_properties,
                              scan_parameters = scan_parameters,
                              method = 'systematic',
                              iterations = 60)
    
    #hypersolH.solve()
    
    
    #with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresH.dat','wb') as fp:
    #    pickle.dump(hypersolH,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresH.dat','rb') as fp:
        hypersolH = pickle.load(fp)
    
    csfont = {'fontname':'Times New Roman'}    
        
    fig2,ax2 = plt.subplots()
    fig2.set_size_inches(3.15, 3)
    fig2.subplots_adjust(0.24, 0.3, 0.96, 0.84, 0.05, 0.05)
    ax2.plot(hypersolH.hyper_solution_variables['square_magnet'],hypersolH.hyper_results['Bmax'][:,0,0], label = '$N_H$=4: Peak $B_x$')
    ax2.plot(hypersolH.hyper_solution_variables['square_magnet'],hypersolH.hyper_results['Bmax'][:,0,2], label = '$N_H$=4: Peak $B_z$')
    ax2.plot(hypersolH.hyper_solution_variables['square_magnet'],hypersolH.hyper_results['Bmax'][:,1,0], label = '$N_H$=6: Peak $B_x$')
    ax2.plot(hypersolH.hyper_solution_variables['square_magnet'],hypersolH.hyper_results['Bmax'][:,1,2], label = '$N_H$=6: Peak $B_z$')
    
    
    ax2.set_xlim(7.5,22.5)
    ax2.set_ylim(1.4,1.9)
    ax2.set_title('Peak Field vs Functional Magnet Cross-Section', fontsize=8, **csfont)
    ax2.set_ylabel('Field $B$ (T)', fontsize = 7, **csfont)
    ax2.set_xlabel('Magnet Size (mm)', fontsize = 7, **csfont)
    ax2.tick_params('both', labelsize = 6)
    fig2.legend(loc="lower right", ncol=2, fontsize = 6)
    fig2.savefig('{}Cross_Section_Peak.png'.format(savepath), dpi=3*fig2.dpi)
    
    
    fig3,ax3 = plt.subplots()
    fig3.set_size_inches(3.15, 3)
    fig3.subplots_adjust(0.24, 0.3, 0.96, 0.84, 0.05, 0.05)
    ax3.plot(hypersolH.solutions[9].case_solutions[9].bprofile[:,0],hypersolH.solutions[1].case_solutions[0].bprofile[:,3], color = '#1f77b4', label = '$B_z$ 10mm Block')
    ax3.plot(hypersolH.solutions[9].case_solutions[9].bprofile[:,0],-hypersolH.solutions[1].case_solutions[1].bprofile[:,1], color = '#1f77b4',linestyle = 'dashed', label = '$B_x$ 10mm Block')
    ax3.plot(hypersolH.solutions[9].case_solutions[9].bprofile[:,0],hypersolH.solutions[5].case_solutions[0].bprofile[:,3], color = '#ff7f0e', label = '$B_z$ 15mm Block')
    ax3.plot(hypersolH.solutions[9].case_solutions[9].bprofile[:,0],-hypersolH.solutions[5].case_solutions[1].bprofile[:,1], color = '#ff7f0e',linestyle = 'dashed', label = '$B_x$ 15mm Block')
    ax3.plot(hypersolH.solutions[9].case_solutions[9].bprofile[:,0],hypersolH.solutions[9].case_solutions[0].bprofile[:,3], color = '#2ca02c', label = '$B_z$ 20mm Block')
    ax3.plot(hypersolH.solutions[9].case_solutions[9].bprofile[:,0],-hypersolH.solutions[9].case_solutions[1].bprofile[:,1], color = '#2ca02c',linestyle = 'dashed', label = '$B_x$ 20mm Block')
    
    
    ax3.set_xlim(-25,25)
    ax3.set_ylim(0,2)
    ax3.set_title('Field Profile vs Functional Magnet Cross-Section', fontsize=8, **csfont)
    ax3.set_ylabel('Field $B$ (T)', fontsize = 7, **csfont)
    ax3.set_xlabel('Position $x$ (mm)', fontsize = 7, **csfont)
    ax3.tick_params('both', labelsize = 6)
    fig3.legend(loc="lower right", ncol=3, fontsize = 6)
    fig3.savefig('{}Cross_Section_Profile.png'.format(savepath), dpi=3*fig3.dpi)
    
    print('figures H completed')
    


def figuresI(savepath): 
    
    #plot of peak field for magnet width
    block_divis = [1,1,1]
    
    def perturbI(s):
        x = s
        z = s
        return np.array([x,s])
        
    #4/period uncompensated/plain APPLE
    figI1params = parameters.model_parameters(type = 'Plain_APPLE',
                                     Mova = 20, 
                                     periods = 13, 
                                     periodlength = 15,
                                     nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                     #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                     nominal_vcmagnet_dimensions = [7.5,0.0,15.0],
                                     nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                     compappleseparation = 7.5,
                                     apple_clampcut = 3.0,
                                     comp_magnet_chamfer = [3.0,0.0,3.0],
                                     magnets_per_period = 6,
                                     gap = 1, 
                                     rowshift = 0,
                                     shiftmode = 'circular',
                                     block_subdivision = block_divis,
                                     rowtorowgap = 0.5,
                                     perturbation_fn = perturbI
                                     )
    
    #scan parameters
    gaprange = np.arange(2.,10.01,12)
    shiftrange = np.arange(0,7.51, 7.5)
    #shiftmoderange = ['linear','circular']
    shiftmoderange = ['linear','circular']
    
    scan_parameters = parameters.scan_parameters(periodlength = figI1params.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    
    #linear perturbation
    
    solI1 = af.Solution(figI1params, scan_parameters)
    solI1.solve('B')
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresI1.dat','wb') as fp:
        pickle.dump(solI1,fp,protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('M:\Work\Athena_APPLEIII\Python\Results\SRI2022\\figuresI1.dat','rb') as fp:
        solI1 = pickle.load(fp)
    
    print("Figures I done")
    
if __name__ == '__main__':
    #Figs A. Variation of Peak Field with Gap for Bx, Bz transverse, and along an axis
    savepath = 'M:/Work/Athena_APPLEIII/Python/Results/SRI2022/'
    
    #basic profile plots and peak field values
    #figuresA(savepath)
    
    #figuresB(savepath)
    
    #figuresC(savepath)
    
    #figuresD() #pictures of magnets
    
    #figuresE()
    
    #figuresLEAPS()
    
    #figuresF()
    
    #Calculate Forces
    #figuresG(savepath)
    
    #Block Size
    #figuresH(savepath)
    
    #perturbations in model
    figuresI(savepath)