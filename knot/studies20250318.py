'''
Created on Mar 18, 2025

testing arbitrary array building modifying HalbachArray class

@author: oqb
'''

import numpy as np
import radia as rd
import random
import time
import matplotlib.pyplot as plt
import srwpy.srwlib as srw
import array

from wradia import wrad_obj as wrd
from wradia import wrad_mat as wrdm

from idcomponents import parameters
from idcomponents import magnet_shapes as ms
from idcomponents import halbach_arrays as ha
from wradia.wrad_obj import wradObjCnt
import apple2p5.model2 as id1

from srwpy.uti_plot import *

class ArbArray():
    '''
    classdocs
    '''


    def __init__(self, model_hyper_parameters = parameters.model_parameters(), magnet = ms.appleMagnet, array_number = 1):
        '''
        Constructor
        '''
        #switch to find out which array order is required, for multi period undulators
        if array_number == 1:
            per_length = model_hyper_parameters.periodlength
            model_hyper_parameters.nominal_fmagnet_dimensions[1] = (model_hyper_parameters.periodlength-model_hyper_parameters.magnets_per_period * model_hyper_parameters.shim) / model_hyper_parameters.magnets_per_period
        
        elif array_number == 2:
            per_length = model_hyper_parameters.secondperiodlength
            model_hyper_parameters.nominal_fmagnet_dimensions[1] = (model_hyper_parameters.secondperiodlength-model_hyper_parameters.magnets_per_period * model_hyper_parameters.shim) / model_hyper_parameters.magnets_per_period
        
            
        elif array_number == 3:
            per_length = model_hyper_parameters.thirdperiodlength
            model_hyper_parameters.nominal_fmagnet_dimensions[1] = (model_hyper_parameters.thirdperiodlength-model_hyper_parameters.magnets_per_period * model_hyper_parameters.shim) / model_hyper_parameters.magnets_per_period
        

        
        #def appleArray(model_hyper_parameters, loc_offset, halbach_direction = -1):
        self.cont = wrd.wradObjCnt([])
        
        loc_offset = [0,0,0]
        
        #define the location offset in S of the magnet
        loc_offset[1] = -((model_hyper_parameters.totalmagnets-1)/2.0) * (model_hyper_parameters.nominal_fmagnet_dimensions[1] + model_hyper_parameters.shim)
        
        
        #functionally efined offset in x and z based on s. Function can be passed in.
        loc_offset[0:3:2] = model_hyper_parameters.perturbation_fn(loc_offset[1])
        
        M = []
        mat = []
        for i in range(model_hyper_parameters.totalmagnets):
            #M.append([halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M*np.sin(2*np.pi*model_hyper_parameters.Mova/360.0),halbach_direction * np.sin(i*np.pi/2.0)*model_hyper_parameters.M * np.cos(2*np.pi*model_hyper_parameters.Mova/360.0), np.cos(i*np.pi/2.0)*model_hyper_parameters.M])
            M.append(model_hyper_parameters.M_list[i])
            
            mat.append(wrdm.wradMatLin(model_hyper_parameters.ksi,M[i].tolist()))
        
        for x in range(-int((model_hyper_parameters.totalmagnets-1)/2),int(1+(model_hyper_parameters.totalmagnets-1)/2)):#0,model_hyper_parameters.appleMagnets
            
            mag = magnet(model_hyper_parameters, loc_offset,mat[x]) 
            loc_offset[1] += model_hyper_parameters.nominal_fmagnet_dimensions[1] + model_hyper_parameters.shim
            loc_offset[0:3:2] = model_hyper_parameters.perturbation_list[x]
            self.cont.wradObjAddToCnt([mag.cont])
            
        #return a
        
    #mag = appleMagnet(AII,4,materiald,[z,y,x])
    #mag apply magnetisation and colour
    #add to container
    
    
