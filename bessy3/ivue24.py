'''
Created on Nov 5, 2024

@author: oqb
'''

#5.11.24 - building a cryo_ap_biii - initially for CryoAPPLE comparison

import numpy as np
import radia as rd
import matplotlib.pyplot as plt
from wradia import wrad_obj as wrd
from apple2p5 import model2 as id
from idcomponents import parameters
from idanalysis import analysis_functions as af
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from matplotlib._constrained_layout import do_constrained_layout


def XY_field_sheet(model, mag_index = 0, linewidth = 1):
    
    #5 plots on A4
    #vertical upper compensation magnets (Q1, Q2)
    #vertical lower compensation magnet (Q3, Q4)
    #horizontal bank side (-X) (Q1, Q3)
    #horizontal structure side (+X) (Q2, Q4)
    
    #define important values for plot scales
    extreme_X = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.nominal_hcmagnet_dimensions[2] + 3*model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    mid_X = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    short_X = model.model_parameters.nominal_vcmagnet_dimensions[0] + model.model_parameters.rowtorowgap/2.0 + model.model_parameters.compappleseparation/2.0
    extreme_Z = model.model_parameters.nominal_fmagnet_dimensions[0]+ model.model_parameters.nominal_vcmagnet_dimensions[2] + 3*model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    mid_Z = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap 
    short_Z = model.model_parameters.nominal_vcmagnet_dimensions[0] + model.model_parameters.gap/2.0 + model.model_parameters.compappleseparation/2.0
    
    #plot for V compensation Magnets Q1, Q2
    plotdims = np.array([-short_X,short_X,mid_Z,extreme_Z])
    fields = 'bxbz'
    #axsQ1Q2 = model.BfieldStreamPlot(fields,plotdims)
    
    
    Zv, Xv = np.mgrid[20:40:41j, -10:10:41j]
    Bxv = Xv.copy()
    Bzv = Zv.copy()
    
    for i in range(len(Xv)):
        for j in range(len(Zv)):
            #print ('coords are {}'.format([Xv[i,j],Zv[i,j]]))
            Bxv[i,j],Bzv[i,j] = rd.Fld(model.cont.radobj,'bxbz',[Xv[i,j],0,Zv[i,j]]) 
            #print ('the field at those coords are Bx: {} Bz: {}'.format(Bxv[i,j],Bzv[i,j]))
    
    fig = plt.figure(figsize=(7, 9))
    gs = gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[1, 1, 2])
    
    #  Varying density along a streamline
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.streamplot(Xv, Zv, Bxv, Bzv, density=[0.5, 1])
    for i in range(2):
        for j in range(4,7,2):
            ax0.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
    ax0.set_title('Vertical Comp Magnets')
    
    ax0.set_aspect('equal')
    
    # Varying color along a streamline
    ax1 = fig.add_subplot(gs[0, 1])
    strm = ax1.streamplot(Xv, Zv, Bxv, Bzv, color=Bzv, linewidth=2, cmap='autumn')
    fig.colorbar(strm.lines)
    for i in range(2):
        for j in range(4,7,2):
            ax1.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
    ax1.set_title('Vertical Comp Magnets')
    
    #region of H magnets
    Zh, Xh = np.mgrid[-10:10:41j, 20:40:41j]
    BXh = Xh.copy()
    BZh = Zh.copy()
    
    for i in range(len(Xh)):
        for j in range(len(Zh)):
            #print ('coords are {}'.format([X[i,j],Y[i,j]]))
            BXh[i,j],BZh[i,j] = rd.Fld(model.cont.radobj,'bxbz',[Xh[i,j],0,Zh[i,j]]) 
            #print ('the field at those coords are Bx: {} Bz: {}'.format(a,b))
    ax1.set_aspect('equal')
    
    #  Varying density along a streamline
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.streamplot(Xh, Zh, BXh, BZh, density=[0.5, 1])
    ax2.set_title('Horizontal Comp Magnets')
    
    for i in range(2):
        for j in range(7,12,4):
            ax2.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
    ax2.set_aspect('equal')
    
    # Varying color along a streamline
    ax3 = fig.add_subplot(gs[1, 1])
    strm = ax3.streamplot(Xh, Zh, BXh, BZh, color=BZh, linewidth=2, cmap='autumn')
    fig.colorbar(strm.lines)
    for i in range(2):
        for j in range(7,12,4):
            ax3.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
    ax3.set_title('Horizontal Comp Magnets')
    ax3.set_aspect('equal')
    
    #region of Functional magnets
    Zf, Xf = np.mgrid[-40:40:81j, -40:40:81j]
    BXf = Xf.copy()
    BZf = Zf.copy()
    
    for i in range(len(Xf)):
        for j in range(len(Zf)):
            #print ('coords are {}'.format([X[i,j],Y[i,j]]))
            BXf[i,j],BZf[i,j] = rd.Fld(model.cont.radobj,'bxbz',[Xf[i,j],0,Zf[i,j]]) 
            #print ('the field at those coords are Bx: {} Bz: {}'.format(a,b))
    
    
    #  Varying density along a streamline
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.streamplot(Xf, Zf, BXf, BZf, density=[0.5, 1])
    ax4.set_title('Functional Magnets')
    for i in range(3):
        for j in range(4):
            ax4.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
            
    for i in range(2):
        for j in range(4,12):
            ax4.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
    ax4.set_aspect('equal')
    
    # Varying color along a streamline
    ax5 = fig.add_subplot(gs[2, 1])
    #strm = ax5.streamplot(Xf, Zf, BXf, BZf, color=BZf, linewidth=1, cmap='autumn')
    #fig.colorbar(strm.lines)
    ax5.set_title('Functional Magnets')
    for i in range(3):
        for j in range(4):
            ax5.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
    for i in range(2):
        for j in range(4,12):
            ax5.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
    
    ax5.set_aspect('equal')
    
    gs.tight_layout(fig, pad = 2)
    plt.show()
    
