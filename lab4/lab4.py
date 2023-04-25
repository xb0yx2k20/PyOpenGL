import glfw
from OpenGL.GL import *
import math
deltax = 0      # Изначальный угол поворота квадрата
deltay = 0      # Изначальный угол поворота квадрата
angle = 0.0      # Изначальный угол поворота квадрата
posx = 0.0       # Изначальная координата по оси X
posy = 0.0       # Изначальная координата по оси Y
size = 0.0       # Изначальный размер квадрата
chpos = 0.0      # Изначальная величина изменения положения квадрата при нажатии на клавиши
FRAME_WIDE = 100
FRAME_HIGH = 100
pFrame = bytearray(FRAME_WIDE * FRAME_HIGH * 3);
prime= (20,20,30,31,35,30,40,25)
def SetPixel(x,y,z):
    if (x < 0 or x >= FRAME_WIDE or y < 0 or y >= FRAME_HIGH):
        return;
    index = int(3 * (y * FRAME_WIDE + x));
    pFrame[index] = z;
    pFrame[index+1] = z;
    pFrame[index+2] = z;
def getPixel(x,y):
    if (x < 0 or x >= FRAME_WIDE or y < 0 or y >= FRAME_HIGH):
        return;
    index = int(3 * (y * FRAME_WIDE + x));
    return  pFrame[index];
def Bresenham(x1,y1,x2,y2):
    de=abs((y2-y1)/(x2-x1))
    e=-1/2
    x=x1
    y=y1
    p = lambda x:x
    q = lambda x:x
    print(x1,y1,x2,y2)
    if (x1<x2):
        p=lambda x:x+1
    else:
        p=lambda x:x-1
    if (y1<y2):
        q=lambda y:y+1
    else:
        q=lambda y:y-1
    for j in range(x,abs(FRAME_WIDE)):
        SetPixel(j,y,abs(getPixel(j,y)-255))

    SetPixel(x,y,0)
    for i in range(abs(x2-x1)):
            e+=de
            x=p(x)
            if(e>=0):
                y=q(y)
                
                for j in range(x,abs(FRAME_WIDE)):
                    SetPixel(j,y,abs(getPixel(j,y)-255))
                SetPixel(x,y,0)
                e-=1
            else :
                SetPixel(x,y,0)
    
            
def display(window):
    global pFrame
    glClear(GL_COLOR_BUFFER_BIT);
    glRasterPos2i(0, 0);
    
    glDrawPixels(FRAME_WIDE, FRAME_HIGH, GL_RGB,GL_UNSIGNED_BYTE, pFrame);
    glfw.swap_buffers(window)    # Переключаем буферы для отображения изображения на экране
    glfw.poll_events()           # Обрабатываем все накопившиеся события

def key_callback(window, key, scancode, action,mods):
    global deltax
    global deltay
    global angle
    global chpos
    
    if action == glfw.PRESS:     # Если клавиша нажата
        if key == glfw.KEY_RIGHT:
            deltax += 1
        if key == 263:          # glfw.KEY_LEFT
            deltax -= 1          # Поворачиваем квадрат против import glfw
        if key == glfw.KEY_UP:
            deltay += 1
        if key == glfw.KEY_DOWN:          # glfw.KEY_LEFT
            deltay -= 1          # Поворачиваем квадрат против import glfw
    SetPixel(deltax,deltay)

def scroll_callback(window, xoffset, yoffset):
    global size
    if (xoffset > 0):
        size -= yoffset/10
    else:
        size += yoffset/10
def main():
    global T;
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Lab1", None, None)
    if not window:
        glfw.terminate()
        return
    for i in range(FRAME_WIDE * FRAME_HIGH * 3):
        pFrame[i]=255;
    
    for i  in range(int(len(prime)/2) - 1 ):
       Bresenham(prime[i*2],prime[i*2+1],prime[i*2+2],prime[i*2+3])
    Bresenham(prime[6],prime[7],prime[0],prime[1])
        
  
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()
main()
