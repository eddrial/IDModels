'''
Created on 22 Aug 2023

@author: oqb

'''
#22.8.23 Looking at IVUE32 - Symmetric or antisymmetric compensation magnets
#creation of indivudual compensated APPLE, quick case solution
#also a hyperparamaterspace search and solution
#parallel axes plotting at the very end, which is broken
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
from idcomponents import magnet_shapes as ms
from idanalysis import analysis_functions as af
from wradia.wrad_obj import wradObjCnt

if __name__ == '__main__':
        ### developing Case Solution ###
    
    block = wrd.wradObjThckPgn(0, 8, [[-20,-3.5],[20,-3.5],[20,-18.5],[-20,-18.5]], extrusion_direction = 'x', magnetisation = [0,0,1.4])
    blocktilt = wrd.wradObjThckPgn(0, 8, [[-20,-3.5],[20,-3.5],[20,-18.5],[-20,-18.5]], extrusion_direction = 'x', magnetisation = [0.122,0,1.395])
    blockweak = wrd.wradObjThckPgn(0, 8, [[-20,-3.5],[20,-3.5],[20,-18.5],[-20,-18.5]], extrusion_direction = 'x', magnetisation = [0,0,1.26])
    blocktilt2 = wrd.wradObjThckPgn(0, 8, [[-20,-3.5],[20,-3.5],[20,-18.5],[-20,-18.5]], extrusion_direction = 'x', magnetisation = [0,0.122,1.395])
    
    dint = np.zeros([3,201])
    dinttilt = np.zeros([3,201])
    dintweak = np.zeros([3,201])
    dinttilt2 = np.zeros([3,201])
    
    i = 0
    for x in range(-100,101):
        dint[:,i] = rd.FldInt(block.radobj, 'inf','ibxibyibz',[-100,x,0], [100,x,0])
        dinttilt[:,i] = rd.FldInt(blocktilt.radobj, 'inf','ibxibyibz',[-100,x,0], [100,x,0])
        dintweak[:,i] = rd.FldInt(blockweak.radobj, 'inf','ibxibyibz',[-100,x,0], [100,x,0])
        dinttilt2[:,i] = rd.FldInt(blocktilt2.radobj, 'inf','ibxibyibz',[-100,x,0], [100,x,0])
        i+=1
        
    rd.FldInt(block.radobj, 'inf','ibxibyibz',[-80,-100,0], [-80,100,0])
    
    
    print('end')