def XY_quiver(model, mag_index = 0, linewidth = 1):
    
    #5 plots on A4
    #vertical upper compensation magnets (Q1, Q2)
    #vertical lower compensation magnet (Q3, Q4)
    #horizontal bank side (-X) (Q1, Q3)
    #horizontal structure side (+X) (Q2, Q4)
    
    #define important values for plot scales
    extreme_X = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.nominal_hcmagnet_dimensions[2] + 3*model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    mid_X = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    short_X = model.model_parameters.nominal_vcmagnet_dimensions[0] + model.model_parameters.rowtorowgap/2.0 + model.model_parameters.compappleseparation/2.0
    extreme_Z = model.model_parameters.nominal_fmagnet_dimensions[0]+ model.model_parameters.nominal_vcmagnet_dimensions[2] + 3*model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    mid_Z = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap 
    short_Z = model.model_parameters.nominal_vcmagnet_dimensions[0] + model.model_parameters.gap/2.0 + model.model_parameters.compappleseparation/2.0
    
    #plot for V compensation Magnets Q1, Q2
    plotdims = np.array([-short_X,short_X,mid_Z,extreme_Z])
    fields = 'bxbz'
    #axsQ1Q2 = model.BfieldStreamPlot(fields,plotdims)
    
    
    Zv, Xv = np.mgrid[20:40:41j, -10:10:41j]
    Bxv = Xv.copy()
    Bzv = Zv.copy()
    
    for i in range(len(Xv)):
        for j in range(len(Zv)):
            #print ('coords are {}'.format([Xv[i,j],Zv[i,j]]))
            Bxv[i,j],Bzv[i,j] = rd.Fld(model.cont.radobj,'bxbz',[Xv[i,j],0,Zv[i,j]]) 
            #print ('the field at those coords are Bx: {} Bz: {}'.format(Bxv[i,j],Bzv[i,j]))
    
    #fig = plt.figure(figsize=(7, 9))
    fig = plt.figure(constrained_layout=True)
    gs = gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[1, 1, 2])

    
    
    #  Varying density along a streamline
    ax0 = fig.add_subplot(gs[0, 0])
    #ax0.streamplot(Xv, Zv, Bxv, Bzv, density=[0.5, 1])
    
    for i in range(2):
        for j in range(4,7,2):
            ax0.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
            ax0.quiver(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,0].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,2].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[0],
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[2], 
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].colour,
                       width = 0.04,
                       scale = 5,
                       pivot = 'middle')
    ax0.set_title('Vertical Comp Magnets')
    
    ax0.set_aspect('equal')
    
    # Varying color along a streamline
    ax1 = fig.add_subplot(gs[0, 1])
    for i in range(2):
        for j in range(8,11,2):
            ax1.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
            ax1.quiver(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,0].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,2].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[0],
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[2], 
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].colour,
                       width = 0.04,
                       scale = 5,
                       pivot = 'middle')
    ax1.set_title('Vertical Comp Magnets')
    
    ax1.set_aspect('equal')
    
    
    #region of H magnets
    Zh, Xh = np.mgrid[-10:10:41j, 20:40:41j]
    BXh = Xh.copy()
    BZh = Zh.copy()
    
    for i in range(len(Xh)):
        for j in range(len(Zh)):
            #print ('coords are {}'.format([X[i,j],Y[i,j]]))
            BXh[i,j],BZh[i,j] = rd.Fld(model.cont.radobj,'bxbz',[Xh[i,j],0,Zh[i,j]]) 
            #print ('the field at those coords are Bx: {} Bz: {}'.format(a,b))
    ax1.set_aspect('equal')
    
    #  Magnetisation Vectors
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_title('Horizontal Comp Magnets')
    
    for i in range(2):
        for j in range(7,12,4):
            ax2.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
            ax2.quiver(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,0].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,2].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[0],
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[2], 
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].colour,
                       width = 0.03,
                       scale = 7,
                       pivot = 'middle')
            
    ax2.set_aspect('equal')
    
    # Varying color along a streamline
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_title('Horizontal Comp Magnets')

    for i in range(2):
        for j in range(5,12,4):
            ax3.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
            ax3.quiver(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,0].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,2].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[0],
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[2], 
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].colour,
                       width = 0.03,
                       scale = 7,
                       pivot = 'middle')
            
    ax3.set_aspect('equal')
    
    #region of Functional magnets
    Zf, Xf = np.mgrid[-40:40:81j, -40:40:81j]
    BXf = Xf.copy()
    BZf = Zf.copy()
    
    for i in range(len(Xf)):
        for j in range(len(Zf)):
            #print ('coords are {}'.format([X[i,j],Y[i,j]]))
            BXf[i,j],BZf[i,j] = rd.Fld(model.cont.radobj,'bxbz',[Xf[i,j],0,Zf[i,j]]) 
            #print ('the field at those coords are Bx: {} Bz: {}'.format(a,b))
    
    
    #  Magnetisation Vectors
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.set_title('Functional Magnets')
    for i in range(3):
        for j in range(4):
            ax4.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
            
            ax4.quiver(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,0].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,2].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[0],
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[2], 
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].colour,
                       width = 0.04,
                       scale = 5,
                       pivot = 'middle')
            
    ax4.set_aspect('equal')
    
    # Varying color along a streamline
    ax5 = fig.add_subplot(gs[2, 1])
    #strm = ax5.streamplot(Xf, Zf, BXf, BZf, color=BZf, linewidth=1, cmap='autumn')
    #fig.colorbar(strm.lines)
    ax5.set_title('Functional Magnets')
        #  Magnetisation Vectors
    for i in range(3):
        for j in range(4):
            ax5.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
            
            ax5.quiver(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,0].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,2].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[0],
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[2], 
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].colour,
                       width = 0.01,
                       scale = 25,
                       pivot = 'middle')
            
    for i in range(2):
        for j in range(4,12):
            ax5.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
            
            ax5.quiver(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,0].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,2].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[0],
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[2], 
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].colour,
                       width = 0.01,
                       scale = 25,
                       pivot = 'middle')
            
    ax5.set_aspect('equal')
    
    #gs.tight_layout(fig, pad = 2)
    plt.show()

