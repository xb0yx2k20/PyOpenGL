from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

# Создаем матрицу преобразования объекта
object_matrix = np.identity(4)

# Обработчик событий мыши для поворота объекта
mouse_down = False
last_mouse_x = None
last_mouse_y = None

def handle_mouse_down(button, state, x, y):
    global mouse_down, last_mouse_x, last_mouse_y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mouse_down = True
        last_mouse_x = x
        last_mouse_y = y

def handle_mouse_up(button, state, x, y):
    global mouse_down
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        mouse_down = False

def handle_mouse_move(x, y):
    global object_matrix, mouse_down, last_mouse_x, last_mouse_y
    if not mouse_down:
        return
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

# Обработчик событий клавиатуры для изменения масштаба объекта
scale = 1.0

def mouse_wheel_callback(button, direction, x, y):
    global scale

    if direction > 0:
        # Масштабируем объект при прокручивании колеса вверх
        scale += 0.1
    else:
        # Масштабируем объект при прокручивании колеса вниз
        scale -= 0.1

    glutPostRedisplay()


# Основной цикл отрисовки сцены
def draw_scene():
    global object_matrix, scale
    # Очищаем экран и устанавливаем цвет фона
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Устанавливаем матрицу в
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    

    # Применяем преобразование объекта
    glPushMatrix()
    glMultMatrixf(object_matrix)

    # Изменяем масштаб объекта
    glScalef(scale*0.25, scale*0.25, scale*0.25)

    # Рисуем объект
    glBegin(GL_QUADS)
    # Передняя грань (красная)
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
    glPopMatrix()
    glutSwapBuffers()


# Функция инициализации


# Создаем окно
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)    
glutInitWindowSize(600, 600)
glutCreateWindow(b"PyOpenGL Example")
glutMouseWheelFunc(mouse_wheel_callback)
glutReshapeFunc(lambda w, h: glViewport(0, 0, w, h))

# Устанавливаем обработчики событий мыши и клавиатуры
glutMouseFunc(handle_mouse_down)
glutMotionFunc(handle_mouse_move)


# Инициализируем сцену и запускаем главный цикл

glutDisplayFunc(draw_scene)
glutMainLoop()
