from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Variables for rain
num_raindrops = 300
raindrops = []
rain_angle = 0  # Angle for the rain direction
rain_speed = 0.2  # Speed of rain falling
background_color = [0.0, 0.0, 0.0]  # Initial background color (black)

def init_raindrops():
    global raindrops
    for i in range(num_raindrops):
        raindrops.append({'x': random.randint(-500, 1000), 'y': random.randint(500, 1000)})


def draw_raindrops():
    glColor3f(0.0, 0.0, 0.9)
    for drop in raindrops:
        draw_line(drop['x'], drop['y'], drop['x'] + rain_angle * 200, drop['y'] - 15)

def draw_points(x, y):
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_triangle(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def animate():
    global rain_angle, rain_speed
    for drop in raindrops:
        drop['y'] -= rain_speed  # Use rain_speed for consistent speed
        drop['x'] += rain_angle  # Adjust based on rain angle
        if drop['y'] < 365 or drop['x'] < -500 or drop['x'] > 1000:
            drop['y'] = random.randint(500, 1000)
            drop['x'] = random.randint(-500, 1000)
    glutPostRedisplay()

def showScreen():
    glClearColor(background_color[0], background_color[1], background_color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    
    # Drawing the house
    glColor3f(0.0, 0.0, 0.9)
    draw_line(100, 350, 100, 124)
    draw_line(100, 124, 450, 124)
    draw_line(450, 124, 450, 350) #upto this house
    draw_line(174, 187, 250, 187) #door start
    draw_line(212, 250, 212, 124)
    draw_line(174, 250, 250, 250)
    draw_line(174, 250, 175, 124)
    draw_line(250, 250, 250, 124)
    draw_points(186, 198) #upto this door
    draw_line(326, 300, 400, 300) #window start
    draw_line(326, 300, 326, 226)
    draw_line(326, 226, 400, 226)
    draw_line(400, 226, 400, 300)
    draw_line(326, 250, 400, 250)
    draw_line(326, 275, 400, 275)
    draw_line(350, 300, 350, 226)
    draw_line(375, 300, 375, 226) #upto this window
    draw_triangle(85, 350, 275, 450, 465, 350)
    
    # Drawing the rain
    draw_raindrops()
    
    glutSwapBuffers()

def update(value):
    glutPostRedisplay()
    glutTimerFunc(50, update, 0)

def keyPressed(key, x, y):
    global rain_angle, rain_speed
    if key == GLUT_KEY_LEFT:
        rain_angle -= 0.01  # Gradually bend the rain to the left
        rain_speed = 0.2
    elif key == GLUT_KEY_RIGHT:
        rain_angle += 0.01  # Gradually bend the rain to the right
        rain_speed = 0.2

def normalKeyPressed(key, x, y):
    global background_color
    if key == b'd':  # Gradually change to night
        background_color[0] = max(0.0, background_color[0] - 0.02)
        background_color[1] = max(0.0, background_color[1] - 0.02)
        background_color[2] = max(0.0, background_color[2] - 0.02)
    elif key == b'l':  # Gradually change to day
        background_color[0] = min(1.0, background_color[0] + 0.02)
        background_color[1] = min(1.0, background_color[1] + 0.02)
        background_color[2] = min(1.0, background_color[2] + 0.02)

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding of House With Rain")
glutDisplayFunc(showScreen)
glutTimerFunc(50, update, 0)
glutIdleFunc(animate)
glutSpecialFunc(keyPressed)
glutKeyboardFunc(normalKeyPressed)
init_raindrops()
glutMainLoop()
