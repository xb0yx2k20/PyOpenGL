# -*- coding: utf-8 -*-
import math
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
#import sys
from random import random
import numpy as np

global pointcolor
object_matrix = np.identity(4)

last_mouse_x = 0
last_mouse_y = 0
n = 10
wireframe_mode = False

def handle_key_press(key, x, y):
    global n, scale
    if key == b'q':
        n -= 1
    if key == b'e':
        n += 1
    global wireframe_mode
    if key == b'x':
        wireframe_mode = not wireframe_mode
        if wireframe_mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glDisable(GL_CULL_FACE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glEnable(GL_CULL_FACE)
    elif key == b'o':
        scale -= 0.1
    elif key == b'p':
        scale += 0.1
    glutPostRedisplay()


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

globalMas = []
pointdata = []
def draw():
    global n, globalMas, scale, pointdata
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnableClientState(GL_VERTEX_ARRAY)            
    glEnableClientState(GL_COLOR_ARRAY)      

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    vectors = []
    for i in range(n+1):
        theta = 2 * math.pi * i / n 
        for j in range(n+1):
            phi = math.pi * j / n
            x = math.cos(theta) * math.sin(phi)
            y = math.sin(theta) * math.sin(phi)
            z = math.cos(phi)
            vectors.append([x, y, z])
        globalMas.append(vectors)
        vectors = []

    for i in range(len(globalMas) - 1):
        for j in range(len(globalMas[0]) - 1):
            pointdata.append(globalMas[i + 1][j][0]) 
            pointdata.append(globalMas[i + 1][j][1]) 
            pointdata.append(globalMas[i + 1][j][2])
            pointdata.append(globalMas[i][j][0]) 
            pointdata.append(globalMas[i][j][1])
            pointdata.append(globalMas[i][j][2])
            pointdata.append(globalMas[i][j + 1][0]) 
            pointdata.append(globalMas[i][j + 1][1]) 
            pointdata.append(globalMas[i][j + 1][2])
            pointdata.append(globalMas[i + 1][j + 1][0]) 
            pointdata.append(globalMas[i + 1][j + 1][1]) 
            pointdata.append(globalMas[i + 1][j + 1][2])

    #globalMas = np.array(globalMas) 
    #print((globalMas))

    glPushMatrix()
    glMultMatrixf(object_matrix)

    glScalef(scale*0.25, scale*0.25, scale*0.25)

    

    glVertexPointer(3, GL_FLOAT, 0, pointdata)
    glColorPointer(3, GL_FLOAT, 0, pointcolor)
    glDrawArrays(GL_QUADS, 0, 12 * n * n)
    glDisableClientState(GL_VERTEX_ARRAY)           
    glDisableClientState(GL_COLOR_ARRAY) 
    glPopMatrix()
    glutSwapBuffers()   



start_time = time.perf_counter()

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(50, 50)
glutInit()
glutCreateWindow(b"Shaders!")
glutReshapeFunc(lambda w, h: glViewport(0, 0, w, h))
glEnable(GL_CULL_FACE)
glutDisplayFunc(draw)
print(globalMas)
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
print(globalMas)
print(globalMas)
print(globalMas)
print(globalMas)

pointcolor = []
print(pointdata)
for i in range(12 * n * n):
    pointcolor.append([1, i%2, 0])


print('total time:', time.perf_counter() - start_time)

glutMainLoop()
