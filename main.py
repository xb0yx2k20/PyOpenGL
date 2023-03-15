from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 1.0, 1.0, 10.0)
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Расположение камеры
    gluLookAt(3,3,3, 0,0,0, 0,1,0)

    # Отрисовка куба
    glBegin(GL_QUADS)
    
    # Верхняя грань
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)
    # Задняя грань (зеленая)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    # Верхняя грань (синяя)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    # Нижняя грань (желтая)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
    # Левая грань (голубая)
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    # Правая грань (фиолетовая)
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)
    glEnd()
    glutSwapBuffers()
def reshape(w, h):
    glViewport(0, 0, w, h)

def keyboard(key, x, y):
    if key == b'\x1b':
        sys.exit()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutCreateWindow("Cube with three-point perspective")
    init()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == '__main__':
    main()