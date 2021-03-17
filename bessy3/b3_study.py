'''
Created on 24 Feb 2021

@author: oqb
'''
#import Local_SRW as srw
import srwlib as srw
import uti_plot as uplt
import numpy as np
import wradia as wrd
import radia as rd
import matplotlib.pyplot as plt
import copy

from idcomponents import parameters
from idanalysis import analysis_functions as af
from apple2p5 import model2 as id

def UE112():
    UE112H_params = testparams = parameters.model_parameters(periods = 10, 
                                         periodlength = 112,
                                         block_subdivision = [2,1,1],
                                         nominal_fmagnet_dimensions = [40.0,0.0,40.0],
                                         apple_clampcut = 5.0,
                                         comp_magnet_chamfer = [3.0,0.0,3.0],
                                         magnets_per_period =4,
                                         gap = 22.9,
                                         rowshift = 56,
                                         rowtorowgap = 1.2,
                                         shiftmode = 'circular',
                                         M = 1.2)
#create model
    UE112H = id.plainAPPLE(UE112H_params)
    
    return UE112H

def UEX(periodlength = 120, gap = 13, rowshift = 0):
    UEXH_params = testparams = parameters.model_parameters(periods = 10, 
                                         periodlength = periodlength,
                                         block_subdivision = [2,1,1],
                                         nominal_fmagnet_dimensions = [40.0,0.0,40.0],
                                         apple_clampcut = 5.0,
                                         magnets_per_period =4,
                                         gap =gap,
                                         rowshift = rowshift,
                                         rowtorowgap = 1.0,
                                         shiftmode = 'circular',
                                         M = 1.3)
#create model
    UEXH = id.plainAPPLE(UEXH_params)
    
    return UEXH

def BrillFromLambdaU(name, length, periodlength, gap, rowshift, eBeam):
    und_wrad = UEX(periodlength, gap, rowshift)
    
    und_wrad.cont.wradSolve()
    
        
    #solving the case
    und_wrad_case = af.CaseSolution(und_wrad)
    und_wrad_case.calculate_B_field()
    
    bmax = und_wrad_case.bmax
    
    harm,harm.n, harm.h_or_v, harm.B  = srw.SRWLMagFldH(), 1, 'h', bmax
    und, und.per, und.name, und.gap = srw.SRWLMagFldU([harmXU80]), periodlength/1000, name, gap
    und.nPer = int(length/und.per)
    Bril = srw.bril_und(eBeam,und,0.3,1,11,NbEnpts,1,plotting = False)
    
    return Bril, und, harm
    

