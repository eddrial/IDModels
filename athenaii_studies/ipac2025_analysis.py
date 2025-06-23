'''
Created on May 9, 2025

analysis of results of hdf5 cryoAPPLE_asym_221_20250507
folder D:\Work - Laptop\CryoAPPLE\Results

@author: oqb
'''



import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
#import fpdf
#from bokeh.core.property.visual import FontSize
from openpyxl.utils.cell import rows_from_range

        ### developing Case Solution ###
def plot_individual_magnets():
    #read in hdf5 data
    thedatacirc = h5.File("M:\Work\Athena_APPLEIII\Python\Results\circ_mag_forces_6per210426.h5",'r')
    thedatalin = h5.File("M:\Work\Athena_APPLEIII\Python\Results\lin_mag_forces_6per210426.h5",'r')
    
    #force_per_magnet_circ [mode,gap,shift,row,position,Bcomponent]
    fpmc = np.array(thedatacirc['Solution_0']['Force_Per_Magnet_Type'])
    fpml = np.array(thedatalin['Solution_0']['Force_Per_Magnet_Type'])
    shift = np.array(thedatacirc['Solution_0']['shiftrange'])
    gaps = np.array(thedatacirc['Solution_0']['gaprange'])
    rows = np.arange(12)
    mag_ID = np.arange(6)
    rowtypes = ['Functional','Functional','Functional','Functional',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation']
    component = ['Transverse','Longitudinal','Vertical']
    #columntext = ['{:.3f}'.format(x) for x in shift]
    columntext = ['' for x in shift]
    rowtext = ('shift','parallel','antiparallel') 
    force_scale = [25,100,75] #max value in newtons of force in each direction
    
    #plotting for each type of magnet
    #for gap
#    for gap in gaps:
#        for row in rows:
#            for magnet in mag_ID:
        #for row
            #for magnet 
    for g in range(len(gaps)):
        for r in range(len(rows)):
            for m in range(len(mag_ID)):
    
                fig, ax = plt.subplots(3,1)
                
                fig.subplots_adjust(hspace=0.8)
                
                fig.set_figheight(9)
                fig.set_figwidth(4.5)
                
                fig.suptitle('Forces on Magnet Row {} Magnet {}\n{} Row : Gap {}mm'.format(r+1,mag_ID[m],rowtypes[r], gaps[g]), fontsize = 'medium')
                
                for i in range(3):
                    #plot formatting
                                           
                    #axes plots
                    ax[i].plot(shift,fpmc[0,g,:,r,m,i], label = 'parallel/circular')
                    ax[i].plot(shift,fpml[0,g,:,r,m,i], label = 'antiparallel/linear')
                    
                    #axis scale
                    ax[i].set_ylim(-force_scale[i],force_scale[i])
                    #Axes title & Text etc
                    ax[i].set_title('{} Axis Force (N)'.format(component[i]),
                                    fontsize = 'small')
                    ax[i].set_xticks(np.arange(-7.5,7.6,1.875))
                    ax[i].tick_params(
                        axis='x',          # changes apply to the x-axis
                        which='both',      # both major and minor ticks are affected
                        bottom=True,      # ticks along the bottom edge are on
                        top=True,         # ticks along the top edge are on
                        labelbottom=False, # labels along the bottom edge are off
                        direction = 'in') # ticks are directed in ) 
                    ax[i].tick_params(
                        axis  = 'y',
                        labelsize = 'x-small'
                        )
                    ax[i].legend(fontsize = 'xx-small')
                    
                    #table Data
                    forcetext = []
                    forcetext.append(['{:.3f}'.format(x) for x in shift])
                    forcetext.append(['{:.2f}'.format(x) for x in fpmc[0,g,:,r,m,i]])
                    forcetext.append(['{:.2f}'.format(x) for x in fpml[0,g,:,r,m,i]])
                        
                    tab = ax[i].table(cellText = forcetext,
                                rowLabels = rowtext,
                                rowLoc = 'right',
                                colLabels = columntext,
                                colLoc = 'right')
                    
                    tab.set_fontsize(5)
                    
                fig.savefig("M:\\Work\\Athena_APPLEIII\\Python\\Results\\Force_Plots\\force_gap_{}_row_{}_magnet_{}.png".format(gaps[g],r+1,mag_ID[m]))
                #fig.show()
def plot_triplet_packs():
    #read in hdf5 data
    thedatacirc = h5.File("M:\Work\Athena_APPLEIII\Python\Results\circ_mag_forces_6per210426.h5",'r')
    thedatalin = h5.File("M:\Work\Athena_APPLEIII\Python\Results\lin_mag_forces_6per210426.h5",'r')
    
    #force_per_magnet_circ [mode,gap,shift,row,position,Bcomponent]
    fpmc = np.array(thedatacirc['Solution_0']['Force_Per_Magnet_Type'])
    fpml = np.array(thedatalin['Solution_0']['Force_Per_Magnet_Type'])
    shift = np.array(thedatacirc['Solution_0']['shiftrange'])
    gaps = np.array(thedatacirc['Solution_0']['gaprange'])
    rows = np.arange(12)
    mag_ID = np.arange(6)
    mag_packs = ['501','234']
    rowtypes = ['Functional','Functional','Functional','Functional',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation']
    component = ['Transverse','Longitudinal','Vertical']
    #columntext = ['{:.3f}'.format(x) for x in shift]
    columntext = ['' for x in shift]
    rowtext = ('shift','parallel','antiparallel') 
    force_scale = [50,100,75] #max value in newtons of force in each direction
    
    #plotting for each type of magnet
    #for gap
#    for gap in gaps:
#        for row in rows:
#            for magnet in mag_ID:
        #for row
            #for magnet 
    for g in range(len(gaps)):
        for r in range(len(rows)):
            for mp in range(2):
    
                fig, ax = plt.subplots(3,1)
                
                fig.subplots_adjust(hspace=0.8)
                
                fig.set_figheight(9)
                fig.set_figwidth(4.5)
                
                fig.suptitle('Forces on Magnet Row {} Triplet {}{}{}\n{} Row : Gap {}mm'.format(r+1,mag_ID[3*mp-1],mag_ID[3*mp],mag_ID[3*mp+1],rowtypes[r], gaps[g]), fontsize = 'medium')
                
                for i in range(3):
                    #plot formatting
                                           
                    #axes plots
                    ax[i].plot(shift,fpmc[0,g,:,r,3*mp-1,i]+fpmc[0,g,:,r,3*mp,i]+fpmc[0,g,:,r,3*mp+1,i], label = 'parallel/circular')
                    ax[i].plot(shift,fpml[0,g,:,r,3*mp-1,i]+fpml[0,g,:,r,3*mp,i]+fpml[0,g,:,r,3*mp+1,i], label = 'antiparallel/linear')
                    
                    #axis scale
                    ax[i].set_ylim(-force_scale[i],force_scale[i])
                    #Axes title & Text etc
                    ax[i].set_title('{} Axis Force (N)'.format(component[i]),
                                    fontsize = 'small')
                    ax[i].set_xticks(np.arange(-7.5,7.6,1.875))
                    ax[i].tick_params(
                        axis='x',          # changes apply to the x-axis
                        which='both',      # both major and minor ticks are affected
                        bottom=True,      # ticks along the bottom edge are on
                        top=True,         # ticks along the top edge are on
                        labelbottom=False, # labels along the bottom edge are off
                        direction = 'in') # ticks are directed in ) 
                    ax[i].tick_params(
                        axis  = 'y',
                        labelsize = 'x-small'
                        )
                    ax[i].legend(fontsize = 'xx-small')
                    
                    #table Data
                    forcetext = []
                    forcetext.append(['{:.3f}'.format(x) for x in shift])
                    forcetext.append(['{:.2f}'.format(x) for x in fpmc[0,g,:,r,3*mp-1,i]+fpmc[0,g,:,r,3*mp,i]+fpmc[0,g,:,r,3*mp+1,i]])
                    forcetext.append(['{:.2f}'.format(x) for x in fpml[0,g,:,r,3*mp-1,i]+fpml[0,g,:,r,3*mp,i]+fpml[0,g,:,r,3*mp+1,i]])
                        
                    tab = ax[i].table(cellText = forcetext,
                                rowLabels = rowtext,
                                rowLoc = 'right',
                                colLabels = columntext,
                                colLoc = 'right')
                    
                    tab.set_fontsize(5)
                    
                fig.savefig("M:\\Work\\Athena_APPLEIII\\Python\\Results\\Force_Plots\\force_gap_{}_row_{}_triplet_{}{}{}.png".format(gaps[g],r+1,mag_ID[3*mp-1],mag_ID[3*mp],mag_ID[3*mp+1]))
                
def plot_keeper():
    #read in hdf5 data
    thedatacirc = h5.File("M:\Work\Athena_APPLEIII\Python\Results\circ_mag_forces_6per210426.h5",'r')
    thedatalin = h5.File("M:\Work\Athena_APPLEIII\Python\Results\lin_mag_forces_6per210426.h5",'r')
    
    #force_per_magnet_circ [mode,gap,shift,row,position,Bcomponent]
    fpmc = np.array(thedatacirc['Solution_0']['Force_Per_Magnet_Type'])
    fpml = np.array(thedatalin['Solution_0']['Force_Per_Magnet_Type'])
    shift = np.array(thedatacirc['Solution_0']['shiftrange'])
    gaps = np.array(thedatacirc['Solution_0']['gaprange'])
    rows = np.arange(12)
    quadrants = np.arange(4)
    mag_ID = np.arange(6)
    rowinq = [[0,4,5],[1,6,7],[2,8,9],[3,10,11]]
    mag_packs = ['501','234']
    rowtypes = ['Functional','Functional','Functional','Functional',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation']
    component = ['Transverse','Longitudinal','Vertical']
    #columntext = ['{:.3f}'.format(x) for x in shift]
    columntext = ['' for x in shift]
    rowtext = ('shift','parallel','antiparallel') 
    force_scale = [50,100,75] #max value in newtons of force in each direction
    
    #plotting for each type of magnet
    #for gap
#    for gap in gaps:
#        for row in rows:
#            for magnet in mag_ID:
        #for row
            #for magnet 
    for g in range(len(gaps)):
        for q in range(len(quadrants)):
            for mp in range(2):
    
                fig, ax = plt.subplots(3,1)
                
                fig.subplots_adjust(hspace=0.8)
                
                fig.set_figheight(9)
                fig.set_figwidth(4.5)
                
                fig.suptitle('Forces on Quadrant {} Keeper {}{}{}\n Gap {}mm'.format(q+1,mag_ID[3*mp-1],mag_ID[3*mp],mag_ID[3*mp+1], gaps[g]), fontsize = 'medium')
                
                for i in range(3):
                    #plot formatting
                                           
                    #axes plots
                    fpkc = (fpmc[0,g,:,q,3*mp-1,i]+fpmc[0,g,:,q,3*mp,i]+fpmc[0,g,:,q,3*mp+1,i] +
                            fpmc[0,g,:,2*q+4,3*mp-1,i]+fpmc[0,g,:,2*q+4,3*mp,i]+fpmc[0,g,:,2*q+4,3*mp+1,i] +
                            fpmc[0,g,:,2*q+5,3*mp-1,i]+fpmc[0,g,:,2*q+5,3*mp,i]+fpmc[0,g,:,2*q+5,3*mp+1,i])
                    
                    fpkl = (fpml[0,g,:,q,3*mp-1,i]+fpml[0,g,:,q,3*mp,i]+fpml[0,g,:,q,3*mp+1,i] +
                            fpml[0,g,:,2*q+4,3*mp-1,i]+fpml[0,g,:,2*q+4,3*mp,i]+fpml[0,g,:,2*q+4,3*mp+1,i] +
                            fpml[0,g,:,2*q+5,3*mp-1,i]+fpml[0,g,:,2*q+5,3*mp,i]+fpml[0,g,:,2*q+5,3*mp+1,i])
                            
                    
                    ax[i].plot(shift,fpkc, label = 'parallel/circular')
                    ax[i].plot(shift,fpkl, label = 'antiparallel/linear')
                    
                    #axis scale
                    ax[i].set_ylim(-force_scale[i],force_scale[i])
                    #Axes title & Text etc
                    ax[i].set_title('{} Axis Force (N)'.format(component[i]),
                                    fontsize = 'small')
                    ax[i].set_xticks(np.arange(-7.5,7.6,1.875))
                    ax[i].tick_params(
                        axis='x',          # changes apply to the x-axis
                        which='both',      # both major and minor ticks are affected
                        bottom=True,      # ticks along the bottom edge are on
                        top=True,         # ticks along the top edge are on
                        labelbottom=False, # labels along the bottom edge are off
                        direction = 'in') # ticks are directed in ) 
                    ax[i].tick_params(
                        axis  = 'y',
                        labelsize = 'x-small'
                        )
                    ax[i].legend(fontsize = 'xx-small')
                    
                    #table Data
                    forcetext = []
                    forcetext.append(['{:.3f}'.format(x) for x in shift])
                    forcetext.append(['{:.2f}'.format(x) for x in fpkc])
                    forcetext.append(['{:.2f}'.format(x) for x in fpkl])
                        
                    tab = ax[i].table(cellText = forcetext,
                                rowLabels = rowtext,
                                rowLoc = 'right',
                                colLabels = columntext,
                                colLoc = 'right')
                    
                    tab.set_fontsize(5)
                    
                fig.savefig("M:\\Work\\Athena_APPLEIII\\Python\\Results\\Force_Plots\\force_gap_{}_quadrant_{}_keeper_{}{}{}.png".format(gaps[g],q+1,mag_ID[3*mp-1],mag_ID[3*mp],mag_ID[3*mp+1]))
                        
    #show geometries
def plot_80_periods_quadrant():
    #read in hdf5 data
    thedatacirc = h5.File("M:\Work\Athena_APPLEIII\Python\Results\circ_mag_forces_6per210426.h5",'r')
    thedatalin = h5.File("M:\Work\Athena_APPLEIII\Python\Results\lin_mag_forces_6per210426.h5",'r')
    
    #force_per_magnet_circ [mode,gap,shift,row,position,Bcomponent]
    fpmc = np.array(thedatacirc['Solution_0']['Force_Per_Magnet_Type'])
    fpml = np.array(thedatalin['Solution_0']['Force_Per_Magnet_Type'])
    shift = np.array(thedatacirc['Solution_0']['shiftrange'])
    gaps = np.array(thedatacirc['Solution_0']['gaprange'])
    rows = np.arange(12)
    quadrants = np.arange(4)
    mag_ID = np.arange(6)
    rowinq = [[0,4,5],[1,6,7],[2,8,9],[3,10,11]]
    mag_packs = ['501','234']
    rowtypes = ['Functional','Functional','Functional','Functional',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation']
    component = ['Transverse','Longitudinal','Vertical']
    #columntext = ['{:.3f}'.format(x) for x in shift]
    columntext = ['' for x in shift]
    rowtext = ('shift','parallel','antiparallel') 
    force_scale = [5000,5000,1500] #max value in newtons of force in each direction
    
    #plotting for each type of magnet
    #for gap
#    for gap in gaps:
#        for row in rows:
#            for magnet in mag_ID:
        #for row
            #for magnet 
    for g in range(len(gaps)):
        for q in range(len(quadrants)):
    
            fig, ax = plt.subplots(3,1)
            
            fig.subplots_adjust(hspace=0.8)
            
            fig.set_figheight(9)
            fig.set_figwidth(4.5)
            
            fig.suptitle('Forces on 80 Period Quadrant {}\n Gap {}mm'.format(q+1, gaps[g]), fontsize = 'medium')
            
            for i in range(3):
                #plot formatting
                                       
                #axes plots
                fpqc = (np.sum(fpmc[0,g,:,q,:,i],1) + np.sum(fpmc[0,g,:,2*q+4,:,i],1) + np.sum(fpmc[0,g,:,2*q + 5,:,i],1))*80
                
                fpql = (np.sum(fpml[0,g,:,q,:,i],1) + np.sum(fpml[0,g,:,2*q+4,:,i],1) + np.sum(fpml[0,g,:,2*q + 5,:,i],1))*80
                        
                
                ax[i].plot(shift,fpqc, label = 'parallel/circular')
                ax[i].plot(shift,fpql, label = 'antiparallel/linear')
                
                #axis scale
                ax[i].set_ylim(-force_scale[i],force_scale[i])
                #Axes title & Text etc
                ax[i].set_title('{} Axis Force (N)'.format(component[i]),
                                fontsize = 'small')
                ax[i].set_xticks(np.arange(-7.5,7.6,1.875))
                ax[i].tick_params(
                    axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=True,      # ticks along the bottom edge are on
                    top=True,         # ticks along the top edge are on
                    labelbottom=False, # labels along the bottom edge are off
                    direction = 'in') # ticks are directed in ) 
                ax[i].tick_params(
                    axis  = 'y',
                    labelsize = 'x-small'
                    )
                ax[i].legend(fontsize = 'xx-small')
                
                #table Data
                forcetext = []
                forcetext.append(['{:.3f}'.format(x) for x in shift])
                forcetext.append(['{:.2f}'.format(x) for x in fpqc])
                forcetext.append(['{:.2f}'.format(x) for x in fpql])
                    
                tab = ax[i].table(cellText = forcetext,
                            rowLabels = rowtext,
                            rowLoc = 'right',
                            colLabels = columntext,
                            colLoc = 'right')
                
                tab.set_fontsize(5)
                
            fig.savefig("M:\\Work\\Athena_APPLEIII\\Python\\Results\\Force_Plots\\force_gap_{}_quadrant_{}.png".format(gaps[g],q+1))
                        
def plot_80_periods_girder():
    #read in hdf5 data
    thedatacirc = h5.File("M:\Work\Athena_APPLEIII\Python\Results\circ_mag_forces_6per210426.h5",'r')
    thedatalin = h5.File("M:\Work\Athena_APPLEIII\Python\Results\lin_mag_forces_6per210426.h5",'r')
    
    #force_per_magnet_circ [mode,gap,shift,row,position,Bcomponent]
    fpmc = np.array(thedatacirc['Solution_0']['Force_Per_Magnet_Type'])
    fpml = np.array(thedatalin['Solution_0']['Force_Per_Magnet_Type'])
    shift = np.array(thedatacirc['Solution_0']['shiftrange'])
    gaps = np.array(thedatacirc['Solution_0']['gaprange'])
    rows = np.arange(12)
    quadrants = np.arange(4)
    girders = np.arange(2)
    mag_ID = np.arange(6)
    rowinq = [[0,4,5],[1,6,7],[2,8,9],[3,10,11]]
    mag_packs = ['501','234']
    rowtypes = ['Functional','Functional','Functional','Functional',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation',
                'Horizontal Force Compensation', 'Vertical Force Compensation']
    component = ['Transverse','Longitudinal','Vertical']
    #columntext = ['{:.3f}'.format(x) for x in shift]
    columntext = ['' for x in shift]
    rowtext = ('shift','parallel','antiparallel') 
    force_scale = [5000,5000,1500] #max value in newtons of force in each direction
    
    #plotting for each type of magnet
    #for gap
#    for gap in gaps:
#        for row in rows:
#            for magnet in mag_ID:
        #for row
            #for magnet 
    for g in range(len(gaps)):
        for gd in range(len(girders)):
    
            fig, ax = plt.subplots(3,1)
            
            fig.subplots_adjust(hspace=0.8)
            
            fig.set_figheight(9)
            fig.set_figwidth(4.5)
            
            fig.suptitle('Forces on 80 Period Girder {}\n Gap {}mm'.format(gd+1, gaps[g]), fontsize = 'medium')
            
            for i in range(3):
                #plot formatting
                                       
                #axes plots[0,1,4,5,6,7][2,3,8,9,10,11]
                fpbc = (np.sum(fpmc[0,g,:,q,:,i],1) + np.sum(fpmc[0,g,:,2*q+4,:,i],1) + np.sum(fpmc[0,g,:,2*q + 5,:,i],1))*80
                
                fpbl = (np.sum(fpml[0,g,:,q,:,i],1) + np.sum(fpml[0,g,:,2*q+4,:,i],1) + np.sum(fpml[0,g,:,2*q + 5,:,i],1))*80
                        
                
                ax[i].plot(shift,fpqc, label = 'parallel/circular')
                ax[i].plot(shift,fpql, label = 'antiparallel/linear')
                
                #axis scale
                ax[i].set_ylim(-force_scale[i],force_scale[i])
                #Axes title & Text etc
                ax[i].set_title('{} Axis Force (N)'.format(component[i]),
                                fontsize = 'small')
                ax[i].set_xticks(np.arange(-7.5,7.6,1.875))
                ax[i].tick_params(
                    axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=True,      # ticks along the bottom edge are on
                    top=True,         # ticks along the top edge are on
                    labelbottom=False, # labels along the bottom edge are off
                    direction = 'in') # ticks are directed in ) 
                ax[i].tick_params(
                    axis  = 'y',
                    labelsize = 'x-small'
                    )
                ax[i].legend(fontsize = 'xx-small')
                
                #table Data
                forcetext = []
                forcetext.append(['{:.3f}'.format(x) for x in shift])
                forcetext.append(['{:.2f}'.format(x) for x in fpqc])
                forcetext.append(['{:.2f}'.format(x) for x in fpql])
                    
                tab = ax[i].table(cellText = forcetext,
                            rowLabels = rowtext,
                            rowLoc = 'right',
                            colLabels = columntext,
                            colLoc = 'right')
                
                tab.set_fontsize(5)
                
            fig.savefig("M:\\Work\\Athena_APPLEIII\\Python\\Results\\Force_Plots\\force_gap_{}_quadrant_{}.png".format(gaps[g],q+1))
                        
def ipac2025_Field_v_Phi(rootname, gap_idx, phis = [0,5,10,15,20,25,30,35,40,45]):
    
    
    lams = [15,17]
    polarisation = [0,1,2]
    #phis = [0,5,10,15,20,25,30,35,40,45]
    
    B = np.zeros([lams.__len__(),phis.__len__(), polarisation.__len__(),2])
    
    for lam in range(len(lams)):
        for poln in range(len(polarisation)):
            for phi in range(len(phis)):
                fname = rootname.format(lams[lam],phis[phi])
                thed = h5.File(fname)
                
                B[lam,phi,poln,0] = thed['Solution_0']['Bprofile'][0,gap_idx,0,500,3]
                B[lam,phi,poln,1] = thed['Solution_0']['Bprofile'][0,gap_idx,2,500,1]
                
                
                
                
                
                
    return B
    
if __name__ == '__main__':
    dirname = "D:\\Work - Laptop\\CryoAPPLE\\Results\\"
    rootname = 'cryoAPPLE_M_1.62_cs_15_lam_{}_tilt_{}_20250514.h5'
    rname4 = 'cryoAPPLE_M_1.62_cs_15_lam_{}_tilt_{}_20250516.h5'
    B_3mm = ipac2025_Field_v_Phi(dirname+rootname, 0)
    B_5mm = ipac2025_Field_v_Phi(dirname+rootname, 1)
    B_4mm = ipac2025_Field_v_Phi(dirname+rname4, 0, phis = [20])
    
    plt.plot(np.abs(B_3mm[0,:,0,0]))
    plt.plot(np.abs(B_3mm[0,:,2,1]))
    plt.plot(np.abs(B_5mm[1,:,0,0]))
    plt.plot(np.abs(B_5mm[1,:,2,1]))
    
    ########
    #thedata = h5.File("D:\Work - Laptop\CryoAPPLE\Results\cryoAPPLE_asym_221_20250507.h5",'r')
    
    #plot_individual_magnets()
    
    #plot_triplet_packs()
    
    #plot_keeper()
    
    #plot_80_periods_quadrant()
    plt.show()
    #plot_80_periods_girder()
    
    print(1)
    
    #build up solution/case tree
    
    #Contains Forces? Bfield?