import math
import logging
import glfw
import OpenGL.GL as gl

PLOTTING_SEGMENTS = 1
SEGMENTS_PLOTTED = 2
CLIPPING = 3
SIZE = 1000
ZONE_PADDING_COEFFICIENT = 0.2
ACCURACY = math.sqrt(2)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

mouse = Point(0, 0)
stage = PLOTTING_SEGMENTS
sizeX = 0
sizeY = 0
segments = []
points = []
zoneLeft = 0
zoneRight = 0
zoneCeil = 0
zoneFloor = 0

def clipping():
    tempSegments = make_segments()
    for segment in tempSegments:
        midpoint_clipping(segment, 1)

def midpoint_clipping(segment, count):
    global segments
    firstCode = get_code(segment[0])
    secondCode = get_code(segment[1])
    if firstCode + secondCode == 0:
        segments.append(segment)
        return
    if firstCode & secondCode != 0:
        return
    if count > 2:
        segments.append(segment)
        return
    firstPoint = segment[0]
    if secondCode == 0:
        segment[1], segment[0] = firstPoint, segment[1]
        count += 1
        midpoint_clipping(segment, count)
        return
    while True:
        if math.hypot(segment[0].x - segment[1].x, segment[0].y - segment[1].y) <= ACCURACY:
            segment[1], segment[0] = firstPoint, segment[1]
            count += 1
            midpoint_clipping(segment, count)
            return
        midpoint = Point((segment[0].x + segment[1].x) / 2, (segment[0].y + segment[1].y) / 2)
        memoizedPoint = segment[0]
        segment[0] = midpoint
        firstCode = get_code(segment[0])
        if firstCode & secondCode != 0:
            segment[0], segment[1] = memoizedPoint, midpoint
            break

def get_code(p):
    code = 0
    if p.y > zoneFloor:
        code += 1
    code *= 2
    if p.x > zoneRight:
        code += 1
    code *= 2
    if p.y < zoneCeil:
        code += 1
    code *= 2
    if p.x < zoneLeft:
        code += 1
    return code

def make_segments():
    temp = []
    for i in range(len(points)//2):
        temp.append([points[2*i], points[2*i+1]])
    return temp

def drawZone():
    global zoneLeft, zoneRight, zoneCeil, zoneFloor
    zoneLeft = sizeX * ZONE_PADDING_COEFFICIENT
    zoneRight = sizeX * (1 - ZONE_PADDING_COEFFICIENT)
    zoneFloor = sizeY * (1 - ZONE_PADDING_COEFFICIENT)
    zoneCeil = sizeY * ZONE_PADDING_COEFFICIENT

    gl.glBegin(gl.GL_LINE_LOOP)
    gl.glVertex2d(zoneLeft, zoneFloor)
    gl.glVertex2d(zoneLeft, zoneCeil)
    gl.glVertex2d(zoneRight, zoneCeil)
    gl.glVertex2d(zoneRight, zoneFloor)
    gl.glEnd()

def drawSegments():
    global stage, points, segments

    if stage == PLOTTING_SEGMENTS or stage == SEGMENTS_PLOTTED:
        gl.glBegin(gl.GL_LINES)
        for p in points:
            gl.glVertex2d(p.x, p.y)
        if stage == PLOTTING_SEGMENTS:
            gl.glVertex2d(mouse.x, mouse.y)
        gl.glEnd()
    else:
        gl.glBegin(gl.GL_LINES)
        for segment in segments:
            gl.glVertex2d(segment[0].x, segment[0].y)
            gl.glVertex2d(segment[1].x, segment[1].y)
        gl.glEnd()


