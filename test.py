import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import time
import math

M_PI = 3.1415926535
delta = 0.05
dt = 0.01
t = 0
velo = -0.1
num = 5000
g = 9.81
pos = 1.
last_pos = 1.
current_time = 0
accumulator = 0
tex_enable = True
shift = 0
WIN_WIDTH, WIN_HEIGHT = 800, 800


def main():
    global tex, num
    if not glfw.init():
        return
    window = glfw.create_window(WIN_WIDTH, WIN_HEIGHT, "Lab7", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    tex = read_texture("/Users/xb0yx2k20/Documents/photo_5456474844414725958_y.jpg")
    # make_list(8)
    make_arrays()
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


def read_texture(filename):
    from PIL import Image
    img = Image.open(filename)
    img_data = np.array(list(img.getdata()), np.int16)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    return texture_id


def make_list(id):
    global M_PI

    glNewList(id, GL_COMPILE)

    c = 0
    v = - M_PI/2
    u = - M_PI + 0.1
    glColor3fv((0.5, 0.5, 0.5))
    glBegin(GL_LINES)
    while (v < M_PI/2):
        while (u < M_PI):
            x = 0.3 * math.cos(v)*math.cos(u)
            y = 0.7*math.cos(v)*math.sin(u)
            z = 0.5*math.sin(v)
            glVertex3f(x, y, z)
            glColor3fv((0.5, 0.5, 0.5))

            x = 0.3*math.cos(v+delta)*math.cos(u)
            y = 0.7 * math.cos(v+delta)*math.sin(u)
            z = 0.5*math.sin(v+delta)
            glVertex3f(x, y, z)
            glColor3fv((0.5, 0.5, 0.5))

            c += 1
            if c == 50:
                c = 0
            u += delta
        u = - M_PI
        v += delta
    glEnd()
    glEndList()


def make_arrays():
    global M_PI
    verticies = []

    c = 0
    v = - M_PI/2
    u = - M_PI + 0.1
    while (v < M_PI/2):
        while (u < M_PI):
            x = 0.3 * math.cos(v)*math.cos(u)
            y = 0.7*math.cos(v)*math.sin(u)
            z = 0.5*math.sin(v)

            x_ = 0.3*math.cos(v+delta)*math.cos(u)
            y_ = 0.7 * math.cos(v+delta)*math.sin(u)
            z_ = 0.5*math.sin(v+delta)
            verticies.extend([.0, .0, .5, .5, 0, x, y, z,
                              .5, 1., .5, .5, 0, x_, y_, z_,
                              1., 1., .5, .5, 0, 0, 0, 1,])

            c += 1
            if c == 50:
                c = 0
            u += delta
        u = - M_PI
        v += delta

    glInterleavedArrays(GL_T2F_C3F_V3F,
                        2 * 4 + 3 * 4 + 3 * 4,
                        np.asarray(verticies, dtype=np.float32))


def display(window):
    global pos, last_pos, shift, current_time, dt, t, accumulator, velo, tex, num
    glEnable(GL_TEXTURE_2D)
    # if tex_enable:
    #     glEnable(GL_TEXTURE_2D)
    # else:
    #     glDisable(GL_TEXTURE_2D)
    glClearColor(0.5, 0.5, 0.5, 0.5)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glDisable(GL_NORMALIZE)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [0.8, -1., 0., 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.7, 0.2])
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.2)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.4)

    new_time = glutGet(GLUT_ELAPSED_TIME)
    frame_time = (new_time - current_time)
    if frame_time > 0.25:
        frame_time = 0.25
    current_time = new_time
    accumulator += frame_time
    while (accumulator >= dt):
        last_pos = pos
        velo -= g * dt
        pos += velo * dt
        if pos <= -0.40:
            pos = -0.40
            velo = (1 - 10) * velo / (1 + 10)
        t += dt
        accumulator -= dt

    alpha = accumulator / dt
    pos = pos * alpha + last_pos * (1 - alpha)
    glPushMatrix()
    glTranslatef(0, pos, 0)
    glTranslatef(shift, 0, 0)
    glRotatef(-90, 1., 0., 0)
    glRotatef(45, 0., 1., 1)
    glDrawArrays(GL_POINTS, 0, num * 3)

    glPopMatrix()
    glfw.swap_buffers(window)
    glfw.poll_events()
    if np.abs(velo) < 5e-2 and pos == -0.4:
        glfw.set_window_should_close(window, True)


def key_callback(window, key, scancode, action, mods):
    global tex_enable, num, shift
    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            tex_enable = not tex_enable
        if key == glfw.KEY_LEFT:
            num -= 1
            if num == 0:
                num = 1
        if key == glfw.KEY_RIGHT:
            num += 1
        if key == glfw.KEY_UP:
            shift += 0.1
        if key == glfw.KEY_DOWN:
            shift -= 0.1


start_time = time.perf_counter()
main()
print('total time:', time.perf_counter() - start_time)
