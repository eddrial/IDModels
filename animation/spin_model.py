import numpy as np
from vispy import app, gloo
from vispy.io import image
from vispy.util.transforms import perspective, translate, rotate
import radia as rd
import wradia as wrd
import apple2p5.model2 as id1
from idcomponents import parameters

import time
import random
from vispy.gloo.util import _screenshot

class IDDraw():
    def __init__(self):
        self.vert = """
        // Uniforms
        // ------------------------------------
        uniform   mat4 u_model;
        uniform   mat4 u_view;
        uniform   mat4 u_projection;
        uniform   vec4 u_color;
        
        // Attributes
        // ------------------------------------
        attribute vec3 a_position;
        attribute vec4 a_color;
        attribute vec3 a_normal;
        
        // Varying
        // ------------------------------------
        varying vec4 v_color;
        
        void main()
        {
            v_color = a_color * u_color;
            gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
        }
        """
        
        
        self.frag = """
        // Varying
        // ------------------------------------
        varying vec4 v_color;
        
        void main()
        {
            gl_FragColor = v_color;
        }
        """
        
        
        # -----------------------------------------------------------------------------
        
        """
        Build vertices for a colored cube.
    
        V  is the vertices
        I1 is the indices for a filled cube (use with GL_TRIANGLES)
        I2 is the indices for an outline cube (use with GL_LINES)
        """
        self.vtype = [('a_position', np.float32, 3),
                 ('a_normal', np.float32, 3),
                 ('a_color', np.float32, 4)]
        
        self.V = np.array([], dtype = self.vtype)
        self.I1 = np.array([], dtype = np.uint32)
        self.I2 = np.array([], dtype = np.uint32)
    
    def cube(self):
        """
        Build vertices for a colored cube.
    
        V  is the vertices
        I1 is the indices for a filled cube (use with GL_TRIANGLES)
        I2 is the indices for an outline cube (use with GL_LINES)
        """
        vtype = [('a_position', np.float32, 3),
                 ('a_normal', np.float32, 3),
                 ('a_color', np.float32, 4)]
        # Vertices positions
        v = [[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
             [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]]
        # Face Normals
        n = [[0, 0, 1], [1, 0, 0], [0, 1, 0],
             [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
        # Vertice colors
        c = [[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 0, 1],
             [1, 1, 0, 1], [1, 1, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1]]
    
        V = np.array([(v[0], n[0], c[0]), (v[1], n[0], c[1]),
                      (v[2], n[0], c[2]), (v[3], n[0], c[3]),
                      (v[0], n[1], c[0]), (v[3], n[1], c[3]),
                      (v[4], n[1], c[4]), (v[5], n[1], c[5]),
                      (v[0], n[2], c[0]), (v[5], n[2], c[5]),
                      (v[6], n[2], c[6]), (v[1], n[2], c[1]),
                      (v[1], n[3], c[1]), (v[6], n[3], c[6]),
                      (v[7], n[3], c[7]), (v[2], n[3], c[2]),
                      (v[7], n[4], c[7]), (v[4], n[4], c[4]),
                      (v[3], n[4], c[3]), (v[2], n[4], c[2]),
                      (v[4], n[5], c[4]), (v[7], n[5], c[7]),
                      (v[6], n[5], c[6]), (v[5], n[5], c[5])],
                     dtype=vtype)
        I1 = np.resize(np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32), 6 * (2 * 3))
        I1 += np.repeat(4 * np.arange(2 * 3, dtype=np.uint32), 6)
    
        I2 = np.resize(
            np.array([0, 1, 1, 2, 2, 3, 3, 0], dtype=np.uint32), 6 * (2 * 4))
        I2 += np.repeat(4 * np.arange(6, dtype=np.uint32), 8)
    
        return V, I1, I2
    
    def cube2(self, my_wradobj):
        
        
        def excavate(objofint):
            if isinstance(objofint, wrd.wrad_obj.wradObjCnt):
                for i in range(len(objofint.objectlist)):
                    print('we are at {}'.format(i))
                    excavate(objofint.objectlist[i])
            else:
                v = objofint.vertices.tolist()
                c = objofint.colour + [1]
                n = [[0, 0, 1], [1, 0, 0], [0, 1, 0],
                     [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
            
                Vtmp = np.array([(v[5], n[0], c), (v[4], n[0], c),
                              (v[0], n[0], c), (v[1], n[0], c),
                              (v[5], n[1], c), (v[1], n[1], c),
                              (v[2], n[1], c), (v[6], n[1], c),
                              (v[5], n[2], c), (v[6], n[2], c),
                              (v[7], n[2], c), (v[4], n[2], c),
                              (v[4], n[3], c), (v[7], n[3], c),
                              (v[3], n[3], c), (v[0], n[3], c),
                              (v[3], n[4], c), (v[2], n[4], c),
                              (v[1], n[4], c), (v[0], n[4], c),
                              (v[2], n[5], c), (v[3], n[5], c),
                              (v[7], n[5], c), (v[6], n[5], c)],
                             dtype=self.vtype)
                
                I1tmp = np.resize(np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32), 6 * (2 * 3))
                I1tmp += np.repeat(4 * np.arange(2 * 3, dtype=np.uint32), 6)
                
                I2tmp = np.resize(np.array([0, 1, 1, 2, 2, 3, 3, 0], dtype=np.uint32), 6 * (2 * 4))
                I2tmp += np.repeat(4 * np.arange(6, dtype=np.uint32), 8)
                
                self.V = np.hstack([self.V,Vtmp])
                if len(self.I1)>0:
                    self.I1 = np.hstack([self.I1,np.max(self.I1)+1+ I1tmp])
                    self.I2 = np.hstack([self.I2,np.max(self.I2)+1+ I2tmp])
                else:
                    self.I1 = I1tmp
                    self.I2 = I2tmp
                
                
            
            #return verts, i1s, i2s
            
            
        excavate(my_wradobj)
    
        return self.V, self.I1, self.I2


# -----------------------------------------------------------------------------
class Canvas(app.Canvas):

    def __init__(self, drawobj, my_wrdobj):
        app.Canvas.__init__(self, keys='interactive', size=(800, 600))

        #self.vertices, self.filled, self.outline = drawobj.cube()
        self.vertices, self.filled, self.outline = drawobj.cube2(my_wrdobj)
        self.filled_buf = gloo.IndexBuffer(self.filled)
        self.outline_buf = gloo.IndexBuffer(self.outline)

        self.program = gloo.Program(drawobj.vert, drawobj.frag)
        self.program.bind(gloo.VertexBuffer(self.vertices))

        self.view = np.dot(translate((0, -150, -301)),
                           rotate(30,(1,0,0)))
        self.model = np.eye(4, dtype=np.float32)

        gloo.set_viewport(0, 0, self.physical_size[0], self.physical_size[1])
        self.projection = perspective(45.0, self.size[0] /
                                      float(self.size[1]), 0.1, 500.0)

        self.program['u_projection'] = self.projection

        self.program['u_model'] = self.model
        self.program['u_view'] = self.view

        self.theta = -90
        self.phi = 45
        
        self.time_count = 0

        gloo.set_clear_color('white')
        gloo.set_state('opaque')
        gloo.set_polygon_offset(1, 1)

        self._timer = app.Timer('auto', connect=self.on_timer, start=True)

        self.show()

    # ---------------------------------
    def on_timer(self, event):
        self.time_count +=0.5
        
        self.theta += .0
        
        if self.time_count < 360 or self.time_count>720:
            self.phi = 45
        else:
            #self.phi = 45+self.time_count
            self.phi = 45 + 360*(np.cos(2*np.pi*self.time_count/720))
            
        
        if self.time_count > 1080:
            self._timer.stop()
        
        self.model = np.dot(rotate(self.theta, (1, 0, 0)),
                            rotate(self.phi, (0, 1, 0)))
        self.program['u_model'] = self.model
        self.update()
        if self.time_count%1 == 0:
            scshframe = _screenshot()
            image.write_png('d:\Profile\oqb\Desktop\presentations\POF2025\Animation\plainAPPLE{}.png'.format(self.time_count), scshframe)

    # ---------------------------------
    def on_resize(self, event):
        gloo.set_viewport(0, 0, event.physical_size[0], event.physical_size[1])
        self.projection = perspective(45.0, event.size[0] /
                                      float(event.size[1]), 0.1, 500.0)
        self.program['u_projection'] = self.projection

    # ---------------------------------
    def on_draw(self, event):
        gloo.clear()

        # Filled cube

        gloo.set_state(blend=False, depth_test=True, polygon_offset_fill=True)
        self.program['u_color'] = 1, 1, 1, 1
        self.program.draw('triangles', self.filled_buf)

        # Outline
        gloo.set_state(blend=True, depth_test=True, polygon_offset_fill=False)
        gloo.set_depth_mask(False)
        self.program['u_color'] = 0, 0, 0, 1
        self.program.draw('lines', self.outline_buf)
        gloo.set_depth_mask(True)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    #create ID
    rd.UtiDelAll()
    a_param = parameters.model_parameters(
        periods = 4,
        periodlength = 32,
        minimumgap = 6,
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
    
    #Drawing stuff
    
    idd = IDDraw()
    canvas = Canvas(idd, a.cont)
    app.run()