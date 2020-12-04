'''
Created on 24 Nov 2020

@author: oqb

'''
import numpy as np
import radia as rd
import matplotlib.pyplot as plt
from apple2p5 import model2 as id
from idcomponents import parameters

class CaseFullSolution():
    '''solves along full axis'''
    def __init__(self):
        pass
    
    

class CaseSolution():
    '''solves a full case = hyperparamaters and parameters fixed'''
    def __init__(self, model):
        self.model = model
        self.model.cont.wradSolve()
    #this should solve a particular model
    #it should contain any of field, peakfield, effectivefield, 1st integral
    
    def calculate_B_field(self, axis = 'default'):
        #define axis
        if axis == 'default':
            limit = self.model.model_parameters.periodlength
            axis = [[0,-limit,0],[0,limit,0]]
        self.axis = axis
        #solve for the fieldlist
        tempb = rd.FldLst(a.cont.radobj,'bxbybz',axis[0],axis[1],int(1+(axis[1][1]-axis[0][1])/0.1),'arg',axis[0][1])
    
    #make that list a numpy array
        self.bfield = np.array(tempb)
        
        self.bmax = np.array([np.max(np.abs(self.bfield[:,1])),np.max(np.abs(self.bfield[:,2])),np.max(np.abs(self.bfield[:,3]))])
        self.beff = np.array([0.0,0.0,0.0])
        
        '''solve for B field for central 2 periods or minimum distance
        Solve for Peak and Effective Bx, Bs, Bz'''
        
    
    def calculate_H_Field(self):
        '''solve for H field over central 2 periods or minimum distance'''
        pass
    
    def calculate_M_field(self):
        '''solve for M over central 2 periods or minimum distance'''
        pass
    
    def calculate_first_integral(self):
        '''solve for the first integral across a sensible width'''
        pass
    
    def calculate_second_integral(self):
        '''solve for the second integral across a sensible width'''
        pass
    
    def calculate_force_per_magnet(self):
        '''solve for an individual magnet in the model'''
        pass
    
    def calculate_force_per_row(self):
        ''' solve for force on row'''
        pass
    
    def calculate_force_per_quadrant(self):
        '''solve for force on quarant'''
        pass
    
    def calculate_force_per_beam(self):
        '''solve for the force on the beam'''
        pass
    
    def calculate_torque_per_magnet(self):
        '''solve for an individual magnet in the model'''
        pass
    
    def calculate_torque_per_row(self):
        ''' solve for torque on row'''
        pass
    
    def calculate_torque_per_quadrant(self):
        '''solve for torque on quarant'''
        pass
    
    def calculate_torque_per_beam(self):
        '''solve for the d on the beam'''
        pass

class Solution():
    '''
    classdocs
    solves a solution - i.e. parameters (gap, phase) swept
    '''
    

    def __init__(self, params):
        '''
        Constructor
        '''
        self.a = 1
        #should solve through parameters
        #for loop on mode
            #for loop on gap
                #for loop on shift
                    #CaseSolution
                    #calculations on casesolution
                    #write to hdf5 file
                    #delete object... actually can just be written over then object is out of reference
        
    def save(self):
        pass
    
    def plot(self):
        pass
        
        
class HyperSolution():
    '''solves a hypersolution - hyperparameters can be varied'''
    def __init__(self):
        pass
        #recursively for each hyperparameter argumment given
    
    def save(self):
        pass
    
if __name__ == '__main__':
    testparams = parameters.model_parameters(Mova = 14, 
                                             periods = 3, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             nominal_cmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period =4)
    a = id.compensatedAPPLEv2(testparams, gap = 2, rowshift =0, shiftmode = 'circular')
    
    
    case1 = CaseSolution(a)
    case1.calculate_B_field()
    
    #draw object
    rd.ObjDrwOpenGL(a.cont.radobj)
    
    plt.plot(case1.bfield[:,0],case1.bfield[:,1:4])
    plt.legend(['bx','by','bz'])
    
    #show it
    plt.show()
    print(1)
    