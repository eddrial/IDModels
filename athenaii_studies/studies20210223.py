'''
Created on 23 Feb 2021

@author: oqb
'''

#Here is a final parameter set (20 degrees Mova, 6 mag per period
#include plotting of XZ at each place for each magnet
#plotting of field along axis
#plotting of field across axis at peaks#

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
from idanalysis import analysis_functions as af
from ipywidgets.widgets.interaction import fixed
from wradia.wrad_obj import wradObjCnt

import matplotlib.gridspec as gridspec

def XY_field_sheet(model, linewidth = 1):
    
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
    axsQ1Q2 = model.BfieldStreamPlot(fields,plotdims)
    
    
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
            ax0.plot(model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
    ax0.set_title('Vertical Comp Magnets')
    
    ax0.set_aspect('equal')
    
    # Varying color along a streamline
    ax1 = fig.add_subplot(gs[0, 1])
    strm = ax1.streamplot(Xv, Zv, Bxv, Bzv, color=Bzv, linewidth=2, cmap='autumn')
    fig.colorbar(strm.lines)
    for i in range(2):
        for j in range(4,7,2):
            ax1.plot(model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
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
            ax2.plot(model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
    ax2.set_aspect('equal')
    
    # Varying color along a streamline
    ax3 = fig.add_subplot(gs[1, 1])
    strm = ax3.streamplot(Xh, Zh, BXh, BZh, color=BZh, linewidth=2, cmap='autumn')
    fig.colorbar(strm.lines)
    for i in range(2):
        for j in range(7,12,4):
            ax3.plot(model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
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
            ax4.plot(model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
            
    for i in range(2):
        for j in range(4,12):
            ax4.plot(model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
    ax4.set_aspect('equal')
    
    # Varying color along a streamline
    ax5 = fig.add_subplot(gs[2, 1])
    strm = ax5.streamplot(Xf, Zf, BXf, BZf, color=BZf, linewidth=1, cmap='autumn')
    fig.colorbar(strm.lines)
    ax5.set_title('Functional Magnets')
    for i in range(3):
        for j in range(4):
            ax5.plot(model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
    for i in range(2):
        for j in range(4,12):
            ax5.plot(model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                     model.cont.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
    
    ax5.set_aspect('equal')
    
    plt.show()

if __name__ == '__main__':
    #parameter_Set Horizontal_polarisation
    ATH_II_hp_horz= parameters.model_parameters(Mova = 20,
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
                                        gap = 2.2, 
                                        rowshift = 0,
                                        shiftmode = 'circular',
                                        block_subdivision = [1,1,1]
                                        )
    
    ATH_II_hp_vert= parameters.model_parameters(Mova = 20,
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
                                        gap = 2.2, 
                                        rowshift = 7.5,
                                        shiftmode = 'circular',
                                        block_subdivision = [1,1,1]
                                        )
    
    #make list of parameter sets to cycle through. In this case H and then V
    param_sets = [ATH_II_hp_horz,ATH_II_hp_vert]
    
    #cycle through sets
    for model in param_sets:
        #create model
        this_id = id.compensatedAPPLEv2(model)
        #solve model
        this_id.cont.wradSolve()
        
        #plot XZ streams
        XY_field_sheet(this_id, linewidth = 1)
        
        
    
    input("Press Enter to continue...")
    