import OpenGL.GLUT as glu
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random


# Global Variables
window_width = 800
window_height = 600
shooter_x = window_width // 2
shooter_radius = 20
projectiles = []
falling_circles = []
score = 0
missed_circles = 0
missed_fire = 0
game_over = False
paused = False
shooter_color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))  # Initial random color
playPauseColor = (255 / 255.0, 165 / 255.0, 0 / 255.0)  # Orange
closeColor = (255 / 255.0, 0 / 255.0, 0 / 255.0)  # Red
resetColor = (0 / 255.0, 255 / 255.0, 255 / 255.0)  # Cyan
color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))

# Midpoint Circle Drawing Algorithm
def circledrawingAlgo(x_center, y_center, radius):
    x = 0
    y = radius
    p = 1 - radius
    
    while x <= y:
        plot_circle_points(x_center, y_center, x, y)
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

def plot_circle_points(x_center, y_center, x, y):
    glBegin(GL_POINTS)
    glVertex2f(x_center + x, y_center + y)
    glVertex2f(x_center - x, y_center + y)
    glVertex2f(x_center + x, y_center - y)
    glVertex2f(x_center - x, y_center - y)
    glVertex2f(x_center + y, y_center + x)
    glVertex2f(x_center - y, y_center + x)
    glVertex2f(x_center + y, y_center - x)
    glVertex2f(x_center - y, y_center - x)
    glEnd()


def drawPoints(x, y, zone):
    if zone == 0:
        glVertex2f(x, y)
    elif zone == 1:
        glVertex2f(y, x)
    elif zone == 2:
        glVertex2f(-y, x)
    elif zone == 3:
        glVertex2f(-x, y)
    elif zone == 4:
        glVertex2f(-x, -y)
    elif zone == 5:
        glVertex2f(-y, -x)
    elif zone == 6:
        glVertex2f(y, -x)
    elif zone == 7:
        glVertex2f(x, -y)


def midpointLine(x1, y1, x2, y2, zone):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x = x1
    y = y1
    drawPoints(x, y, zone)
    while x < x2:
        if d < 0:
            d = d + dE
            x = x + 1
        else:
            d = d + dNE
            x = x + 1
            y = y + 1
        drawPoints(x, y, zone)
    # return x1, y1, x2, y2


def convertToZoneZero(x1, y1, x2, y2, zone):
    if zone == 0:
        return x1, y1, x2, y2
    elif zone == 1:
        return y1, x1, y2, x2
    elif zone == 2:
        return y1, -x1, y2, -x2
    elif zone == 3:
        return -x1, y1, -x2, y2
    elif zone == 4:
        return -x1, -y1, -x2, -y2
    elif zone == 5:
        return -y1, -x1, -y2, -x2
    elif zone == 6:
        return -y1, x1, -y2, x2
    elif zone == 7:
        return x1, -y1, x2, -y2


def getZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx > 0:
            if dy >= 0:
                return 0
            else:
                return 7
        else:
            if dy >= 0:
                return 3
            else:
                return 4
    else:
        if dx > 0:
            if dy >= 0:
                return 1
            else:
                return 6
        else:
            if dy >= 0:
                return 2
            else:
                return 5


def linedrawingalgo(x1, y1, x2, y2):
    zone = getZone(x1, y1, x2, y2)

    x1, y1, x2, y2 = convertToZoneZero(x1, y1, x2, y2, zone)
    midpointLine(x1, y1, x2, y2, zone)


def draw_left_arrow():
    glColor3f(
        resetColor[0],
        resetColor[1],
        resetColor[2],
    )
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(55, 575, 75, 590)
    linedrawingalgo(55, 575, 90, 575)
    linedrawingalgo(55, 575, 75, 560)
    glEnd()


def draw_pause_icon():
    glColor3f(
        playPauseColor[0],
        playPauseColor[1],
        playPauseColor[2],
    )
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(388, 555, 388, 595)
    linedrawingalgo(412, 555, 412, 595)
    glEnd()    

def draw_play_icon():
    glColor3f(
        playPauseColor[0],
        playPauseColor[1],
        playPauseColor[2],
    )
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(380, 555, 420, 575)
    linedrawingalgo(380, 595, 420, 575)
    linedrawingalgo(380, 555, 380, 595)
    glEnd()

def draw_cross():
    glColor3f(
        closeColor[0],
        closeColor[1],
        closeColor[2]
    )
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(705, 555, 745, 595)
    linedrawingalgo(745, 555, 705, 595)
    glEnd()


