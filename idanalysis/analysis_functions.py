'''
Created on 24 Nov 2020

@author: oqb

'''
import numpy as np
import radia as rd
import random
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
        tempb = rd.FldLst(self.model.cont.radobj,'bxbybz',axis[0],axis[1],int(1+self.model.model_parameters.pointsperperiod*2),'arg',axis[0][1])
    
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
    

    def __init__(self, hyper_params, gaprange = np.arange(5,6,5), shiftrange = np.arange(0,1,10), shiftmoderange = ['circular'], property = ['B']):
        '''
        Constructor
        '''
        self.a = 1
        self.results = {}
        #build results dict
        if 'B' in property:
            self.results['Bmax'] = np.zeros([len(shiftmoderange),len(gaprange),len(shiftrange),3])
            self.results['Bfield'] = np.zeros([len(shiftmoderange),len(gaprange),len(shiftrange),int(1+hyper_params.pointsperperiod*2),4])
            self.results['Beff'] = np.zeros([len(shiftmoderange),len(gaprange),len(shiftrange),3])
        
        #should solve through parameters
        for shiftmode in range(len(shiftmoderange)):
            for gap in range(len(gaprange)):
                for shift in range(len(shiftrange)):
                    #set the specific case solution
                    print ('Calculating stuff for model at gap {} mm, shift {} mm, mode {}'.format(gaprange[gap], shiftrange[shift], shiftmoderange[shiftmode]))
                    hyper_params.gap = gaprange[gap]
                    hyper_params.rowshift = shiftrange[shift]
                    hyper_params.shiftmode = shiftmoderange[shiftmode]
                    
                    #build the case models
                    casemodel = id.compensatedAPPLEv2(hyper_params)
                    
                    #solve the case model
                    casesol = CaseSolution(casemodel)
                    
                    #solve each type of calculation
                    if 'B' in property:
                        casesol.calculate_B_field()
                        print ('The peak field of this arrangement is {}'.format(casesol.bmax))
                        self.results['Bmax'][shiftmode,gap,shift] = casesol.bmax
                        self.results['Bfield'][shiftmode,gap,shift] = casesol.bfield
            #for loop on gap
                #for loop on shift
                    #CaseSolution
                    #calculations on casesolution
                    #If B
                    #If Integrals
                    #If Force
                    #If Torque
                    #write to hdf5 file
                    #delete object... actually can just be written over then object is out of reference
        
    def save(self):
        pass
    
    def plot(self):
        pass
        
        
class HyperSolution():
    '''solves a hypersolution - hyperparameters can be varied'''
    def __init__(self,test_hyper_params, solution_parameters, hyper_solution_variables, hyper_solution_property = ['B'], method = 'random'):
        
        solvecount = 0
        
        if method == 'systematic':
            pass
            #time one solution
            #offer estimate
            #offer random
        
        if method == 'random':
            #for key in dictionary
            for key in hyper_solution_variables:
                #if key is list
                if type(hyper_solution_variables[key]) is list:
                    tmp_list = [0 for x in range(len(hyper_solution_variables[key]))]
                    for i in range(len(hyper_solution_variables[key])):
                        tmp_list[i] = random.choice(hyper_solution_variables[key][i])
                    setattr(test_hyper_params,key, tmp_list)
                    #for element in list
                        #pick random and assign to test_hyper_params
                #else
                    #pick random and assign to test hyperparams
                    
            
            pass
            #for element of dict
            #randomly select value
            #Solution
            
        
        #when 
        #recursively for each hyperparameter argumment given
    
    def save(self):
        pass
    
if __name__ == '__main__':
    ### developing Case Solution ###
    
    test_hyper_params = parameters.model_parameters(Mova = 14, 
                                             periods = 3, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             nominal_cmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period =4,
                                             gap = 2, 
                                             rowshift = 4,
                                             shiftmode = 'circular')
    a = id.compensatedAPPLEv2(test_hyper_params)
    
    
    case1 = CaseSolution(a)
    case1.calculate_B_field()
    
    #draw object
    rd.ObjDrwOpenGL(a.cont.radobj)
    
    plt.plot(case1.bfield[:,0],case1.bfield[:,1:4])
    plt.legend(['bx','by','bz'])
    
    #show it
    plt.show()
    
    ### Developing Model Solution ### Range of gap. rowshift and shiftmode ###
    gaprange = np.arange(2,10.1,4)
    shiftrange = np.arange(-2,2.1,2)
    shiftmoderange = ['linear','circular']
    
    #sol1 = Solution(test_hyper_params, gaprange, shiftrange, shiftmoderange)
    
    ### Developing model Hypersolution
    
    #test_hyper_params is a params object
    #solution_parameters is a list of two iterators and a list
    
    solution_parameters = parameters.scan_parameters(gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    #hypersolution_variables a dict of ranges. Can only be ranges of existing parameters in test_hyper_params
    hyper_solution_variables = {
        "block_subdivision" : [np.arange(1,6),np.arange(1,6),np.arange(1,6)]
        }
    
    hyper_solution_properties = ['B']
    
    #create hypersolution object
    hypersol1 = HyperSolution(test_hyper_params, solution_parameters, hyper_solution_variables, hyper_solution_properties)
    
    print(1)
    