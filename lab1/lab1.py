from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

triangle_x = 0.0
triangle_y = 0.0
size = 0.5


def display():
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glPushMatrix()
   glTranslatef(triangle_x, triangle_y, 0)
   glScalef(size, size, size)
   glBegin(GL_TRIANGLES)
   glVertex3f(0, 1, 0)
   glVertex3f(-0.2, 0.2, 0)
   glVertex3f(0.2, 0.2, 0)
   glVertex3f(0, -1, 0)
   glVertex3f(-0.2, -0.2, 0)
   glVertex3f(0.2, -0.2, 0)
   glVertex3f(-1, 0, 0)
   glVertex3f(-0.2, -0.2, 0)
   glVertex3f(-0.2, 0.2, 0)
   glVertex3f(1, 0, 0)
   glVertex3f(0.2, -0.2, 0)
   glVertex3f(0.2, 0.2, 0)
   glEnd()
   glPopMatrix()
   glutSwapBuffers()

def mouse(button, state, x, y):
   global triangle_x, triangle_y
   if button == GLUT_LEFT_BUTTON:
      if state == GLUT_DOWN:
         triangle_x = 2.0 * float(x) / glutGet(GLUT_WINDOW_WIDTH) - 1.0
         triangle_y = -2.0 * float(y) / glutGet(GLUT_WINDOW_HEIGHT) + 1.0
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
glutInitWindowSize(500 , 500)
glutCreateWindow("Triangle")
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutMouseFunc(mouse)
glutMainLoop()
