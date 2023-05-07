import glfw
import numpy as np
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


width, height = 720, 640
points = []
points_rast = []

raster_buffer = np.zeros((height, width, 3), dtype=np.uint8)


def bresenham_line(p0, p1):
    x0, y0 = p0.x, p0.y
    x1, y1 = p1.x, p1.y
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy
    x = x0
    y = y0
    while True:
        yield x, y
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def scanline_fill(start_x, start_y, fill_color):
    stack = [(start_x, start_y)]
    old_color = [0, 0, 0]

    while stack:
        x, y = stack.pop()

        while x >= 0 and np.array_equal(raster_buffer[x, y], old_color):
            x -= 1

        x += 1
        left = x

        while x < raster_buffer.shape[0] and np.array_equal(raster_buffer[x, y], old_color):
            raster_buffer[x, y] = fill_color
            x += 1

        right = x - 1

        if y > 0:
            i = left
            while i <= right:
                if np.array_equal(raster_buffer[i, y - 1], old_color):
                    while i < right and np.array_equal(raster_buffer[i, y - 1], old_color):
                        i += 1
                    if np.array_equal(raster_buffer[i, y - 1], old_color):
                        stack.append((i, y - 1))
                    else:
                        stack.append((i - 1, y - 1))
                i += 1

        if y < raster_buffer.shape[1] - 1:
            i = left
            while i <= right:
                if np.array_equal(raster_buffer[i, y + 1], old_color):
                    while i < right and np.array_equal(raster_buffer[i, y + 1], old_color):
                        i += 1
                    if np.array_equal(raster_buffer[i, y + 1], old_color):
                        stack.append((i, y + 1))
                    else:
                        stack.append((i - 1, y + 1))
                i += 1


def display(window):
    global width, height, raster_buffer, points_rast

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glClearColor(1.0, 1.0, 1.0, 1.0)

    new_width, new_height = glfw.get_framebuffer_size(window)
    if new_width != width or new_height != height:
        width, height = new_width, new_height
        raster_buffer = np.zeros((height, width, 3), dtype=np.uint8)
        points_rast = []

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glDrawPixels(width, height, GL_RGB, GL_UNSIGNED_BYTE, raster_buffer)

    glfw.swap_buffers(window)

    glfw.poll_events()


def main():

    if not glfw.init():
        return
    window = glfw.create_window(width, height, "Lab4", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_callback)

    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(window):
        display(window)

    glfw.terminate()


def mouse_callback(window, button, action, mods):
    if action == glfw.PRESS:
        x_pos, y_pos = glfw.get_cursor_pos(window)
        x_pos = (x_pos - width / 2) * 2 / width
        y_pos = (height / 2 - y_pos) * 2 / height

        if button == glfw.MOUSE_BUTTON_LEFT:
            points.append(Point(x_pos, y_pos))

            x_pos, y_pos = glfw.get_cursor_pos(window)
            points_rast.append(Point(height - y_pos, x_pos))
            if len(points_rast) > 1:
                for point in bresenham_line(points_rast[-1], points_rast[-2]):
                    raster_buffer[int(point[0])][int(point[1])][0] = 255

        if button == glfw.MOUSE_BUTTON_RIGHT:
          
            x_pos, y_pos = glfw.get_cursor_pos(window)
            points.append(Point(height - y_pos, x_pos))
            if len(points_rast) > 2:
                for point in bresenham_line(points_rast[0], points_rast[-1]):
                    raster_buffer[int(point[0])][int(point[1])][0] = 255


def key_callback(window, key, scancode, action, mods):
    global points, points_rast
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            points = []
            points_rast = []
        if key == glfw.KEY_R:
            scanline_fill(int(points[-1].x), int(points[-1].y), [255, 255, 255])


if __name__ == '__main__':
    main()
