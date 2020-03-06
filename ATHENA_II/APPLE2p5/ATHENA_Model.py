'''
Created on 3 Mar 2020

@author: oqb

NOTE on ORIENTATION.

Dimensions given as three element list relative to direction of extrusion:
[z,y,x] when extrusion direction is y,
[y,x,z] when extrusion direction is x,
[x,z,y] when extrusion direction is z.

Holds for 2d coordinates in perpendicular plane.

For This Model, y is electron direction, x is transverse, z is vertical
'''
from wRadia import wradObj as wrd
from wRadia import wradMat
import radia as rd
import numpy as np

class model_parameters():
    
    def __init__(self):
        #general
        self.origin = np.zeros(3)

        
        #Undulator
        self.applePeriods = 10;
        self.appleMagnets = self.applePeriods*4 + 1;
        self.minimumgap = 2
        self.rowtorowgap = 0.5
        self.shim = 0.05
        self.periodlength = 15
        
        #magnet shape
        self.mainmagthick = (self.periodlength-4 * self.shim) / 4.0
        self.mainmagdimension = 30
        self.clampcut = 5
        self.direction = 'y'
        
        #magnetmaterial
        self.ksi = [.019, .06]
        self.M = 1.21*1.344
        self.magnet_material = wradMat.wradMatLin(self.ksi,self.M)
        
        #wrd.wradObj
    


def appleMagnet(parameter_class, mag_center, magnet_material, loc_offset = [0,0,0]):
    '''orientation order z,y,x'''
    a = wrd.wradObjCnt([])
    a.magnet_material = magnet_material
    p1 = wrd.wradObjThckPgn(loc_offset[1], parameter_class.mainmagthick, [[loc_offset[0]-parameter_class.mainmagdimension/2 + parameter_class.clampcut,loc_offset[2]-parameter_class.mainmagdimension/2],
                                                              [loc_offset[0]-parameter_class.mainmagdimension/2 + parameter_class.clampcut,loc_offset[2]+parameter_class.mainmagdimension/2],
                                                              [loc_offset[0]+parameter_class.mainmagdimension/2 - parameter_class.clampcut,loc_offset[2]+parameter_class.mainmagdimension/2],
                                                              [loc_offset[0]+parameter_class.mainmagdimension/2 - parameter_class.clampcut,loc_offset[2]-parameter_class.mainmagdimension/2]], 
                                                              parameter_class.direction)
    p2 = wrd.wradObjThckPgn(loc_offset[1], parameter_class.mainmagthick, [[loc_offset[0]-parameter_class.mainmagdimension/2,loc_offset[2]-parameter_class.mainmagdimension/2],
                                                              [loc_offset[0]-parameter_class.mainmagdimension/2,loc_offset[2]+parameter_class.mainmagdimension/2 - parameter_class.clampcut],
                                                              [loc_offset[0]-parameter_class.mainmagdimension/2 + parameter_class.clampcut,loc_offset[2]+parameter_class.mainmagdimension/2 - parameter_class.clampcut],
                                                              [loc_offset[0]-parameter_class.mainmagdimension/2 + parameter_class.clampcut,loc_offset[2]-parameter_class.mainmagdimension/2]], 
                                                              parameter_class.direction)
    p3 = wrd.wradObjThckPgn(loc_offset[1], parameter_class.mainmagthick, [[loc_offset[0]+parameter_class.mainmagdimension/2,loc_offset[2]-parameter_class.mainmagdimension/2 + parameter_class.clampcut],
                                                              [loc_offset[0]+parameter_class.mainmagdimension/2,loc_offset[2]+parameter_class.mainmagdimension/2],
                                                              [loc_offset[0]+parameter_class.mainmagdimension/2 - parameter_class.clampcut,loc_offset[2]+parameter_class.mainmagdimension/2],
                                                              [loc_offset[0]+parameter_class.mainmagdimension/2 - parameter_class.clampcut,loc_offset[2]-parameter_class.mainmagdimension/2 + parameter_class.clampcut]], 
                                                              parameter_class.direction)
    
    a.wradObjAddToCnt([p1,p2,p3])
    a.wradMatAppl(a.magnet_material)
    
    return a

def appleArray(parameter_class,loc_offset, magnet_material):
    a = wrd.wradObjCnt([])
    for x in range(0,parameter_class.appleMagnets):
        mag = appleMagnet(parameter_class, loc_offset[1], magnet_material, loc_offset) 
        loc_offset[1] += 10
        a.wradObjAddToCnt([mag])
        
    return a
        
    #mag = appleMagnet(AII,4,materiald,[z,y,x])
    #mag apply magnetisation and colour
    #add to container

def appleTotal():
    pass

if __name__ == '__main__':
    
    #my parameter list
    '''    origin = np.zeros(3)
    mainmagthick = 5
    mainmagdimension = 30
    clamput = 5
    direction = 'y'
    '''
    #ATHENA_II Parameters
    AII = model_parameters()
    
    #magnet Material
    mat1 = wradMat.wradMatLin(AII.ksi,[0,AII.M,0])
    
    #my magnet model
    
    a = appleMagnet(AII,4,mat1,[10,20,30])
    magcol = [x / 2.0 for x in [0,AII.M,0]]
    a.wradObjDrwAtr([x / 2.0 for x in [1,AII.M,0]], 2)
    a.wradObjDivMag([3,2,1])
    
    #my beam model
    
    b = appleArray(AII, [-AII.mainmagdimension/2.0 - AII.minimumgap,0,-AII.mainmagdimension/2.0 - AII.rowtorowgap], mat1)
    
    #my apple model
    print(AII.origin)
    print(a.objectlist)
    
    rd.ObjDrwOpenGL(a.radobj)
    rd.ObjDrwOpenGL(b.radobj)
    
    
    
    input("Press Enter to continue...")
    
    # All examples built from
    #basemagnet = wrd.wradObjThckPgn(0, AII.mainmagthick, [[-5,-5],[-5,5],[5,5],[5,-5]], AII.direction)
