import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

WIDTH = 500
HEIGHT = 750
basketColor = (145 / 255.0, 145 / 255.0, 255 / 255.0)  # Violet
playPauseColor = (255 / 255.0, 165 / 255.0, 0 / 255.0)  # Orange
closeColor = (255 / 255.0, 0 / 255.0, 0 / 255.0)  # Red
resetColor = (0 / 255.0, 255 / 255.0, 255 / 255.0)  # Cyan


class ObjectBox:
    def __init__(self, x, y, w, h, s):
        self.x, self.y, self.width, self.height, self.speed = x, y, w, h, s
        self.color = (
            random.uniform(0.5, 1),
            random.uniform(0.5, 1),
            random.uniform(0.5, 1),
        )

    def moveRight(self):
        if self.x + self.width + 10 + self.speed < WIDTH:
            self.x += 2 * self.speed

    def moveLeft(self):
        if self.x - 10 - self.speed > 0:
            self.x -= self.speed

    def moveDown(self):
        self.y -= self.speed

    def collidesWith(self, obj):
        return (self.x < obj.x + obj.width and  # x_min_1 < x_max_2
                self.x + self.width > obj.x and  # x_max_1 > m_min_2
                self.y < obj.y + obj.height and  # y_min_1 < y_max_2
                self.y + self.height > obj.y)  # y_max_1 > y_min_2

    def checkClick(self, x, y):


        return (self.x < x < self.x + self.width and
                self.y > y > self.y - self.height
                )


basket = ObjectBox(200, 10, 100, 30, 20)
diamond = ObjectBox(random.randint(10, 470), 650, 20, 50, 0.2)
close = ObjectBox(440, 740, 50, 70, 0)
pause = ObjectBox(225, 740, 50, 70, 0)
reset = ObjectBox(10, 740, 50, 70, 0)
collide = True
resume = True
points = 0
end = False
storeBasketSpeed = 0
storeDiamondSpeed = 0


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


def drawMidpointLine(x1, y1, x2, y2, zone):
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


def drawLine(x1, y1, x2, y2):
    zone = getZone(x1, y1, x2, y2)

    x1, y1, x2, y2 = convertToZoneZero(x1, y1, x2, y2, zone)
    drawMidpointLine(x1, y1, x2, y2, zone)


def drawBasket(obj):
    if end:
        glColor3f(closeColor[0], closeColor[1], closeColor[2])
    else:
        glColor3f(basketColor[0], basketColor[1], basketColor[2])
    glPointSize(2)
    glBegin(GL_POINTS)

    drawLine(obj.x, obj.y + obj.height, obj.x + obj.width, obj.y + obj.height)  # --
    drawLine(obj.x, obj.y + obj.height, obj.x + 10, obj.y)  # \
    drawLine(obj.x + 10, obj.y, obj.x + obj.width - 10, obj.y)  # _
    drawLine(obj.x + obj.width - 10, obj.y, obj.x + obj.width, obj.y + obj.height)  # /
    glEnd()


def drawDiamond(obj):
    glColor3f(
        obj.color[0],
        obj.color[1],
        obj.color[2]
    )
    glPointSize(2)
    glBegin(GL_POINTS)

    drawLine(obj.x + int(obj.width / 2), obj.y,
             obj.x, obj.y - int(obj.height / 2))
    drawLine(obj.x, obj.y - int(obj.height / 2),
             obj.x + int(obj.width / 2), obj.y - obj.height)
    drawLine(obj.x + int(obj.width / 2), obj.y - obj.height,
             obj.x + obj.width, obj.y - int(obj.height / 2))
    drawLine(obj.x + obj.width, obj.y - int(obj.height / 2),
             obj.x + int(obj.width / 2), obj.y)
    glEnd()


def drawCloseButton(obj):
    glColor3f(
        closeColor[0],
        closeColor[1],
        closeColor[2]
    )
    glPointSize(2)
    glBegin(GL_POINTS)

    drawLine(obj.x, obj.y,
             obj.x + obj.width, obj.y - obj.height)
    drawLine(obj.x, obj.y - obj.height,
             obj.x + obj.width, obj.y)

    glEnd()


