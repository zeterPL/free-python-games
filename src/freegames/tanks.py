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


def square(turtleObject, x, y, size=20, squareColor=None, circuitColor=None):
    """Draw square using path at (x, y)."""
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


def world():
    """Draw map using path."""
    bgcolor('black')
    for index in range(len(tiles)):
        tile = tiles[index]
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            tileColor = "yellow" if tile == 1 else "blue" if tile == 2 else "green" if tile == 3 else "gray" if tile == 4 else "orange"
            square(mapTurtle, x, y, squareColor=tileColor)


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
        # Obrót o 0 stopni (czołg skierowany do przodu)
        if angle == 0:
            square(tankTurtle, x, y+4, 4, "green")     # left track
            square(tankTurtle, x, y+8, 4, "green")     # left track
            square(tankTurtle, x, y+12, 4, "green")    # left track
            square(tankTurtle, x+4, y+1, 8, "green")   # tank hull
            square(tankTurtle, x+7, y+9, 2, "green")   # tank canon
            square(tankTurtle, x+7, y+11, 2, "green")  # tank canon
            square(tankTurtle, x+7, y+13, 2, "green")  # tank canon
            square(tankTurtle, x+12, y, 4, "green")     # right track
            square(tankTurtle, x+12, y+4, 4, "green")   # right track
            square(tankTurtle, x+12, y+8, 4, "green")   # right track
            square(tankTurtle, x+12, y+12, 4, "green")  # right track
            square(tankTurtle, x, y, 4, "green")       # left track
        # Obrót o 90 stopni w prawo (czołg skierowany w prawo)
        elif angle == 90:
            square(tankTurtle, x+4, y, 4, "green")     # bottom track
            square(tankTurtle, x+8, y, 4, "green")     # bottom track
            square(tankTurtle, x+12, y, 4, "green")    # bottom track
            square(tankTurtle, x+1, y+4, 8, "green")   # tank hull
            square(tankTurtle, x+9, y+7, 2, "green")   # tank canon
            square(tankTurtle, x+11, y+7, 2, "green")  # tank canon
            square(tankTurtle, x+13, y+7, 2, "green")  # tank canon
            square(tankTurtle, x, y+12, 4, "green")     # top track
            square(tankTurtle, x+4, y+12, 4, "green")   # top track
            square(tankTurtle, x+8, y+12, 4, "green")   # top track
            square(tankTurtle, x+12, y+12, 4, "green")  # top track
            square(tankTurtle, x, y, 4, "green")       # bottom track
        # Obrót o 180 stopni (czołg skierowany do tyłu)
        elif angle == 180:
            square(tankTurtle, x, y+4, 4, "green")  # left track
            square(tankTurtle, x, y+8, 4, "green")  # left track
            square(tankTurtle, x, y+12, 4, "green")  # left track
            square(tankTurtle, x+4, y+7, 8, "green")  # tank hull
            square(tankTurtle, x+7, y+5, 2, "green")   # tank canon
            square(tankTurtle, x+7, y+3, 2, "green")  # tank canon
            square(tankTurtle, x+7, y+1, 2, "green")  # tank canon
            square(tankTurtle, x + 12, y, 4, "green")  # right track
            square(tankTurtle, x + 12, y + 4, 4, "green")  # right track
            square(tankTurtle, x + 12, y + 8, 4, "green")  # right track
            square(tankTurtle, x + 12, y + 12, 4, "green")  # right track
            square(tankTurtle, x, y, 4, "green")  # left track
        # Obrót o 270 stopni (czołg skierowany w lewo)
        elif angle == 270:
            square(tankTurtle, x + 4, y, 4, "green")  # bottom track
            square(tankTurtle, x + 8, y, 4, "green")  # bottom track
            square(tankTurtle, x + 12, y, 4, "green")  # bottom track
            square(tankTurtle, x + 7, y + 4, 8, "green")  # tank hull
            square(tankTurtle, x + 5, y + 7, 2, "green")  # tank canon
            square(tankTurtle, x + 3, y + 7, 2, "green")  # tank canon
            square(tankTurtle, x + 1, y + 7, 2, "green")  # tank canon
            square(tankTurtle, x, y+12, 4, "green")  # top track
            square(tankTurtle, x + 4, y + 12, 4, "green")  # top track
            square(tankTurtle, x + 8, y + 12, 4, "green")  # top track
            square(tankTurtle, x + 12, y + 12, 4, "green")  # top track
            square(tankTurtle, x, y, 4, "green")  # bottom track


setup(420, 420, 500, 100)
hideturtle()
tracer(False)


tank = Tank(40+tankCentralization, 0+tankCentralization)


def move():
    tankTurtle.clear()
    tank.move()
    update()
    ontimer(move, 100)


listen()
onkey(lambda: tank.change(vector(0, 0)), 'space')
onkey(lambda: tank.change(vector(5, 0), 90), 'Right')
onkey(lambda: tank.change(vector(-5, 0), 270), 'Left')
onkey(lambda: tank.change(vector(0, 5), 0), 'Up')
onkey(lambda: tank.change(vector(0, -5), 180), 'Down')

world()
move()
done()
