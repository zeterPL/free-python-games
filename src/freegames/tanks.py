from random import choice
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


def world():
    """Draw map using path."""
    bgcolor('black')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            tileColor = "yellow" if tile == 1 else "blue" if tile == 2 else "green" if tile == 3 else "gray" if tile == 4 else "orange"
            square(x, y, 20, tileColor, "black")


def drawTank(startPoint, angle=0):
    x, y = startPoint.x + 2, startPoint.y + 2

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


setup(420, 420, 500, 100)
hideturtle()
tracer(False)

world()

tank = vector(0, 0)
drawTank(tank, 0)
tank = vector(20, 0)
drawTank(tank, 90)
tank = vector(40, 0)
drawTank(tank, 180)
tank = vector(60, 0)
drawTank(tank, 270)


done()
