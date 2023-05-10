from OpenGL.GL import *
import glfw
from PIL import Image
import numpy as np
import math
object_matrix = np.identity(4)

G = 9.81
INITIAL_CUBE_VELOCITY = 0 # начальная скорость куба
CUBE_HEIGHT_RANGE = (0, 10000)

cube_velocity = INITIAL_CUBE_VELOCITY
cube_height = CUBE_HEIGHT_RANGE[1]
theta = 0

rot = 0
scale = 1
is_texturing_enabled = True


def normalize(x, x_range, normalization_range):
    a, b = normalization_range
    x_min, x_max = x_range
    return (b - a) * ((x - x_min) / (x_max - x_min)) + a


def program():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Lab6", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    setup()

    while not glfw.window_should_close(window):
        prepare()
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()


def key_callback(window, key, scancode, action, mods):
    global rot, scale, is_texturing_enabled

    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            rot -= 3
        if key == glfw.KEY_LEFT:
            rot += 3
        if key == glfw.KEY_UP:
            scale += 0.02
        if key == glfw.KEY_DOWN:
            scale -= 0.02
        if key == glfw.KEY_C:
            is_texturing_enabled = not is_texturing_enabled


def enable_texturing():
    global is_texturing_enabled
    if is_texturing_enabled:
        glEnable(GL_TEXTURE_2D)


def disable_texturing():
    global is_texturing_enabled
    if is_texturing_enabled:
        glDisable(GL_TEXTURE_2D)


def setup():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-0.1, 0.1, -0.1, 0.1, 0.2, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(GL_FRONT, GL_DIFFUSE)
    glShadeModel(GL_SMOOTH)

    load_texture()


def load_texture():
    img = Image.open("lab6/text.bmp")
    img_data = np.array(list(img.getdata()), np.int8)

    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)


def prepare():
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def display():
    global CUBE_HEIGHT_RANGE, cube_velocity, cube_height, theta, rot, scale
    glPushMatrix()
    glRotatef(-60, 1, 0, 0)
    glRotatef(33, 0, 0, 1)
    glTranslatef(2, 3, -2.5)

    glRotatef(rot, 0, 0, 1)
    glScalef(scale, scale, scale)

    glPushMatrix()

    if cube_height - cube_velocity > CUBE_HEIGHT_RANGE[0]:
        cube_height -= cube_velocity
        if cube_velocity < 0 and cube_velocity + G > 0:
            cube_velocity = 0
        else:
            cube_velocity += G
    else:
        cube_height = CUBE_HEIGHT_RANGE[0]
        cube_velocity = -cube_velocity

    glRotatef(45, 0, 0, 1)
    glTranslatef(0, 0, normalize(cube_height, CUBE_HEIGHT_RANGE, (0.5, 1)))
    glScalef(0.35, 0.35, 0.35)
    draw_cube()

    glPopMatrix()

    glPushMatrix()
    glRotatef(45, 0, 1, 0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 1, 0))

    glTranslatef(0, 0, 2)
    glScalef(0.2, 0.2, 0.2)
    glColor3f(1, 1, 1)
    draw_plane()
    glPopMatrix()

    glPopMatrix()

    theta += 0.9

n = 3
scale = 1.0
def draw_cube():
    enable_texturing()
    glBegin(GL_QUADS)


    global n
    global object_matrix, scale

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
    for i in range(len(globalMas) - 1):
        glColor3f(0, i % 2, 1)
        for j in range(len(globalMas[0]) - 1):
            glBegin(GL_POLYGON)
            glNormal3f(1.0, 0.0, 0.0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(globalMas[i + 1][j][0], globalMas[i + 1][j][1], globalMas[i + 1][j][2])
            glTexCoord2f(0.0, 0.0)
            glVertex3f(globalMas[i][j][0], globalMas[i][j][1], globalMas[i][j][2])
            glTexCoord2f(0.0, 1.0)
            glVertex3f(globalMas[i][j + 1][0], globalMas[i][j + 1][1], globalMas[i][j + 1][2])
            glTexCoord2f(1.0, 1.0)
            glVertex3f(globalMas[i + 1][j + 1][0], globalMas[i + 1][j + 1][1], globalMas[i + 1][j + 1][2])
            glEnd()
    

    

    
    

    glEnd()
    disable_texturing()


def draw_plane():
    verticies = (
        -1, -1, 0,
        1, -1, 0,
        1, 1, 0,
        -1, 1, 0
    )

    normals = (
        -1, -1, 3,
        1, -1, 3,
        1, 1, 3,
        -1, 1, 3
    )

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glVertexPointer(3, GL_FLOAT, 0, verticies)
    glNormalPointer(GL_FLOAT, 0, normals)
    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)


def main():
    try:
        program()
    except Exception as e:
        print('Error')
        print(e)


if __name__ == '__main__':
    main()