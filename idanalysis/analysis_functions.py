'''
Created on 24 Nov 2020

@author: oqb

'''
import numpy as np
import radia as rd
import h5py as h5
import random
import itertools
import copy
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tracemalloc
import time

from wradia import wrad_obj as wrd
from apple2p5 import model2 as id
from idcomponents import parameters
from ipywidgets.widgets.interaction import fixed
from wradia.wrad_obj import wradObjCnt

class CaseFullSolution():
    '''solves along full axis'''
    def __init__(self):
        pass
    
    

class CaseSolution():
    '''solves a full case = hyperparamaters and parameters fixed'''
    def __init__(self, model):
        self.model = model
        self.model.cont.wradSolve()
        self.solved_attributes = []
    #this should solve a particular model
    #it should contain any of field, peakfield, effectivefield, 1st integral
    
    def case_save(self,h5object = False,h5path = 'Single_Case', fname = ''):
        if h5object == False:
            h5object = h5.File(fname, 'w')
            
        h5object.create_group(h5path)
        
        for item in self.solved_attributes:
            h5object.create_dataset('{}/{}'.format(h5path,item),data = getattr(self,item))
        
    
    def calculate_B_field(self, axis = 'default'):
        #define axis
        if axis == 'default':
            limit = self.model.model_parameters.periodlength
            axis = [[0,-limit,0],[0,limit,0]]
        self.axis = axis
        #solve for the fieldlist
        tempb = rd.FldLst(self.model.cont.radobj,'bxbybz',axis[0],axis[1],int(1+self.model.model_parameters.pointsperperiod*2),'arg',axis[0][1])
        
        #absolutely temporary streamplot example
        #self.model.wradStreamPlot(corner1 = np.array([-10,-10,0]), corner2 = np.array([-10,-10,0]), fields = 'bxbz')
        
    #make that list a numpy array
        self.bfield = np.array(tempb)
        
        self.bmax = np.array([np.max(np.abs(self.bfield[:,1])),np.max(np.abs(self.bfield[:,2])),np.max(np.abs(self.bfield[:,3]))])
        self.beff = np.linalg.norm(self.bmax)
        
        self.solved_attributes.append('bfield')
        self.solved_attributes.append('bmax')
        self.solved_attributes.append('beff')
        '''solve for B field for central 2 periods or minimum distance
        Solve for Peak and Effective Bx, Bs, Bz'''
        
    
    def calculate_H_Field(self):
        '''solve for H field over central 2 periods or minimum distance'''
        pass
    
    def calculate_M_field(self):
        '''solve for M over central 2 periods or minimum distance'''
        pass
    
    def calculate_first_integral(self, plane = 'default'):
        '''solve for the first integral across a sensible width'''
        if plane == 'default':
            plane = []
        self.plane = plane
        #solve for the 1st integral
        for x in range(plane):
            print(1)
        
        pass
    
    def calculate_second_integral(self):
        '''solve for the second integral across a sensible width'''
        pass
    
    def calculate_force_per_magnet(self):
        '''solve for an individual magnet in the model'''
        if self.model.model_parameters.type == 'Compensated_APPLE':
            self.forceonmagnets = {}
            rowlist = list(self.model.allarrays)
            mag_list = []
            
            for i in range(self.model.model_parameters.magnets_per_period):
                mag_list.append('mag_{}'.format(i))
            
            rowmaglist = []
            
            for row in rowlist:
                for i in range(self.model.model_parameters.magnets_per_period):
                    for mag in range(len(mag_list)):
                        rowmaglist.append('{}_{}'.format(row,mag))
                        self.forceonmagnets['{}_{}'.format(row,mag_list[mag])] = wrd.wradObjCnt()
                        self.forceonmagnets['not{}_{}'.format(row,mag_list[mag])] = wrd.wradObjCnt()
                        
                        
                        #i = 0 => central magnet
                        #i = 2 => next magnet downstream
                        if (mag - i) == (len(mag_list) - 1)/2:
                            self.forceonmagnets['{}_{}'.format(row,mag_list[mag])].wradObjAddToCnt(mag_list[mag])
                            
                    
                        else:
                            self.forceonmagnets['not{}_{}'.format(row,mag_list[mag])].wradObjAddToCnt(mag_list[mag])
                            
                    

                    
            
            self.solved_attributes.append('forceonmagnets')
            
    def calculate_force_per_row(self):
        ''' solve for force on row'''
        if self.model.model_parameters.type == 'Compensated_APPLE':
                          #"General Solution Method"
            rows = []
            for i in range(self.model.model_parameters.rows):
                #append to the list, a list of two containers. 
                #The Container we chack the force on, 
                #and the container for objects 'creating rest of field 
                rows.append([wrd.wradObjCnt(),wrd.wradObjCnt()])
            
            self.rownames = self.model.rownames
            
            #for each magnet row
            for i in range(self.model.model_parameters.rows):
                #for each beam option
                for j in range(self.model.model_parameters.rows):
                    #if the row is the desired row
                    if self.model.allarraytabs[i].row == j:
                        #put it in the 'is this' container
                        rows[j][0].wradObjAddToCnt([self.model.allarraytabs[i].cont])
                    else:
                        #put it in the 'is not this' container
                        rows[j][1].wradObjAddToCnt([self.model.allarraytabs[i].cont])
            
            
            self.rowforces = np.zeros([len(rows),3])
            
            
            #calculate forces on 'this' due to 'not this' in model
            for i in range(len(self.rowforces)):
                self.rowforces[i] = np.array(rd.FldEnrFrc(rows[i][0].radobj,rows[i][1].radobj,"fxfyfz"))
            
        self.solved_attributes.append('rowforces')
    
    def calculate_force_per_quadrant(self):
        '''solve for force on quadrant'''
        if self.model.model_parameters.type == 'Compensated_APPLE':
