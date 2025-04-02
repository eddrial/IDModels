'''
Created on Apr 2, 2025

@author: oqb
'''
import time
import random

import OpenGL.GL as ogl
import OpenGL.GLU as oglu
import OpenGL.GLUT as oglut

import numpy as np

import apple2p5.model2 as id1

import radia as rd
from idcomponents import parameters

class IDDraw():
    def __init__(self, 
                 frame_details,
                 my_object, my_object2):
        self.width = 500
        self.height = 500

        #self.vertices = [(-2,-2,-2), ( 0,-2,-2), ( 0, 0,-2), (-2, 0,-2), (-2,-2, 0), ( 0,-2, 0), ( 0, 0, 0), (-2, 0, 0)]
        self.vertices = my_object.vertices
        self.vertices2 = my_object2.vertices
        #self.faces = [(4,0,3,7), (1,0,4,5), (0,1,2,3), (1,5,6,2), (3,2,6,7), (5,4,7,6)]
        self.faces = my_object.polygons
        self.faces2 = my_object2.polygons
        #self.colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
        self.colours = [my_object.colour]*len(self.faces)

    def cube(self, vertices, faces, colours):
        ogl.glRotatef(1, 3, 1, 1)
        ogl.glBegin(ogl.GL_QUADS)
        for i, face in enumerate(faces):
            ogl.glColor3fv(colours[i])
            for vertex in face:
                ogl.glVertex3fv(vertices[vertex])
        ogl.glEnd()

    def showScreen(self):
        ogl.glClearColor(0, 0, 0, 1)
        ogl.glClear(ogl.GL_COLOR_BUFFER_BIT | ogl.GL_DEPTH_BUFFER_BIT)
        self.cube(self.vertices,self.faces,self.colours)
        self.cube(self.vertices2,self.faces2,self.colours)
        oglut.glutSwapBuffers()

    def mouseTracker(self,mousex, mousey):
        print(f"Mouse pos: {mousex}, {mousey}")

    def reshapeWindow(self, x, y):
        self.width = x
        self.height = y
        print(x, y)
        ogl.glMatrixMode(ogl.GL_PROJECTION)
        ogl.glLoadIdentity()
        oglu.gluPerspective(45, (self.width/self.height), 0.0001, 1000)
        ogl.glMatrixMode(ogl.GL_MODELVIEW)
        
    def displayWindow(self):
        oglut.glutDisplayFunc(self.showScreen)
        oglut.glutIdleFunc(self.showScreen)
        oglut.glutMotionFunc(self.mouseTracker)
        oglut.glutPassiveMotionFunc(self.mouseTracker)
        oglut.glutReshapeFunc(self.reshapeWindow)
        
        ogl.glMatrixMode(ogl.GL_MODELVIEW)
        ogl.glLoadIdentity()
        ogl.glTranslatef(0, 0, -100)
        
        ogl.glEnable(ogl.GL_DEPTH_TEST)
        
        while True:
            oglut.glutMainLoopEvent()
            oglut.glutPostRedisplay()
            time.sleep(0.01)



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
    oglut.glutInitWindowSize(800, 500)
    wind = oglut.glutCreateWindow(b'OpenGL')
    
    id_canvas = IDDraw(0,a.cont.objectlist[0].objectlist[0].objectlist[20].objectlist[0], a.cont.objectlist[0].objectlist[0].objectlist[20].objectlist[1])
    
    id_canvas.displayWindow()
    pass