class ArbAPPLE():
    '''
    classdocs
    '''

        
    def __init__(self, 
         model_parameters = parameters.model_parameters(),
         fmagnet = ms.appleMagnet):
        
        rd.UtiDelAll()
        self.cont = wrd.wradObjCnt([])
        
        self.model_parameters = model_parameters
        mp = self.model_parameters
        
        if mp.shiftmode == 'circular':
            shiftmodesign = 1
        elif mp.shiftmode == 'linear':
            shiftmodesign = -1
        else:
            shiftmodesign = 0
        
        self.rownames = ['q1','q2','q3','q4']
        self.allarraytabs = np.array([ha.MagnetRow(self.rownames[0], ArbArray(model_parameters,fmagnet),ha.HalbachTermination_APPLE(model_parameters,fmagnet)) for _ in range(4)])
        
        for r in range(4):
            self.allarraytabs[r] = ha.MagnetRow(self.rownames[r], ArbArray(mp,fmagnet),
                                              ha.HalbachTermination_APPLE(mp,fmagnet), beam = int((r//2)), quadrant = int(self.rownames[r][1])-1, row = r)
        
        ##### Functional Magnets #####
        
        ### Q1 ###

        self.allarraytabs[0].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 -(mp.nominal_fmagnet_dimensions[0] + mp.gap)/2.0])
        self.allarraytabs[0].cont.wradFieldInvert()
        self.allarraytabs[0].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        self.allarraytabs[0].cont.wradReflect([0,0,0],[1,0,0])

        
        ### Q2 ###
        self.allarraytabs[1].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 mp.rowshift,
                                                 -(mp.nominal_fmagnet_dimensions[0] + mp.gap)/2.0])
        self.allarraytabs[1].cont.wradFieldInvert()
        self.allarraytabs[1].cont.wradRotate([0,0,0],[0,1,0],np.pi)
        

        
        
        ### Q3 ###
        self.allarraytabs[2].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 mp.rowshift*shiftmodesign,
                                                 -(mp.nominal_fmagnet_dimensions[0] + mp.gap)/2.0])
 
        
        ### Q4 ###
        self.allarraytabs[3].cont.wradTranslate([-(mp.nominal_fmagnet_dimensions[2] + mp.rowtorowgap)/2.0,
                                                 0.0,
                                                 -(mp.nominal_fmagnet_dimensions[0] + mp.gap)/2.0])
        self.allarraytabs[3].cont.wradReflect([0,0,0],[1,0,0])


        
        
        for row in range(len(self.allarraytabs)):
            self.cont.wradObjAddToCnt([self.allarraytabs[row].cont])


    
