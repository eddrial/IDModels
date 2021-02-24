'''
Created on 19 Feb 2021

@author: oqb
'''
import pyvista as pv
from pyvista import examples
import tetgen

import numpy as np
import radia as rad

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from tqdm import tqdm
import pickle

if __name__ == '__main__':


    def setup_axes(fig, rows, cols, subplot, title='', proj='persp', elev=20, azim=-80, x=(-1, 1, 5), z=(-1, 1, 5), s=(-1, 1, 5)):
        ax = fig.add_subplot(rows, cols, subplot, projection='3d')
        ax.set_proj_type(proj)
        ax.view_init(elev=elev, azim=azim)
        ax.set_box_aspect([1,1,1])
        ax.xaxis.pane.fill, ax.yaxis.pane.fill, ax.zaxis.pane.fill = False, False, False
        ax.set_xlabel('X Axis')
        ax.set_zlabel('Z Axis (Transverse)')
        ax.set_ylabel('S Axis')
        ax.set_xlim3d(*x[:2])
        ax.set_zlim3d(*z[:2])
        ax.set_ylim3d(*s[:2])
        ax.set_xticks(np.linspace(*x))
        ax.set_zticks(np.linspace(*z))
        ax.set_yticks(np.linspace(*s))
        ax.set_title(title, fontdict={'size': 22})
        return ax
    
    def plot_radia_object(ax, obj, color, matrix):
        polygons = rad.ObjDrwVTK(obj, 'Axes->False')['polygons']
        lengths  = polygons['lengths']
        vertices = np.reshape(polygons['vertices'], (-1, 3))
        vertices = np.array(transform_points(vertices, matrix))
        
        idx = 0
        faces = []
        for length in lengths:
            faces += [vertices[idx:(idx+length), [0, 2, 1]]]
            idx += length
            
        ax.add_collection3d(Poly3DCollection(faces, facecolors=[color], edgecolors=['k'], 
                                             linewidth=0.02, alpha=0.04))
        
    def transform_points(lattice, matrix):
        lattice = np.concatenate([lattice, np.ones(lattice.shape[:-1] + (1,))], axis=-1)
        return (lattice @ matrix)[..., :-1]
    
    def radians(degrees):
        return degrees * (np.pi / 180.0)
    
    def rotate_x(theta):
        c, s = np.cos(theta), np.sin(theta)
        return np.array([[ 1,  0,  0,  0],
                         [ 0,  c, -s,  0],
                         [ 0,  s,  c,  0],
                         [ 0,  0,  0,  1]],
                        dtype=np.float32).T
    
    def scale(x, z, s):
        return np.array([[x, 0, 0, 0],
                         [0, z, 0, 0],
                         [0, 0, s, 0],
                         [0, 0, 0, 1]],
                        dtype=np.float32).T