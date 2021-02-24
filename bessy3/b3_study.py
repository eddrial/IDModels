'''
Created on 24 Feb 2021

@author: oqb
'''
#import Local_SRW as srw
import srwlib as srw
import numpy as np
import wradia as wrd

from apple2p5 import model2 as id

if __name__ == '__main__':
    #eBeams Structure
    
    BII_lb_eBeam = srw.srwl_uti_src_e_beam('BESSYII Low Beta')
    BII_hb_eBeam = srw.srwl_uti_src_e_beam('BESSYII High Beta')
    BIII_eBeam = srw.srwl_uti_src_e_beam('BESSYIII Beta')
    
    #undulators
    #UE112
    def UE112():
        id.plainAPPLE
    #create model
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
    
    NbEnpts = 1001
    
    BII_U80_Bril = srw.bril_und(BII_lb_eBeam,und,0.3,1,11,NbEnpts,1,plotting = False)
    BIII_U80_Bril = srw.bril_und(BIII_eBeam,und,0.3,1,11,NbEnpts,1,plotting = False)
    
    srw.plotbril([BII_U80_Bril,BIII_U80_Bril],BII_lb_eBeam, und)
    
    print(1)
    
    
    input("Press Enter to continue...")
    