from turtle import *
from freegames import floor, vector

mapTurtle = Turtle(visible=False)
tankTurtle = Turtle(visible=False)
"""
0 - no tile
1 - road
2 - river
3 - forest
4 - industructible block
5 - destructible block
"""
tiles = [
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 4,
    4, 1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 4,
    4, 1, 3, 3, 3, 3, 3, 3, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 4,
    4, 1, 3, 3, 3, 3, 3, 3, 1, 1, 5, 1, 1, 1, 1, 1, 1, 5, 1, 4,
    4, 1, 3, 3, 3, 3, 3, 3, 1, 1, 5, 1, 1, 1, 1, 1, 1, 5, 1, 4,
    4, 1, 3, 3, 3, 3, 3, 3, 1, 1, 5, 1, 1, 1, 1, 1, 1, 5, 1, 4,
    4, 1, 3, 3, 3, 3, 3, 3, 1, 1, 5, 1, 1, 1, 1, 1, 1, 5, 1, 4,
    4, 1, 3, 3, 3, 3, 3, 3, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
]


def drawSquare(turtleObject, x, y, size=20, squareColor=None, circuitColor=None):
    """Draw drawSquare using path at (x, y)."""
    if circuitColor:
        turtleObject.color(circuitColor)
    turtleObject.fillcolor(squareColor)
    turtleObject.up()
    turtleObject.goto(x, y)
    turtleObject.down()
    turtleObject.begin_fill()
    for count in range(4):
        turtleObject.forward(size)
        turtleObject.left(90)
    turtleObject.end_fill()


def drawBoard():
    """Draw map using path."""
    bgcolor('black')
    for index in range(len(tiles)):
        tile = tiles[index]
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            tileColor = "light goldenrod" if tile == 1 else "navy" if tile == 2 else "forest green" if tile == 3 else "snow2" if tile == 4 else "dark orange"
            drawSquare(mapTurtle, x, y, squareColor=tileColor)


def offset(point):
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


tankCentralization = 2  # minimal shift of tank to make tank stay in the center of the title


def valid(point):
    index = offset(point)
    if tiles[index] in [0, 2, 4]:
        return False
    index = offset(point + 19 - tankCentralization)
    if tiles[index] in [0, 2, 4]:
        return False
    return point.x % 20 == tankCentralization or point.y % 20 == tankCentralization


class Tank:
    def __init__(self, x, y, tankColor, controls, stoppingControl):
        self.position = vector(x, y)
        self.speed = vector(0, 0)
        self.direction = 0  # 0 - forward, 90 - right, 180 - backward, 270 - left
        self.tankColor = tankColor
        self.controls = controls
        self.stoppingControl = stoppingControl
        self.setControls()
        self.keysPressed = {key: False for key in controls}

    def change(self, tankSpeedDirection, angle=None):
        offsets = {
            90: vector(5, 0),  # prawo
            180: vector(0, -5),  # dół
            270: vector(-5, 0),  # lewo
            0: vector(0, 5)  # góra
        }
        if angle in offsets and valid(self.position + offsets[angle]):
            self.speed = tankSpeedDirection
            self.direction = angle
            return 0
        # stop tank
        if tankSpeedDirection.x == 0 and tankSpeedDirection.y == 0:
            self.speed = tankSpeedDirection
            return 1
        # if tank was stopped before then he can turn in any direction
        if self.speed.x == 0 and self.speed.y == 0 and angle is not None:
            self.direction = angle
            return 2
        # if tank move in wrong direction, where he can't go
        return -1

    def move(self):
        if valid(self.position + self.speed):
            self.position.move(self.speed)
        self.drawTank()

    def drawTank(self):
        x = self.position.x
        y = self.position.y
        angle = self.direction
        """Draw tracks."""
        trackOffsets = {
            0: [(0, 0), (0, 4), (0, 8), (0, 12), (12, 0), (12, 4), (12, 8), (12, 12)],
            90: [(0, 0), (4, 0), (8, 0), (12, 0), (0, 12), (4, 12), (8, 12), (12, 12)],
            180: [(0, 0), (0, 4), (0, 8), (0, 12), (12, 0), (12, 4), (12, 8), (12, 12)],
            270: [(0, 0), (4, 0), (8, 0), (12, 0), (0, 12), (4, 12), (8, 12), (12, 12)]
        }
        for dx, dy in trackOffsets[angle]:
            drawSquare(tankTurtle, x + dx, y + dy, 4, self.tankColor)
        """Draw hull."""
        hullOffsets = {0: (4, 1), 90: (1, 4), 180: (4, 7), 270: (7, 4)}
        drawSquare(tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 8, self.tankColor)
        """Draw cannon."""
        cannonOffsets = {
            0: [(7, 9), (7, 11), (7, 13)],
            90: [(9, 7), (11, 7), (13, 7)],
            180: [(7, 5), (7, 3), (7, 1)],
            270: [(5, 7), (3, 7), (1, 7)]
        }
        for dx, dy in cannonOffsets[angle]:
            drawSquare(tankTurtle, x + dx, y + dy, 2, self.tankColor)
        drawSquare(tankTurtle, x, y, 3, "red")

    def setControls(self):
        onkey(lambda: self.change(vector(0, 0)), self.stoppingControl)
        for key, (tankSpeed, angle) in self.controls.items():
            onkey(lambda k=key: self.keyPressHandler(k), key)

    def keyPressHandler(self, key):
        self.keysPressed[key] = True

    def tankMovement(self):
        for key, (tankSpeed, angle) in self.controls.items():
            if self.keysPressed[key]:
                if self.change(tankSpeed, angle) != -1:
                    for k in self.keysPressed:
                        self.keysPressed[k] = False
                break


setup(420, 420, 500, 100)
hideturtle()
tracer(False)
listen()

controls1 = {
    "Up": (vector(0, 5), 0),
    "Down": (vector(0, -5), 180),
    "Left": (vector(-5, 0), 270),
    "Right": (vector(5, 0), 90)
}
controls2 = {
    "w": (vector(0, 5), 0),
    "s": (vector(0, -5), 180),
    "a": (vector(-5, 0), 270),
    "d": (vector(5, 0), 90)
}

tank = Tank(40+tankCentralization, 0+tankCentralization, "dark green", controls1, "Control_R")
enemyTank = Tank(-100+tankCentralization, 100+tankCentralization, "slate gray", controls2, "Shift_L")


def tanksCollision(tank1, tank2, collisionThreshold=20):
    distanceBetweenTanks = abs(tank1.position - tank2.position)
    return distanceBetweenTanks < collisionThreshold


def move():
    tankTurtle.clear()
    tank.tankMovement()
    enemyTank.tankMovement()
    tank.move()
    enemyTank.move()
    w = tanksCollision(tank, enemyTank)
    if w:
        print("Tanks collide. Everyone died")
        return
    update()
    ontimer(move, 100)


drawBoard()
move()
done()
