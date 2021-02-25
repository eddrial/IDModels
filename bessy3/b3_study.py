'''
Created on 24 Feb 2021

@author: oqb
'''
#import Local_SRW as srw
import srwlib as srw
import numpy as np
import wradia as wrd
import radia as rd
import matplotlib.pyplot as plt

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

def UEX():
    UEXH_params = testparams = parameters.model_parameters(periods = 10, 
                                         periodlength = 80,
                                         block_subdivision = [2,1,1],
                                         nominal_fmagnet_dimensions = [40.0,0.0,40.0],
                                         apple_clampcut = 5.0,
                                         magnets_per_period =4,
                                         gap = 11,
                                         rowshift = 0,
                                         rowtorowgap = 1.0,
                                         shiftmode = 'circular',
                                         M = 1.3)
#create model
    UEXH = id.plainAPPLE(UEXH_params)
    
    return UEXH

if __name__ == '__main__':
    #eBeams Structure
    
    BII_lb_eBeam = srw.srwl_uti_src_e_beam('BESSYII Low Beta')
    BII_hb_eBeam = srw.srwl_uti_src_e_beam('BESSYII High Beta')
    BIII_eBeam = srw.srwl_uti_src_e_beam('BESSYIII Beta')
    
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
    UEXH.cont.wradSolve()
    
        
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
    undU17.name = 'U17'
    
    #UE_5eV
    harm5eV = srw.SRWLMagFldH() #magnetic field harmonic
    harm5eV.n = 1 #harmonic number
    harm5eV.h_or_v = 'h' #magnetic field plane: horzontal ('h') or vertical ('v')
    harm5eV.B = 1.28
    
    und5eV = srw.SRWLMagFldU([harm5eV])
    und5eV.per = 0.080 #period length [m]
    und5eV.nPer = int(5.0/und5eV.per) #number of periods (will be rounded to integer)
    und5eV.name = '5eV'
    
    NbEnpts = 1001
    
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
    
    BIII_5eV_Bril = srw.bril_und(BIII_eBeam,und5eV,0.3,1,5,NbEnpts,1,plotting = False)
    
    
    #plots to show stuff
    #BII standards
    BII_Range = srw.plotbril([BII_UE112H_Bril,BII_UE56H_Bril,BII_UE48H_Bril,BII_U41_Bril,BII_U17_Bril],BII_lb_eBeam, ['UE112','UE56','UE48','U41','U17'])
    BII_Range.set_title('Example IDs installed in BESSY II')
    BII_Range.legend()
    
    
    #EMIL comparison
    EMIL_Compare = srw.plotbril([BII_UE48H_Bril,BIII_UE48H_Bril,BII_U17_Bril,BIII_U17_Bril],BII_lb_eBeam, ['BII U48','BIII U48','BII U17','BIII U17'])
    EMIL_Compare.set_title('Comparison of EMIL IDs between BII and BIII')
    EMIL_Compare.legend()
    
    #BIII 5eV
    BIII_5eV = srw.plotbril([BII_UE112H_Bril,BIII_5eV_Bril],BIII_eBeam,['BII_UE112','5eV device {}mm period {} periods'.format(1000*und5eV.per, und5eV.nPer)])
    BIII_5eV.set_title('5eV Device')
    BIII_5eV.set_ylim(1e15, 1e19)
    BIII_5eV.legend()
    
    HVdiff = srw.plotbril([BII_UE112H_Bril,BII_UE112V_Bril],BII_lb_eBeam,['H','V'])
    
    
    #show all the plots
    plt.show()

    
    print(1)
    
    
    input("Press Enter to continue...")
    