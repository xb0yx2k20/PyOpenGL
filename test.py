from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0, 0)

    glBegin(GL_TRIANGLES)
    for edge in edges:
        glVertex2f(edge[0][0], edge[0][1])
        glVertex2f(edge[1][0], edge[1][1])
        glVertex2f(vertex[0], vertex[1])
    glEnd()

    glutSwapBuffers()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0, 500, 0, 500)

def main():
    global edges, vertex

    vertex = (100, 100)
    edges = [((100, 200), (200, 200)),
             ((200, 200), (200, 100)),
             ((200, 100), (100, 100)),
             ((100, 100), (100, 150)),
             ((100, 150), (150, 150)),
             ((150, 150), (150, 100)),
             ((150, 100), (100, 100))]

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow("test")

    glutDisplayFunc(display)

    init()

    glutMainLoop()

if __name__ == '__main__':
    main()
