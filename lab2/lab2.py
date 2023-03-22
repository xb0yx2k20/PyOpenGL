from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
import numpy as np

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



def draw_scene():
    global object_matrix, scale
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPushMatrix()
    glMultMatrixf(object_matrix)

    glScalef(scale*0.25, scale*0.25, scale*0.25)

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

    glPopMatrix()
    glutSwapBuffers()


wireframe_mode = False

def handle_key_press(key, x, y):
    global wireframe_mode
    global scale
    if key == b'q':
        wireframe_mode = not wireframe_mode
        if wireframe_mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glDisable(GL_CULL_FACE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glEnable(GL_CULL_FACE)
    elif key == b'e':
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        matrix = [1, 0, 0, 0.1, 0, 1, 0, 0.1, 0, 0, 0, -0.1, 0, 0, 0, 1]
        glPopMatrix()
        glMultMatrixf(matrix)
    elif key == b'o':
        scale -= 0.1
    elif key == b'p':
        scale += 0.1
    
    glutPostRedisplay()



def reshape(width, height):
   aspect = float(width) / float(height)
   glViewport(0, 0, width, height)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   if aspect > 1:
      glOrtho(-aspect, aspect, -1.0, 1.0, -1.0, 1.0)
   else:
      glOrtho(-1.0, 1.0, -1.0/aspect, 1.0/aspect, -1.0, 1.0)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)    
glutInitWindowSize(600, 600)
glutCreateWindow(b"PyOpenGL Example")

glutReshapeFunc(lambda w, h: glViewport(0, 0, w, h))
glutKeyboardFunc(handle_key_press)
glutReshapeFunc(reshape)
glEnable(GL_CULL_FACE)
glutDisplayFunc(draw_scene)
glutMouseFunc(handle_mouse_down)
glutMotionFunc(handle_mouse_move)
#glutMouseWheelFunc(mouse_wheel_callback)
glutMainLoop()
