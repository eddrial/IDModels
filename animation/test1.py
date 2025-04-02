'''
Created on Apr 2, 2025

@author: oqb
'''
import time
import random

import pygame as pyg
import pygame.locals as pygl
import OpenGL.GL as ogl
import OpenGL.GLU as oglu

import numpy as np

import apple2p5.model2 as id1

import radia as rd
from idcomponents import parameters

def Cube(vertices, edges):
    ogl.glBegin(ogl.GL_LINES)
    for edge in edges:
        for vertex in edge:
            ogl.glVertex3fv(vertices[vertex])
    
    ogl.glEnd

if __name__ == '__main__':
    rd.UtiDelAll()
    a_param = parameters.model_parameters(
        periods = 10,
        periodlength = 40,
        minimumgap = 15,
        M = 1.32,
        block_subdivision = [1,1,1])
    #a_param.block_subdivision = [1,1,1]
    #a_param.periods = 20
    #a_param.periodlength = 40
    #a_param.minimumgap = 15
    
    #a_param.M = 1.32
    
    t0 = time.time()
    
    for i in range(len(a_param.M_list[:])):
        ang = random.random()*2*np.pi
        
        
        a_param.M_list[i,0:3:2] = np.array([a_param.M*np.sin(ang), a_param.M*np.cos(ang)])
    
    
    #a = ArbAPPLE(model_parameters = a_param)
    
    a = id1.plainAPPLE(model_parameters = a_param)
    
    rd.ObjDrwOpenGL(a.cont.radobj)
    
    edges = np.array([[0,1],[0,3],[0,4],[1,5],[1,2],[2,6],[2,3],[3,7],[4,5],[4,7],[5,6],[6,7]])
    
    cube = Cube(a.cont.objectlist[0].objectlist[0].objectlist[0].objectlist[0].vertices,edges)
    
    pyg.init()
    display = (800,600)
    pyg.display.set_mode(display, pygl.DOUBLEBUF|pygl.OPENGL)
    pass