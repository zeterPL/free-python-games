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
            tileColor = "yellow" if tile == 1 else "blue" if tile == 2 else "green" if tile == 3 else "gray" if tile == 4 else "orange"
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
    def __init__(self, x, y):
        self.position = vector(x, y)
        self.speed = vector(0, 0)
        self.direction = 0  # 0 - forward, 90 - right, 180 - backward, 270 - left

    def change(self, tankSpeedDirection, angle=None):
        if self.speed.x == 0 and self.speed.y == 0 and angle is not None:
            self.direction = angle  # if tank was stopped before then he can turn in any direction
            self.speed = tankSpeedDirection

        if tankSpeedDirection.x == 0 and tankSpeedDirection.y == 0:
            self.speed = tankSpeedDirection  # stop tank

        offsets = {
            90: vector(5, 0),  # prawo
            180: vector(0, -5),  # dół
            270: vector(-5, 0),  # lewo
            0: vector(0, 5)  # góra
        }
        if angle in offsets and valid(self.position + offsets[angle]):
            self.speed = tankSpeedDirection
            self.direction = angle

    def move(self):
        if valid(self.position + self.speed):
            self.position.move(self.speed)
        self.drawTank()

    def drawTank(self):
        x = self.position.x
        y = self.position.y
        angle = self.direction
        """Rysuje gasienice"""
        trackOffsets = {
            0: [(0, 0), (0, 4), (0, 8), (0, 12), (12, 0), (12, 4), (12, 8), (12, 12)],
            90: [(0, 0), (4, 0), (8, 0), (12, 0), (0, 12), (4, 12), (8, 12), (12, 12)],
            180: [(0, 0), (0, 4), (0, 8), (0, 12), (12, 0), (12, 4), (12, 8), (12, 12)],
            270: [(0, 0), (4, 0), (8, 0), (12, 0), (0, 12), (4, 12), (8, 12), (12, 12)]
        }
        for dx, dy in trackOffsets[angle]:
            drawSquare(tankTurtle, x + dx, y + dy, 4, "green")
        """Rysuje kadłub czołgu."""
        hullOffsets = {0: (4, 1), 90: (1, 4), 180: (4, 7), 270: (7, 4)}
        drawSquare(tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 8, "green")
        """Rysuje lufę czołgu."""
        cannonOffsets = {
            0: [(7, 9), (7, 11), (7, 13)],
            90: [(9, 7), (11, 7), (13, 7)],
            180: [(7, 5), (7, 3), (7, 1)],
            270: [(5, 7), (3, 7), (1, 7)]
        }
        for dx, dy in cannonOffsets[angle]:
            drawSquare(tankTurtle, x + dx, y + dy, 2, "green")


setup(420, 420, 500, 100)
hideturtle()
tracer(False)


tank = Tank(40+tankCentralization, 0+tankCentralization)

keysPressed = {"Up": False, "Down": False, "Left": False, "Right": False}
listen()
onkey(lambda: tank.change(vector(0, 0)), 'space')
onkeypress(lambda: keyPressHandler("Up"), "Up")
onkeypress(lambda: keyPressHandler("Down"), "Down")
onkeypress(lambda: keyPressHandler("Left"), "Left")
onkeypress(lambda: keyPressHandler("Right"), "Right")
onkeyrelease(lambda: keyReleaseHandler("Up"), "Up")
onkeyrelease(lambda: keyReleaseHandler("Down"), "Down")
onkeyrelease(lambda: keyReleaseHandler("Left"), "Left")
onkeyrelease(lambda: keyReleaseHandler("Right"), "Right")


def keyPressHandler(key):
    keysPressed[key] = True


def keyReleaseHandler(key):
    keysPressed[key] = False


def move():
    tankTurtle.clear()
    if keysPressed["Up"]:
        tank.change(vector(0, 5), 0)
    elif keysPressed["Down"]:
        tank.change(vector(0, -5), 180)
    elif keysPressed["Left"]:
        tank.change(vector(-5, 0), 270)
    elif keysPressed["Right"]:
        tank.change(vector(5, 0), 90)

    tank.move()
    update()
    ontimer(move, 100)


drawBoard()
move()
done()