def drawPauseButton(obj):
    glColor3f(
        playPauseColor[0],
        playPauseColor[1],
        playPauseColor[2],
    )
    glPointSize(2)
    glBegin(GL_POINTS)

    drawLine(obj.x + 10, obj.y,
             obj.x + 10, obj.y - obj.height)
    drawLine(obj.x + 40, obj.y,
             obj.x + 40, obj.y - obj.height)

    glEnd()


def drawPlayButton(obj):
    glColor3f(
        playPauseColor[0],
        playPauseColor[1],
        playPauseColor[2],
    )
    glPointSize(2)
    glBegin(GL_POINTS)

    drawLine(obj.x + obj.width, obj.y - int(obj.height / 2),
             obj.x + int(obj.width / 2), obj.y - int(obj.height / 4))
    drawLine(obj.x + obj.width, obj.y - int(obj.height / 2),
             obj.x + int(obj.width / 2), obj.y - 3 * int(obj.height / 4))
    drawLine(obj.x + int(obj.width / 2), obj.y - int(obj.height / 4),
             obj.x + int(obj.width / 2), obj.y - 3 * int(obj.height / 4))

    glEnd()


def drawResetButton(obj):
    glColor3f(
        resetColor[0],
        resetColor[1],
        resetColor[2],
    )
    glPointSize(2)
    glBegin(GL_POINTS)

    drawLine(obj.x, obj.y - int(obj.height / 2),
             obj.x + obj.width, obj.y - int(obj.height / 2))
    drawLine(obj.x, obj.y - int(obj.height / 2),
             obj.x + int(obj.width / 2), obj.y - int(obj.height / 4))
    drawLine(obj.x, obj.y - int(obj.height / 2),
             obj.x + int(obj.width / 2), obj.y - 3 * int(obj.height / 4))
    glEnd()


def collision():
    global collide, diamond, resume, end, points

    if basket.collidesWith(diamond):
        points += 1
        # if diamond.speed < 1:
        newSpeed = min(1, diamond.speed + 0.1)
        diamond = ObjectBox(random.randint(10, 470), 650, 20, 50, newSpeed)
        print("Score: ", points)
    else:
        if diamond.y < 10:
            collide = False
            if not end:
                print("Game Over! Score: ", points)
            end = True


def keyboardListener(key, x, y):
    glutPostRedisplay()


def specialKeyListener(key, x, y):
    if resume and collide:
        if key == GLUT_KEY_LEFT:
            basket.moveLeft()

        if key == GLUT_KEY_RIGHT:
            basket.moveRight()

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global diamond, basket, resume, end, points, collide
    y = HEIGHT - y
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if pause.checkClick(x, y):
                if resume:
                    resume = False
                else:
                    resume = True
            if reset.checkClick(x, y):
                end = False
                points = 0
                collide = True
                basket = ObjectBox(200, 10, 100, 30, 30)
                diamond = ObjectBox(random.randint(10, 470), 650, 20, 50, 0.2)

            if close.checkClick(x, y):
                print("Goodbye! Score: ", points)
                glutLeaveMainLoop()

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            pass

    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.1, 0.1, 0.2, 0)

    drawBasket(basket)
    drawDiamond(diamond)
    if resume:
        drawPauseButton(pause)
    else:
        drawPlayButton(pause)
    drawCloseButton(close)

    drawResetButton(reset)
    glutSwapBuffers()


def animate():

    if resume:
        if diamond.y - diamond.height - basket.height + 10 < 30:
            collision()
        diamond.moveDown()
        glutPostRedisplay()


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)


glutInit()
glutInitWindowSize(WIDTH, HEIGHT)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Catch the Diamond")
init()
glutDisplayFunc(display)  
glutIdleFunc(animate)  
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()  