if __name__ == '__main__':
    #eBeams Structure
    
    BII_lb_eBeam = srw.srwl_uti_src_e_beam('BESSYII Low Beta')
    BII_hb_eBeam = srw.srwl_uti_src_e_beam('BESSYII High Beta')
    BIII_eBeam = srw.srwl_uti_src_e_beam('BESSYIII Beta')
    
    #General Parameters
    straight_length = 4.5
    short_straight_length = 2
    
    NbEnpts = 1001
    
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
    
    #undulators
    #UE112
    UE112H = UE112()
    print('p')    
    UE112H.cont.wradSolve()
    
        
        #solving the case
    UE112Hcase = af.CaseSolution(UE112H)
    UE112Hcase.calculate_B_field()
    print(UE112Hcase.bmax)

    UEXH = UEX()
    print('p')    
    UEXHcase = af.CaseSolution(UEXH)
    UEXHcase.calculate_B_field()
    UEXH.cont.wradSolve()
    print('peak field at 13mm is {}'.format(UEXHcase.bmax))
    
        
        #solving the case
    UEXHcase = af.CaseSolution(UEXH)
    UEXHcase.calculate_B_field()
    print(UEXHcase.bmax)    
    print('p')    
    #calculate Bmax
    #create srwundulator
    #UE56
    #create model
    #calculate Bmx
    #create srwundulator
    #U41
    #create model
    #create srwundulator
    #U17
    #create model
    #calculate Bmax
    #create srwundulator
    #UE48
    #create model
    #calculate Bmax
    #create srwundulator
    
    
    #magnet Structure
    harmB = srw.SRWLMagFldH() #magnetic field harmonic
    harmB.n = 1 #harmonic number
    harmB.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmB.B = 1.25 #magnetic field amplitude [T]
    
    
    und = srw.SRWLMagFldU([harmB])
    und.per = 0.080 #period length [m]
    und.nPer = 62 #number of periods (will be rounded to integer)
    und.name = 'UE80'
    
    #From XYP values
    #UE112
    harmUE112H = srw.SRWLMagFldH() #magnetic field harmonic
    harmUE112H.n = 1 #harmonic number
    harmUE112H.h_or_v = 'h' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmUE112H.B = 0.938
    
    undUE112H = srw.SRWLMagFldU([harmUE112H])
    undUE112H.per = 0.112 #period length [m]
    undUE112H.nPer = 33 #number of periods (will be rounded to integer)
    undUE112H.name = 'UE112H'
    
    harmUE112V = srw.SRWLMagFldH() #magnetic field harmonic
    harmUE112V.n = 1 #harmonic number
    harmUE112V.h_or_v = 'h' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmUE112V.B = 0.664
    
    undUE112V = srw.SRWLMagFldU([harmUE112V])
    undUE112V.per = 0.112 #period length [m]
    undUE112V.nPer = 33 #number of periods (will be rounded to integer)
    undUE112V.name = 'UE112V'
    
    #UE56
    harmUE56H = srw.SRWLMagFldH() #magnetic field harmonic
    harmUE56H.n = 1 #harmonic number
    harmUE56H.h_or_v = 'h' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmUE56H.B = 0.732
    
    undUE56H = srw.SRWLMagFldU([harmUE56H])
    undUE56H.per = 0.056 #period length [m]
    undUE56H.nPer = 30 #number of periods (will be rounded to integer)
    undUE56H.name = 'UE56H'
    
    harmUE56V = srw.SRWLMagFldH() #magnetic field harmonic
    harmUE56V.n = 1 #harmonic number
    harmUE56V.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmUE56V.B = 0.49
    
    undUE56V = srw.SRWLMagFldU([harmUE56V])
    undUE56V.per = 0.056 #period length [m]
    undUE56V.nPer = 30 #number of periods (will be rounded to integer)
    undUE56V.name = 'UE56V'
    
    #UE48
    harmUE48H = srw.SRWLMagFldH() #magnetic field harmonic
    harmUE48H.n = 1 #harmonic number
    harmUE48H.h_or_v = 'h' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmUE48H.B = 0.76
    
    undUE48H = srw.SRWLMagFldU([harmUE48H])
    undUE48H.per = 0.048 #period length [m]
    undUE48H.nPer = 29 #number of periods (will be rounded to integer)
    undUE48H.name = 'UE48H'
    
    harmUE48V = srw.SRWLMagFldH() #magnetic field harmonic
    harmUE48V.n = 1 #harmonic number
    harmUE48V.h_or_v = 'v' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmUE48V.B = 0.519
    
    undUE48V = srw.SRWLMagFldU([harmUE48V])
    undUE48V.per = 0.048 #period length [m]
    undUE48V.nPer = 29 #number of periods (will be rounded to integer)
    undUE48V.name = 'UE48V'
    
    #U41
    harmU41 = srw.SRWLMagFldH() #magnetic field harmonic
    harmU41.n = 1 #harmonic number
    harmU41.h_or_v = 'h' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmU41.B = 0.63
    
    undU41 = srw.SRWLMagFldU([harmU41])
    undU41.per = 0.0412 #period length [m]
    undU41.nPer = 80 #number of periods (will be rounded to integer)
    undU41.name = 'U41'

    
    #CPMU17
    harmU17 = srw.SRWLMagFldH() #magnetic field harmonic
    harmU17.n = 1 #harmonic number
    harmU17.h_or_v = 'h' #magnetic field plane: horzontal ('h') or vertical ('v')
    harmU17.B = 1.15
    
    undU17 = srw.SRWLMagFldU([harmU17])
    undU17.per = 0.017 #period length [m]
    undU17.nPer = 80 #number of periods (will be rounded to integer)
    undU17.name = 'U17_80period'
    
    undU17_120 = srw.SRWLMagFldU([harmU17])
    undU17_120.per = 0.017 #period length [m]
    undU17_120.nPer = 120 #number of periods (will be rounded to integer)
    undU17_120.name = 'U17_120 periods'
    
    
    
    ####### Peak_Field_Undulators ######
    #XU112
    harmXU112,harmXU112.n, harmXU112.h_or_v, harmXU112.B  = srw.SRWLMagFldH(), 1, 'h', 1.15
    undXU112, undXU112.per, undXU112.name, undXU112.gap = srw.SRWLMagFldU([harmXU112]), 0.112, 'XU112', 0.013
    undXU112.nPer = int(straight_length/undXU112.per)
    BIII_XU112_Bril = srw.bril_und(BIII_eBeam,undXU112,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU80
    harmXU80,harmXU80.n, harmXU80.h_or_v, harmXU80.B  = srw.SRWLMagFldH(), 1, 'h', 1.15
    undXU80, undXU80.per, undXU80.name, undXU80.gap = srw.SRWLMagFldU([harmXU80]), 0.08, 'XU80', 0.013
    undXU80.nPer = int(straight_length/undXU80.per)
    BIII_XU80_Bril = srw.bril_und(BIII_eBeam,undXU80,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU70
    harmXU70,harmXU70.n, harmXU70.h_or_v, harmXU70.B  = srw.SRWLMagFldH(), 1, 'h', 1.11
    undXU70, undXU70.per, undXU70.name, undXU70.gap = srw.SRWLMagFldU([harmXU70]), 0.07, 'XU70', 0.013
    undXU70.nPer = int(straight_length/undXU70.per)
    BIII_XU80_Bril = srw.bril_und(BIII_eBeam,undXU80,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU60
    harmXU60,harmXU60.n, harmXU60.h_or_v, harmXU60.B  = srw.SRWLMagFldH(), 1, 'h', 1.04
    undXU60, undXU60.per, undXU60.name, undXU60.gap = srw.SRWLMagFldU([harmXU60]), 0.06, 'XU60', 0.013
    undXU60.nPer = int(straight_length/undXU60.per)
    BIII_XU60_Bril = srw.bril_und(BIII_eBeam,undXU60,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU50
    harmXU50,harmXU50.n, harmXU50.h_or_v, harmXU50.B  = srw.SRWLMagFldH(), 1, 'h', 0.95
    undXU50, undXU50.per, undXU50.name, undXU50.gap = srw.SRWLMagFldU([harmXU50]), 0.05, 'XU50', 0.013
    undXU50.nPer = int(straight_length/undXU50.per)
    BIII_XU50_Bril = srw.bril_und(BIII_eBeam,undXU50,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU40
    harmXU40,harmXU40.n, harmXU40.h_or_v, harmXU40.B  = srw.SRWLMagFldH(), 1, 'h', 0.78
    undXU40, undXU40.per, undXU40.name, undXU40.gap = srw.SRWLMagFldU([harmXU40]), 0.04, 'XU40', 0.013
    undXU40.nPer = int(straight_length/undXU40.per)
    BIII_XU40_Bril = srw.bril_und(BIII_eBeam,undXU40,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU30
    harmXU30,harmXU30.n, harmXU30.h_or_v, harmXU30.B  = srw.SRWLMagFldH(), 1, 'h', 0.56
    undXU30, undXU30.per, undXU30.name, undXU30.gap = srw.SRWLMagFldU([harmXU30]), 0.03, 'XU30', 0.013
    undXU30.nPer = int(straight_length/undXU30.per)
    BIII_XU30_Bril = srw.bril_und(BIII_eBeam,undXU30,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU25
    harmXU25,harmXU25.n, harmXU25.h_or_v, harmXU25.B  = srw.SRWLMagFldH(), 1, 'h', 0.43
    undXU25, undXU25.per, undXU25.name, undXU25.gap = srw.SRWLMagFldU([harmXU25]), 0.025, 'XU25', 0.013
    undXU25.nPer = int(straight_length/undXU25.per)
    BIII_XU25_Bril = srw.bril_und(BIII_eBeam,undXU25,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU20
    harmXU20,harmXU20.n, harmXU20.h_or_v, harmXU20.B  = srw.SRWLMagFldH(), 1, 'h', 0.29
    undXU20, undXU20.per, undXU20.name, undXU20.gap = srw.SRWLMagFldU([harmXU20]), 0.02, 'XU20', 0.013
    undXU20.nPer = int(straight_length/undXU20.per)
    BIII_XU20_Bril = srw.bril_und(BIII_eBeam,undXU20,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU20_5mm_2m
    harmXU20_5mm_2m,harmXU20_5mm_2m.n, harmXU20_5mm_2m.h_or_v, harmXU20_5mm_2m.B  = srw.SRWLMagFldH(), 1, 'h', 0.96
    undXU20_5mm_2m, undXU20_5mm_2m.per, undXU20_5mm_2m.name, undXU20_5mm_2m.gap = srw.SRWLMagFldU([harmXU20_5mm_2m]), 0.02, 'XU20_5mm_2m', 0.013
    undXU20_5mm_2m.nPer = int(short_straight_length/undXU20_5mm_2m.per)
    BIII_XU20_5mm_2m_Bril = srw.bril_und(BIII_eBeam,undXU20_5mm_2m,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU20_4mm_2m
    harmXU20_4mm_2m,harmXU20_4mm_2m.n, harmXU20_4mm_2m.h_or_v, harmXU20_4mm_2m.B  = srw.SRWLMagFldH(), 1, 'h', 1.1
    undXU20_4mm_2m, undXU20_4mm_2m.per, undXU20_4mm_2m.name, undXU20_4mm_2m.gap = srw.SRWLMagFldU([harmXU20_4mm_2m]), 0.02, 'XU20_4mm_2m', 0.013
    undXU20_4mm_2m.nPer = int(short_straight_length/undXU20_4mm_2m.per)
    BIII_XU20_4mm_2m_Bril = srw.bril_und(BIII_eBeam,undXU20_4mm_2m,0.3,1,11,NbEnpts,1,plotting = False)
    
    ### BIII suggestions
    #XU56
    harmXU56,harmXU56.n, harmXU56.h_or_v, harmXU56.B  = srw.SRWLMagFldH(), 1, 'h', 1.01
    undXU56, undXU56.per, undXU56.name, undXU56.gap = srw.SRWLMagFldU([harmXU56]), 0.056, 'XU56', 0.013
    undXU56.nPer = int(straight_length/undXU56.per)
    BIII_XU56_Bril = srw.bril_und(BIII_eBeam,undXU56,0.3,1,11,NbEnpts,1,plotting = False)    
    
    #XU49
    harmXU49,harmXU49.n, harmXU49.h_or_v, harmXU49.B  = srw.SRWLMagFldH(), 1, 'h', 1.0
    undXU49, undXU49.per, undXU49.name, undXU49.gap = srw.SRWLMagFldU([harmXU49]), 0.049, 'XU49', 0.013
    undXU49.nPer = int(straight_length/undXU49.per)
    BIII_XU49_Bril = srw.bril_und(BIII_eBeam,undXU49,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU48
    harmXU48,harmXU48.n, harmXU48.h_or_v, harmXU48.B  = srw.SRWLMagFldH(), 1, 'h', 0.91
    undXU48, undXU48.per, undXU48.name, undXU48.gap = srw.SRWLMagFldU([harmXU48]), 0.048, 'XU48', 0.013
    undXU48.nPer = int(straight_length/undXU48.per)
    BIII_XU48_Bril = srw.bril_und(BIII_eBeam,undXU48,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU46
    harmXU46,harmXU46.n, harmXU46.h_or_v, harmXU46.B  = srw.SRWLMagFldH(), 1, 'h', 0.877
    undXU46, undXU46.per, undXU46.name, undXU46.gap = srw.SRWLMagFldU([harmXU46]), 0.046, 'XU46', 0.013
    undXU46.nPer = int(straight_length/undXU46.per)
    BIII_XU46_Bril = srw.bril_und(BIII_eBeam,undXU46,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU52
    harmXU52,harmXU52.n, harmXU52.h_or_v, harmXU52.B  = srw.SRWLMagFldH(), 1, 'h', 0.967
    undXU52, undXU52.per, undXU52.name, undXU52.gap = srw.SRWLMagFldU([harmXU52]), 0.052, 'XU52', 0.013
    undXU52.nPer = int(straight_length/undXU52.per)
    BIII_XU52_Bril = srw.bril_und(BIII_eBeam,undXU52,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU38
    harmXU38,harmXU38.n, harmXU38.h_or_v, harmXU38.B  = srw.SRWLMagFldH(), 1, 'h', 0.728
    undXU38, undXU38.per, undXU38.name, undXU38.gap = srw.SRWLMagFldU([harmXU38]), 0.038, 'XU38', 0.013
    undXU38.nPer = int(straight_length/undXU38.per)
    BIII_XU38_Bril = srw.bril_und(BIII_eBeam,undXU38,0.3,1,11,NbEnpts,1,plotting = False)
    
    #XU32
    harmXU32,harmXU32.n, harmXU32.h_or_v, harmXU32.B  = srw.SRWLMagFldH(), 1, 'h', 1.1
    undXU32, undXU32.per, undXU32.name, undXU32.gap = srw.SRWLMagFldU([harmXU32]), 0.032, 'XU32', 0.006
    undXU32.nPer = int(straight_length/undXU32.per)
    BIII_XU32_Bril = srw.bril_und(BIII_eBeam,undXU32,0.3,1,11,NbEnpts,1,plotting = False)
    
    
    #UE_5eV
    harm5eV = srw.SRWLMagFldH() #magnetic field harmonic
    harm5eV.n = 1 #harmonic number
    harm5eV.h_or_v = 'h' #magnetic field plane: horzontal ('h') or vertical ('v')
    harm5eV.B = 1.24
    
    und5eV = srw.SRWLMagFldU([harm5eV])
    und5eV.per = 0.120 #period length [m]
    und5eV.nPer = int(straight_length/und5eV.per) #number of periods (will be rounded to integer)
    und5eV.name = '5eV'
    

    
    BII_UE112H_Bril = srw.bril_und(BII_lb_eBeam,undUE112H,0.3,1,5,NbEnpts,1,plotting = False)
    BII_UE112V_Bril = srw.bril_und(BII_lb_eBeam,undUE112V,0.3,1,5,NbEnpts,1,plotting = False)
    BIII_UE112H_Bril = srw.bril_und(BIII_eBeam,undUE112H,0.3,1,5,NbEnpts,1,plotting = False)
    BIII_UE112V_Bril = srw.bril_und(BIII_eBeam,undUE112V,0.3,1,5,NbEnpts,1,plotting = False)
    
    
    BII_UE56H_Bril = srw.bril_und(BII_lb_eBeam,undUE56H,0.3,1,5,NbEnpts,1,plotting = False)
    BII_UE56V_Bril = srw.bril_und(BII_lb_eBeam,undUE56V,0.3,1,5,NbEnpts,1,plotting = False)
    BIII_UE56H_Bril = srw.bril_und(BIII_eBeam,undUE56H,0.3,1,5,NbEnpts,1,plotting = False)
    BIII_UE56V_Bril = srw.bril_und(BIII_eBeam,undUE56V,0.3,1,5,NbEnpts,1,plotting = False)
    
    BII_UE48H_Bril = srw.bril_und(BII_lb_eBeam,undUE48H,0.3,1,5,NbEnpts,1,plotting = False)
    BII_UE48V_Bril = srw.bril_und(BII_lb_eBeam,undUE48V,0.3,1,5,NbEnpts,1,plotting = False)
    BIII_UE48H_Bril = srw.bril_und(BIII_eBeam,undUE48H,0.3,1,5,NbEnpts,1,plotting = False)
    BIII_UE48V_Bril = srw.bril_und(BIII_eBeam,undUE48V,0.3,1,5,NbEnpts,1,plotting = False)
    
    BII_U41_Bril = srw.bril_und(BII_hb_eBeam,undU41,0.3,1,9,NbEnpts,1,plotting = False)
    BIII_U41_Bril = srw.bril_und(BIII_eBeam,undU41,0.3,1,9,NbEnpts,1,plotting = False)
    
    BII_U17_Bril = srw.bril_und(BII_hb_eBeam,undU17,0.3,1,9,NbEnpts,1,plotting = False)
    BIII_U17_Bril = srw.bril_und(BIII_eBeam,undU17,0.3,1,9,NbEnpts,1,plotting = False)
    BIII_U17_120_Bril = srw.bril_und(BIII_eBeam,undU17_120,0.3,1,9,NbEnpts,1,plotting = False)
    
    BIII_5eV_Bril = srw.bril_und(BIII_eBeam,und5eV,0.3,1,5,NbEnpts,1,plotting = False)
    
    
    #plots to show brilliances
    #BII standards
    BII_Range = srw.plotbril([BII_UE112H_Bril,BII_UE56H_Bril,BII_UE48H_Bril,BII_U41_Bril,BII_U17_Bril],BII_lb_eBeam, ['UE112','UE56','UE48','U41','U17'])
    BII_Range = srw.plotbril([BII_UE112H_Bril,BII_UE48H_Bril,BII_U41_Bril,BII_U17_Bril],BII_lb_eBeam, ['UE112','UE48','U41','U17'])
    BII_Range.set_title('Example IDs installed in BESSY II')
    BII_Range.legend()
    
    
    #EMIL comparison
    EMIL_Compare = srw.plotbril([BII_UE48H_Bril,BIII_UE48H_Bril,BII_U17_Bril,BIII_U17_Bril],BII_lb_eBeam, ['BII U48','BIII U48','BII U17','BIII U17'])
    EMIL_Compare.set_title('Comparison of EMIL IDs between BII and BIII')
    EMIL_Compare.legend()
    
    #BIII eXample Undulators
    BIII_Example = srw.plotbril([BIII_XU112_Bril, BIII_XU40_Bril, BIII_XU30_Bril, BIII_XU20_Bril], BIII_eBeam,
                                ['BIII_U112','BIII_U40','BIII_U30','BIII_U20'])
    BIII_Example.set_title('Ex-Vac APPLEs in BIII')
    BIII_Example.legend()
    
    #BIII eXample 20mm period
    BIII_Example_20mm = srw.plotbril([BIII_XU20_Bril, BIII_XU30_Bril, BIII_XU20_4mm_2m_Bril], BIII_eBeam,
                                     ['U20, 5m, 13mm gap','U30, 5m, 13mm gap', 'U20, 2m, 4mm gap'])
    BIII_Example_20mm.set_title('Impact of Gap')
    BIII_Example_20mm.legend()
    
    #U17 #Periods vs Brilliance
    BIII_U17_Length = srw.plotbril([BIII_U17_Bril,BIII_U17_120_Bril], BIII_eBeam,
                                   ['80 Period U17', '120 Period U17'])
    BIII_U17_Length.set_title('Impact of Period Number')
    BIII_U17_Length.legend()
    
    #UE56 BESSY III
    BIII_UE56_Length = srw.plotbril([BIII_XU56_Bril], BIII_eBeam,
                                   ['UE56, 13mm gap, 4.5m length'])
    BIII_UE56_Length.set_title('UE56 for BIII Stand 3.3.21')
    BIII_UE56_Length.legend()
    
        #U49 BESSY III
    BIII_U49_Length = srw.plotbril([BIII_XU49_Bril], BIII_eBeam,
                                   ['U49, 13mm gap, 4.5m length'])
    BIII_U49_Length.set_title('U49 for BIII Stand 3.3.21')
    BIII_U49_Length.legend()
    
        #UE48 BESSY III
    BIII_UE48_Length = srw.plotbril([BIII_XU48_Bril], BIII_eBeam,
                                   ['UE48, 13mm gap, 4.5m length'])
    BIII_UE48_Length.set_title('UE48 for BIII Stand 3.3.21')
    BIII_UE48_Length.legend()
    
    #UE49 BESSY III
    BIII_UE49_Length = srw.plotbril([BIII_XU49_Bril], BIII_eBeam,
                                   ['UE49, 13mm gap, 4.5m length'])
    BIII_UE49_Length.set_title('UE49 for BIII Stand 3.3.21')
    BIII_UE49_Length.legend()
    
    #UE46 BESSY III
    BIII_UE46_Length = srw.plotbril([BIII_XU46_Bril], BIII_eBeam,
                                   ['UE46, 13mm gap, 4.5m length'])
    BIII_UE46_Length.set_title('UE46 for BIII Stand 3.3.21')
    BIII_UE46_Length.legend()
    
    #UE52 BESSY III
    BIII_UE52_Length = srw.plotbril([BIII_XU52_Bril], BIII_eBeam,
                                   ['UE52, 13mm gap, 4.5m length'])
    BIII_UE52_Length.set_title('UE52 for BIII Stand 3.3.21')
    BIII_UE52_Length.legend()
    
    #UE38 BESSY III
    BIII_UE38_Length = srw.plotbril([BIII_XU38_Bril], BIII_eBeam,
                                   ['UE38, 13mm gap, 4.5m length'])
    BIII_UE38_Length.set_title('UE38 for BIII Stand 3.3.21')
    BIII_UE38_Length.legend()
    
    #UE32 BESSY III
    BIII_UE32_Length = srw.plotbril([BIII_XU32_Bril], BIII_eBeam,
                                   ['IVUE32,6mm gap, 4.5m length'])
    BIII_UE32_Length.set_title('IVUE32 for BIII Stand 3.3.21')
    BIII_UE32_Length.legend()
    
    #BIII 5eV
    BIII_5eV = srw.plotbril([BII_UE112H_Bril,BIII_5eV_Bril],BIII_eBeam,['BII_UE112','5eV device {}mm period {} periods'.format(1000*und5eV.per, und5eV.nPer)])
    BIII_5eV.set_title('5eV Device')
    BIII_5eV.set_ylim(1e15, 1e21)
    BIII_5eV.legend()
    
    #In Vac vs Ex Vac APPLE
    BIII_IVUE38_Bril, IVUE38_und, IVUE38_harm = BrillFromLambdaU('IVUE38', straight_length, 38, 6.5, 0, BIII_eBeam)
    BIII_IVUE38_vlong_Bril, IVUE38_vlong_und, IVUE38_vlong_harm = BrillFromLambdaU('IVUE38', 10*straight_length, 38, 6.5, 0, BIII_eBeam)
    
    
    BIII_IVUE39_Bril, IVUE39_und, IVUE39_harm = BrillFromLambdaU('IVUE39', straight_length, 39, 6.5, 0, BIII_eBeam)
    
    BIII_IVvsEV = srw.plotbril([BIII_IVUE38_Bril, BIII_IVUE38_vlong_Bril], BIII_eBeam, ['BIII_IVUE38 6mm aperture', 'BIII_IVUE38_vlong'])
    BIII_IVvsEV.set_title('In-Vac vs Ex-Vac APPLE')
    BIII_IVvsEV.set_ylim(1e17, 1e23)
    BIII_IVvsEV.legend()
    
    #HVdiff = srw.plotbril([BII_UE112H_Bril,BII_UE112V_Bril],BII_lb_eBeam,['H','V'])
    
    
    #Flux through aperture 1mmx1mm aperture at 30m
    print('   Performing Spectral Flux (Stokes parameters) calculation ... ', end='')
    srw.srwl.CalcStokesUR(stkF, BIII_eBeam, undU17, arPrecF)
    BIII_U17_Flux = copy.deepcopy(stkF)
    
    srw.srwl.CalcStokesUR(stkF, BIII_eBeam, undU17_120, arPrecF)
    BIII_U17_120_Flux = copy.deepcopy(stkF)
    
    
    print('done')
    f, ax = plt.subplots()
    ax.plot(np.linspace(BIII_U17_120_Flux.mesh.eStart, BIII_U17_120_Flux.mesh.eFin, BIII_U17_120_Flux.mesh.ne),np.array(BIII_U17_120_Flux.arS)[0:BIII_U17_120_Flux.mesh.ne],label ='120 Period CPMU17')
    ax.plot(np.linspace(BIII_U17_Flux.mesh.eStart, BIII_U17_Flux.mesh.eFin, BIII_U17_Flux.mesh.ne),np.array(BIII_U17_Flux.arS)[0:BIII_U17_Flux.mesh.ne], label = '80 Period CPMU17')
    
    ax.set_title('80 vs 120 period CPMU17 @ BESSYIII')
    ax.set_xlabel('Photon Energy')
    ax.set_ylabel('Flux (Ph/s/0.1%bw/mmm^2@30m)')
    
    ax.set_xlim(0,10000)
    
    
    ax.legend()
    #show all the plots
    plt.show()

    
    print(1)
    
    
    input("Press Enter to continue...")
    