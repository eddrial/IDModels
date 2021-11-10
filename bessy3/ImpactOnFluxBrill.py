'''
Created on 10 Sep 2021

@author: oqb

Plot and show impact of varying ID and Ebeam parameters on Flux and Brilliance
'''

#import Local_SRW as srw
import srwlib as srw
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
plt.rcParams["figure.figsize"] = (8,4.5)
import copy



def plot_flux_comparison(a):
    
    for j in range (a.shape[0]):
        
        plt.plot(np.linspace(a[j].mesh.eStart, a[j].mesh.eFin, a[j].mesh.ne),np.array(a[j].arS)[0:a[j].mesh.ne])
        
        
    plt.ylim(0,1.7e14)
    plt.xlim(0,1500)
    
    plt.ylabel('Flux (Ph/s/0.1%bw)')
    plt.xlabel("Energy (eV)")
    
    return plt
    print (1)

def plot_bril_comparison(a):
    crange = ['tab:blue','tab:orange','tab:green']
    
    for j in range (a.shape[0]):
        
        for i in range(int(a.shape[1]/2)):
            plt.plot(a[j,2*i,:],a[j,2*i+1,:],crange[j])
            
    plt.yscale("log")
    plt.xscale("log")
    
    
    plt.ylim(1e18,1e20)
    plt.xlim(100,10000)        
    
    plt.ylabel('Brilliance (Ph/s/0.1%bw/mrad$^2$/mm$^2$)')
    plt.xlabel("Energy (eV)")
    
    
            
    
    return plt
    
    #print(1)

