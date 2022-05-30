import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

if __name__ == '__main__':
    #load Bfield data as a json feed. 4d array [X_pos, S_pos, Z_pos, B_component (x,s,z)]
    with open('M:\\Work\\JiliAPPLE\\Bfield_x_s_z_Bxsz_fine_25mm.json','r') as fp:
        B_Array = json.load(fp)
        
    fp.close()
    
    #copy into numpy array
    B_Array_np = np.array(B_Array)
    
    #load position data as a json feed. 3d array [X_pos, S_pos, Z_pos]
    with open('M:\\Work\\JiliAPPLE\\Location_x_s_z.json','r') as fp:
        pos = json.load(fp)
        
    fp.close()
    #copy into numpy array
    pos_np = np.array(pos)
    
    #the range over which the data was calculated
    xrange = np.arange(-50,51)
    srange = np.arange(-50,51)
    zrange = np.arange(-12,13)
    
    #create a grid to plot against
    Xx,Ss = np.meshgrid(xrange,srange)
    
    #3d plot of Bz
    figz, axz = plt.subplots(subplot_kw={"projection": "3d"})
    surfz = axz.plot_surface(Xx, Ss, B_Array_np[:,:,12,2], cmap=cm.coolwarm, linewidth=0, antialiased=False)
    
    #3d plot of Bx
    figx, axx = plt.subplots(subplot_kw={"projection": "3d"})
    surfx = axx.plot_surface(Xx, Ss, B_Array_np[:,:,12,0], cmap=cm.coolwarm, linewidth=0, antialiased=False)
    
    plt.show()
    
    input("Press Enter to continue...")