def plot_geometry(model, linewidth = 1, mag_index = 0, highlightrows = 0, highlightmagnets = 0):
    
    #5 plots on A4
    #vertical upper compensation magnets (Q1, Q2)
    #vertical lower compensation magnet (Q3, Q4)
    #horizontal bank side (-X) (Q1, Q3)
    #horizontal structure side (+X) (Q2, Q4)
    
    #define important values for plot scales
    extreme_X = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.nominal_hcmagnet_dimensions[2] + 3*model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    mid_X = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    short_X = model.model_parameters.nominal_vcmagnet_dimensions[0] + model.model_parameters.rowtorowgap/2.0 + model.model_parameters.compappleseparation/2.0
    extreme_Z = model.model_parameters.nominal_fmagnet_dimensions[0]+ model.model_parameters.nominal_vcmagnet_dimensions[2] + 3*model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    mid_Z = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap 
    short_Z = model.model_parameters.nominal_vcmagnet_dimensions[0] + model.model_parameters.gap/2.0 + model.model_parameters.compappleseparation/2.0
    

    
    
    #fig = plt.figure(figsize=(7, 9))
    fig, ax = plt.subplots(1,1)

    
    
    
    for j in range(12):
        for i in range(len(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist)):
            ax.plot(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], color = 'k')
            if j in highlightrows:
                ax.fill(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,0],
                         model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[i].vertices[:,2], 
                         color = 'r', alpha = 0.3)
                ax.quiver(model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,0].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].vertices[:,2].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[0],
                       model.cont.objectlist[j].objectlist[0].objectlist[mag_index].objectlist[0].magnetisation[2],
                       width = 0.04,
                       scale = 25,
                       pivot = 'middle')
            
    ax.set_title('Transverse Cross Section\n Row {} Magnet {}'.format(highlightrows[0]+1,mag_index-15))
    
    ax.set_xlabel('Transverse (mm)')
    ax.set_ylabel('Vertical (mm)')
    ax.set_aspect('equal')
    
    
    #plt.show()
    
    return fig

