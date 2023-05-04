import glfw
import numpy as np
import math
from OpenGL.GL import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.x = self.p2.x - self.p1.x
        self.y = self.p2.y - self.p1.y

    def __str__(self):
        return "(" + str(self.p1) + ", " + str(self.p2) + ")"

    def scalar_product(self, other):
        if isinstance(other, Line):
            x1 = self.p2.x - self.p1.x
            y1 = self.p2.y - self.p1.y
            x2 = other.p2.x - other.p1.x
            y2 = other.p2.y - other.p1.y
            return float(x1 * x2 + y1 * y2)
        return 0

    def cross_product(self, other):
        if isinstance(other, Line):
            return float(other.x * self.y - self.x * other.y)
        return 0

    def get_normal(self):
        if self.x == 0:
            return Line(Point(0, 0), Point(0, 1))
        return Line(Point(0, 0), Point(-1 * (self.y / self.x), 1))

    def get_midpoint(self):
        return Point((self.p2.x + self.p1.x) / 2, (self.p2.y + self.p1.y) / 2)

    def reverse(self):
        temp = self.p1
        self.p1 = self.p2
        self.p2 = temp


angle = 0.0
angle_2 = 0.0
switch = False

sizeX = 1200
sizeY = 900

points = []
clipper_points = []
segments = []
normals = []
clipper_segments = []
additional_points = []
additional_clippers = []
mouse = Point(0, 0)

DRAWING_LINES = 0
DRAWING_POLYGON = 1
CLIPPING = 2

state = DRAWING_LINES

clipper_points.append(Point(0, 1.0))
clipper_points.append(Point(0.5, 0))
clipper_points.append(Point(0, -0.5))
clipper_points.append(Point(-0.5, 0))
clipper_points.append(Point(-0.7, 0.6))


points.append(Point(0.7, 0.3))
points.append(Point(-0.7, -0.3))


def projection1(f, a):
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, np.cos(a), np.sin(a), 0.0],
        [0.0, -np.sin(a), np.cos(a), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])


def projection2(f, a):
    return np.array([
        [np.cos(f), 0.0, -np.sin(f), 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [np.sin(f), 0.0, np.cos(f), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])


def rotation_matrix(i, f):
    i = np.asarray(i)
    assert i.size == 3, "i must be a 3d vector"
    i /= np.linalg.norm(i)

    c, s = np.cos(f), np.sin(f)
    a = 1 - c

    R = np.array([[i[0] ** 2 * a + c, i[0] * i[1] * a - i[2] * s, i[0] * i[2] * a + i[1] * s, 0],
                  [i[0] * i[1] * a + i[2] * s, i[1] ** 2 * a + c, i[1] * i[2] * a - i[0] * s, 0],
                  [i[0] * i[2] * a - i[1] * s, i[1] * i[2] * a + i[0] * s, i[2] ** 2 * a + c, 0],
                  [0, 0, 0, 1]], dtype=np.float32)
    return R


def points_to_segments(points):
    segments = []
    if len(points) % 2 == 1:
        points.pop()
    for i in range(0, len(points), 2):
        segments.append(Line(points[i], points[i + 1]))
    return segments


def points_to_polygon(points):
    segments = []
    for i in range(len(points)):
        segments.append(Line(points[i], points[(i + 1) % len(points)]))
    return segments


def find_normals(faces):
    normals = []
    for i in range(len(faces)):
        normal = faces[i].get_normal()
        if normal.scalar_product(Line(faces[i].p1, faces[(i + 1) % len(faces)].p2)) < 0:
            normal.reverse()
        normals.append(normal)
    return normals


def cyrus_beck(segment, faces, normals, is_inner):
    t_start = 0
    t_end = 1
    for i in range(len(faces)):
        d = segment.scalar_product(normals[i])
        w = normals[i].scalar_product(Line(faces[i].p1, segment.p1))
        if d == 0:
            if w < 0:
                if is_inner:
                    return []
                return [segment]
            continue
        t = -1 * w / d
        if d > 0:
            t_start = max(t_start, t)
        if d < 0:
            t_end = min(t_end, t)
    if t_start <= t_end:
        if is_inner:
            return [Line(Point(segment.p1.x + segment.x * t_start, segment.p1.y + segment.y * t_start),
                         Point(segment.p1.x + segment.x * t_end, segment.p1.y + segment.y * t_end))]

        return [Line(Point(segment.p1.x, segment.p1.y),
                     Point(segment.p1.x + segment.x * t_start, segment.p1.y + segment.y * t_start)),
                Line(Point(segment.p1.x + segment.x * t_end, segment.p1.y + segment.y * t_end),
                     Point(segment.p2.x, segment.p2.y))]
    if is_inner:
        return []
    return [segment]


def clipping(clipper_segments, segments, is_inner):
    normals = find_normals(clipper_segments)
    result = []
    for s in segments:
        visible = cyrus_beck(s, clipper_segments, normals, is_inner)
        if len(visible) > 0:
            result.extend(visible)
    return result



def complete_polygon(points):
    global additional_points
    additional_points = []
    temp = []
    if len(points) < 3:
        return
    while True:
        changes = 0
        previous = points[len(points) - 1]
        i = 0
        while i < len(points):
            current = points[i]
            next = points[(i + 1) % len(points)]
            if (Line(previous, current).cross_product(Line(current, next)) > 0):
                changes += 1
                temp.append(previous)
                points.pop(i)
                i -= 1
            elif len(temp) > 0:
                temp.append(previous)
                temp.append(current)
                additional_points.append(temp)
                temp = []
            previous = current
            i += 1
        if len(temp) > 0:
            temp.append(previous)
            temp.append(points[0])
            additional_points.append(temp)
            temp = []
        if changes == 0:
            break
    return points


def draw():

    glBegin(GL_LINE_LOOP)
    for point in clipper_points:
        glVertex2f(point.x, point.y)
    if state == DRAWING_POLYGON:
        glVertex2f(mouse.x, mouse.y)
    glEnd()

    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_LINES)
    for s in segments:
        glVertex2f(s.p1.x, s.p1.y)
        glVertex2f(s.p2.x, s.p2.y)
    glEnd()


def display(window):
    global segments, clipper_segments, clipper_points, additional_clippers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    width, height = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPushMatrix()


    segments = points_to_segments(points)
    clipper_segments = points_to_polygon(clipper_points)
    segments = clipping(clipper_segments, segments, False)
    print(segments[1].p1)

    draw()  

    glPopMatrix()

    glfw.swap_buffers(window)

    glfw.poll_events()


def main():
    if not glfw.init():
        return
    # Create the window
    window = glfw.create_window(sizeX, sizeY, "Lab5", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(window):
        display(window)

    # Terminate GLFW
    glfw.terminate()


def key_callback(window, key, scancode, action, mods):
    global angle, angle_2, switch
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            angle_2 += 10
        if key == 263: 
            angle_2 -= 10
        if key == glfw.KEY_UP:
            angle -= 10
        if key == glfw.KEY_DOWN:
            angle += 10
        if key == glfw.KEY_SPACE:
            angle = 0.0
            angle_2 = 0.0
        if key == glfw.KEY_S:
            switch = not switch


if __name__ == '__main__':
    main()