#            self.forceonquadrants = {}
#            self.forceonquadrantsarray = np.zeros([3,4])
#            #create upper wrad object
#            for quad in range(1,5,1):
#                self.forceonquadrants['quad{}'.format(quad)] = wrd.wradObjCnt()
#                self.forceonquadrants['notquad{}'.format(quad)] = wrd.wradObjCnt()
#                self.forceonquadrants['quad{}'.format(quad)].wradObjAddToCnt([self.model.allarrays['q{}'.format(quad)].cont,
#                                       self.model.allarrays['c{}v'.format(quad)].cont,
#                                       self.model.allarrays['c{}h'.format(quad)].cont])
#                for notquad in range(1,5,1):
#                    if notquad != quad:
#                        self.forceonquadrants['notquad{}'.format(quad)].wradObjAddToCnt([self.model.allarrays['q{}'.format(notquad)].cont,
#                                       self.model.allarrays['c{}v'.format(notquad)].cont,
#                                       self.model.allarrays['c{}h'.format(notquad)].cont])
                
                
            #solve forces on each due to the rest
#            for quadsol in range(1,5,1):
#                self.forceonquadrants['force_on_quadrant_{}'.format(quadsol)] = rd.FldEnrFrc(self.forceonquadrants['quad{}'.format(quadsol)].radobj,self.forceonquadrants['notquad{}'.format(quadsol)].radobj,"fxfyfz")
#                self.forceonquadrantsarray[:,quadsol-1] = self.forceonquadrants['force_on_quadrant_{}'.format(quadsol)]
                
            #"General Solution Method"
            quadrants = []
            for i in range(self.model.model_parameters.quadrants):
                #append to the list, a list of two containers. 
                #The Container we chack the force on, 
                #and the container for objects 'creating rest of field 
                quadrants.append([wrd.wradObjCnt(),wrd.wradObjCnt()])
            
            self.quadrantnames = ['q1','q2','q3','q4']
            
            #for each magnet row
            for i in range(self.model.model_parameters.rows):
                #for each beam option
                for j in range(self.model.model_parameters.quadrants):
                    #if the row is in the quadrant option
                    if self.model.allarraytabs[i].quadrant == j:
                        #put it in the 'is this' container
                        quadrants[j][0].wradObjAddToCnt([self.model.allarraytabs[i].cont])
                    else:
                        #put it in the 'is not this' container
                        quadrants[j][1].wradObjAddToCnt([self.model.allarraytabs[i].cont])
            
            
            self.quadrantforces = np.zeros([len(quadrants),3])
            
            #calculate forces on 'this' due to 'not this' in model
            for i in range(len(self.quadrantforces)):
                self.quadrantforces[i] = np.array(rd.FldEnrFrc(quadrants[i][0].radobj,quadrants[i][1].radobj,"fxfyfz"))

            self.solved_attributes.append('quadrantforces')
    
    def calculate_force_per_beam(self):
        '''solve for the force on the beam'''
        if self.model.model_parameters.type == 'Compensated_APPLE':
            #create upper wrad object
            #upper_beam = wrd.wradObjCnt()
            #upper_beam.wradObjAddToCnt([self.model.allarrays['q1'].cont,
            #                           self.model.allarrays['q2'].cont,
            #                           self.model.allarrays['c1h'].cont,
            #                           self.model.allarrays['c1v'].cont,
            #                           self.model.allarrays['c2h'].cont,
            #                           self.model.allarrays['c2v'].cont])
            
            
            #create lower rad object
            #lower_beam = wrd.wradObjCnt()
            #lower_beam.wradObjAddToCnt([self.model.allarrays['q3'].cont,
            #                           self.model.allarrays['q4'].cont,
            #                           self.model.allarrays['c3h'].cont,
            #                           self.model.allarrays['c3v'].cont,
            #                           self.model.allarrays['c4h'].cont,
            #                           self.model.allarrays['c4v'].cont])
            
            beams = []
            for i in range(self.model.model_parameters.beams):
                #append to the list, a list of two containers. 
                #The Container we chack the force on, 
                #and the container for objects 'creating rest of field 
                beams.append([wrd.wradObjCnt(),wrd.wradObjCnt()])
            
            self.beamnames = ['upper','lower']
            
            #for each magnet row
            for i in range(self.model.model_parameters.rows):
                #for each beam option
                for j in range(self.model.model_parameters.beams):
                    #if the row is in the beam option
                    if self.model.allarraytabs[i].beam == j:
                        #put it in the 'is this' container
                        beams[j][0].wradObjAddToCnt([self.model.allarraytabs[i].cont])
                    else:
                        #put it in the 'is not this' container
                        beams[j][1].wradObjAddToCnt([self.model.allarraytabs[i].cont])
            
            #solve force lower due to all the rest
            #a = rd.FldEnrFrc(upper_beam.radobj,lower_beam.radobj,"fxfyfz")
            #solve force on upper due to all the rest
            #b = rd.FldEnrFrc(lower_beam.radobj,upper_beam.radobj,"fxfyfz")
            
            #self.forceonlower = a
            #self.forceonupper = b
            
            self.beamforces = np.zeros([len(beams),3])
            
            for i in range(len(self.beamforces)):
                self.beamforces[i] = np.array(rd.FldEnrFrc(beams[i][0].radobj,beams[i][1].radobj,"fxfyfz"))
        
        self.solved_attributes.append('beamforces')
            
    
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
    

    def __init__(self, hyper_params, scan_parameters, property = ['B','Forces']):
        '''
        Constructor
        '''
        self.hyper_params = hyper_params
        self.scan_parameters = scan_parameters
        self.property = property
        self.results = {}
        self.case_solutions = []
        
        
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
        
        if 'Integrals' in property:
            
            self.results['1st_Integral'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             81,
                                             2])
            
            self.results['2nd_Integral'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             81,
                                             2])
            
        if 'Forces' in property:
            
            self.results['Force_Per_Magnet_Type'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             self.hyper_params.magnets_per_period * self.hyper_params.magnet_rows,
                                             3])
            
            self.results['Force_Per_Row'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             self.hyper_params.magnet_rows,
                                             3])
            
            self.results['Force_Per_Quadrant'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             4,
                                             3])
            
            self.results['Force_Per_Beam'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             2,
                                             3])
            
        if 'Torques' in property:
            
            self.results['Torque_Per_Magnet_Type'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             self.hyper_params.magnets_per_period * self.magnet_rows,
                                             3])
            
            self.results['Torque_Per_Row'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             self.magnet_rows,
                                             3])
            
            self.results['Torque_Per_Quadrant'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             4,
                                             3])
            
            self.results['Torque_Per_Beam'] = np.zeros([len(self.scan_parameters.shiftmoderange),
                                             len(self.scan_parameters.gaprange),
                                             len(self.scan_parameters.shiftrange),
                                             2,
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
        
    def solve(self, property):
        #should solve through parameters
        self.property = property
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
                    
                    time1 = time.time()
                    #build the case models
                    casemodel = id.compensatedAPPLEv2(self.hyper_params)
                    time2 = time.time()
                    #solve the case model
                    casesol = CaseSolution(casemodel)
                    time3 = time.time()
                    #solve each type of calculation
                    if 'B' in self.property:
                        casesol.calculate_B_field()
                        print ('The peak field of this arrangement is {}'.format(casesol.bmax))
                        self.results['Bmax'][shiftmode,gap,shift] = casesol.bmax
                        self.results['Bfield'][shiftmode,gap,shift] = casesol.bfield
                    
                    if 'Integrals' in self.property:
                        casesol.calculate_first_integral()
                        casesol.calculate_second_integral()
                        
                    if 'Forces' in self.property:
                        #casesol.calculate_force_per_magnet()
                        casesol.calculate_force_per_row()
                        casesol.calculate_force_per_quadrant()
                        casesol.calculate_force_per_beam()
                        
                        print ('The force on this arrangement is {}'.format(casesol.beamforces[0]))
                        #load results into the solution
                        
                        self.results['Force_Per_Row'][shiftmode,gap,shift] = casesol.rowforces
                        self.results['Force_Per_Beam'][shiftmode,gap,shift] = casesol.beamforces
                        self.results['Force_Per_Quadrant'][shiftmode,gap,shift] = casesol.quadrantforces
                        #np.array([casesol.forceonquadrants['force_on_quadrant_1'],
                        #                                                                casesol.forceonquadrants['force_on_quadrant_2'],
                        #                                                                casesol.forceonquadrants['force_on_quadrant_3'],
                        #                                                                casesol.forceonquadrants['force_on_quadrant_4']])
                    time4 = time.time()
                    
                    print('time to build case model is {}'.format(time2-time1))
                    print('time to solve case model is {}'.format(time3-time2))
                    print('time to calculate case model is {}'.format(time4-time3))
                    
                    
                    self.case_solutions.append(casesol)
    
    def save(self,hf = None,solstring = 'Solution_0', fname = 'M:\Work\Athena_APPLEIII\Python\Results\\'):
        if hf == None:
            hf = h5.File(fname, 'w')
        
        hf.create_group(solstring)
        
        for key in self.results:
            hf.create_dataset('{}/{}'.format(solstring,key),data = self.results[key])
            
        hf.create_dataset('{}/{}'.format(solstring,'shiftrange'), data = self.scan_parameters.shiftrange)
        
        hf.create_dataset('{}/{}'.format(solstring,'gaprange'), data = self.scan_parameters.gaprange)
            
        for case in range(len(self.case_solutions)):
            thiscase = 'Case_'+str(case)
            self.case_solutions[case].case_save(hf,'{}/{}'.format(solstring,thiscase))
                
                #thiscase = 'Case_'+str(case)
                #hf.create_group('HyperSolution1/Solutions/Solution_'+ str(sol) + '/' +thiscase)
            
                #hf.create_dataset('{}/{}/{}/TwoPeriodB'.format(solstring,key,thiscase), data = self.case_solutions[case].bfield)
            
        
        pass
    
    def plot(self):
        pass
        
        
class HyperSolution():
    '''solves a hypersolution - hyperparameters can be varied'''
    def __init__(self,
                 base_hyper_parameters,
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
        
        self.base_hyper_parameters = parameters.model_parameters(**base_hyper_parameters)  #what is the fundamental model
        self.hyper_solution_variables = copy.deepcopy(hyper_solution_variables) #what parameters in the hyperparameters are being varied and their ranges
        self.hyper_solution_properties = copy.deepcopy(hyper_solution_properties) # 
        self.hyper_inputs = []
        self.hyper_results = {}
        self.solutions = []
        
        keylist = list(self.hyper_solution_variables.keys())
        
        #Build Hyper_Inputs
        
        if method == 'systematic':
            tmp = []
            for key in keylist:
                if type(self.hyper_solution_variables[key]) is list:
                    for i in range(len(self.hyper_solution_variables[key])):
                        tmp.append(self.hyper_solution_variables[key][i])
                
                else:
                    tmp.append(self.hyper_solution_variables[key])
            
            tmp1 = list(itertools.product(*tmp))
            
            for j in tmp1:
                jlist = list(j)
                for key in range(len(keylist)):
                    keylen = 1
                    if isinstance(base_hyper_parameters[keylist[key]],list):
                        keylen = len(base_hyper_parameters[keylist[key]])
                        base_hyper_parameters[keylist[key]] = jlist[0:keylen]
                    else:
                        base_hyper_parameters[keylist[key]] = jlist[0]
                    del jlist[0:keylen]
                    #check exisitng length
                
                new_hyper_params = parameters.model_parameters(**base_hyper_parameters)
                self.hyper_inputs.append(new_hyper_params)
            
    
        if method == 'random':
            #for n in iterations - build hyperparameter cases
            for n in range(iterations):
                
                
                
                
#                new_hyper_params = copy.deepcopy(base_hyper_params)
                #for key in dictionary
                for key in self.hyper_solution_variables:
                    #if key is list... or even if it's not
                    a = self.randomise_hyper_input(self.hyper_solution_variables[key])
                    base_hyper_parameters[key] = a
                    
#                    setattr(new_hyper_params,key, copy.copy(a))

                new_hyper_params = parameters.model_parameters(**base_hyper_parameters)
                self.hyper_inputs.append(new_hyper_params)
                
                    
                        
            
                    
            
        #build hyper_results dict
        
        #what shape of results array needed (i.e. steps in hyper_solution_variables)
        list_of_hyper_vars = list(self.hyper_solution_variables.keys())
        hyper_result_shape = []
        
#        for var in list_of_hyper_vars:
#            hyper_result_shape.append(len(self.hyper_solution_variables[var]))
            
        for var in list_of_hyper_vars:
            if isinstance(self.hyper_solution_variables[var], list):
                for i in range(len(self.hyper_solution_variables[var])):
                    hyper_result_shape.append(self.hyper_solution_variables[var][i].__len__())
                
            else:
                hyper_result_shape.append(self.hyper_solution_variables[var].__len__())
        
        if 'B' in self.hyper_solution_properties:
            self.hyper_results['Bmax'] = np.zeros(np.append(hyper_result_shape,3))
            
            #self.hyper_results['Bfieldharmonics'] = np.zeros(np.append(hyper_result_shape,[2,10]))
            
            self.hyper_results['Beff'] = np.zeros(np.append(hyper_result_shape,3))
        
        if 'Integrals' in self.hyper_solution_properties:
            self.hyper_results['1st_Integral_Max_Harmonic'] = np.zeros(np.append(hyper_result_shape,11,2))
            self.hyper_results['2nd_Integral_Max_Harmonic'] = np.zeros(np.append(hyper_result_shape,11,2))
          
        if 'Forces' in self.hyper_solution_properties:
            self.hyper_results['Force_Per_Magnet_Type'] = np.zeros(np.append(hyper_result_shape,[self.base_hyper_parameters.magnet_rows*self.base_hyper_parameters.magnets_per_period, 3]))
            self.hyper_results['Force_Per_Row'] = np.zeros(np.append(hyper_result_shape,[self.base_hyper_parameters.magnet_rows,3]))
            self.hyper_results['Force_Per_Quadrant'] = np.zeros(np.append(hyper_result_shape,[4,3]))
            self.hyper_results['Force_Per_Beam'] = np.zeros(np.append(hyper_result_shape,[2,3]))
            
            
        if 'Torques' in self.hyper_solution_properties:
            self.hyper_results['Max_Single_Magnet_Torque'] = np.zeros(np.append(hyper_result_shape,3))
            self.hyper_results['Max_Single_Row_Torque'] = np.zeros(np.append(hyper_result_shape,3))
            self.hyper_results['Max_Single_Quadrant_Torque'] = np.zeros(np.append(hyper_result_shape,3))
            self.hyper_results['Max_Single_Beam_Torque'] = np.zeros(np.append(hyper_result_shape,3))
            
            #time one solution
            #offer estimate
            #offer random
        
        
        
            #for element of dict
            #randomly select value
            #Solution
            #extract hyperresults
            
        
        #when 
        #recursively for each hyperparameter argumment given
    def solve(self):
        i = 0
        for hpset in self.hyper_inputs: #hpset = hyperparameter set
            
            #memory tracing
            tracemalloc.start(5)
            time1 = tracemalloc.take_snapshot()
            
            print("Solving HyperParameter Set {} of {}".format(i+1, len(self.hyper_inputs)))
            tmp_sol = Solution(hpset, self.scan_parameters, property = self.hyper_solution_properties)
            print('Solving for slices of {}'.format(hpset.block_subdivision))
            tmp_sol.solve(self.hyper_solution_properties)
            
            
            
            #self.hyper_results.append(tmp_sol.results)
            
            self.solutions.append(tmp_sol)
            
            i+=1
            
            #print malloc output here
            time2 = tracemalloc.take_snapshot()
            
            stats = time2.compare_to(time1, 'lineno') 
            for stat in stats[:3]:
                print(stat)
                

            
        self.extract_hyper_results(tmp_sol)
            
    def extract_hyper_results(self,solution):
        for attribute in self.hyper_results:
            a = 0
            #reshape solutions into numpy array
            tmpsolshape = []
            #workaround beacuase some attributes are lists of np arrays, others are just np arrays.
            #must be a better way of doing this!
            
            for key in self.hyper_solution_variables:
                if isinstance(self.hyper_solution_variables[key], list):
                    for i in range(len(self.hyper_solution_variables[key])):
                        tmpsolshape.append(self.hyper_solution_variables[key][i].__len__())
                
                else:
                    tmpsolshape.append(self.hyper_solution_variables[key].__len__())

            
            #for i in range(len(list(self.hyper_solution_variables.keys()))):
            #    tmpsolshape.append(len(list(self.hyper_solution_variables.values())[i]))
            
            #tmpsols = np.reshape(np.array(self.solutions),self.hyper_results[attribute].shape[:-1])
            tmpsols = np.reshape(np.array(self.solutions),tmpsolshape)
            
            for idx, value in np.ndenumerate(self.hyper_results[attribute]):
            #for idx, value in np.ndenumerate(tmpsols):

                if a != idx[:len(tmpsolshape)]: 
                    #self.hyper_results[attribute][idx[:len(tmpsolshape)]] = np.amax(tmpsols[idx[:len(tmpsolshape)]].results[attribute],2)
                    self.hyper_results[attribute][idx[:len(tmpsolshape)]] = self.maxabs2(self.maxabs2(tmpsols[idx[:len(tmpsolshape)]].results[attribute],2),1)
                    print (idx[:len(tmpsolshape)])
                a = idx[:len(tmpsolshape)]
            
            #for soln in range(len(self.hyper_results[attribute])):
                #self.hyper_results[attribute][soln] = np.amax(self.solutions[soln].results[attribute],2)
        
        print(1)
        
    def maxabs2(self, a, axis = None):
        #first mind amin
        mins = np.amin(a,axis)
        maxs = np.amax(a,axis)
        res = mins
        
        it = np.nditer(maxs, flags=['multi_index'])
        while not it.finished:
            if np.abs(mins[it.multi_index])> np.abs(maxs[it.multi_index]):
                res[it.multi_index] = mins[it.multi_index]
            elif np.abs(maxs[it.multi_index])> np.abs(mins[it.multi_index]):
                res[it.multi_index] = maxs[it.multi_index]
            it.iternext()
        
        return res
    
    def maxabs(self, a, axis=None):
        """Return slice of a, keeping only those values that are furthest away
        from 0 along axis"""
        maxa = a.max(axis=axis)
        mina = a.min(axis=axis)
        p = abs(maxa) > abs(mina) # bool, or indices where +ve values win
        n = abs(mina) > abs(maxa) # bool, or indices where -ve values win
        if axis == None:
            if p: return maxa
            else: return mina
        shape = list(a.shape)
        shape.pop(axis)
        out = np.zeros(shape, dtype=a.dtype)
        out[p] = maxa[p]
        out[n] = mina[n]
        return out
    
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
            

    def save(self,savefile):
        hf = h5.File(savefile, 'w')
        
        #save info on hyperspace search
        #what name? HS1, HS2, HS3 etc - HyperSolution1
        #saves hyperspace inputs and outputs (are there any sensible HyperSpace outputs?)
        hf.create_group('HyperSolution1')
        hf.create_group('HyperSolution1/HyperParamaters')
        #pop iterated hyperparamaters to new dict... actually can they be binned?
        
        #iterate keys in base_hypersolution_variables to create dataset
        for fixed_parameter in self.base_hyper_parameters.__dict__.keys():
            print('saving fixed parameter {}'.format(fixed_parameter))
            #skip varied parameters
            if fixed_parameter in self.hyper_solution_variables.keys():
                print ('{} is not fixed in this hypersolution'.format(fixed_parameter))
            #if is a class
            elif hasattr(self.base_hyper_parameters.__dict__[fixed_parameter],'__dict__'):
                hf.create_group('HyperSolution1/HyperParamaters/'+fixed_parameter)
                for fixed_sub_parameter in self.base_hyper_parameters.__dict__[fixed_parameter].__dict__.keys():
                    hf.create_dataset('HyperSolution1/HyperParamaters/'+fixed_parameter+'/'+fixed_sub_parameter, data = self.base_hyper_parameters.__dict__[fixed_parameter].__dict__[fixed_sub_parameter])
            #if just a supported type, write.
            else:
                hf.create_dataset('HyperSolution1/HyperParamaters/'+fixed_parameter, data = self.base_hyper_parameters.__dict__[fixed_parameter])
        
        # write varied hyperparameters = Hypervariables
        for varied_parameter in self.hyper_solution_variables.keys():
            dname = 'HyperSolution1/HyperVariables/{}'.format(varied_parameter)
            if isinstance(self.hyper_solution_variables[varied_parameter],list):
                for i in range(len(self.hyper_solution_variables[varied_parameter])):
                    dnamei = '{}_{}'.format(dname,i)
                    hf.create_dataset(dnamei, data = self.hyper_solution_variables[varied_parameter][i])
            else:
                hf.create_dataset(dname, data = self.hyper_solution_variables[varied_parameter])
#            hf[dname].make_scale(varied_parameter)
            
        dscalnames = list(self.hyper_solution_variables.keys())
        
        # write hyperresults
        hf.create_group('HyperSolution1/HyperResults')
        
        for result in self.hyper_results.keys():
            dname = 'HyperSolution1/HyperResults/{}'.format(result)
            hf.create_dataset(dname, data = self.hyper_results[result])
            for i in range(len(dscalnames)):
                hf[dname].dims[0].label = dscalnames[0]
            print (1)
            #need to add attribute of min/max etc
        
        #for each solution, creat group SolutionX
        #has results and inputs and search spaces (gap, shift scan etc(
        for sol in range(len(self.solutions)):
#            this solution = 
            solstring = 'HyperSolution1/Solutions/Solution_'+ str(sol)
            self.solutions[sol].save(hf,solstring)
            #hf.create_group('HyperSolution1/Solutions/Solution_'+ str(sol))
        #for each case, create group CaseX
        #has results and inputs for each case
            #for case in range(len(self.solutions[sol].case_solutions)):
            #    thiscase = 'Case_'+str(case)
            #    hf.create_group('HyperSolution1/Solutions/Solution_'+ str(sol) + '/' +thiscase)
            #    
            #    hf.create_dataset('HyperSolution1/Solutions/Solution_'+ str(sol) + '/' +thiscase + '/TwoPeriodB', data = self.solutions[sol].case_solutions[case].bfield)
                #hf.create_dataset('HyperSolution1/Solutions/Solution_'+ str(sol) + '/' +thiscase + '/B/Per_Beam', data = self.solutions[sol].case_solutions[case].
                
        
        #does this leave a lot of duplicated data? Yes
        
        hf.close()
        
    
if __name__ == '__main__':
    ### developing Case Solution ###
    
    test_hyper_params = parameters.model_parameters(Mova = 20, 
                                             periods = 1, 
                                             periodlength = 15,
                                             nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                             #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                             nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                             nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                             compappleseparation = 7.5,
                                             apple_clampcut = 3.0,
                                             comp_magnet_chamfer = [3.0,0.0,3.0],
                                             magnets_per_period = 6,
                                             gap = 2, 
                                             rowshift = 0,
                                             shiftmode = 'circular',
                                             block_subdivision = [1,1,1]
                                             )
    a = id.compensatedAPPLEv2(test_hyper_params)
#    
    case1 = CaseSolution(a)
    case1.calculate_B_field()
    print(case1.bmax)
    print(1)
#    case1.calculate_force_per_beam()
#    case1.calculate_force_per_quadrant()
#    case1.calculate_force_per_row()
    
#    case1.case_save(False, 'Single_Case', fname = 'M:\Work\Athena_APPLEIII\Python\Results\\casedev210210.h5')
#    
    #draw object
#    rd.ObjDrwOpenGL(a.cont.radobj)
    
#    plt.plot(case1.bfield[:,0],case1.bfield[:,1:4])
#    plt.legend(['bx','by','bz'])
    
    #show it
#    plt.show()
    
    ### Developing Model Solution ### Range of gap. rowshift and shiftmode ###
    gaprange = np.arange(2,10.1,40)
    shiftrange = np.arange(-7.5,7.51, 3.75)
    shiftmoderange = ['linear','circular']
    
    #scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange, shiftmoderange = shiftmoderange)
    scan_parameters = parameters.scan_parameters(periodlength = test_hyper_params.periodlength, gaprange = gaprange, shiftrange = shiftrange)
    
#    sol1 = Solution(test_hyper_params, scan_parameters)
#    sol1.solve()
#    sol1.save(hf = None, solstring = 'Sol1', fname = 'M:\Work\Athena_APPLEIII\Python\Results\\Solution.h5')
    
    ### Developing model Hypersolution
    
    #test_hyper_params is a params object
    #solution_parameters is a list of two iterators and a list
    
    #create test hyper params as dict
    test_hyper_params_dict = {'Mova': 20,
                              'periods' : 5,
                              'periodlength' : 15,
                              'nominal_fmagnet_dimensions' : [15.0,0.0,15.0], #obsoleted by 'square_magnet'
                              'nominal_cmagnet_dimensions' : [7.5,0.0,15.0], #obsoleted by 'square_magnet'
                              'nominal_vcmagnet_dimensions' : [7.5,0.0,15.0], #obsoleted by 'square_magnet'
                              'nominal_hcmagnet_dimensions' : [7.5,0.0,15.0], #obsoleted by 'square_magnet'
                              'compappleseparation' : 7.5,
                              'apple_clampcut' : 3.0,
                              'comp_magnet_chamfer' : [3.0,0.0,3.0],
                              'magnets_per_period' :6,
                              'gap' : 2, 
                              'rowshift' : 4,
                              'shiftmode' : 'circular',
                              #'square_magnet' : 15.0,
                              #'block_subdivision' : [1,1,1]
                              }
    
    #hypersolution_variables a dict of ranges. Can only be ranges of existing parameters in test_hyper_params
    hyper_solution_variables = {
        #"block_subdivision" : [np.array([2]),np.arange(2,4),np.arange(3,4)],
        #"Mova" : np.arange(15,25.1,5),
        #"nominal_vcmagnet_dimensions": [np.arange(7.5,8,10),np.arange(0.0,1.0,10.0),np.arange(10,25.1,2.5)],
        #"nominal_hcmagnet_dimensions": [np.arange(7.5,8.1,2),np.arange(0.0,1.0,10.0),np.arange(10,15.1,1)],
        #"square_magnet" : np.arange(10,20.1,5),
        #"rowtorowgap" : np.arange(0.4,0.51,0.1),
        "magnets_per_period" : np.arange(4,11,2)
        }
    
    hyper_solution_properties = ['B']
    
    #create hypersolution object
    hypersol1 = HyperSolution(base_hyper_parameters = test_hyper_params_dict, 
                              hyper_solution_variables = hyper_solution_variables, 
                              hyper_solution_properties = hyper_solution_properties,
                              scan_parameters = scan_parameters,
                              method = 'systematic',
                              iterations = 60)
    
#    hypersol1.solve()
    
    rootname = 'nper210216'
    
#    with open('M:\Work\Athena_APPLEIII\Python\Results\\{}.dat'.format(rootname),'wb') as fp:
#        pickle.dump(hypersol1,fp,protocol=pickle.HIGHEST_PROTOCOL)
    
    with open('M:\Work\Athena_APPLEIII\Python\Results\\{}.dat'.format(rootname),'rb') as fp:
        hypersol1 = pickle.load(fp)
    
    hypersol1.save('M:\Work\Athena_APPLEIII\Python\Results\\{}.h5'.format(rootname))
    
    mynumpyarray = np.zeros([len(hypersol1.hyper_results),2])
    
    for i in range(len(hypersol1.hyper_results)):
        mynumpyarray[i] = [hypersol1.hyper_inputs[i].square_magnet,
                           hypersol1.hyper_results[i]['Bmax'][0,0,0,0]]
        
    plt.plot(mynumpyarray[:,0],mynumpyarray[:,1])
    
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
    