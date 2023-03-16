from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import numpy as np
def handle_mouse_down(button, state, x, y):
    global mouse_down, last_mouse_x, last_mouse_y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
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
def draw_circle(x, y, z, radius, num_segments):
    glBegin(GL_POLYGON)
    for i in range(num_segments):
        angle = i * 2 * math.pi / num_segments
        glVertex3f(x + radius * math.cos(angle), y + radius * math.sin(angle), z)
    glEnd()

def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
    glColor3f(1.0, 0.0, 0.0)
    draw_circle(0, 0, 0, 1, 20)
    glutSwapBuffers()
def mouse_wheel_callback(button, direction, x, y):
    global scale
    if direction > 0:
        scale += 0.1
    else:
        scale -= 0.1
    glutPostRedisplay()
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(640, 480)
glutCreateWindow(b"Circle")
glutMouseWheelFunc(mouse_wheel_callback)
glutReshapeFunc(lambda w, h: glViewport(0, 0, w, h))
glutMouseFunc(handle_mouse_down)
glutMotionFunc(handle_mouse_move)
glutDisplayFunc(draw_scene)
glutMainLoop()
