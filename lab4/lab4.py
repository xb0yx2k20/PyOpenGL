import math
import glfw
import logging
import numpy as np
from OpenGL import GL as gl
from OpenGL.GL import *



BUILDING_POLYGON = 1
POLYGON_BUILDED = 2
RASTERISATION = 3
FILTRATION = 4
SIZE = 1000

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

mouse = Point(0, 0)
stage = BUILDING_POLYGON
points = []
sizeX, sizeY = SIZE, SIZE
pixels = np.zeros((sizeY, sizeX), dtype=np.uint8)
tempPixels = np.zeros((sizeY, sizeX), dtype=np.uint8)
list = {}
edges = []

def makeEdges():
    global edges
    edges = np.zeros((len(points), 2, 2))
    for i, p in enumerate(points):
        nextP = points[(i+1)%len(points)]
        edges[i] = np.array([p, nextP])

def isExtrema(y, y1, y2):
    return (y > y1 and y > y2) or (y < y1 and y < y2)

def vertexCountTwice(i, j):
    l = len(edges)
    return isExtrema(edges[i][j].y, edges[i][(j+1)%2].y, edges[(i-1+l)%l][j].y)

def addToList(x, y):
    y = int(math.floor(y))
    if y not in list:
        list[y] = []
    list[y].append(int(math.floor(x)))

def DDA():
    global list
    for i, edge in enumerate(edges):
        if vertexCountTwice(i, 0):
            addToList(edge[0][0], edge[0][1])
        addToList(edge[1][0], edge[1][1])

        dy = edge[1][1] - edge[0][1]
        dx = edge[1][0] - edge[0][0]

        if dy == 0:
            continue

        count = int(math.ceil(math.fabs(dy)))
        dy = dy / float(count)
        dx = dx / float(count)

        def checkEndFunc(i):
            if dy > 0:
                return edge[0][1]+i*dy < edge[1][1]
            else:
                return edge[0][1]+i*dy > edge[1][1]

        for i in range(1, count):
            addToList(edge[0][0]+i*dx, edge[0][1]+i*dy)

def drawLine(y, x1, x2):
    for i in range(x1, x2+1):
        pixels[sizeY-y, i] = 255

def fill():
    for y in list:
        list[y].sort()
        for i in range(0, len(list[y]), 2):
            drawLine(y, list[y][i], list[y][i+1])

def rasterisation():
    global pixels, list
    pixels = np.zeros((sizeY, sizeX), dtype=np.uint8)
    list = {}
    makeEdges()
    DDA()
    fill()

def getNeighborsSum(matrix, row, col):
    rows = len(matrix)
    cols = len(matrix[0])
    total_sum = 0

    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            if i == row and j == col:
                continue

            if 0 <= i < rows and 0 <= j < cols:
                total_sum += matrix[i][j]

    return total_sum

def filtrate():
    global pixels
    tempPixels = np.zeros(sizeY*sizeX, dtype=np.uint8)
    for i in range(sizeY):
        for j in range(sizeX):
            sum, counter = getNeighborsSum(i, j)
            tempPixels[i*sizeX+j] = int(sum / counter)
    pixels = tempPixels


def drawPolygon():
    global stage
    if stage == 1 or stage == 2:
        if len(points) > 0:
            gl.glBegin(gl.GL_LINE_LOOP)
            for p in points:
                gl.glVertex2d(p.x, p.y)
            if stage == 1:
                gl.glVertex2d(mouse.x, mouse.y)
            gl.glEnd()
    else:
        gl.glDrawPixels(sizeX, sizeY, gl.GL_BLUE, gl.GL_UNSIGNED_BYTE, pixels)


def cycleInit(w):
    mouse.x, mouse.y = glfw.get_cursor_pos(w)


def closeWindowCallback(w):
    logging.info("ESC")
    glfw.set_window_should_close(w, True)


def sizeCallback(w, width, height):
    global sizeX, sizeY, points, pixels, stage
    sizeX, sizeY = width, height
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0, float(width), float(height), 0, 0, 1)

    gl.glViewport(0, 0, width, height)

    points = []
    pixels = np.zeros(sizeY*sizeX, dtype=np.uint8)
    stage = 1


def changeStateCallback():
    global stage
    if len(points) > 2:
        stage += 1
        if stage > 3:
            stage = 1
        if stage == 3:
            filtrate()
        logging.info(stage)


def clear():
    global points
    points = []


def keyCallback(w, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            closeWindowCallback(w)
        if key == glfw.KEY_SPACE:
            changeStateCallback()
        if key == glfw.KEY_DELETE:
            clear()


def makePoint(w, button, action, mod):
    global stage, points
    if stage == 1:
        x, y = glfw.get_cursor_pos(w)
        logging.info(f"{x} {y} :mouse")
        points.append(Point(x, y))


def deletePoint(w, button, action, mod):
    global stage, points
    if stage == 1 and len(points) > 0:
        points = points[:-1]

def mouseCallback(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        makePoint(window, button, action, mods)
    if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
        deletePoint(window, button, action, mods)

def initWindow():
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
    window = glfw.create_window(SIZE, SIZE, "lab4", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Failed to create window")

    glfw.make_context_current(window)

    return window

def main():
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = initWindow()
    glfw.set_framebuffer_size_callback(window, sizeCallback)
    glfw.set_key_callback(window, keyCallback)
    glfw.set_mouse_button_callback(window, mouseCallback)

    w, h = glfw.get_framebuffer_size(window)
    sizeCallback(window, w, h)

    glfw.show_window(window)

    while not glfw.window_should_close(window):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        cycleInit(window)

        drawPolygon()

        glfw.wait_events()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == '__main__':
    main()