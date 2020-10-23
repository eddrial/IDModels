'''
Created on 24 Sep 2020

@author: oqb
'''

from wradia import wrad_obj as wrd

from idcomponents import parameters

class appleMagnet():
    '''
    classdocs
    '''
    def __init__(self, model_parameters = parameters.model_parameters(), magnet_centre  = [0,0,0], this_magnet_material = 0):
        
        '''
        Constructor
        '''
        
        mp = model_parameters
        self.magnet_centre = magnet_centre
        
        if this_magnet_material == 0:
            this_magnet_material = mp.magnet_material
        
        '''orientation order z,y,x'''
        self.cont = wrd.wradObjCnt([])  # Container
    #    a.magnet_material = magnet_material
        p1 = wrd.wradObjThckPgn(magnet_centre[1], mp.nominal_fmagnet_dimensions[1], [[magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2 + mp.apple_clampcut,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2 + mp.apple_clampcut,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2 - mp.apple_clampcut,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2 - mp.apple_clampcut,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2]], 
                                                                  mp.direction)
        p2 = wrd.wradObjThckPgn(magnet_centre[1], mp.nominal_fmagnet_dimensions[1], [[magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2 - mp.apple_clampcut],
                                                                  [magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2 + mp.apple_clampcut,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2 - mp.apple_clampcut],
                                                                  [magnet_centre[0]-mp.nominal_fmagnet_dimensions[0]/2 + mp.apple_clampcut,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2]], 
                                                                  mp.direction)
        p3 = wrd.wradObjThckPgn(magnet_centre[1], mp.nominal_fmagnet_dimensions[1], [[magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2 + mp.apple_clampcut],
                                                                  [magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2 - mp.apple_clampcut,magnet_centre[2]+mp.nominal_fmagnet_dimensions[2]/2],
                                                                  [magnet_centre[0]+mp.nominal_fmagnet_dimensions[0]/2 - mp.apple_clampcut,magnet_centre[2]-mp.nominal_fmagnet_dimensions[2]/2 + mp.apple_clampcut]], 
                                                                  mp.direction)
        
        self.cont.wradObjAddToCnt([p1,p2,p3])
        self.cont.wradMatAppl(this_magnet_material)
        
class compMagnet():
    '''
    classdocs
    '''
    def __init__(self, model_parameters = parameters.model_parameters(), magnet_centre  = [0,0,0], this_magnet_material = 0):
                
        '''
        Constructor
        '''
        
        mp = model_parameters
        self.magnet_centre = magnet_centre
        if this_magnet_material == 0:
            this_magnet_material = mp.magnet_material
        '''orientation order z,y,x'''
        self.cont = wrd.wradObjCnt([])
        
        p1 = wrd.wradObjThckPgn(magnet_centre[1], model_parameters.nominal_cmagnet_dimensions[1], [[magnet_centre[0]-model_parameters.nominal_cmagnet_dimensions[0]/2.0,magnet_centre[2]-model_parameters.nominal_cmagnet_dimensions[2]/2.0],
                                                                  [magnet_centre[0]-model_parameters.nominal_cmagnet_dimensions[0]/2.0,magnet_centre[2]+model_parameters.nominal_cmagnet_dimensions[2]/2.0],
                                                                  [magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2.0 - model_parameters.comp_magnet_chamfer[0],magnet_centre[2]+model_parameters.nominal_cmagnet_dimensions[2]/2.0],
                                                                  [magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2.0 - model_parameters.comp_magnet_chamfer[0],magnet_centre[2]-model_parameters.nominal_cmagnet_dimensions[2]/2.0]], 
                                                                  model_parameters.direction)
        p2 = wrd.wradObjThckPgn(magnet_centre[1], model_parameters.nominal_cmagnet_dimensions[1], [[magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2,magnet_centre[2]-model_parameters.nominal_cmagnet_dimensions[2]/2 + model_parameters.comp_magnet_chamfer[2]/2.0],
                                                                  [magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2,magnet_centre[2]+model_parameters.nominal_cmagnet_dimensions[2]/2.0 - model_parameters.comp_magnet_chamfer[2]/2.0],
                                                                  [magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2.0 - model_parameters.comp_magnet_chamfer[0],magnet_centre[2]+model_parameters.nominal_cmagnet_dimensions[2]/2 - model_parameters.comp_magnet_chamfer[2]/2.0],
                                                                  [magnet_centre[0]+model_parameters.nominal_cmagnet_dimensions[0]/2.0 - model_parameters.comp_magnet_chamfer[0],magnet_centre[2]-model_parameters.nominal_cmagnet_dimensions[2]/2 + model_parameters.comp_magnet_chamfer[2]/2.0]], 
                                                                  model_parameters.direction)
        
        self.cont.wradObjAddToCnt([p1,p2])
        self.cont.wradMatAppl(this_magnet_material)
        
        
if __name__ == '__main__':
    a = appleMagnet()
    b = compMagnet()
    
    print('{}{}'.format(a.cont.radobj,b.cont.radobj))
    
        