if __name__ == '__main__':
    rd.UtiDelAll()
    a_param = parameters.model_parameters(
        periods = 10,
        periodlength = 40,
        minimumgap = 15,
        M = 1.32,
        block_subdivision = [1,1,1])
    #a_param.block_subdivision = [1,1,1]
    #a_param.periods = 20
    #a_param.periodlength = 40
    #a_param.minimumgap = 15
    
    #a_param.M = 1.32
    
    t0 = time.time()
    
    for i in range(len(a_param.M_list[:])):
        ang = random.random()*2*np.pi
        
        
        a_param.M_list[i,0:3:2] = np.array([a_param.M*np.sin(ang), a_param.M*np.cos(ang)])
    
    
    #a = ArbAPPLE(model_parameters = a_param)
    
    a = id1.plainAPPLE(model_parameters = a_param)
    
    rd.ObjDrwOpenGL(a.cont.radobj)
    
    rd.Solve(a.cont.radobj, 0.001,1000)
    
    afld = rd.FldLst(a.cont.radobj,'bxbybz',[0,-500,0],[0,500,0],2001,'arg',-500)
    aarr = np.array(afld)
    atraj = np.array(rd.FldPtcTrj(a.cont.radobj,-2.5,[0,0,0,0],[-500,500],2001))
    
    t1 = time.time()
    
    print("time taken was {}".format(t1-t0))
    
    #create Machine
    #**********************Defining Magnetic Field:
    xcID = 0 #Transverse Coordinates of ID Center [m]
    ycID = 0
    zcID = 0 #Longitudinal Coordinate of ID Center [m]
        
    magFldCnt = srw.SRWLMagFldC() #Container
    magFldCnt.allocate(1) #Magnetic Field consists of 1 part
    locArBx = array.array('d',aarr[:,1])
    locArBy = array.array('d',aarr[:,3])
    locArBz = array.array('d',aarr[:,2])   
    xNp = 1
    yNp = 1    
    zNp = len(aarr[:,0])
    
    xRange = 0
    yRange = 0
    zRange = (aarr[1,0]-aarr[0,0])*(zNp-1)/1000
    
    magFldCnt.arMagFld[0] = srw.SRWLMagFld3D(locArBx, locArBy, locArBz, xNp, yNp, zNp, xRange, yRange, zRange, 1)
    print('done')
    magFldCnt.arXc[0] = xcID
    magFldCnt.arYc[0] = ycID
    magFldCnt.arZc[0] = zcID
    magFldCnt.arMagFld[0].nRep = 1 #Entire ID = no repeats of field
    
    #pass field into single electron case of SRW
    #**********************Trajectory structure (where the results will be stored)
    part = srw.SRWLParticle()
    part.x = 0.0 #Initial Transverse Coordinates (initial Longitudinal Coordinate will be defined later on) [m]
    part.y = 0.0
    part.z = -0.5 #Initial Longitudinal Coordinate (set before the ID)
    part.xp = 0 #Initial Transverse Velocities
    part.yp = 0
    part.gamma = 2.5/0.51099890221e-03 #Relative Energy
    part.relE0 = 1 #Electron Rest Mass
    part.nq = -1 #Electron Charge
    
    partTraj = srw.SRWLPrtTrj()
    partTraj.partInitCond = part
    npTraj = 2001 #Number of Points for Trajectory calculation
    partTraj.allocate(npTraj)
    partTraj.ctStart = 00.0 #Start Time for the calculation
    partTraj.ctEnd = 1.0  #End Time
    
    #**********************Calculation (SRWLIB function call)
    print('   Performing Trajectory calculation ... ', end='')
    partTraj = srw.srwl.CalcPartTraj(partTraj, magFldCnt, 0)
    
    #evaluate brilliance at 5eV
    
    #**********************Electron Beam
    elecBeam = srw.SRWLPartBeam()
    elecBeam.Iavg = 0.5 #Average Current [A]
    elecBeam.partStatMom1 = part
    
    #**********************Precision parameters for SR calculation
    meth = 0 #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
    relPrec = 0.01 #relative precision
    zStartInteg = -1 #-129.029 #part.z - 0.1 #longitudinal position to start integration (effective if < zEndInteg)
    zEndInteg =1 #129.029 #part.z + 5.3 #longitudinal position to finish integration (effective if > zStartInteg)
    #* Already specified before : npTraj 
    useTermin = 1 #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
    sampFactNxNyForProp = 0 #sampling factor for adjusting nx, ny (effective if > 0)
    arPrecPar = [meth, relPrec, zStartInteg, zEndInteg, npTraj, useTermin, sampFactNxNyForProp]

    #**********************Wavefront
    wfr1 = srw.SRWLWfr() #For spectrum vs photon energy
    wfr1.allocate(5000, 1, 1) #Numbers of points vs Photon Energy, Horizontal and Vertical Positions
    wfr1.mesh.zStart = 10. #Longitudinal Position [m] at which SR has to be calculated
    wfr1.mesh.eStart = 75.0 #Initial Photon Energy [eV]
    wfr1.mesh.eFin = 100.0 #Final Photon Energy [eV]
    wfr1.mesh.xStart = 0. #Initial Horizontal Position [m]
    wfr1.mesh.xFin = 0 #Final Horizontal Position [m]
    wfr1.mesh.yStart = 0 #Initial Vertical Position [m]
    wfr1.mesh.yFin = 0 #Final Vertical Position [m]
    wfr1.partBeam = elecBeam
    
    wfr2 = srw.SRWLWfr() #For intensity distribution at fixed photon energy
    wfr2.allocate(1, 61, 61) #Numbers of points vs Photon Energy, Horizontal and Vertical Positions
    wfr2.mesh.zStart = 10. #Longitudinal Position [m] at which SR has to be calculated
    wfr2.mesh.eStart = 5915.5 #Initial Photon Energy [eV]
    wfr2.mesh.eFin = 5915.5 #Final Photon Energy [eV]
    wfr2.mesh.xStart = -0.0006 #Initial Horizontal Position [m]
    wfr2.mesh.xFin = 0.0006 #Final Horizontal Position [m]
    wfr2.mesh.yStart = -0.0006 #Initial Vertical Position [m]
    wfr2.mesh.yFin = 0.0006 #Final Vertical Position [m]
    wfr2.partBeam = elecBeam

    #**********************Calculation (SRWLIB function calls)
    print('   Performing Electric Field calculation ... ', end='')
    #srwl.CalcElecFieldSR(wfr1, partTraj, magFldCnt, arPrecPar)
    srw.srwl.CalcElecFieldSR(wfr1, 0, magFldCnt, arPrecPar)
    print('done')
    print('   Extracting Intensity from calculated Electric Field ... ', end='')
    arI1 = array.array('f', [0]*wfr1.mesh.ne)
    srw.srwl.CalcIntFromElecField(arI1, wfr1, 6, 0, 0, wfr1.mesh.eStart, wfr1.mesh.xStart, wfr1.mesh.yStart)
    print('done')
    
    print('   Performing Electric Field calculation ... ', end='')
    srw.srwl.CalcElecFieldSR(wfr2, 0, magFldCnt, arPrecPar)
    print('done')
    print('   Extracting Intensity from calculated Electric Field ... ', end='')
    arI2 = array.array('f', [0]*wfr2.mesh.nx*wfr2.mesh.ny) #"flat" array to take 2D intensity data
    srw.srwl.CalcIntFromElecField(arI2, wfr2, 6, 0, 3, wfr2.mesh.eStart, 0, 0)
    print('done')
    
    #**********************Plotting results (requires 3rd party graphics package)
    print('   Plotting the results (blocks script execution; close any graph windows to proceed) ... ', end='')
    ctMesh = [partTraj.ctStart, partTraj.ctEnd, partTraj.np]
    for i in range(partTraj.np): partTraj.arY[i] *= 1000
    uti_plot1d(partTraj.arX, ctMesh, ['ct [m]', 'Horizontal Position [mm]', 'Electron Trajectory'])
    uti_plot1d(partTraj.arY, ctMesh, ['ct [m]', 'Vertical Position [mm]', 'Electron Trajectory'])
    
    uti_plot1d(arI1, [wfr1.mesh.eStart, wfr1.mesh.eFin, wfr1.mesh.ne], ['Photon Energy [eV]', 'Intensity [ph/s/.1%bw/mm^2]', 'On-Axis Spectrum'])
    
    plotMeshX = [1000*wfr2.mesh.xStart, 1000*wfr2.mesh.xFin, wfr2.mesh.nx]
    plotMeshY = [1000*wfr2.mesh.yStart, 1000*wfr2.mesh.yFin, wfr2.mesh.ny]
    uti_plot2d(arI2, plotMeshX, plotMeshY, ['Horizontal Position [mm]', 'Vertical Position [mm]', 'Intensity at ' + str(wfr2.mesh.eStart) + ' eV'])
    
    arI2x = array.array('f', [0]*wfr2.mesh.nx) #array to take 1D intensity data
    srw.srwl.CalcIntFromElecField(arI2x, wfr2, 6, 0, 1, wfr2.mesh.eStart, 0, 0)
    uti_plot1d(arI2x, plotMeshX, ['Horizontal Position [mm]', 'Intensity [ph/s/.1%bw/mm^2]', 'Intensity at ' + str(wfr2.mesh.eStart) + ' eV\n(horizontal cut at y = 0)'])
    
    arI2y = array.array('f', [0]*wfr2.mesh.ny) #array to take 1D intensity data
    srw.srwl.CalcIntFromElecField(arI2y, wfr2, 6, 0, 2, wfr2.mesh.eStart, 0, 0)
    uti_plot1d(arI2y, plotMeshY, ['Horizontal Position [mm]', 'Intensity [ph/s/.1%bw/mm^2]', 'Intensity at ' + str(wfr2.mesh.eStart) + ' eV\n(vertical cut at x = 0)'])
    
    uti_plot_show() #show all graphs (blocks script execution; close all graph windows to proceed)
    print('done')

    #debug plots

    fig, ax = plt.subplots(3,3)
    
    ax[0,0].plot(np.multiply(partTraj.arZ,1000),np.multiply(partTraj.arX,1000))
    ax[0,0].plot(np.multiply(partTraj.arZ,1000),np.multiply(partTraj.arY,1000))
    #ax[0,0].plot(partTraj.arZ)
    ax[1,0].plot(aarr[:,0],aarr[:,1:])
    ax[1,1].plot(atraj[:,0],atraj[:,1:])
    ax[2,0].plot(magFldCnt.arMagFld[0].arBx)
    
    plt.show()
    print('done')