import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import serial
import math

verticies = (
    (2, -0.5, -2),
    (2, 0.5, -2),
    (-2, 0.5, -2),
    (-2, -0.5, -2),
    (2, -0.5, 2),
    (2, 0.5, 2),
    (-2, -0.5, 2),
    (-2, 0.5, 2)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

fXg = 0
fYg = 0
fZg = 0

def angle(AcX, AcY, AcZ) -> list:
    RADIAN_TO_DEGREES = 180/3.14139
    val_y = math.atan(AcX/math.sqrt(pow(AcY, 2) + pow(AcZ, 2))) * RADIAN_TO_DEGREES
    val_x = math.atan(AcY/math.sqrt(pow(AcX, 2) + pow(AcZ, 2))) * RADIAN_TO_DEGREES
    return [val_x, val_y]

def roll_pitch(Xg, Yg, Zg) -> list:
    global fXg, fYg, fZg
    alpha = 0.5

    # Low Pass Filter
    fXg = Xg * alpha + (fXg * (1.0 - alpha))
    fYg = Yg * alpha + (fYg * (1.0 - alpha))
    fZg = Zg * alpha + (fZg * (1.0 - alpha))

    # Roll & Pitch Equations
    roll = (math.atan2(-fYg, fZg) * 180.0) / math.pi
    # pitch = (math.atan2(-fXg, fZg) * 180.0) / math.pi
    pitch = (math.atan2(fXg, math.sqrt(fYg * fYg + fZg * fZg)) * 180.0) / math.pi

    return [roll, pitch]


def Cube():
    glBegin(GL_LINES)
    # print("Cube")
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -15)

    x = 0
    pre_x = 0
    post_x = 0

    y = 0
    pre_y = 0
    post_y = 0

    ser = serial.Serial('COM15', 11520)
    Angle_data = []
    Acc_data = []
    print('start...')

    while True:
        for event in pygame.event.get():
            print('event : ' + str(event))
            # < Event(4 - MouseMotion{'pos': (460, 433), 'rel': (32, -24), 'buttons': (0, 0, 0), 'window': None}) >
            event_str = str(event)
            print(event.type)
            if event.type == 4:
                x01 = event_str.split('rel')
                # x02 = x01[1].split('(')
                # print(x02)
                # x03 = x02[1].split(',')
                # x = int(x03[0])
                #
                # glRotatef(x*0.1, 0, 2, 0)

            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(y, 0, 0, 2)
        glRotatef(x, 2, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        # pygame.time.wait(10)

        glRotatef(-x, 2, 0, 0)
        glRotatef(-y, 0, 0, 2)

        raw_data = ser.read_until(b'\r')
        str_data = raw_data.decode('utf-8')
        str_data = str_data[0:-1]
        list_data = str_data.split(' ')
        Acc_data.append(list_data)
        # print(list_data)

        # andata = angle(float(list_data[0]), float(list_data[1]), float(list_data[2]))
        andata = roll_pitch(float(list_data[0]), float(list_data[1]), float(list_data[2]))
        # print(andata)
        # print(andata)
        # pre_x =  andata[0]
        # x = post_x - pre_x
        # post_x = pre_x
        x = andata[0]

        # pre_y = andata[1]
        # y = post_y - pre_y
        # post_y = pre_y
        y = andata[1]

        # print(list_data)
        # print(angle(float(list_data[0]), float(list_data[1]), float(list_data[2])))

main()



# ser = serial.Serial('COM15', 11520)
# byte_data = []
# Acc_data = []
# print('start...')
# while True:
#     raw_data = ser.read_until(b'\r')
#     str_data = raw_data.decode('utf-8')
#     str_data = str_data[0:-1]
#     list_data = str_data.split(' ')
#     Acc_data.append(list_data)
#     # print(list_data)
#     print(angle(float(list_data[0]), float(list_data[1]), float(list_data[2])))


