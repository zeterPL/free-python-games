from turtle import *
from freegames import floor, vector
from enum import Enum


class Tile(Enum):
    NO_TILE = 0
    ROAD = 1
    RIVER = 2
    FOREST = 3
    INDESTRUCTIBLE_BLOCK = 4
    DESTRUCTIBLE_BLOCK = 5
    DESTROYED_DESTRUCTIBLE_BLOCK = 6
    MINE = 7


tiles = [
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
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
tileColors = {
    Tile.ROAD.value: "light goldenrod",
    Tile.RIVER.value: "navy",
    Tile.FOREST.value: "forest green",
    Tile.INDESTRUCTIBLE_BLOCK.value: "snow2",
    Tile.DESTRUCTIBLE_BLOCK.value: "dark orange",
    Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value: "tan1",
    Tile.MINE.value: "light goldenrod",
}
mapTurtle = Turtle(visible=False)
tankTurtle = Turtle(visible=False)


def drawSquare(turtleObject, x, y, size=20, squareColor=None, circuitColor="black"):
    """Draw drawSquare using path at (x, y)."""
    if circuitColor:
        turtleObject.color(circuitColor)
    else:
        turtleObject.color("")
    turtleObject.fillcolor(squareColor)
    turtleObject.up()
    turtleObject.goto(x, y)
    turtleObject.down()
    turtleObject.begin_fill()
    for count in range(4):
        turtleObject.forward(size)
        turtleObject.left(90)
    turtleObject.end_fill()


def getTilePosition(index):
    x = (index % 20) * 20 - 200
    y = 180 - (index // 20) * 20
    return x, y


def drawBoard():
    """Draw map using path."""
    bgcolor('black')
    for index in range(len(tiles)):
        tile = tiles[index]
        if tile > 0:
            x, y = getTilePosition(index)
            tileColor = tileColors[tile]
            drawSquare(mapTurtle, x, y, squareColor=tileColor)
            if tile == Tile.MINE.value:  # drawing mines
                goto(x+10, y+10)
                dot(10, "black")


def offset(point):
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


tankCentralization = 2  # minimal shift of tanks to make tanks stay in the center of the title


def valid(point):
    blockingTiles = [Tile.NO_TILE.value, Tile.RIVER.value, Tile.INDESTRUCTIBLE_BLOCK.value, Tile.DESTRUCTIBLE_BLOCK.value]
    index = offset(point)
    if tiles[index] in blockingTiles:
        return False
    index = offset(point + 19 - tankCentralization)
    if tiles[index] in blockingTiles:
        return False
    return point.x % 20 == tankCentralization or point.y % 20 == tankCentralization


class Bullet:
    def __init__(self, bulletPosition, direction, owner, bulletSpeed=10):
        self.position = vector(bulletPosition.x+7, bulletPosition.y+7)  # plus 7 to make more or less shooting from the middle of the title
        self.direction = direction
        self.bulletSpeed = bulletSpeed
        self.owner = owner
        self.bulletTurtle = Turtle(visible=False)

    def move(self):
        self.bulletTurtle.clear()
        bulletOffsets = {
            90: vector(self.bulletSpeed, 0),
            180: vector(0, -self.bulletSpeed),
            270: vector(-self.bulletSpeed, 0),
            0: vector(0, self.bulletSpeed)
        }
        self.position.move(bulletOffsets[self.direction])
        drawSquare(self.bulletTurtle, self.position.x, self.position.y, 3, "red")

    def drawExplosion(self, x, y, explosionIteration=0, maxIterations=3):
        explosionColors = ["red", "yellow", "orange"]
        explosionColor = explosionColors[explosionIteration % len(explosionColors)]
        offsets = [
            (0, 0),
            (2, 2), (-2, -2), (-2, 2), (2, -2),
            (4, 0), (0, 4), (-4, 0), (0, -4),
        ]
        for dx, dy in offsets:
            drawSquare(self.bulletTurtle, x + dx * (explosionIteration + 1), y + dy * (explosionIteration + 1), 2 + explosionIteration, explosionColor)
        if explosionIteration < maxIterations:
            ontimer(lambda: self.drawExplosion(x, y, explosionIteration + 1, maxIterations), 150)
        else:
            ontimer(self.bulletTurtle.clear, 200)


class Tank:
    def __init__(self, x, y, tankColor, tankId, moveControls, stoppingControl, shootingControl):
        self.position = vector(x, y)
        self.speed = vector(0, 0)
        self.direction = 0  # 0 - forward, 90 - right, 180 - backward, 270 - left
        self.tankColor = tankColor
        self.tankId = tankId
        self.moveControls = moveControls
        self.stoppingControl = stoppingControl
        self.shootingControl = shootingControl
        self.setControls()
        self.keysPressed = {key: False for key in moveControls}

    def change(self, tankSpeedDirection, angle=None):
        offsets = {
            90: vector(5, 0),  # right
            180: vector(0, -5),  # down
            270: vector(-5, 0),  # left
            0: vector(0, 5)  # up
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
        if not valid(self.position + self.speed):
            return
        self.position.move(self.speed)
        if tiles[offset(self.position)] == Tile.MINE.value:
            x, y = getTilePosition(offset(self.position))
            drawSquare(mapTurtle, x, y, squareColor=tileColors[Tile.MINE.value])
            stopGame([self], "tank ran over a mine")
        elif tiles[offset(self.position)] == Tile.FOREST.value:
            pass  # tank hide in forest
        else:
            self.drawTank()

    def drawTank(self, tankDestroyed=False):
        x, y = self.position
        angle = self.direction
        """Draw tracks."""
        trackOffsets = {
            0: [(0, 0), (0, 4), (0, 8), (0, 12), (12, 0), (12, 4), (12, 8), (12, 12)],
            90: [(0, 0), (4, 0), (8, 0), (12, 0), (0, 12), (4, 12), (8, 12), (12, 12)],
            180: [(0, 0), (0, 4), (0, 8), (0, 12), (12, 0), (12, 4), (12, 8), (12, 12)],
            270: [(0, 0), (4, 0), (8, 0), (12, 0), (0, 12), (4, 12), (8, 12), (12, 12)]
        }
        for index, (dx, dy) in enumerate(trackOffsets[angle]):
            drawSquare(tankTurtle, x + dx, y + dy, 4, self.tankColor)
            if tankDestroyed and index in [0, 3, 5, 6]:
                drawSquare(tankTurtle, x + dx, y + dy, 4, "black")
        """Draw hull."""
        hullOffsets = {0: (4, 1), 90: (1, 4), 180: (4, 7), 270: (7, 4)}
        drawSquare(tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 8, self.tankColor)
        if tankDestroyed:
            drawSquare(tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 2, "black", "")
            drawSquare(tankTurtle, x + hullOffsets[angle][0]+4, y + hullOffsets[angle][1], 2, "black", "")
            drawSquare(tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1]+4, 2, "black", "")
            drawSquare(tankTurtle, x + hullOffsets[angle][0]+2, y + hullOffsets[angle][1]+2, 2, "black", "")
            drawSquare(tankTurtle, x + hullOffsets[angle][0]+6, y + hullOffsets[angle][1]+4, 2, "black", "")
        """Draw cannon."""
        cannonOffsets = {
            0: [(7, 9), (7, 11), (7, 13)],
            90: [(9, 7), (11, 7), (13, 7)],
            180: [(7, 5), (7, 3), (7, 1)],
            270: [(5, 7), (3, 7), (1, 7)]
        }
        for dx, dy in cannonOffsets[angle]:
            drawSquare(tankTurtle, x + dx, y + dy, 2, self.tankColor)
        if tankDestroyed:
            drawSquare(tankTurtle, x + cannonOffsets[angle][1][0], y + cannonOffsets[angle][1][1], 2, "black")

    def setControls(self):
        onkey(lambda: self.shoot(), self.shootingControl)
        onkey(lambda: self.change(vector(0, 0)), self.stoppingControl)
        for key, (tankSpeed, angle) in self.moveControls.items():
            onkey(lambda k=key: self.keyPressHandler(k), key)

    def keyPressHandler(self, key):
        self.keysPressed[key] = True

    def tankMovement(self):
        for key, (tankSpeed, angle) in self.moveControls.items():
            if self.keysPressed[key]:
                if self.change(tankSpeed, angle) != -1:
                    for k in self.keysPressed:
                        self.keysPressed[k] = False
                break

    def shoot(self):
        bullet = Bullet(self.position, self.direction, self)
        bullets.append(bullet)


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

firstTank = Tank(40 + tankCentralization, 0 + tankCentralization, "dark green", 1, controls1, "Control_R", "Return")
secondTank = Tank(-100 + tankCentralization, 100 + tankCentralization, "slate gray", 2, controls2, "Control_L", "Shift_L")
bullets = []
gameRunning = True


def stopGame(tanks, reason):
    global gameRunning
    gameRunning = False
    for tank in tanks:
        tank.drawTank(True)
        print(f"Game ended, tank {tank.tankId} lost because: {reason}.")


def tanksCollision(tank1, tank2, collisionThreshold=20):
    distanceBetweenTanks = abs(tank1.position - tank2.position)
    if distanceBetweenTanks < collisionThreshold:
        stopGame([tank1, tank2], "tanks collision. Everyone died")


def checkBulletCollision(bullet, tanks, tankSize=16):
    for tank in tanks:
        if tank != bullet.owner and tank.position.x <= bullet.position.x <= tank.position.x+tankSize and tank.position.y <= bullet.position.y <= tank.position.y+tankSize:
            bullet.drawExplosion(bullet.position.x, bullet.position.y)
            stopGame([tank], f"tank were shot down by {bullet.owner.tankId}")
            return True
    bulletTileValue = tiles[offset(bullet.position)]
    if bulletTileValue in [Tile.INDESTRUCTIBLE_BLOCK.value, Tile.DESTRUCTIBLE_BLOCK.value]:
        bullet.bulletTurtle.clear()
        if bulletTileValue == Tile.DESTRUCTIBLE_BLOCK.value:
            tiles[offset(bullet.position)] = Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value
            x, y = getTilePosition(offset(bullet.position))
            drawSquare(mapTurtle, x, y, squareColor=tileColors[Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value])
        return True
    return False


def move():
    tankTurtle.clear()
    firstTank.tankMovement()
    secondTank.tankMovement()
    firstTank.move()
    secondTank.move()
    tanksCollision(firstTank, secondTank)

    for bullet in bullets:
        bullet.move()
        if checkBulletCollision(bullet, [firstTank, secondTank]):
            bullets.remove(bullet)

    update()
    if gameRunning:
        ontimer(move, 100)


drawBoard()
move()
done()
