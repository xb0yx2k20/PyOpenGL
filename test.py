# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
#import sys
from random import random
import numpy as np

global pointcolor
object_matrix = np.identity(4)

last_mouse_x = 0
last_mouse_y = 0

def mouse_wheel_callback(wheel, direction, x, y):
    global scale
    if direction > 0:
        scale += 0.1
    else:
        scale -= 0.1
    glutPostRedisplay()


def handle_mouse_down(button, state, x, y):
    global mouse_down, last_mouse_x, last_mouse_y
    if button == 1 and state == 1:
        last_mouse_x = x
        last_mouse_y = y

def handle_mouse_move(x, y):
    global object_matrix, last_mouse_x, last_mouse_y
    delta_x = x - last_mouse_x
    delta_y = y - last_mouse_y
    rotation_y = np.identity(4)
    rotation_x = np.identity(4)
    rotation_y[0, 0] = np.cos(delta_x / 100.0)
    rotation_y[2, 0] = -np.sin(delta_x / 100.0)
    rotation_y[0, 2] = np.sin(delta_x / 100.0)
    rotation_y[2, 2] = np.cos(delta_x / 100.0)
    rotation_x[1, 1] = np.cos(delta_y / 100.0)
    rotation_x[2, 1] = np.sin(delta_y / 100.0)
    rotation_x[1, 2] = -np.sin(delta_y / 100.0)
    rotation_x[2, 2] = np.cos(delta_y / 100.0)
    object_matrix = np.dot(rotation_x, object_matrix)
    object_matrix = np.dot(rotation_y, object_matrix)
    last_mouse_x = x
    last_mouse_y = y
    glutPostRedisplay()


scale = 1.0

def specialkeys(key, x, y):
    global pointcolor
    if key == GLUT_KEY_UP:          
        glRotatef(5, 1, 0, 0)       
    if key == GLUT_KEY_DOWN:       
        glRotatef(-5, 1, 0, 0)      
    if key == GLUT_KEY_LEFT:        
        glRotatef(5, 0, 1, 0)       
    if key == GLUT_KEY_RIGHT:       
        glRotatef(-5, 0, 1, 0)      
    if key == GLUT_KEY_END:         
        pointcolor = [[random(), random(), random()], [random(), random(), random()], [random(), random(), random()]]


def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnableClientState(GL_VERTEX_ARRAY)            
    glEnableClientState(GL_COLOR_ARRAY)      

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPushMatrix()
    glMultMatrixf(object_matrix)

    glScalef(scale*0.25, scale*0.25, scale*0.25)
    
    glVertexPointer(3, GL_FLOAT, 0, pointdata)
    glColorPointer(3, GL_FLOAT, 0, pointcolor)
    glDrawArrays(GL_QUADS, 0, 8)
    '''
    glBegin(GL_QUADS)

    glColor3f(0.0, 0.0, 1.0);
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)

    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, -1, -1)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)



    glEnd()
    '''
    glDisableClientState(GL_VERTEX_ARRAY)           
    glDisableClientState(GL_COLOR_ARRAY) 
    glPopMatrix()
    glutSwapBuffers()   

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(50, 50)
glutInit(sys.argv)
glutCreateWindow(b"Shaders!")
glutReshapeFunc(lambda w, h: glViewport(0, 0, w, h))
glEnable(GL_CULL_FACE)
glutDisplayFunc(draw)
glutMouseFunc(handle_mouse_down)
glutMotionFunc(handle_mouse_move)
glutIdleFunc(draw)
glutSpecialFunc(specialkeys)
glClearColor(0.2, 0.2, 0.2, 1)
vertex = create_shader(GL_VERTEX_SHADER, """
varying vec4 vertex_color;
            void main(){
                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                vertex_color = gl_Color;
            }""")
fragment = create_shader(GL_FRAGMENT_SHADER, """
varying vec4 vertex_color;
            void main() {
                gl_FragColor = vertex_color;
}""")
program = glCreateProgram()
glAttachShader(program, vertex)
glAttachShader(program, fragment)
glLinkProgram(program)
glUseProgram(program)
pointdata = [1, -1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 
                      -1, -1, 1, -1, 1, 1, -1, 1, -1, -1, -1, -1, 
                      -1, -1, -1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 
                      1, -1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 
                      1, 1, 1, 1, 1, -1, -1, 1, -1, -1, 1, 1, 
fg                      1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1]
pointcolor = [[1, 1, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0],
              [1, 1, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
#pointcolor = [1, 0, 1]*8
glutMainLoop()