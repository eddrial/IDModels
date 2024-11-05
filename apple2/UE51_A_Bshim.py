'''
Created on 4 Jan 2022

@author: oqb
'''
import numpy as np
import radia as rd
from wradia import wrad_obj as wrd
import apple2p5.model2 as id1
from idcomponents import parameters
from idanalysis import analysis_functions as af
from idanalysis.analysis_functions import Solution
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation,  CubicTriInterpolator
from shapely.geometry import LineString, point
import time
import h5py as h5
from scipy.interpolate import CubicSpline
from scipy.linalg import pinv


if __name__ == '__main__':
    #define parameter space
    #gaps = np.array([15,17,20,25,30,40,50])
    gaps = np.arange(15,16,100)
    shifts = np.arange(-25.65,25.7,12.825)
    #shifts = np.arange(0,3,4)
    #shiftmodes = ['circular', 'linear']
    shiftmodes = ['circular']
    #set up APPLE 2 device (UE51)
    #solve peakfield in parameter space
    print (gaps)
    print(shifts)
    
    min_gap = 15
    
    #parameter_Set Horizontal_polarisation
    UE51_params = parameters.model_parameters(Mova = 0,
                                        periods = 15, 
                                        periodlength =51.3,
                                        nominal_fmagnet_dimensions = [40.0,0.0,40.0], 
                                        #square_magnet = True,
                                        nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                        #nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                        #nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                        compappleseparation = 75,
                                        apple_clampcut = 5.0,
                                        comp_magnet_chamfer = [3.0,0.0,3.0],
                                        magnets_per_period = 4,
                                        gap = min_gap, 
                                        rowshift = 0,
                                        shiftmode = 'linear', 
                                        block_subdivision = [3,2,1],
                                        M = 1.3                                        
                                        )
    
    basescan = parameters.scan_parameters(51,gaprange = gaps,shiftrange = shifts, shiftmoderange = shiftmodes)
    
    #set up z axis
    
    z_scale = np.arange(-30,30.1,2)
    
    
    
    #calculate response matrices
    #there are 8 knobs. ALL MOTION IN GLOBAL COORDINATE SYSTEM
    #OH (Z- Y+) horizontal shift axis zero of model - positive is towards slot [ Z shift]
    #OH (Z- Y+) vertical shift axis zero of model - positive is out of gap
    #OV (Z+ Y+) horizontal shift axis 1 of model - positive isaway from slot
    #OV (Z+ Y+) vertical shift axis one of model - positive out of gap
    #UH (Z- Y-) horizontal shift axis two of model - positive in to gap
    #UH (Z- Y-) vertical shift axis two of model - positive is towards slot
    #UV (Z- Y+) horizontal shift axis three of model - positive is away from slot
    #UV (Z- Y+) vertical shift axis three of model - positive in towards gap
    
    #Order of quadrants
    quadrant_names = ['OH','OV','UH','UV']
    #order of shifts
    shim_order = ['Horz','Vert']
    
    #order of integrals in results
    field_integrals = ['IBy', 'IBz']
    
    #calculate base scenario [z_pos, IBY/IBZ]
    base_integral = np.zeros([z_scale.__len__(),2])
    
    UE51 = id1.plainAPPLE(UE51_params)
    UE51.cont.wradSolve()
    a = rd.FldPtcTrj(UE51.cont.radobj,1.7,[0,0,0,0],[-500,500],1001)
    a = np.asarray(a)
    
    b = rd.FldLst(UE51.cont.radobj,'bxbybz',[0,-500,0],[0,500,0],1001,'arg')
    b = np.asarray(b)
    
    for i in range(len(z_scale)):
        base_integral[i,0] = rd.FldInt(UE51.cont.radobj,'inf','ibz',[z_scale[i],-500,0],[z_scale[i],500,0])
        base_integral[i,1] = rd.FldInt(UE51.cont.radobj,'inf','ibx',[z_scale[i],-500,0],[z_scale[i],500,0])
    
    rd.UtiDelAll()
    
    #calculate signal
    shift_signal = np.zeros([len(shifts),len(z_scale),len(field_integrals)])
    
    
    for shift in range(len(shifts)):
        tmp_response = np.zeros([len(z_scale),len(field_integrals)])
        UE51_params.rowshift = shifts[shift]
        
        vshim = id1.plainAPPLE(UE51_params)
        vshim.cont.wradSolve()

        for i in range(len(z_scale)):
            tmp_response[i,0] = rd.FldInt(vshim.cont.radobj,'inf','ibz',[z_scale[i],-500,0],[z_scale[i],500,0])
            tmp_response[i,1] = rd.FldInt(vshim.cont.radobj,'inf','ibx',[z_scale[i],-500,0],[z_scale[i],500,0])
        
        shift_signal[shift] = tmp_response-base_integral
        rd.UtiDelAll()
    
