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
View from Downstream

~~~~~~~~C1v~C2v~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~            ^z
~~C1h~~~~Q1~Q2~~~~C2h~~            |
~~~~~~~~~~~~~~~~~~~~~~~            __> x
~~C3h~~~~Q3~Q4~~~~C4h~~
~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~C3v~C4v~~~~~~~~


'''
from wradia import wrad_obj as wrd
from wradia import wrad_mat as wrdm
import radia as rd
import numpy as np
import matplotlib.pyplot as plt
from idcomponents import parameters
from idcomponents import magnet_shapes as ms
#from matplotlib.cbook.deprecation import _deprecated_parameter_class
#from uti_plot import *


class model_hyper_parameters():
    
    def __init__(self, **kwargs):
        #general
        prop_defaults = {
            "origin": np.zeros(3), #set the origin of the device. Default is array([0., 0., 0.])
            
            ######  Undulator Parameters  ######
            
            "applePeriods" : 3, # Number of Periods of the APPLE Undulator
            "minimumgap" : 2, # Gap used in calculation in mm
            "rowtorowgap": 0.5, # for APPLE devices the distance between functional rows on the same jaw
            "shim" : 0.05, # The gap between each magnet in a row / magnet array.
            "compappleseparation" : 15.0, # The gap between functional magnets and compenation magnets
            "periodlength" : 15, # The period length of the undulator
            "circlin" : 1, # Polarisation mode of the undulator -1 is circ (parallel), 1 is linear (antiparallel)
            "shift" : 0, # distance of row shift in mm
            "halbach_direction" : 1,  # a value to determine the sense of magnet rotation along the axis. 1 = Field BELOW array. -1 Field ABOVE array 
            
            #####  Magnet Shape  #####
            
            "mainmagdimension" : 30, # The primary magnet dimension for the functional magnets [mm]
            "clampcut" : 5, # The size of the square removed for clamping [mm]
            "direction" : 'y', # The direction of extrusion - along the direction of travel of the electrons. Dimensions propogate in the order [z,y,x]
        
            #####  Compensation Magnets #####
            
            # "compmagdimensions" : [15.0,self.mainmagthick,30.0] # dimensions of the compensation magnets [mm]
            
            #####  Magnet Material #####
            
            "ksi" : [.019, .06], # Permeability - anisotropic
            "M" : 1.21*1.344, # Block Remanence [T]
            "Mova" : 0.0 # Off Vertical Angle of Vertical type magnet blocks [degrees]
        }
        
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))
        
        ###Derived Attributes###
        
        #Undulator
        self.appleMagnets = int(self.applePeriods*4 + 1);
        
        #magnet shape
        self.mainmagthick = (self.periodlength-4 * self.shim) / 4.0

        
        #compensation magnets
        self.compmagdimensions = [15.0,self.mainmagthick,30.0]
        
        #magnetmaterial
        self.magnet_material = wrdm.wradMatLin(self.ksi,[0,0,self.M])
        
        
        #wrd.wradObj
    

'''def compMagnet(parameter_class, mag_center, magnet_material, loc_offset = [0,0,0]):
    #[z,y,x]
    
    a = wrd.wradObjCnt([])
    
    p1 = wrd.wradObjThckPgn(loc_offset[1], parameter_class.mainmagthick, [[loc_offset[0]-parameter_class.compmagdimensions[0]/2.0,loc_offset[2]-parameter_class.compmagdimensions[2]/2.0],
                                                              [loc_offset[0]-parameter_class.compmagdimensions[0]/2.0,loc_offset[2]+parameter_class.compmagdimensions[2]/2.0],
                                                              [loc_offset[0]+parameter_class.compmagdimensions[0]/2.0 - parameter_class.clampcut,loc_offset[2]+parameter_class.compmagdimensions[2]/2.0],
                                                              [loc_offset[0]+parameter_class.compmagdimensions[0]/2.0 - parameter_class.clampcut,loc_offset[2]-parameter_class.compmagdimensions[2]/2.0]], 
                                                              parameter_class.direction)
    p2 = wrd.wradObjThckPgn(loc_offset[1], parameter_class.mainmagthick, [[loc_offset[0]+parameter_class.compmagdimensions[0]/2,loc_offset[2]-parameter_class.compmagdimensions[2]/2 + parameter_class.clampcut/2.0],
                                                              [loc_offset[0]+parameter_class.compmagdimensions[0]/2,loc_offset[2]+parameter_class.compmagdimensions[2]/2 - parameter_class.clampcut/2.0],
                                                              [loc_offset[0]+parameter_class.compmagdimensions[0]/2 - parameter_class.clampcut,loc_offset[2]+parameter_class.compmagdimensions[2]/2 - parameter_class.clampcut/2.0],
                                                              [loc_offset[0]+parameter_class.compmagdimensions[0]/2 - parameter_class.clampcut,loc_offset[2]-parameter_class.compmagdimensions[2]/2 + parameter_class.clampcut/2.0]], 
                                                              parameter_class.direction)
    
    a.wradObjAddToCnt([p1,p2])
    a.wradMatAppl(magnet_material)
    
    return a'''

def compHArray(parameter_class, loc_offset, halbach_direction = -1):
    a = wrd.wradObjCnt([])
    
    loc_offset[1] = -((parameter_class.appleMagnets-1)/2.0) * (parameter_class.mainmagthick+parameter_class.shim)
    M = []
    mat = []
    for i in range(4):
        M.append([halbach_direction * np.cos(i*np.pi/2.0)*parameter_class.M*np.sin(2*np.pi*parameter_class.Mova/360.0),halbach_direction * np.sin(i*np.pi/2.0)*parameter_class.M, np.cos(i*np.pi/2.0)*parameter_class.M * np.cos(2*np.pi*parameter_class.Mova/360.0)])
        mat.append(wrdm.wradMatLin(parameter_class.ksi,M[i]))
    
    for x in range(0,parameter_class.appleMagnets):
        
        mag = compMagnet(parameter_class, loc_offset[1], mat[x%4], loc_offset) 
        loc_offset[1] += parameter_class.mainmagthick + parameter_class.shim
        magcol = [(2 + y) / 4.0 for y in M[x%4]]
        print(magcol)
        mag.wradObjDrwAtr(magcol, 2) # [x / myInt for x in myList]
        mag.wradObjDivMag([2,3,1])
        a.wradObjAddToCnt([mag])
    
    
    return a


def compVArray(parameter_class, loc_offset, halbach_direction = -1):
    a = wrd.wradObjCnt([])
    
    loc_offset[1] = -((parameter_class.appleMagnets-1)/2.0) * (parameter_class.mainmagthick+parameter_class.shim)
    M = []
    mat = []
    for i in range(4):
        #M.append([np.sin(i*np.pi/2.0)*parameter_class.M*np.sin(2*np.pi*parameter_class.Mova/360.0),np.sin(i*np.pi/2.0)*parameter_class.M * np.cos(2*np.pi*parameter_class.Mova/360.0),halbach_direction * np.cos(i*np.pi/2.0)*parameter_class.M])
        M.append([-halbach_direction * np.cos(i*np.pi/2.0)*parameter_class.M*np.cos(2*np.pi*parameter_class.Mova/360.0),halbach_direction * np.sin(i*np.pi/2.0)*parameter_class.M, np.cos(i*np.pi/2.0)*parameter_class.M * np.sin(2*np.pi*parameter_class.Mova/360.0)])
        mat.append(wrdm.wradMatLin(parameter_class.ksi,M[i]))
    
    for x in range(0,parameter_class.appleMagnets):
        
        mag = compMagnet(parameter_class, loc_offset[1], mat[x%4], loc_offset) 
        loc_offset[1] += parameter_class.mainmagthick + parameter_class.shim
        magcol = [(2 + y) / 4.0 for y in M[x%4]]
        mag.wradObjDrwAtr(magcol, 2) # [x / myInt for x in myList]
        mag.wradObjDivMag([2,3,1])
        a.wradObjAddToCnt([mag])
        
    a.wradRotate([0,0,0], [0,1,0], np.pi/2.0)
    
    
    return a

def compUpperBeam(parameter_class):
    a = wrd.wradObjCnt([])
    
    q1v = compVArray(parameter_class, [0,0,-parameter_class.compappleseparation], halbach_direction = -1)
#    q1h
#    q2v
#    q2h
    
    a.wradObjAddToCnt([q1v])
    
    return a

def compLowerBeam():
    return

def compBothBeams():
    return


'''def appleMagnet(parameter_class, mag_center, magnet_material, loc_offset = [0,0,0]):'''
'''orientation order z,y,x'''
'''    a = wrd.wradObjCnt([])
#    a.magnet_material = magnet_material
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
    
    a.cont.wradObjAddToCnt([p1,p2,p3])
    a.cont.wradMatAppl(magnet_material)
    
    return a'''

def appleArray(parameter_class, loc_offset, halbach_direction = -1):
    a = wrd.wradObjCnt([])
    
    loc_offset[1] += -((parameter_class.appleMagnets-1)/2.0) * (parameter_class.mainmagthick+parameter_class.shim)
    M = []
    mat = []
    for i in range(4):
        #M.append([halbach_direction * np.sin(i*np.pi/2.0)*parameter_class.M*np.sin(2*np.pi*parameter_class.Mova/360.0),halbach_direction * np.sin(i*np.pi/2.0)*parameter_class.M * np.cos(2*np.pi*parameter_class.Mova/360.0), np.cos(i*np.pi/2.0)*parameter_class.M])
        M.append([np.cos(i*np.pi/2.0)*parameter_class.M*np.sin(2*np.pi*parameter_class.Mova/360.0),halbach_direction * np.sin(i*np.pi/2.0)*parameter_class.M, np.cos(i*np.pi/2.0)*parameter_class.M * np.cos(2*np.pi*parameter_class.Mova/360.0)])
        
        mat.append(wrdm.wradMatLin(parameter_class.ksi,M[i]))
    
    for x in range(-int((parameter_class.appleMagnets-1)/2),int(1+(parameter_class.appleMagnets-1)/2)):#0,parameter_class.appleMagnets
        
        mag = ms.appleMagnet(parameter_class, loc_offset) 
        loc_offset[1] += parameter_class.mainmagthick + parameter_class.shim
        magcol = [(2 + y) / 4.0 for y in M[(x)%4]]
        mag.wradObjDrwAtr(magcol, 2) # [x / myInt for x in myList]
        mag.wradObjDivMag([2,3,1])
        a.wradObjAddToCnt([mag])
        
    return a
        
    #mag = appleMagnet(AII,4,materiald,[z,y,x])
    #mag apply magnetisation and colour
    #add to container

def appleLowerBeam(parameter_class):
    halbach_direction = - 1 ##Field ABOVE the Halbach array
    q3 = appleArray(parameter_class, [-parameter_class.mainmagdimension/2.0 - parameter_class.minimumgap/2.0,0,-parameter_class.mainmagdimension/2.0 - parameter_class.rowtorowgap/2.0], halbach_direction)
    q4 = appleArray(parameter_class, [-parameter_class.mainmagdimension/2.0 - parameter_class.minimumgap/2.0, parameter_class.circlin * parameter_class.shift,-parameter_class.mainmagdimension/2.0 - parameter_class.rowtorowgap/2.0], halbach_direction)
    
    q4.wradReflect(parameter_class.origin, [1,0,0])
    
    a = wrd.wradObjCnt([])
    a.wradObjAddToCnt([q3,q4])
    
    return a
    

def appleUpperBeam(parameter_class):
    halbach_direction = 1 ##Field BELOW the Halbach array
    q1 = appleArray(parameter_class, [parameter_class.mainmagdimension/2.0 + parameter_class.minimumgap/2.0, parameter_class.circlin * parameter_class.shift,parameter_class.mainmagdimension/2.0 + parameter_class.rowtorowgap/2.0], halbach_direction)
    q2 = appleArray(parameter_class, [parameter_class.mainmagdimension/2.0 + parameter_class.minimumgap/2.0, 0,parameter_class.mainmagdimension/2.0 + parameter_class.rowtorowgap/2.0], halbach_direction)
    
    q1.wradReflect(parameter_class.origin, [1,0,0])
    
    a = wrd.wradObjCnt([])
    a.wradObjAddToCnt([q1,q2])
    
    return a

def appleComplete(parameter_class):
    ##### UPPER BEAM #####
    halbach_direction = 1 ##Field BELOW the Halbach array
    q1 = appleArray(parameter_class, [parameter_class.mainmagdimension/2.0 + parameter_class.minimumgap/2.0, parameter_class.circlin * parameter_class.shift,parameter_class.mainmagdimension/2.0 + parameter_class.rowtorowgap/2.0], halbach_direction)
    q2 = appleArray(parameter_class, [parameter_class.mainmagdimension/2.0 + parameter_class.minimumgap/2.0, 0,parameter_class.mainmagdimension/2.0 + parameter_class.rowtorowgap/2.0], halbach_direction)
    
    q1.wradReflect(parameter_class.origin, [1,0,0])
    
    ##### LOWER BEAM #####
    halbach_direction = - 1 ##Field ABOVE the Halbach array
    q3 = appleArray(parameter_class, [-parameter_class.mainmagdimension/2.0 - parameter_class.minimumgap/2.0,0,-parameter_class.mainmagdimension/2.0 - parameter_class.rowtorowgap/2.0], halbach_direction)
    q4 = appleArray(parameter_class, [-parameter_class.mainmagdimension/2.0 - parameter_class.minimumgap/2.0, parameter_class.circlin * parameter_class.shift,-parameter_class.mainmagdimension/2.0 - parameter_class.rowtorowgap/2.0], halbach_direction)
    
    q4.wradReflect(parameter_class.origin, [1,0,0])
    
    a = wrd.wradObjCnt([])
    a.wradObjAddToCnt([q1,q2,q3,q4])
    
    return a


    ###Old Way
#    ub = appleUpperBeam(parameter_class)
#    lb = appleLowerBeam(parameter_class)
#    
#    ap = wrd.wradObjCnt([])
#    ap.wradObjAddToCnt([ub,lb])
    
#    return ap

def compensatedAppleComplete(parameter_class, style = "symmetric"):
    ##### FUNCTIONAL MAGNETS #####
    ##### UPPER BEAM #####
    halbach_direction = 1 ##Field BELOW the Halbach array
    q1 = appleArray(parameter_class, [parameter_class.mainmagdimension/2.0 + parameter_class.minimumgap/2.0, parameter_class.circlin * parameter_class.shift,parameter_class.mainmagdimension/2.0 + parameter_class.rowtorowgap/2.0], halbach_direction)
    q2 = appleArray(parameter_class, [parameter_class.mainmagdimension/2.0 + parameter_class.minimumgap/2.0, 0,parameter_class.mainmagdimension/2.0 + parameter_class.rowtorowgap/2.0], halbach_direction)
    
    q1.wradReflect(parameter_class.origin, [1,0,0])
    
    ##### LOWER BEAM #####
    halbach_direction = - 1 ##Field ABOVE the Halbach array
    q3 = appleArray(parameter_class, [-parameter_class.mainmagdimension/2.0 - parameter_class.minimumgap/2.0,0,-parameter_class.mainmagdimension/2.0 - parameter_class.rowtorowgap/2.0], halbach_direction)
    q4 = appleArray(parameter_class, [-parameter_class.mainmagdimension/2.0 - parameter_class.minimumgap/2.0, parameter_class.circlin * parameter_class.shift,-parameter_class.mainmagdimension/2.0 - parameter_class.rowtorowgap/2.0], halbach_direction)
    
    q4.wradReflect(parameter_class.origin, [1,0,0])
    
    ##### Q1 Compensation Magnets #####
    q1v = compVArray(parameter_class, [-parameter_class.compmagdimensions[0]/2.0 - parameter_class.rowtorowgap/2.0,
                                       0,
                                       -parameter_class.compmagdimensions[2]/2.0 - parameter_class.minimumgap/2.0 - parameter_class.mainmagdimension-parameter_class.compappleseparation], 
                                       halbach_direction = 1)
    
    q1h  = compHArray(parameter_class,[-parameter_class.compmagdimensions[0]/2.0 - parameter_class.minimumgap/2.0,
                                       0,
                                       -parameter_class.compmagdimensions[2]/2.0 - parameter_class.rowtorowgap/2.0 - parameter_class.mainmagdimension-parameter_class.compappleseparation],
                                       halbach_direction = -1)
    
    q1h.wradReflect(parameter_class.origin, [0,0,1])
    
    ##### Q2 Compensation Magnets #####
    q2v = compVArray(parameter_class, [-parameter_class.compmagdimensions[0]/2.0 - parameter_class.rowtorowgap/2.0,
                                       0,
                                       -parameter_class.compmagdimensions[2]/2.0 - parameter_class.minimumgap/2.0 - parameter_class.mainmagdimension-parameter_class.compappleseparation], 
                                       halbach_direction = -1)
    
    q2h  = compHArray(parameter_class,[-parameter_class.compmagdimensions[0]/2.0 - parameter_class.minimumgap/2.0,
                                       0,
                                       -parameter_class.compmagdimensions[2]/2.0 - parameter_class.rowtorowgap/2.0 - parameter_class.mainmagdimension-parameter_class.compappleseparation],
                                       halbach_direction = -1)
    
    q2v.wradReflect(parameter_class.origin, [1,0,0])
    q2h.wradRotate(parameter_class.origin,[0,1,0],np.pi)
    q2h.wradFieldInvert()
    
    ##### Q3 Compensation Magnets #####
    q3v = compVArray(parameter_class, [-parameter_class.compmagdimensions[0]/2.0 - parameter_class.rowtorowgap/2.0,
                                       0,
                                       parameter_class.compmagdimensions[2]/2.0 + parameter_class.minimumgap/2.0 + parameter_class.mainmagdimension + parameter_class.compappleseparation], 
                                       halbach_direction = -1)
    
    q3h  = compHArray(parameter_class,[-parameter_class.compmagdimensions[0]/2.0 - parameter_class.minimumgap/2.0,
                                       0,
                                       -parameter_class.compmagdimensions[2]/2.0 - parameter_class.rowtorowgap/2.0 - parameter_class.mainmagdimension-parameter_class.compappleseparation],
                                       halbach_direction = -1)
    
    q3v.wradFieldInvert()
    
    ##### Q4 Compensation Magnets #####
    q4v = compVArray(parameter_class, [-parameter_class.compmagdimensions[0]/2.0 - parameter_class.rowtorowgap/2.0,
                                       0,
                                       -parameter_class.compmagdimensions[2]/2.0 - parameter_class.minimumgap/2.0 - parameter_class.mainmagdimension-parameter_class.compappleseparation], 
                                       halbach_direction = 1)
    
    q4h  = compHArray(parameter_class,[-parameter_class.compmagdimensions[0]/2.0 - parameter_class.minimumgap/2.0,
                                       0,
                                       -parameter_class.compmagdimensions[2]/2.0 - parameter_class.rowtorowgap/2.0 - parameter_class.mainmagdimension-parameter_class.compappleseparation],
                                       halbach_direction = -1)
    
    q4h.wradReflect(parameter_class.origin, [1,0,0])
    q4h.wradFieldInvert()
    q4v.wradRotate(parameter_class.origin,[0,1,0],np.pi)
    
    a = wrd.wradObjCnt([])
    a.wradObjAddToCnt([q1,q1h,q1v,q2,q2h,q2v,q3,q3h,q3v,q4,q4h,q4v])
    
    return a

if __name__ == '__main__':
    
    #my parameter list
    '''    origin = np.zeros(3)
    mainmagthick = 5
    mainmagdimension = 30
    clamput = 5
    direction = 'y'
    '''
    #ATHENA_II Parameters
    AII = parameters.model_hyper_parameters()
    
    #magnet Material [Bx,By,Bz]
    mat1 = wrdm.wradMatLin(AII.ksi,[0,0,AII.M])
    
    #my magnet model
    
    a = ms.appleMagnet(AII)
    magcol = [(2+x) / 4.0 for x in [0,AII.M,0]]
    a.cont.wradObjDrwAtr(magcol, 2)
    a.cont.wradObjDivMag([3,2,1])
    
    a1 = ms.compMagnet(AII,[0,0,0])
    a1.cont.wradObjDrwAtr(magcol, 2)
    a1.cont.wradObjDivMag([3,2,1])
    
#    rd.ObjDrwOpenGL(a.radobj)
#    rd.ObjDrwOpenGL(a1.radobj)
    
    #my beam model
    #halbach direction describes the relative rotation of magnetisation as you progress downstream. 
    #1 = clockwise, -1 = anticlockwise
    halbach_direction = 1
    b = appleArray(AII, [-AII.mainmagdimension/2.0 - AII.minimumgap,0,-AII.mainmagdimension/2.0 - AII.rowtorowgap], halbach_direction)
    b1 = compVArray(AII, [-AII.mainmagdimension/2.0 - AII.minimumgap,0,-AII.mainmagdimension/2.0 - AII.rowtorowgap], halbach_direction)
    b1i = compVArray(AII, [-AII.mainmagdimension/2.0 - AII.minimumgap,0,-AII.mainmagdimension/2.0 - AII.rowtorowgap], halbach_direction)
    b1i.wradReflect([0,0,0], [1,0,0])
    
    b2 = compHArray(AII, [-AII.mainmagdimension/2.0 - AII.minimumgap,0,-AII.mainmagdimension/2.0 - AII.rowtorowgap], halbach_direction)
    
#    rd.ObjDrwOpenGL(b.radobj)
#    rd.ObjDrwOpenGL(b1.radobj)
#    rd.ObjDrwOpenGL(b1i.radobj)

    
    c = appleLowerBeam(AII)
    d = appleUpperBeam(AII)
    
    e = appleComplete(AII)
    
    f = compensatedAppleComplete(AII)
    
    #comp upper beam
#    f = compUpperBeam(AII)
    
#    rd.ObjDrwOpenGL(f.radobj)
    #comp lower beam
    
    #rota = rd.TrfRot([0,0,0],[1,1,1],np.pi/7.0)
#    rd.ObjDrwOpenGL(c.radobj)
#    rd.ObjDrwOpenGL(d.radobj)
#    rd.ObjDrwOpenGL(e.radobj)
    rd.ObjDrwOpenGL(f.radobj)
    #EXAMPLES OF TRANSFORMATIONS
    #b.wradRotate([0,0,0],[1,0,0],np.pi)
    
    #b.wradTranslate([10,20,30])
        
    #b.wradReflect([0,0,0], [4,1,1])
    
    #Lower APPLE BEAM
    
    
    #my apple model
    print(AII.origin)
    print(b.objectlist)
    
    #rd.ObjDrwOpenGL(a.radobj)
    #rd.ObjDrwOpenGL(b.radobj)
    
    
    #######PLOT SOMETHING#######################
    tmpob = f
    tmpob.wradSolve(0.001, 1000)
    
    z = 0; x1 = -15; x2 = 0; ymax = 400; nump = 2001
    
    Bz1 = rd.FldLst(tmpob.radobj, 'bz', [x1,-ymax,z], [x1,ymax,z], nump, 'arg', 0)
    Bz2 = rd.FldLst(tmpob.radobj, 'bz', [x2,-ymax,z], [x2,ymax,z], nump, 'arg',0 )
    
    Bx1 = rd.FldLst(tmpob.radobj, 'bx', [x1,-ymax,z], [x1,ymax,z], nump, 'arg', 0)
    Bx2 = rd.FldLst(tmpob.radobj, 'bx', [x2,-ymax,z], [x2,ymax,z], nump, 'arg',0 )
    
    Bz1 = np.array(Bz1)
    Bz2 = np.array(Bz2)

    Bx1 = np.array(Bx1)
    Bx2 = np.array(Bx2)
    
    #set up plot
    # set width and height
    width = 7
    height = 9
    
    #create the figure with nice margins
    fig, axs = plt.subplots(2,1, sharex = False, sharey = False)
    fig.subplots_adjust(left=.15, bottom=.16, right=.85, top= 0.9, wspace = 0.7, hspace = 0.6)
    fig.set_size_inches(width, height)
    
    
    axs[0].plot(Bz1[:,0],Bz1[:,1])
    axs[0].plot(Bx1[:,0],Bx1[:,1])
    axs[1].plot(Bz2[:,0],Bz2[:,1])
    axs[1].plot(Bx2[:,0],Bx2[:,1])
    
    plt.show()
    
#    uti_plot1d_m([Bz1,Bz2],
#                 labels=['Y', 'Vertical Magnetic Field', 'Vertical Magnetic Field vs. Vertical Position'], units=['mm', 'T'],
#                 styles=['-b.', '--r.'], legend=['X = {} mm'.format(x1), 'X = {} mm'.format(x2)])
    
    
#input("Press Enter to continue...")
    
    # All examples built from
    #basemagnet = wrd.wradObjThckPgn(0, AII.mainmagthick, [[-5,-5],[-5,5],[5,5],[5,-5]], AII.direction)


# After you have done the vertical compensation magnets. Maybe call the upnunder magnets.
#four uu magnet arrays
#four lr magnet arrays
#apple array already done.

#four cases. One for each quadrant.
#Force and Torque. Once the four cases are built, solving for force and torque should be easy.
#Then just saving out and plotting the data.
#that's all there is to it, right?a