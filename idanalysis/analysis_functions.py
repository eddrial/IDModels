'''
Created on 24 Nov 2020

@author: oqb

'''
import numpy as np
import radia as rd
import random
import copy
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    

    def __init__(self, hyper_params, scan_parameters, property = ['B']):
        '''
        Constructor
        '''
        self.hyper_params = hyper_params
        self.scan_parameters = scan_parameters
        self.property = property
        self.results = {}
        
        
        #build results dict
        if 'B' in property:
            self.results['Bmax'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             3])
            
            self.results['Bfield'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                               len(self.scan_parameters.gaprange),
                                               len(self.scan_parameters.shiftrange),
                                               int(1+hyper_params.pointsperperiod*2),
                                               4])
            
            self.results['Beff'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             3])
        
        
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
        print(1)
        
    def solve(self):
        #should solve through parameters
        for shiftmode in range(len(self.scan_parameters.shiftmoderange)):
            for gap in range(len(self.scan_parameters.gaprange)):
                for shift in range(len(self.scan_parameters.shiftrange)):
                    #set the specific case solution
                    print ('Calculating stuff for model at gap {} mm, shift {} mm, mode {}'.format(
                        self.scan_parameters.gaprange[gap], 
                        self.scan_parameters.shiftrange[shift], 
                        self.scan_parameters.shiftmoderange[shiftmode]))
                    self.hyper_params.gap = self.scan_parameters.gaprange[gap]
                    self.hyper_params.rowshift = self.scan_parameters.shiftrange[shift]
                    self.hyper_params.shiftmode = self.scan_parameters.shiftmoderange[shiftmode]
                    
                    #build the case models
                    casemodel = id.compensatedAPPLEv2(self.hyper_params)
                    
                    #solve the case model
                    casesol = CaseSolution(casemodel)
                    
                    #solve each type of calculation
                    if 'B' in self.property:
                        casesol.calculate_B_field()
                        print ('The peak field of this arrangement is {}'.format(casesol.bmax))
                        self.results['Bmax'][shiftmode,gap,shift] = casesol.bmax
                        self.results['Bfield'][shiftmode,gap,shift] = casesol.bfield
    
    def save(self):
        pass
    
    def plot(self):
        pass
        
        
class HyperSolution():
    '''solves a hypersolution - hyperparameters can be varied'''
    def __init__(self,
                 base_hyper_params,  
                 hyper_solution_variables,
                 scan_parameters = 'default', 
                 hyper_solution_properties = ['B'], 
                 method = 'random',
                 iterations = 20):
        
        
        if scan_parameters == 'default':
            self.scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength)
        else:
            self.scan_parameters = scan_parameters
        solvecount = 0
        
        self.base_hyper_parameters = copy.deepcopy(base_hyper_params)  #what is the fundamental model
        self.hyper_solution_variables = copy.deepcopy(hyper_solution_variables) #what parameters in the hyperparameters are being varied and their ranges
        self.hyper_solution_properties = copy.deepcopy(hyper_solution_properties) # 
        self.hyper_inputs = []
        self.hyper_results = []
        
        
        if method == 'systematic':
            nkeys = len(self.hyper_solution_variables.keys)
            
            pass
            #time one solution
            #offer estimate
            #offer random
        
        if method == 'random':
            #for n in iterations - build hyperparameter cases
            for n in range(iterations):
                new_hyper_params = copy.deepcopy(base_hyper_params)
                #for key in dictionary
                for key in self.hyper_solution_variables:
                    #if key is list
                    a = self.randomise_hyper_input(self.hyper_solution_variables[key])
                    
                    setattr(new_hyper_params,key, copy.copy(a))
                    
                self.hyper_inputs.append(new_hyper_params)
                
                    
                        
            
                    
            
        
            #for element of dict
            #randomly select value
            #Solution
            #extract hyperresults
            
        
        #when 
        #recursively for each hyperparameter argumment given
    def solve(self):
        for input in self.hyper_inputs:
            tmp_sol = Solution(input, self.scan_parameters, property = ['B'])
            print('Solving for slices of {}'.format(input.block_subdivision))
            tmp_sol.solve()
            
            self.hyper_results.append(tmp_sol.results)
    
    def sequence_hyper_input(self,input):
        pass
    
    def randomise_hyper_input(self, input):
        if type(input) is list:
            tmp = [0 for x in range(len(input))]
            #for element in list
            for i in range(len(input)):
                #pick random 
                tmp[i] = random.choice(input[i])
            #and assign to test_hyper_params
            
        else:
            tmp = random.choice(input)
            
        return tmp
            

    def save(self):
        pass
    
if __name__ == '__main__':
    ### developing Case Solution ###
    
    test_hyper_params = parameters.model_parameters(Mova = 0, 
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
#    rd.ObjDrwOpenGL(a.cont.radobj)
    
#    plt.plot(case1.bfield[:,0],case1.bfield[:,1:4])
#    plt.legend(['bx','by','bz'])
    
    #show it
#    plt.show()
    
    ### Developing Model Solution ### Range of gap. rowshift and shiftmode ###
    gaprange = np.arange(2,10.1,4)
    shiftrange = np.arange(-2,2.1,2)
    shiftmoderange = ['linear','circular']
    
    #scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, shiftrange = np.arange(0,1,10))
    
    sol1 = Solution(test_hyper_params, scan_parameters)
    #sol1.solve()
    
    ### Developing model Hypersolution
    
    #test_hyper_params is a params object
    #solution_parameters is a list of two iterators and a list
    
    #hypersolution_variables a dict of ranges. Can only be ranges of existing parameters in test_hyper_params
    hyper_solution_variables = {
        "block_subdivision" : [np.arange(1,4),np.arange(1,4),np.arange(1,4)]
        }
    
    hyper_solution_properties = ['B']
    
    #create hypersolution object
    hypersol1 = HyperSolution(base_hyper_params = test_hyper_params, 
                              hyper_solution_variables = hyper_solution_variables, 
                              hyper_solution_properties = hyper_solution_properties,
                              scan_parameters = scan_parameters,
                              method = 'random',
                              iterations = 60)
    
    hypersol1.solve()
    
    with open('M:\Work\Athena_APPLEIII\Python\Results\\test_data.dat','wb') as fp:
        pickle.dump(hypersol1,fp,protocol=pickle.HIGHEST_PROTOCOL)
    
#    with open('M:\Work\Athena_APPLEIII\Python\Results\\test_data.dat','rb') as fp:
#        hypersol1 = pickle.load(fp)
    
    mynumpyarray = np.zeros([60,4])
    
    for i in range(60):
        mynumpyarray[i] = [hypersol1.hyper_inputs[i].block_subdivision[0],
                           hypersol1.hyper_inputs[i].block_subdivision[1],
                           hypersol1.hyper_inputs[i].block_subdivision[2],
                           hypersol1.hyper_results[i]['Bmax'][0,0,0,2]]
        
    eddf = pd.DataFrame(data = mynumpyarray, index = range(60), columns = ['Slice X', 'Slice Y', 'Slice Z', 'Bmax'])

    fig = px.parallel_coordinates(eddf, color="Bmax", labels={"Bmax": "Bmax",
            "Slice X": "Slice X", "Slice Y": "Slice Y",
            "Slice Z": "Slice Z", },
                         color_continuous_scale=px.colors.diverging.Tealrose,
                         color_continuous_midpoint=1.58)
        
    fig.show()
        
    
    print(1)
    