#plot responses with titles and all
    
    shim_response_plots = plt.subplots(len(quadrant_names),len(shim_order), sharex = True, sharey = True, figsize = (5,10))
    
    for quad in range(len(quadrant_names)):
        for dir in range(len(shim_order)):
            for integ in range(len(field_integrals)):
                shim_response_plots[1][quad][dir].plot(z_scale,shim_response[quad,dir,:,integ],
                                                      label = '{}'.format(field_integrals[integ]))
                shim_response_plots[1][quad][dir].set_title('Quadrant {}, Direction {}'.format(quadrant_names[quad], shim_order[dir]))
                
    shim_response_plots[0].legend((shim_response_plots[1][0,0].lines[0],shim_response_plots[1][0,0].lines[1]),
                                  (shim_response_plots[1][0,0].lines[0].get_label(),shim_response_plots[1][0,0].lines[1].get_label()))
    
    shim_response_plots[0].suptitle('UE51 Shim Response Signals for +0.1mm motion in Y and Z. - Magnet')
    shim_response_plots[0].text(0.5, 0.04, 'Z (mm)', ha='center')
    shim_response_plots[0].text(0.04, 0.5, 'IBy/IBz (Tmm)', va='center', rotation='vertical')
    shim_response_plots[0].savefig('D:/Work - Laptop/UE51/UE51 Measurements/virtual_shim_response.png', transparent=False)
    
    
    
#    print('saving hdf5 data')
    
#    with h5.File('D:/Work - Laptop/UE51/UE51 Measurements/virtual_shim_response.h5', 'a') as f:
#        dset = f.require_dataset('Virtual Shim Response',shape = shim_response.shape, dtype = shim_response.dtype)
#        dset[...] = shim_response
#        
#        f['Virtual Shim Response'].dims[0].label = 'Quadrant'
#        f['Virtual Shim Response'].dims[1].label = 'Shim Direction'
 #       f['Virtual Shim Response'].dims[2].label = 'Z'
#        f['Virtual Shim Response'].dims[3].label = 'Field Integral'
#        
#        f['Quadrants'] = quadrant_names
#        f['z_scale'] = z_scale
#        f['Shim Direction'] = shim_order
#        f['Field Integrals'] = field_integrals
#        
#        f['z_scale'].make_scale()
#        
#        f['Virtual Shim Response'].dims[1].attach_scale(f['z_scale'])
        
    
    
    #function to calculate pseudoinverse
    #stack signals and invert to create target. (IYIZ)
    #rebase measured signal to y_scale
    #make interpolation
    spliy = CubicSpline(UE51_MW_Meas35[:,0]-70,UE51_MW_Meas35[:,1])
    spliz = CubicSpline(UE51_MW_Meas35[:,0]-70,UE51_MW_Meas35[:,2])
    
    target_iy = spliy(z_scale)
    target_iz = spliz(z_scale)
    
    target = -1*(np.hstack((target_iy, target_iz)))
    
    flat_shim_response = shim_response.reshape((shim_response.shape[0],
                                                shim_response.shape[1],
                                                shim_response.shape[2]*shim_response.shape[3]),order = 'F')
    flatter_shim_response = np.vstack((flat_shim_response[0,0,:],flat_shim_response[0,1,:],
                                       flat_shim_response[1,0,:],flat_shim_response[1,1,:],
                                       flat_shim_response[2,0,:],flat_shim_response[2,1,:],
                                       flat_shim_response[3,0,:],flat_shim_response[3,1,:]))
    
    pinv_response = pinv(flatter_shim_response)
    
    correction = np.dot(target,pinv_response)
    
    rounded_correction =np.round(2*correction)/2 
    
    prediction = np.dot(correction,flatter_shim_response)
    
    rounded_prediction = np.dot(rounded_correction,flatter_shim_response)
    prediction_residual = prediction - target
    
    rounded_residual = (rounded_prediction - target)
    
    shim_prediction_plot = plt.subplots(1,1)
    
    shim_prediction_plot[1].plot(z_scale,target[:len(z_scale)], label = 'Target Iy')
    shim_prediction_plot[1].plot(z_scale,target[len(z_scale):], label = 'Target Iz')
    shim_prediction_plot[1].plot(z_scale,rounded_prediction[:len(z_scale)], label = 'Predicted Iy')
    shim_prediction_plot[1].plot(z_scale,rounded_prediction[len(z_scale):], label = 'Predicted Iz')
    shim_prediction_plot[1].plot(z_scale,rounded_residual[:len(z_scale)], label = 'Residual Iy')
    shim_prediction_plot[1].plot(z_scale,rounded_residual[len(z_scale):], label = 'Residual Iz')
    
    shim_prediction_plot[1].legend()
    
    plt.show()
    
    print('correction is {}'.format(rounded_correction))
    
    print('pause')
    #reshape response matrix
    #solve for pinv
    #plot out expected solution
    #print out 
    
    print('placeholder')
    
    