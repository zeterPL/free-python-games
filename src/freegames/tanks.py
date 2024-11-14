from turtle import *
from freegames import floor, vector

path = Turtle(visible=False)
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


def squareMap(x, y, squareColor):
    """Draw square using path at (x, y)."""
    path.color("black")
    path.fillcolor(squareColor)
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()
    for count in range(4):
        path.forward(20)
        path.left(90)
    path.end_fill()


def world():
    """Draw map using path."""
    bgcolor('black')
    for index in range(len(tiles)):
        tile = tiles[index]
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            tileColor = "yellow" if tile == 1 else "blue" if tile == 2 else "green" if tile == 3 else "gray" if tile == 4 else "orange"
            squareMap(x, y, tileColor)


def square(x, y, size, fillColor, circuitColor=None):
    up()
    goto(x, y)
    down()
    if circuitColor:
        pencolor(circuitColor)
    else:
        pencolor(fillColor)
    fillcolor(fillColor)
    begin_fill()
    for count in range(4):
        forward(size)
        left(90)
    end_fill()
    up()


def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


tankCentralization = 2  # minimal shift to make tank stay in the center of the title


def valid(point):
    """Return True if point is valid in tiles."""

    # oA = offset(point)
    # print(f"A offset = {oA}  tiles value = {tiles[oA]}")
    # oL = offset(point + vector(-20, 0))
    # print(f"L offset = {oL}  tiles value = {tiles[oL]}")
    # oR = offset(point + vector(20, 0))
    # print(f"R offset = {oR}  tiles value = {tiles[oR]}")
    # oU = offset(point + vector(0, 20))
    # print(f"U offset = {oU}  tiles value = {tiles[oU]}")
    # oD = offset(point + vector(0, -20))
    # print(f"D offset = {oD}  tiles value = {tiles[oD]}")

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
        if (angle == 90 and valid(self.position + vector(25, 0))) or (angle == 180 and valid(self.position + vector(0, -25))) or (angle == 270 and valid(self.position + vector(-25, 0))) or (angle == 0 and valid(self.position + vector(0, 25))):
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
            square(x, y, 4, "green")       # left track
            square(x, y+4, 4, "green")     # left track
            square(x, y+8, 4, "green")     # left track
            square(x, y+12, 4, "green")    # left track
            square(x+4, y+1, 8, "green")   # tank hull
            square(x+7, y+9, 2, "green")   # tank canon
            square(x+7, y+11, 2, "green")  # tank canon
            square(x+7, y+13, 2, "green")  # tank canon
            square(x+12, y, 4, "green")     # right track
            square(x+12, y+4, 4, "green")   # right track
            square(x+12, y+8, 4, "green")   # right track
            square(x+12, y+12, 4, "green")  # right track
        # Obrót o 90 stopni w prawo (czołg skierowany w prawo)
        elif angle == 90:
            square(x, y, 4, "green")       # bottom track
            square(x+4, y, 4, "green")     # bottom track
            square(x+8, y, 4, "green")     # bottom track
            square(x+12, y, 4, "green")    # bottom track
            square(x+1, y+4, 8, "green")   # tank hull
            square(x+9, y+7, 2, "green")   # tank canon
            square(x+11, y+7, 2, "green")  # tank canon
            square(x+13, y+7, 2, "green")  # tank canon
            square(x, y+12, 4, "green")     # top track
            square(x+4, y+12, 4, "green")   # top track
            square(x+8, y+12, 4, "green")   # top track
            square(x+12, y+12, 4, "green")  # top track
        # Obrót o 180 stopni (czołg skierowany do tyłu)
        elif angle == 180:
            square(x, y, 4, "green")  # left track
            square(x, y+4, 4, "green")  # left track
            square(x, y+8, 4, "green")  # left track
            square(x, y+12, 4, "green")  # left track
            square(x+4, y+7, 8, "green")  # tank hull
            square(x+7, y+5, 2, "green")   # tank canon
            square(x+7, y+3, 2, "green")  # tank canon
            square(x+7, y+1, 2, "green")  # tank canon
            square(x + 12, y, 4, "green")  # right track
            square(x + 12, y + 4, 4, "green")  # right track
            square(x + 12, y + 8, 4, "green")  # right track
            square(x + 12, y + 12, 4, "green")  # right track
        # Obrót o 270 stopni (czołg skierowany w lewo)
        elif angle == 270:
            square(x, y, 4, "green")  # bottom track
            square(x + 4, y, 4, "green")  # bottom track
            square(x + 8, y, 4, "green")  # bottom track
            square(x + 12, y, 4, "green")  # bottom track
            square(x + 7, y + 4, 8, "green")  # tank hull
            square(x + 5, y + 7, 2, "green")  # tank canon
            square(x + 3, y + 7, 2, "green")  # tank canon
            square(x + 1, y + 7, 2, "green")  # tank canon
            square(x, y+12, 4, "green")  # top track
            square(x + 4, y + 12, 4, "green")  # top track
            square(x + 8, y + 12, 4, "green")  # top track
            square(x + 12, y + 12, 4, "green")  # top track
        square(x, y, 1, "red")


setup(420, 420, 500, 100)
hideturtle()
tracer(False)


tank = Tank(40+tankCentralization, 0+tankCentralization)


def move():
    clear()
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
