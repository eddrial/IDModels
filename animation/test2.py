'''
Created on Apr 3, 2025

@author: oqb
'''

import pygame
from OpenGL.GL import *
from ctypes import *

if __name__ == '__main__':

    
    pygame.init ()
    screen = pygame.display.set_mode ((800,600), pygame.OPENGL|pygame.DOUBLEBUF, 24)
    glViewport (0, 0, 800, 600)
    glClearColor (0.0, 0.5, 0.5, 1.0)
    glEnableClientState (GL_VERTEX_ARRAY)
    
    vertices = [ 0.0, 1.0, 0.0,  0.0, 0.0, 0.0,  1.0, 0.0, 0.0,  1.0, 1.0, 0.0 ]
    vbo = glGenBuffers (1)
    glBindBuffer (GL_ARRAY_BUFFER, vbo)
    glBufferData (GL_ARRAY_BUFFER, len(vertices)*4, (c_float*len(vertices))(*vertices), GL_STATIC_DRAW)
    
    running = True
    while running:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        glClear (GL_COLOR_BUFFER_BIT)
    
        glBindBuffer (GL_ARRAY_BUFFER, vbo)
        glVertexPointer (3, GL_FLOAT, 0, None)
    
        glDrawArrays (GL_TRIANGLES, 0, 3)
    
        pygame.display.flip ()