def plot_long_geometry(model, linewidth = 1, mag_index = 0, highlightrows = 0, highlightmagnets = 0):
    
    #5 plots on A4
    #vertical upper compensation magnets (Q1, Q2)
    #vertical lower compensation magnet (Q3, Q4)
    #horizontal bank side (-X) (Q1, Q3)
    #horizontal structure side (+X) (Q2, Q4)
    
    #define important values for plot scales
    extreme_X = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.nominal_hcmagnet_dimensions[2] + 3*model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    mid_X = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    short_X = model.model_parameters.nominal_vcmagnet_dimensions[0] + model.model_parameters.rowtorowgap/2.0 + model.model_parameters.compappleseparation/2.0
    extreme_Z = model.model_parameters.nominal_fmagnet_dimensions[0]+ model.model_parameters.nominal_vcmagnet_dimensions[2] + 3*model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap
    mid_Z = model.model_parameters.nominal_fmagnet_dimensions[2]+ model.model_parameters.compappleseparation/2.0 + model.model_parameters.rowtorowgap 
    short_Z = model.model_parameters.nominal_vcmagnet_dimensions[0] + model.model_parameters.gap/2.0 + model.model_parameters.compappleseparation/2.0
    
    #plot for V compensation Magnets Q1, Q2
    plotdims = np.array([-short_X,short_X,mid_Z,extreme_Z])

    #fig = plt.figure(figsize=(7, 9))
    fig, ax = plt.subplots(1,1)

    
    
    a = [0,2,4,6,0]
    b = [0,2,6,4,0]
    for k in range(10,21):#len(model.cont.objectlist[j].objectlist[0].objectlist[k]
        for j in range(12):
            for i in range(len(model.cont.objectlist[j].objectlist[0].objectlist[k].objectlist)):
                ax.plot(model.cont.objectlist[j].objectlist[0].objectlist[k].objectlist[i].vertices[a,1],
                         model.cont.objectlist[j].objectlist[0].objectlist[k].objectlist[i].vertices[b,2], color = 'k')
                if j in highlightrows and k in highlightmagnets:
                    ax.fill(model.cont.objectlist[j].objectlist[0].objectlist[k].objectlist[i].vertices[a,1],
                             model.cont.objectlist[j].objectlist[0].objectlist[k].objectlist[i].vertices[b,2], 
                             color = 'r', alpha = 0.3)
                    ax.quiver(model.cont.objectlist[j].objectlist[0].objectlist[k].objectlist[0].vertices[:,1].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[k].objectlist[0].vertices[:,2].mean(),
                       model.cont.objectlist[j].objectlist[0].objectlist[k].objectlist[0].magnetisation[1],
                       model.cont.objectlist[j].objectlist[0].objectlist[k].objectlist[0].magnetisation[2],
                       width = 0.04,
                       scale = 25,
                       pivot = 'middle')
                    

    ax.set_xlabel('Longitudinal (mm)')
    ax.set_ylabel('Vertical (mm)')        
    ax.set_title('Longitudinal Cross Section\n Row {} Magnet {}'.format(highlightrows[0]+1,highlightmagnets[0]-15))
    
    #ax.set_aspect('equal')
    
    
    #plt.show()
    
    return fig

def axial_field_plot(model):
    #plot for V compensation Magnets Q1, Q2
    plotdims = np.array([-100,100,-2,2])
    fields = 'bxbz'
    x = 30
    
    a = rd.FldLst(model.cont.radobj,fields,[0,-x,0],[0,x,0],1001,'arg',-x)
    a = np.array(a)
    
    b = rd.FldLst(model.cont.radobj,fields,[-x,0,0],[x,0,0],1001,'arg',-x)
    b = np.array(b)
    
    fig = plt.figure()
    gs = gridspec.GridSpec(nrows=1, ncols=3)

    fig.suptitle('Field Profile Row Shift {}mm'.format(model.model_parameters.rowshift))
    
    #  Field Along Axis
    ax0 = fig.add_subplot(gs[0, 0:2])
    
    ax0.plot(a[:,0],a[:,1:])
    
    ax0.set_ylabel('Bx (T)')
    ax0.set_xlabel('s (mm)')
    
    #Field Across Pole
    ax1 = fig.add_subplot(gs[0,2], sharey = ax0)
    plt.setp(ax1.get_yticklabels(), visible=False)
    ax1.plot(b[:,0],b[:,1:])
    ax1.set_xlabel('x (mm)')
    
    
    
    plt.show()
    
    print(1)    

