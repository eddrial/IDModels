'''
Created on Apr 9, 2025

@author: oqb
'''
import matplotlib.pyplot as plt
import numpy as np
import h5py as h5

import plotly

if __name__ == '__main__':
    filename = 'D:\Profile\oqb\IVUE32_2023\Calculations\ivue32_lin_asym_comp_221_20250409.h5'
    dname = 'D:\Profile\oqb\IVUE32_2023\Calculations\Plots'
    
    #read hdf5
    with h5.File(filename, "r") as f:
        # Print all root level object names (aka keys) 
        # these can be group or dataset names 
        print("Keys: %s" % f.keys())
        # get first object name/key; may or may NOT be a group
        a_group_key = list(f.keys())[0]
    
        # get the object type for a_group_key: usually group or dataset
        print(type(f[a_group_key])) 
    
        # If a_group_key is a group name, 
        # this gets the object names in the group and returns as a list
        data = list(f[a_group_key])
    
        # If a_group_key is a dataset name, 
        # this gets the dataset values and returns as a list
        data = list(f[a_group_key])
        # preferred methods to get dataset values:
        ds_obj = f[a_group_key]      # returns as a h5py dataset object
#        ds_arr = f[a_group_key][()]  # returns as a numpy array

        forces = f['Solution_0']['Force_Per_Quadrant'][()][0,0,:,:,:]
        
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
#soa = np.array([[0, 0, 1, 1, -2, 0], [0, 0, 2, 1, 1, 0], [0, 0, 3, 2, 1, 0], [0, 0, 4, 0.5, 0.7, 0]])
#X, Y, Z, U, V, W = zip(*soa)
X, Y, Z = np.zeros(3)
colours = ['red','green','yellow','blue']
for shift in range(len(forces)):
    
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlim([-2000, 2000])
    ax.set_ylim([-2000, 2000])
    ax.set_zlim([-2000, 2000])
    for row in range(len(forces[shift])):
        U,V,W = forces[shift,row]
        ax.quiver(X, Y, Z, U, V, W, color=colours[row])
        #ax.quiverkey(ax, 0,0,500, 'Quadrant {}'.format(row+1))
    
    ax.set_title("Force Vectors per Quadrant")
    plt.savefig('{}\\forcevectorscompapple_lin{}.png'.format(dname, shift))
    #plt.show()