def animate():
    global projectiles, falling_circles, game_over, shooter_color

    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1.0, 0.0, 0.0) 
    draw_left_arrow()
    if not paused:
        draw_pause_icon()
    else: 
        draw_play_icon()
    draw_cross()
    
    if not game_over:
        # Draw Shooter
        glColor3f(*shooter_color)
        circledrawingAlgo(shooter_x, shooter_radius + 10, shooter_radius)

        # Draw Projectiles
        glColor3f(0.0, 0.0, 1.0)
        for proj in projectiles:
            circledrawingAlgo(proj[0], proj[1], 5)

        # Draw Falling Circles
        glColor3f(random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))
        for circle in falling_circles:
            circledrawingAlgo(circle[0], circle[1], 15)

        # animate Score
        glColor3f(0.0, 1.0, 0.0)
        glRasterPos2f(10, window_height - 80)
        for ch in f'Score: {score}':
            glutBitmapCharacter(glu.GLUT_BITMAP_HELVETICA_18, ord(ch))

        # Animate Misses
        glRasterPos2f(10, window_height - 100)
        for ch in f'Misses: {missed_circles}':
            glutBitmapCharacter(glu.GLUT_BITMAP_HELVETICA_18, ord(ch))

        glRasterPos2f(10, window_height - 120)
        for ch in f'Misfire: {missed_fire}':
            glutBitmapCharacter(glu.GLUT_BITMAP_HELVETICA_18, ord(ch))

    else:
        # Game Over Screen
        glColor3f(1.0, 0.0, 0.0)
        circledrawingAlgo(shooter_x, shooter_radius + 10, shooter_radius)
        glColor3f(0.0, 1.0, 0.0)
        glRasterPos2f(window_width // 2 - 50, window_height // 2)
        
        for ch in 'Game Over':
            glutBitmapCharacter(glu.GLUT_BITMAP_HELVETICA_18, ord(ch))
        glRasterPos2f(window_width // 2 - 70, window_height // 2 - 20)
        for ch in f'Final Score: {score}':
            glutBitmapCharacter(glu.GLUT_BITMAP_HELVETICA_18, ord(ch))

    glutSwapBuffers()

# Timer Function
def timer(value):
    global projectiles, falling_circles, score, missed_circles, game_over, shooter_radius, shooter_x, shooter_color, missed_fire, projectiles_to_remove

    if not game_over and not paused:
        # Update Projectiles
        projectiles = [(x, y + 5) for (x, y) in projectiles if y < window_height]

        # Update Falling Circles
        new_falling_circles = []
        for circle in falling_circles:
            if circle[1] - 15 > 0:
                circle = (circle[0], circle[1] - 1)
                new_falling_circles.append(circle)
            else:
                missed_circles += 1

        falling_circles = new_falling_circles

                
        for proj in projectiles:
            # Check if the projectile is out of bounds
            if proj[1] >= window_height:
                missed_fire += 1
                projectiles.remove(proj)
            if missed_fire == 3:
                game_over = True
                break 
            
            # Check for hits
            for circle in falling_circles[:]:
                if math.sqrt((proj[0] - circle[0]) ** 2 + (proj[1] - circle[1]) ** 2) < 20:
                    projectiles.remove(proj)
                    falling_circles.remove(circle)
                    score += 1
                    break
        
        # Remove projectiles that missed or hit

        # Check if any falling circle touches the shooter
        for circle in falling_circles:
            if math.sqrt((circle[0] - shooter_x) ** 2 + (circle[1] - (shooter_radius + 10)) ** 2) < (shooter_radius + 15):
                game_over = True  
                break
            if missed_circles == 3:
                game_over = True  
                break

        # Spawn New Circle
        if random.random() < 0.02:
            falling_circles.append((random.randint(20, window_width - 20), window_height - 20))

    glutPostRedisplay()
    glutTimerFunc(25, timer, 0)


# Keyboard Function
def keyboard(key, x, y):
    global shooter_x, projectiles, misfires, game_over, paused

    if key == b'a' and shooter_x - shooter_radius > 0:
        shooter_x -= 20
    elif key == b'd' and shooter_x + shooter_radius < window_width:
        shooter_x += 20
    elif key == b' ' and not game_over and not paused:
        projectiles.append((shooter_x, shooter_radius + 10))
        

# Restart Game
def restart_game():
    global projectiles, falling_circles, score, missed_circles, game_over, missed_fire
    projectiles = []
    falling_circles = []
    score = 0
    missed_circles = 0
    missed_fire = 0
    game_over = False

def mouse_click(button, state, x, y):
    global paused, game_over
    if state == GLUT_DOWN:
        y = 600 - y 
        if 50 <= x <= 100 and 550 <= y <= 600:
            restart_game()
            print("Starting Over")
        elif 375 <= x <= 425 and 550 <= y <= 600:
            paused = not paused
        elif 700 <= x <= 750 and 550 <= y <= 600:
            game_over = True
            print(f"Goodbye. Final Score: {score}")
            glutLeaveMainLoop()
            exit(0)


# Initialize OpenGL
def init_gl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b'Shoot The Circles!')
glutDisplayFunc(animate)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse_click)
glutTimerFunc(0, timer, 0)
init_gl()
glutMainLoop()
