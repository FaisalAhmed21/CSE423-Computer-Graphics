from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500, 500
movement_speed = 0.1
point_size = 5
is_frozen = False

moving_points = []

class MovingPoint:
    def __init__(self, x, y, p, q, color):
        self.x = x
        self.y = y
        self.p = p
        self.q = q
        self.color = color
        self.is_blinking = False
        self.is_visible = True

def convert_to_gl_coordinates(x, y):
    global W_Width, W_Height
    gl_x = x - (W_Width / 2)
    gl_y = (W_Height / 2) - y
    return gl_x, gl_y

def draw_point(x, y, size, color):
    glPointSize(size)
    glBegin(GL_POINTS)
    glColor3f(*color)
    glVertex2f(x, y)
    glEnd()

def draw_axes():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(W_Width / 2, 0)
    glVertex2f(-W_Width / 2, 0)
    glVertex2f(0, W_Height / 2)
    glVertex2f(0, -W_Height / 2)
    
    # Draw box around the axes
    glVertex2f(W_Width / 2, W_Height / 2)
    glVertex2f(W_Width / 2, -W_Height / 2)
    
    glVertex2f(W_Width / 2, -W_Height / 2)
    glVertex2f(-W_Width / 2, -W_Height / 2)
    
    glVertex2f(-W_Width / 2, -W_Height / 2)
    glVertex2f(-W_Width / 2, W_Height / 2)
    
    glVertex2f(-W_Width / 2, W_Height / 2)
    glVertex2f(W_Width / 2, W_Height / 2)
    
    glEnd()

    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(0, 1.0, 0.0)
    glVertex2f(0, 0)
    glEnd()

def handle_keyboard_input(key, x, y):
    global point_size, is_frozen, movement_speed
    if key == b'w':
        point_size += 3
        print("Increased point size")
    elif key == b's':
        point_size -= 6
        print("Decreased point size")
    elif key == b' ':
        is_frozen = not is_frozen
        if is_frozen:
            print("Animation frozen")
        else:
            print("Animation resumed")
    glutPostRedisplay()

def handle_special_input(key, x, y):
    global movement_speed
    if key == GLUT_KEY_UP:
        movement_speed *= 2
        print("Speed doubled")
        for point in moving_points:
            point.p *= 2
            point.q *= 2
    elif key == GLUT_KEY_DOWN:
        movement_speed /= 2
        print("Speed halved")
        for point in moving_points:
            point.p /= 2
            point.q /= 2
    glutPostRedisplay()

def handle_mouse_input(button, state, x, y):
    global moving_points
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for point in moving_points:
            point.is_blinking = True
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        gl_x, gl_y = convert_to_gl_coordinates(x, y)
        p = random.choice([-1, 1]) * movement_speed
        q = random.choice([-1, 1]) * movement_speed
        color = [random.random() for i in range(3)]
        moving_points.append(MovingPoint(gl_x, gl_y, p, q, color))
    glutPostRedisplay()

def render_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    draw_axes()

    for point in moving_points:
        if point.is_blinking:
            point.is_visible = not point.is_visible
        if point.is_visible:
            draw_point(point.x, point.y, point_size, point.color)

    glutSwapBuffers()

def animate():
    if not is_frozen:
        for point in moving_points:
            point.x += point.p
            point.y += point.q
            if abs(point.x) > W_Width / 2:
                point.p = -point.p
            if abs(point.y) > W_Height / 2:
                point.q = -point.q
    glutPostRedisplay()

def initialize():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

window = glutCreateWindow(b"OpenGL moving ball in the box")
initialize()

glutDisplayFunc(render_scene)
glutIdleFunc(animate)
glutKeyboardFunc(handle_keyboard_input)
glutSpecialFunc(handle_special_input)
glutMouseFunc(handle_mouse_input)

glutMainLoop()