if __name__ == '__main__':
    #Define Baseline Undulator 30mm, 2m 1T
    harmB30 = srw.SRWLMagFldH() #magnetic field harmonic
    harmB30.n = 1 #harmonic number
    harmB30.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmB30.B = 1.0 #magnetic field amplitude [T]
    
    
    und30 = srw.SRWLMagFldU([harmB30])
    und30.per = 0.030 #period length [m]
    und30.nPer = 2.0/und30.per #number of periods (will be rounded to integer)
    und30.name = 'U30_2m'
    
    #Stronger/Weaker Field
    #1.1T
    harmB30_1p1 = srw.SRWLMagFldH() #magnetic field harmonic
    harmB30_1p1.n = 1 #harmonic number
    harmB30_1p1.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmB30_1p1.B = 1.1 #magnetic field amplitude [T]
    
    
    und30_1p1 = srw.SRWLMagFldU([harmB30_1p1])
    und30_1p1.per = 0.030 #period length [m]
    und30_1p1.nPer = 2.0/und30_1p1.per #number of periods (will be rounded to integer)
    und30_1p1.name = 'U30_1.1T'
    
    harmB30_0p9 = srw.SRWLMagFldH() #magnetic field harmonic
    harmB30_0p9.n = 1 #harmonic number
    harmB30_0p9.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmB30_0p9.B = 0.9 #magnetic field amplitude [T]
    
    und30_0p9 = srw.SRWLMagFldU([harmB30_0p9])
    und30_0p9.per = 0.030 #period length [m]
    und30_0p9.nPer = 2.0/und30_0p9.per #number of periods (will be rounded to integer)
    und30_0p9.name = 'U30_0.9T'
    
    #Longer/Shorter Period Length
    #20mm
    harmB20 = srw.SRWLMagFldH() #magnetic field harmonic
    harmB20.n = 1 #harmonic number
    harmB20.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmB20.B = 1.0 #magnetic field amplitude [T]
    
    
    und20 = srw.SRWLMagFldU([harmB20])
    und20.per = 0.020 #period length [m]
    und20.nPer = 1.33/und20.per #number of periods (will be rounded to integer)
    und20.name = 'U20_2m'
    
    #40mm
    harmB40 = srw.SRWLMagFldH() #magnetic field harmonic
    harmB40.n = 1 #harmonic number
    harmB40.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmB40.B = 1.0 #magnetic field amplitude [T]
    
    
    und40 = srw.SRWLMagFldU([harmB40])
    und40.per = 0.040 #period length [m]
    und40.nPer = 2.6/und40.per #number of periods (will be rounded to integer)
    und40.name = 'U40_2m'
    
    #Longer/Shorter Device
    #1m
    harmB30_1 = srw.SRWLMagFldH() #magnetic field harmonic
    harmB30_1.n = 1 #harmonic number
    harmB30_1.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmB30_1.B = 1.0 #magnetic field amplitude [T]
    
    
    und30_1 = srw.SRWLMagFldU([harmB30_1])
    und30_1.per = 0.030 #period length [m]
    und30_1.nPer = 1.0/und30_1.per #number of periods (will be rounded to integer)
    und30_1.name = 'U30_1m'
    
    #3m
    harmB30_3 = srw.SRWLMagFldH() #magnetic field harmonic
    harmB30_3.n = 1 #harmonic number
    harmB30_3.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmB30_3.B = 1.0 #magnetic field amplitude [T]
    
    
    und30_3 = srw.SRWLMagFldU([harmB30_3])
    und30_3.per = 0.030 #period length [m]
    und30_3.nPer = 3.0/und30_3.per #number of periods (will be rounded to integer)
    und30_3.name = 'U30_3m'
    
    
    
    
    ###E Beams
    
    #Define Base E Beam
    BII_lb_eBeam = srw.srwl_uti_src_e_beam('BESSYII Low Beta')
    
    #Higher/Lower E Beam Emittance
    BII_HiEmit = srw.srwl_uti_src_e_beam('BESSYII Low Beta high eps')
    BII_LoEmit = srw.srwl_uti_src_e_beam('BESSYII Low Beta low eps')
    
    
    #Higher/Lower E Beam Energy
    BII_HiEn = srw.srwl_uti_src_e_beam('BESSYII Low Beta 2GeV')
    BII_LoEn = srw.srwl_uti_src_e_beam('BESSYII Low Beta 1.4GeV')
    
    
    
    #Sampling Point
        ### Stokes Structures ###
        #***********Precision Parameters
    arPrecF = [0]*5 #for spectral flux vs photon energy
    arPrecF[0] = 1 #initial UR harmonic to take into account
    arPrecF[1] = 21 #final UR harmonic to take into account
    arPrecF[2] = 1.5 #longitudinal integration precision parameter
    arPrecF[3] = 1.5 #azimuthal integration precision parameter
    arPrecF[4] = 1 #calculate flux (1) or flux per unit surface (2)
    
    arPrecP = [0]*5 #for power density
    arPrecP[0] = 1.5 #precision factor
    arPrecP[1] = 1 #power density computation method (1- "near field", 2- "far field")
    arPrecP[2] = 0 #initial longitudinal position (effective if arPrecP[2] < arPrecP[3])
    arPrecP[3] = 0 #final longitudinal position (effective if arPrecP[2] < arPrecP[3])
    arPrecP[4] = 20000 #number of points for (intermediate) trajectory calculation
    
    #***********UR Stokes Parameters (mesh) for Spectral Flux
    stkF = srw.SRWLStokes() #for spectral flux vs photon energy
    stkF.allocate(10000, 1, 1) #numbers of points vs photon energy, horizontal and vertical positions
    stkF.mesh.zStart = 30. #longitudinal position [m] at which UR has to be calculated
    stkF.mesh.eStart = 10. #initial photon energy [eV]
    stkF.mesh.eFin = 20000. #final photon energy [eV]
    stkF.mesh.xStart = -0.0005 #initial horizontal position [m]
    stkF.mesh.xFin = 0.0005 #final horizontal position [m]
    stkF.mesh.yStart = -0.0005 #initial vertical position [m]
    stkF.mesh.yFin = 0.0005 #final vertical position [m]
    
    stkP = srw.SRWLStokes() #for power density
    stkP.allocate(1, 101, 101) #numbers of points vs horizontal and vertical positions (photon energy is not taken into account)
    stkP.mesh.zStart = 30. #longitudinal position [m] at which power density has to be calculated
    stkP.mesh.xStart = -0.02 #initial horizontal position [m]
    stkP.mesh.xFin = 0.02 #final horizontal position [m]
    stkP.mesh.yStart = -0.015 #initial vertical position [m]
    stkP.mesh.yFin = 0.015 #final vertical position [m]
    
    ##Legend stuff
    
    
    #Brilliance and Flux Curves
    U30_Bril = srw.bril_und(BII_lb_eBeam,und30,0.3,1,11,1001,1,plotting = False)
    
    base_bril = plot_bril_comparison(np.array([U30_Bril]))
    base_bril.title('U30 Basic Brilliance Curve')
    base_bril.annotate('Undulator Properties: \n\
        Length: {} m \n\
        Period: {} m\n\
        Peak Field: {} T\n\
E Beam Properties:\n\
        Current: {} A \n\
        Energy: {} GeV \n\
        Emittance: {} nm'.format(2.0,und30.per, harmB30.B,300,1.7,5), 
        (3000,1.8e19))
    base_bril.show()
    
    srw.srwl.CalcStokesUR(stkF, BII_lb_eBeam, und30, arPrecF)
    U30_Flux = copy.deepcopy(stkF)
    
    base_flux = plot_flux_comparison(np.array([U30_Flux]))
    
    base_flux.title('U30 Basic Flux Curve')
    
    base_flux.annotate('Undulator Properties: \n\
        Length: {} m \n\
        Period: {} m\n\
        Peak Field: {} T\n\
E Beam Properties:\n\
        Current: {} A \n\
        Energy: {} GeV \n\
        Emittance: {} nm'.format(2.0,und30.per, harmB30.B,300,1.7,5), 
        (1100,1.05e14))
    
    base_flux.show()
    

    
    #Field
    U30_Bril_1p1 = srw.bril_und(BII_lb_eBeam,und30_1p1,0.3,1,11,1001,1,plotting = False)
    U30_Bril_0p9 = srw.bril_und(BII_lb_eBeam,und30_0p9,0.3,1,11,1001,1,plotting = False)
    
    srw.srwl.CalcStokesUR(stkF, BII_lb_eBeam, und30_1p1, arPrecF)
    U30_1p1_Flux = copy.deepcopy(stkF)
    
    srw.srwl.CalcStokesUR(stkF, BII_lb_eBeam, und30_0p9, arPrecF)
    U30_0p9_Flux = copy.deepcopy(stkF)
    
    
    B_var_bril = plot_bril_comparison(np.array([U30_Bril_1p1,U30_Bril,U30_Bril_0p9]))
    B_var_bril.title('Brilliance vs Peak Field')
    B_var_bril.annotate('Undulator Properties: \n\
        Length: {} m \n\
        Period: {} m\n\
E Beam Properties:\n\
        Current: {} A \n\
        Energy: {} GeV \n\
        Emittance: {} nm'.format(2.0,und30.per,300,1.7,5), 
        (3000,2e19))
    
    blue_line = mlines.Line2D([],[],color = 'tab:blue',label = 'Peak Field: 1.1 T')
    orange_line = mlines.Line2D([],[],color = 'tab:orange', label = 'Peak Field: 1.0 T')
    green_line = mlines.Line2D([],[],color = 'tab:green', label = 'Peak Field: 0.9 T')
    
    B_var_bril.legend(handles = [blue_line, orange_line, green_line], loc = 'upper left')
    
    B_var_bril.show()
    
    B_var_flux = plot_flux_comparison(np.array([U30_1p1_Flux,U30_Flux,U30_0p9_Flux]))
    B_var_flux.legend(handles = [blue_line, orange_line, green_line], loc = 'upper left')
    
    B_var_flux.annotate('Undulator Properties: \n\
        Length: {} m \n\
        Period: {} m\n\
E Beam Properties:\n\
        Current: {} A \n\
        Energy: {} GeV \n\
        Emittance: {} nm'.format(2.0,und30.per, harmB30.B,300,1.7,5), 
        (1100,1.05e14))
    
    B_var_flux.title('Flux vs Peak Field')
    
    B_var_flux.show()
    
    #Length
    U30_Bril_3m = srw.bril_und(BII_lb_eBeam,und30_3,0.3,1,11,1001,1,plotting = False)
    U30_Bril_1m = srw.bril_und(BII_lb_eBeam,und30_1,0.3,1,11,1001,1,plotting = False)
    
    srw.srwl.CalcStokesUR(stkF, BII_lb_eBeam, und30_3, arPrecF)
    U30_3_Flux = copy.deepcopy(stkF)
    
    srw.srwl.CalcStokesUR(stkF, BII_lb_eBeam, und30_1, arPrecF)
    U30_1_Flux = copy.deepcopy(stkF)
    
    len_var_bril = plot_bril_comparison(np.array([U30_Bril_1m,U30_Bril,U30_Bril_3m]))
    len_var_bril.title('Brilliance vs Undulator Length')
    len_var_bril.annotate('Undulator Properties: \n\
        Period: {} m\n\
        Peak Field: {} T\n\
E Beam Properties:\n\
        Current: {} A \n\
        Energy: {} GeV \n\
        Emittance: {} nm'.format(und30.per, harmB30.B,300,1.7,5), 
        (3000,2e19))
    
    blue_line = mlines.Line2D([],[],color = 'tab:blue',label = 'Length: 1 m')
    orange_line = mlines.Line2D([],[],color = 'tab:orange', label = 'Length: 2 m')
    green_line = mlines.Line2D([],[],color = 'tab:green', label = 'Length: 3 m')
    
    len_var_bril.legend(handles = [blue_line, orange_line, green_line], loc = 'upper left')
    
    len_var_bril.show()
    
    len_var_flux = plot_flux_comparison(np.array([U30_1_Flux,U30_Flux,U30_3_Flux]))
    len_var_flux.legend(handles = [blue_line, orange_line, green_line], loc = 'upper left')
    
    len_var_flux.annotate('Undulator Properties: \n\
        Period: {} m\n\
        Peak Field: {} T\n\
E Beam Properties:\n\
        Current: {} A \n\
        Energy: {} GeV \n\
        Emittance: {} nm'.format(und30.per, harmB30.B,300,1.7,5), 
        (1100,1.05e14))
    
    len_var_flux.title('Flux vs Undulator Length')
    
    len_var_flux.show()
    
    #PeriodLength
    U20_Bril = srw.bril_und(BII_lb_eBeam,und20,0.3,1,11,1001,1,plotting = False)
    U40_Bril = srw.bril_und(BII_lb_eBeam,und40,0.3,1,11,1001,1,plotting = False)
    
    srw.srwl.CalcStokesUR(stkF, BII_lb_eBeam, und20, arPrecF)
    U20_Flux = copy.deepcopy(stkF)
    
    srw.srwl.CalcStokesUR(stkF, BII_lb_eBeam, und40, arPrecF)
    U40_Flux = copy.deepcopy(stkF)
    
    lam_var_bril = plot_bril_comparison(np.array([U40_Bril,U30_Bril,U20_Bril]))
    lam_var_bril.title('Brilliance vs Period Length')
    lam_var_bril.annotate('Undulator Properties: \n\
        Length: {} per \n\
        Peak Field: {} T\n\
E Beam Properties:\n\
        Current: {} A \n\
        Energy: {} GeV \n\
        Emittance: {} nm'.format(66, harmB30.B,300,1.7,5), 
        (3000,2e19))
    blue_line = mlines.Line2D([],[],color = 'tab:blue',label = 'Period : 40 mm')
    orange_line = mlines.Line2D([],[],color = 'tab:orange', label = 'Period: 30 mm')
    green_line = mlines.Line2D([],[],color = 'tab:green', label = 'Period: 20 mm')
    lam_var_bril.legend(handles = [blue_line, orange_line, green_line], loc = 'upper left')
    
    lam_var_bril.show()
    
    lam_var_flux = plot_flux_comparison(np.array([U40_Flux,U30_Flux,U20_Flux]))
    lam_var_flux.legend(handles = [blue_line, orange_line, green_line], loc = 'upper left')
    
    lam_var_flux.title('Flux vs Period Length')
    
    lam_var_flux.annotate('Undulator Properties: \n\
        Length: {} per \n\
        Peak Field: {} T\n\
E Beam Properties:\n\
        Current: {} A \n\
        Energy: {} GeV \n\
        Emittance: {} nm'.format(66, harmB30.B,300,1.7,5), 
        (1100,1.05e14))
    
    lam_var_flux.show()
    
    #Emittance
    low_emit_Bril = srw.bril_und(BII_LoEmit,und30,0.3,1,11,1001,1,plotting = False)
    high_emit_Bril = srw.bril_und(BII_HiEmit,und30,0.3,1,11,1001,1,plotting = False)
    
    srw.srwl.CalcStokesUR(stkF, BII_LoEmit, und30, arPrecF)
    low_emit_Flux = copy.deepcopy(stkF)
    
    srw.srwl.CalcStokesUR(stkF, BII_HiEmit, und30, arPrecF)
    hi_emit_Flux = copy.deepcopy(stkF)
    
    emit_var_bril = plot_bril_comparison(np.array([low_emit_Bril,U30_Bril,high_emit_Bril]))
    emit_var_bril.title('Brilliance vs Emittance')
    emit_var_bril.annotate('Undulator Properties: \n\
        Length: {} m \n\
        Period: {} m\n\
        Peak Field: {} T\n\
E Beam Properties:\n\
        Current: {} A \n\
        Energy: {} GeV'.format(2.0,und30.per, harmB30.B,300,1.7), 
        (3000,2e19))
    
    blue_line = mlines.Line2D([],[],color = 'tab:blue',label = 'Emittance: 0.5 nm')
    orange_line = mlines.Line2D([],[],color = 'tab:orange', label = 'Emittance: 5 nm')
    green_line = mlines.Line2D([],[],color = 'tab:green', label = 'Emittance: 50 nm')
    emit_var_bril.legend(handles = [blue_line, orange_line, green_line], loc = 'upper left')
    
    emit_var_bril.show()
    
    emit_var_flux = plot_flux_comparison(np.array([low_emit_Flux,U30_Flux,hi_emit_Flux]))
    emit_var_flux.legend(handles = [blue_line, orange_line, green_line], loc = 'upper left')
    
    emit_var_flux.title('Flux vs Emittance')
    
    emit_var_flux.annotate('Undulator Properties: \n\
        Length: {} m \n\
        Period: {} m\n\
        Peak Field: {} T\n\
E Beam Properties:\n\
        Current: {} A \n\
        Energy: {} GeV '.format(2.0,und30.per, harmB30.B,300,1.7), 
        (1100,1.05e14))
    
    emit_var_flux.show()
    
    #Energy
    low_en_Bril = srw.bril_und(BII_LoEn,und30,0.3,1,11,1001,1,plotting = False)
    high_en_Bril = srw.bril_und(BII_HiEn,und30,0.3,1,11,1001,1,plotting = False)
    
    srw.srwl.CalcStokesUR(stkF, BII_LoEn, und30, arPrecF)
    low_en_Flux = copy.deepcopy(stkF)
    
    srw.srwl.CalcStokesUR(stkF, BII_HiEn, und30, arPrecF)
    hi_en_Flux = copy.deepcopy(stkF)
    
    en_var_bril = plot_bril_comparison(np.array([low_en_Bril,U30_Bril,high_en_Bril]))
    en_var_bril.title('Brilliance vs Beam Energy')
    en_var_bril.annotate('Undulator Properties: \n\
        Length: {} m \n\
        Period: {} m\n\
        Peak Field: {} T\n\
E Beam Properties:\n\
        Current: {} A \n\
        Emittance: {} nm'.format(2.0,und30.per, harmB30.B,300,5), 
        (3000,2e19))
    
    blue_line = mlines.Line2D([],[],color = 'tab:blue',label = 'Energy: 1.4 GeV nm')
    orange_line = mlines.Line2D([],[],color = 'tab:orange', label = 'Energy: 1.7 GeV nm')
    green_line = mlines.Line2D([],[],color = 'tab:green', label = 'Energy: 2.0 GeV nm')
    en_var_bril.legend(handles = [blue_line, orange_line, green_line], loc = 'upper left')
    
    en_var_bril.show()
    
    en_var_flux = plot_flux_comparison(np.array([low_en_Flux,U30_Flux,hi_en_Flux]))
    en_var_flux.legend(handles = [blue_line, orange_line, green_line], loc = 'upper left')
    
    en_var_flux.title('Flux vs Beam Energy')
    
    base_flux.annotate('Undulator Properties: \n\
        Length: {} m \n\
        Period: {} m\n\
        Peak Field: {} T\n\
E Beam Properties:\n\
        Current: {} A \n\
        Emittance: {} nm'.format(2.0,und30.per, harmB30.B,300,5), 
        (1100,1.05e14))
    
    en_var_flux.show()
    
    print(1)