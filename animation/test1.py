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
import OpenGL.GLUT as oglut

import numpy as np

import apple2p5.model2 as id1

import radia as rd
from idcomponents import parameters

width = 500
height = 500

vertices = [(-1,-1,-1), ( 1,-1,-1), ( 1, 1,-1), (-1, 1,-1), (-1,-1, 1), ( 1,-1, 1), ( 1, 1, 1), (-1, 1, 1)]
faces = [(4,0,3,7), (1,0,4,5), (0,1,2,3), (1,5,6,2), (3,2,6,7), (5,4,7,6)]
colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]

def cube():
    ogl.glRotatef(1, 3, 1, 1)
    ogl.glBegin(ogl.GL_QUADS)
    for i, face in enumerate(faces):
        ogl.glColor3fv(colors[i])
        for vertex in face:
            ogl.glVertex3fv(vertices[vertex])
    ogl.glEnd()

def showScreen():
    ogl.glClearColor(0, 0, 0, 1)
    ogl.glClear(ogl.GL_COLOR_BUFFER_BIT | ogl.GL_DEPTH_BUFFER_BIT)
    cube()
    oglut.glutSwapBuffers()

def mouseTracker(mousex, mousey):
    print(f"Mouse pos: {mousex}, {mousey}")

def reshapeWindow(x, y):
    global width, height
    width = x
    height = y
    print(x, y)
    ogl.glMatrixMode(ogl.GL_PROJECTION)
    ogl.glLoadIdentity()
    oglu.gluPerspective(45, (width / height), 0.0001, 1000)
    ogl.glMatrixMode(ogl.GL_MODELVIEW)



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
    
    #rd.ObjDrwOpenGL(a.cont.radobj)
    
    oglut.glutInit()
    oglut.glutInitDisplayMode(oglut.GLUT_RGBA)
    oglut.glutInitWindowSize(500, 500)
    wind = oglut.glutCreateWindow(b'OpenGL')
    oglut.glutDisplayFunc(showScreen)
    oglut.glutIdleFunc(showScreen)
    oglut.glutMotionFunc(mouseTracker)
    oglut.glutPassiveMotionFunc(mouseTracker)
    oglut.glutReshapeFunc(reshapeWindow)
    
    ogl.glMatrixMode(ogl.GL_MODELVIEW)
    ogl.glLoadIdentity()
    ogl.glTranslatef(0, 0, -5)
    
    ogl.glEnable(ogl.GL_DEPTH_TEST)
    
    while True:
        oglut.glutMainLoopEvent()
        oglut.glutPostRedisplay()
        time.sleep(0.01)
    pass