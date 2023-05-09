import math
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

object_matrix = np.identity(4)

last_mouse_x = None
last_mouse_y = None
move_sphere = False
# глобальные переменные для начальной позиции и скорости
position = np.array([0.0, 0.0, 0.0])
velocity = np.array([0.01, 0.01, 0.01])

# границы стенок
bounds = np.array([5, 5, 5])

def update_object_matrix(value):
    global object_matrix, position, velocity, bounds
    k = 0.1
    for i in object_matrix:
        i[0] += k
        glutPostRedisplay()
        if i[0] > bounds[0] or i[0] > -bounds[0]:
            k *= -1




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
    print(object_matrix)
    glutPostRedisplay()


scale = 1.0


def mouse_wheel_callback(wheel, direction, x, y):
    global scale
    if direction > 0:
        scale += 0.1
    else:
        scale -= 0.1
    glutPostRedisplay()



n = 3
def draw_scene():
    global n
    global object_matrix, scale, move_sphere
    if move_sphere == False:
        update_object_matrix(1)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPushMatrix()
    glMultMatrixf(object_matrix)
    glScalef(scale*0.25, scale*0.25, scale*0.25)
    globalMas = []
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
    globalMas = np.array(globalMas)
    print("\n\n")
    for i in range(len(globalMas) - 1):
        glColor3f(0, i % 2, 1)
        for j in range(len(globalMas[0]) - 1):
            glBegin(GL_POLYGON)
            glVertex3f(globalMas[i + 1][j][0], globalMas[i + 1][j][1], globalMas[i + 1][j][2])
            glVertex3f(globalMas[i][j][0], globalMas[i][j][1], globalMas[i][j][2])
            glVertex3f(globalMas[i][j + 1][0], globalMas[i][j + 1][1], globalMas[i][j + 1][2])
            glVertex3f(globalMas[i + 1][j + 1][0], globalMas[i + 1][j + 1][1], globalMas[i + 1][j + 1][2])
            glEnd()

 
    

    glPopMatrix()
    glutSwapBuffers()




# глобальная переменная-флаг
wireframe_mode = False
ch = 0
def handle_key_press(key, x, y):
    global n, scale
    if key == b'q':
        n -= 1
    if key == b'e':
        n += 1
    if key == b'm':
        if ch == 0:
            move_sphere = True
            ch = 1
        else:
            move_sphere = False
            ch = 0
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
glutMouseFunc(handle_mouse_down)
glutMotionFunc(handle_mouse_move)
glutKeyboardFunc(handle_key_press)

glutReshapeFunc(reshape)
glEnable(GL_CULL_FACE)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)

ambient_light = [0.2, 0.2, 0.2, 1.0]
glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_light)

light_pos = [1.0, 1.0, 1.0, 0.0]
glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.4, 0.4, 0.4, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))


glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR,( 0.5, 0.5, 0.5, 1.0))
glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 32)

glutDisplayFunc(draw_scene)
glutTimerFunc(10, update_object_matrix, 0)
glutMainLoop()
