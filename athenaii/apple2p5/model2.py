'''
Created on 23 Oct 2020

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
from idcomponents import halbach_arrays as ha

class plainAPPLE():
    '''
    classdocs
    '''
    def __init__(self, 
                 model_parameters = parameters.model_parameters(),
                 fmagnet = ms.appleMagnet, 
                 cmagnet = ms.compMagnet, 
                 gap = 50, 
                 rowshift = 0,
                 jawshift = 0, 
                 shiftmode = 'circular'):
        
        self.cont = wrd.wradObjCnt([])
        
        mp = model_parameters
        
        if shiftmode == 'circular':
            shiftmodesign = 1
        elif shiftmode == 'linear':
            shiftmodesign = -1
        else:
            shiftmodesign = 0
        
        self.allarrays = {'q1' : ha.HalbachArray(model_parameters,fmagnet),
                          'q2' : ha.HalbachArray(model_parameters,fmagnet),
                          'q3' : ha.HalbachArray(model_parameters,fmagnet),
                          'q4' : ha.HalbachArray(model_parameters,fmagnet)
                          }
        
        ##### Functional Magnets #####
        
        ### Q1 ###
        self.allarrays['q1'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 rowshift,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q1'].cont.wradFieldInvert()
        self.allarrays['q1'].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        
        
        ### Q2 ###
        self.allarrays['q2'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q2'].cont.wradFieldInvert()
        self.allarrays['q2'].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        self.allarrays['q2'].cont.wradReflect([0,0,0],[1,0,0])
        
        ### Q3 ###
        self.allarrays['q3'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q3'].cont.wradReflect([0,0,0],[1,0,0])
        
        ### Q4 ###
        self.allarrays['q4'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 rowshift*shiftmodesign,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        
        
        for key in self.allarrays:
            self.cont.wradObjAddToCnt([self.allarrays[key].cont])
        
        print('my APPLE calculated at a gap of {}mm'.format(gap))

class compensatedAPPLEv1():
    '''
    classdocs
    '''
    def __init__(self, 
                 model_parameters = parameters.model_parameters(),
                 fmagnet = ms.appleMagnet, 
                 cmagnet = ms.compMagnet, 
                 gap = 2, 
                 rowshift = 0,
                 jawshift = 0, 
                 shiftmode = 'circular'):
        
        self.cont = wrd.wradObjCnt([])
        
        mp = model_parameters
        
        if shiftmode == 'circular':
            shiftmodesign = 1
        elif shiftmode == 'linear':
            shiftmodesign = -1
        else:
            shiftmodesign = 0
        
        self.allarrays = {'q1' : ha.HalbachArray(model_parameters,fmagnet),
                          'q2' : ha.HalbachArray(model_parameters,fmagnet),
                          'q3' : ha.HalbachArray(model_parameters,fmagnet),
                          'q4' : ha.HalbachArray(model_parameters,fmagnet),
                          'c1v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c1h' : ha.HalbachArray(model_parameters,cmagnet),
                          'c2v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c2h' : ha.HalbachArray(model_parameters,cmagnet),
                          'c3v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c3h' : ha.HalbachArray(model_parameters,cmagnet),
                          'c4v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c4h' : ha.HalbachArray(model_parameters,cmagnet),
                          }
        
        ##### Functional Magnets #####
        
        ### Q1 ###
        self.allarrays['q1'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 rowshift,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q1'].cont.wradFieldInvert()
        self.allarrays['q1'].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        
        
        ### Q2 ###
        self.allarrays['q2'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q2'].cont.wradFieldInvert()
        self.allarrays['q2'].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        self.allarrays['q2'].cont.wradReflect([0,0,0],[1,0,0])
        
        ### Q3 ###
        self.allarrays['q3'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q3'].cont.wradReflect([0,0,0],[1,0,0])
        
        ### Q4 ###
        self.allarrays['q4'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 rowshift*shiftmodesign,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        
        
        ##### Compensation Magnets #####
        
        ### C1h ###
        self.allarrays['c1h'].cont.wradTranslate([-(mp.nominal_cmagnet_dimensions[2] + mp.rowtorowgap + 2 * (mp.nominal_fmagnet_dimensions[0] + mp.compappleseparation))/2.0,
                                                 rowshift,
                                                 -(mp.nominal_cmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['c1h'].cont.wradFieldInvert()
        self.allarrays['c1h'].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        
        ### C2h ###
        self.allarrays['c2h'].cont.wradTranslate([(mp.nominal_cmagnet_dimensions[2] + mp.rowtorowgap + 2 * (mp.nominal_fmagnet_dimensions[0] + mp.compappleseparation))/2.0,
                                                 0.0,
                                                 -(mp.nominal_cmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['c2h'].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        
        ### C3h ###
        self.allarrays['c3h'].cont.wradTranslate([-(mp.nominal_cmagnet_dimensions[2] + mp.rowtorowgap + 2 * (mp.nominal_fmagnet_dimensions[0] + mp.compappleseparation))/2.0,
                                                 0.0,
                                                 -(mp.nominal_cmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['c3h'].cont.wradFieldInvert()
        self.allarrays['c3h'].cont.wradReflect([0,0,0],[1,0,0])
        
        ### C4h ###
        self.allarrays['c4h'].cont.wradTranslate([(mp.nominal_cmagnet_dimensions[2] + mp.rowtorowgap + 2 * (mp.nominal_fmagnet_dimensions[0] + mp.compappleseparation))/2.0,
                                                 rowshift*shiftmodesign,
                                                 -(mp.nominal_cmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['c4h'].cont.wradReflect([0,0,0],[1,0,0])
        
        ### C1v ###
        self.allarrays['c1v'].cont.wradRotate([0,0,0],[0,1,0],-np.pi/2)
        self.allarrays['c1v'].cont.wradFieldRotate([0,0,0],[0,1,0],-np.pi/2)
        self.allarrays['c1v'].cont.wradTranslate([(mp.nominal_cmagnet_dimensions[2]/2.0 + mp.rowtorowgap)/2.0,
                                                 rowshift,
                                                 (mp.nominal_cmagnet_dimensions[2] + gap + 2 * (mp.nominal_fmagnet_dimensions[2] + mp.compappleseparation))/2.0])

        ### C2v ###
        self.allarrays['c2v'].cont.wradRotate([0,0,0],[0,1,0],-np.pi/2)
        self.allarrays['c2v'].cont.wradFieldRotate([0,0,0],[0,1,0],-np.pi/2)
        self.allarrays['c2v'].cont.wradFieldInvert()
        self.allarrays['c2v'].cont.wradReflect([0,0,0],[1,0,0])
        self.allarrays['c2v'].cont.wradTranslate([-(mp.nominal_cmagnet_dimensions[2]/2.0 + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 (mp.nominal_cmagnet_dimensions[2] + gap + 2 * (mp.nominal_fmagnet_dimensions[2] + mp.compappleseparation))/2.0])

        ### C3v ###
        self.allarrays['c3v'].cont.wradRotate([0,0,0],[0,1,0],-np.pi/2)
        self.allarrays['c3v'].cont.wradFieldRotate([0,0,0],[0,1,0],np.pi/2)
        self.allarrays['c3v'].cont.wradTranslate([(mp.nominal_cmagnet_dimensions[2]/2.0 + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 (mp.nominal_cmagnet_dimensions[2] + gap + 2 * (mp.nominal_fmagnet_dimensions[2] + mp.compappleseparation))/2.0])
        self.allarrays['c3v'].cont.wradReflect([0,0,0],[0,0,1])
        
        ### C4v ###
        self.allarrays['c4v'].cont.wradRotate([0,0,0],[0,1,0],np.pi/2)
        self.allarrays['c4v'].cont.wradFieldRotate([0,0,0],[0,1,0],-np.pi/2)
        self.allarrays['c4v'].cont.wradTranslate([-(mp.nominal_cmagnet_dimensions[2]/2.0 + mp.rowtorowgap)/2.0,
                                                 rowshift*shiftmodesign,
                                                 -(mp.nominal_cmagnet_dimensions[2] + gap + 2 * (mp.nominal_fmagnet_dimensions[2] + mp.compappleseparation))/2.0])
        
        
        
        for key in self.allarrays:
            self.cont.wradObjAddToCnt([self.allarrays[key].cont])
        
        print('my compensated APPLE calculated at a gap of {}mm'.format(gap))

class compensatedAPPLEv2():
    '''
    classdocs
    '''
    def __init__(self, 
                 model_parameters = parameters.model_parameters(),
                 fmagnet = ms.appleMagnet, 
                 cmagnet = ms.compMagnet, 
                 gap = 50, 
                 rowshift = 0,
                 jawshift = 0, 
                 shiftmode = 'circular'):
        
        self.cont = wrd.wradObjCnt([])
        
        mp = model_parameters
        
        if shiftmode == 'circular':
            shiftmodesign = 1
        elif shiftmode == 'linear':
            shiftmodesign = -1
        else:
            shiftmodesign = 0
        
        self.allarrays = {'q1' : ha.HalbachArray(model_parameters,fmagnet),
                          'q2' : ha.HalbachArray(model_parameters,fmagnet),
                          'q3' : ha.HalbachArray(model_parameters,fmagnet),
                          'q4' : ha.HalbachArray(model_parameters,fmagnet),
                          'c1v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c1h' : ha.HalbachArray(model_parameters,cmagnet),
                          'c2v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c2h' : ha.HalbachArray(model_parameters,cmagnet),
                          'c3v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c3h' : ha.HalbachArray(model_parameters,cmagnet),
                          'c4v' : ha.HalbachArray(model_parameters,cmagnet),
                          'c4h' : ha.HalbachArray(model_parameters,cmagnet),
                          }
        
        ##### Functional Magnets #####
        
        ### Q1 ###
        self.allarrays['q1'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 rowshift,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q1'].cont.wradFieldInvert()
        self.allarrays['q1'].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        
        
        ### Q2 ###
        self.allarrays['q2'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q2'].cont.wradFieldInvert()
        self.allarrays['q2'].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        self.allarrays['q2'].cont.wradReflect([0,0,0],[1,0,0])
        
        ### Q3 ###
        self.allarrays['q3'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['q3'].cont.wradReflect([0,0,0],[1,0,0])
        
        ### Q4 ###
        self.allarrays['q4'].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 rowshift*shiftmodesign,
                                                 -(mp.nominal_fmagnet_dimensions[0] + gap)/2.0])
        
        
        ##### Compensation Magnets #####
        
        ### C1h ###
        self.allarrays['c1h'].cont.wradTranslate([-(mp.nominal_cmagnet_dimensions[2] + mp.rowtorowgap + 2 * (mp.nominal_fmagnet_dimensions[0] + mp.compappleseparation))/2.0,
                                                 rowshift,
                                                 -(mp.nominal_cmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['c1h'].cont.wradFieldInvert()
        self.allarrays['c1h'].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        
        ### C2h ###
        self.allarrays['c2h'].cont.wradTranslate([-(mp.nominal_cmagnet_dimensions[2] + mp.rowtorowgap + 2 * (mp.nominal_fmagnet_dimensions[0] + mp.compappleseparation))/2.0,
                                                 0.0,
                                                 -(mp.nominal_cmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['c2h'].cont.wradReflect([0,0,0],[0,0,1])
        
        ### C3h ###
        self.allarrays['c3h'].cont.wradTranslate([-(mp.nominal_cmagnet_dimensions[2] + mp.rowtorowgap + 2 * (mp.nominal_fmagnet_dimensions[0] + mp.compappleseparation))/2.0,
                                                 0.0,
                                                 -(mp.nominal_cmagnet_dimensions[0] + gap)/2.0])
        self.allarrays['c3h'].cont.wradFieldInvert()
        self.allarrays['c3h'].cont.wradReflect([0,0,0],[1,0,0])
        
        ### C4h ###
        self.allarrays['c4h'].cont.wradTranslate([-(mp.nominal_cmagnet_dimensions[2] + mp.rowtorowgap + 2 * (mp.nominal_fmagnet_dimensions[0] + mp.compappleseparation))/2.0,
                                                 rowshift*shiftmodesign,
                                                 -(mp.nominal_cmagnet_dimensions[0] + gap)/2.0])
        
        ### C1v ###
        self.allarrays['c1v'].cont.wradRotate([0,0,0],[0,1,0],-np.pi/2)
        self.allarrays['c1v'].cont.wradFieldRotate([0,0,0],[0,1,0],np.pi/2)
        self.allarrays['c1v'].cont.wradTranslate([(mp.nominal_cmagnet_dimensions[2]/2.0 + mp.rowtorowgap)/2.0,
                                                 rowshift,
                                                 (mp.nominal_cmagnet_dimensions[2] + gap + 2 * (mp.nominal_fmagnet_dimensions[2] + mp.compappleseparation))/2.0])

        ### C2v ###
        self.allarrays['c2v'].cont.wradRotate([0,0,0],[0,1,0],np.pi/2)
        self.allarrays['c2v'].cont.wradFieldRotate([0,0,0],[0,1,0],-np.pi/2)
        self.allarrays['c2v'].cont.wradReflect([0,0,0],[0,0,1])
        self.allarrays['c2v'].cont.wradTranslate([-(mp.nominal_cmagnet_dimensions[2]/2.0 + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 (mp.nominal_cmagnet_dimensions[2] + gap + 2 * (mp.nominal_fmagnet_dimensions[2] + mp.compappleseparation))/2.0])

        ### C3v ###
        self.allarrays['c3v'].cont.wradRotate([0,0,0],[0,1,0],-np.pi/2)
        self.allarrays['c3v'].cont.wradFieldRotate([0,0,0],[0,1,0],np.pi/2)
        self.allarrays['c3v'].cont.wradTranslate([(mp.nominal_cmagnet_dimensions[2]/2.0 + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 (mp.nominal_cmagnet_dimensions[2] + gap + 2 * (mp.nominal_fmagnet_dimensions[2] + mp.compappleseparation))/2.0])
        self.allarrays['c3v'].cont.wradReflect([0,0,0],[0,0,1])
        
        ### C4v ###
        self.allarrays['c4v'].cont.wradRotate([0,0,0],[0,1,0],np.pi/2)
        self.allarrays['c4v'].cont.wradFieldRotate([0,0,0],[0,1,0],-np.pi/2)
        self.allarrays['c4v'].cont.wradTranslate([-(mp.nominal_cmagnet_dimensions[2]/2.0 + mp.rowtorowgap)/2.0,
                                                 rowshift*shiftmodesign,
                                                 -(mp.nominal_cmagnet_dimensions[2] + gap + 2 * (mp.nominal_fmagnet_dimensions[2] + mp.compappleseparation))/2.0])
        
        
        
        for key in self.allarrays:
            self.cont.wradObjAddToCnt([self.allarrays[key].cont])
        
        print('my compensated APPLE calculated at a gap of {}mm'.format(gap))
        '''
        Constructor
        '''


if __name__ == '__main__':
    testparams = parameters.model_parameters(Mova = 14, 
                                             periods = 15, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             nominal_cmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0])
    a = compensatedAPPLEv2(testparams, gap = 2, rowshift =7.5, shiftmode = 'circular')
    
    #draw object
    rd.ObjDrwOpenGL(a.cont.radobj)
    
    #solve object
    a.cont.wradSolve()
    
    #calculate field at a point
    aa = rd.Fld(a.cont.radobj,'bxbybz',[0,0,10])
    
    #define line start and end points
    linestart = [0,-60,0]
    lineend = [0,60,0]
    
    #calculate field on a line
    bb = rd.FldLst(a.cont.radobj,'bxbybz',linestart,lineend,int(1+(lineend[1]-linestart[1])/0.1),'arg',linestart[1])
    
    #make that list a numpy array
    bbn = np.array(bb)
    
    #plot the calculated field
    plt.plot(bbn[:,0],bbn[:,1:4])
    plt.legend(['bx','by','bz'])
    
    #show it
#    plt.show()
    
    #list of things to show (max 4)
    quads = ['q1','q2','q3','q4']
    #calculate the field on a line due to each element of list
    qbfields = [[],[],[],[]]
    i = 0 
    for quadrant in quads:
        qq = rd.FldLst(a.allarrays[quadrant].cont.radobj,'bxbybz',linestart,lineend,int(1+(lineend[1]-linestart[1])/0.1),'arg',linestart[1])
        qbfields[i] = qq
        i += 1
        
    qbfieldsn = np.array(qbfields)
    
    #create subplots fig
    
    #set up plot
    # set width and height
    width = 7
    height = 9
    
    #create the figure with nice margins
    figqb, axsqb = plt.subplots(2,2, sharex = False, sharey = False)
    figqb.subplots_adjust(left=.15, bottom=.16, right=.85, top= 0.9, wspace = 0.7, hspace = 0.6)
    figqb.set_size_inches(width, height)
    
    #plot stuff
    axsqb[0,0].plot(qbfieldsn[0,:,0],qbfieldsn[0,:,1:4])
    axsqb[0,1].plot(qbfieldsn[1,:,0],qbfieldsn[1,:,1:4])
    axsqb[1,0].plot(qbfieldsn[2,:,0],qbfieldsn[2,:,1:4])
    axsqb[1,1].plot(qbfieldsn[3,:,0],qbfieldsn[3,:,1:4])
    
    #legends
    axsqb[0,0].legend(['bx','by','bz'])
    
    #calculate field of a particular block in quadrant 1
    
    
    #show them off
    plt.show()
    
    print('read out the field {}'.format(aa))
    
    input("Press Enter to continue...")
    print('{}'.format(a.cont.radobj))
    #a.allarrays['q1'].cont.objectlist[4].objectlist[0].magnetisation