if __name__ == '__main__':
    
    '''fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y, Z = axes3d.get_test_data(0.05)
    ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
    cset = ax.contourf(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm) 
    cset = ax.contourf(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
    cset = ax.contourf(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
    
    ax.set_xlabel('X')
    ax.set_xlim(-40, 40)
    ax.set_ylabel('Y')
    ax.set_ylim(-40, 40)
    ax.set_zlabel('Z')
    ax.set_zlim(-100, 100)
    
    plt.show()'''
    #parameter_Set Horizontal_polarisation
    cryo_ap_biii_horz= parameters.model_parameters(Mova = 0,
                                        periods = 5, 
                                        periodlength = 18,
                                        nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                        #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                        nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                        nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                        compappleseparation = 7.5,
                                        apple_clampcut = 3.0,
                                        comp_magnet_chamfer = [3.0,0.0,3.0],
                                        magnets_per_period = 4,
                                        gap = 5, 
                                        rowshift = 0,
                                        shiftmode = 'circular',
                                        block_subdivision = [3,3,3]
                                        )
    
    cryo_ap_biii_vert= parameters.model_parameters(Mova = 0,
                                        periods = 5, 
                                        periodlength = 18,
                                        nominal_fmagnet_dimensions = [15.0,0.0,15.0], 
                                        #nominal_cmagnet_dimensions = [10.0,0.0,15.0],
                                        nominal_vcmagnet_dimensions = [7.5,0.0,12.5],
                                        nominal_hcmagnet_dimensions = [7.5,0.0,15.0], 
                                        compappleseparation = 7.5,
                                        apple_clampcut = 3.0,
                                        comp_magnet_chamfer = [3.0,0.0,3.0],
                                        magnets_per_period = 4,
                                        gap = 5, 
                                        rowshift = 9,
                                        shiftmode = 'circular',
                                        block_subdivision = [3,3,3]
                                        )
    
    #make list of parameter sets to cycle through. In this case H and then V
    param_sets = [cryo_ap_biii_horz,cryo_ap_biii_vert]
    
    
    this_id = id.compensatedAPPLEv2(cryo_ap_biii_horz)
    
    #this_id.cont.wradSolve()
    
    
#    for i in range(12):
#        figi = plot_geometry(this_id, linewidth = 1, mag_index = 0, highlightrows = [i], highlightmagnets = [0])
#        figi.savefig("M:\\Work\\cryo_ap_biii\\Python\\Results\\Geometry_pics\\row_{}.png".format(i+1))

#Create pics for one period in YZ. this works    5.11.24  
#    for r in range(12):
#        for m in range(cryo_ap_biii_vert.magnets_per_period):
#            figl = plot_long_geometry(this_id, linewidth = 1, mag_index = 5, highlightrows = [r], highlightmagnets = [m+15])
#            figl.savefig("M:\\Work\\cryo_ap_biii\\Python\\Results\\Geometry_pics\\L_row_{}_magnet_{}.png".format(r+1,m))
#            figt = plot_geometry(this_id, linewidth = 1, mag_index = m+15, highlightrows = [r], highlightmagnets = [m+15])
#            figt.savefig("M:\\Work\\cryo_ap_biii\\Python\\Results\\Geometry_pics\\T_row_{}_magnet_{}.png".format(r+1,m))
            
    #cycle through sets
    for model in param_sets:
        #create model
        this_id = id.compensatedAPPLEv2(model)
 #       this_id = id.compensatedAPPLEv2(cryo_ap_biii_horz)
        #solve model
        this_id.cont.wradSolve()
        
        #plot geometry
#        for i in range(12):
#            figi = plot_geometry(this_id, linewidth = 1, mag_index = 0, highlightrows = [i], highlightmagnets = [0])
#            figi.savefig("M:\\Work\\cryo_ap_biii\\Python\\Results\\Geometry_pics\\row_{}.png".format(i+1))
        
        #plot XZ streams
        #XY_field_sheet(this_id, linewidth = 1)
#        for i in range(4):
#            XY_quiver(this_id, mag_index=i)


        axial_field_plot(this_id)
        
    
    input("Press Enter to continue...")
    