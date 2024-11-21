from turtle import *
from freegames import floor, vector
from enum import Enum


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


def offset(point):
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def load_map_from_file(filename):
    new_tiles = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                new_tiles.extend(map(int, line.split()))
        if len(new_tiles) != 400:  
            raise ValueError("Invalid map size. Map must have 400 tiles.")
    except Exception as e:
        print(f"Error loading map: {e}")
        return None
    return new_tiles


class Tile(Enum):
    NO_TILE = 0
    ROAD = 1
    RIVER = 2
    FOREST = 3
    INDESTRUCTIBLE_BLOCK = 4
    DESTRUCTIBLE_BLOCK = 5
    DESTROYED_DESTRUCTIBLE_BLOCK = 6
    MINE = 7


dafault_tiles = [
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 7, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 7, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 7, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    4, 1, 1, 1, 1, 1, 1, 1, 7, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
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


class Game:
    def __init__(self, dafault_tiles, initialTileColors, map_file=None):
        self.initialTiles = dafault_tiles
        if map_file:
            loaded_tiles = load_map_from_file(map_file)
            if loaded_tiles:
                self.initialTiles = loaded_tiles
                print(f"Map successfully loaded from '{map_file}'!")
        
        self.tiles = list(self.initialTiles)
        self.tileColors = initialTileColors

        self.mapTurtle = Turtle(visible=False)
        self.tankTurtle = Turtle(visible=False)
        self.messageTurtle = Turtle(visible=False)
        self.minesTurtle = Turtle(visible=False)

        self.bullets = []

        self.gameRunning = False
        self.gamePaused = False

        self.firstTank = None
        self.secondTank = None

        self.controls1 = {
            "Up": (vector(0, 5), 0),
            "Down": (vector(0, -5), 180),
            "Left": (vector(-5, 0), 270),
            "Right": (vector(5, 0), 90)
        }
        self.controls2 = {
            "w": (vector(0, 5), 0),
            "s": (vector(0, -5), 180),
            "a": (vector(-5, 0), 270),
            "d": (vector(5, 0), 90)
        }

        self.tankCentralization = 2  # minimal shift of tanks to make tanks stay in the center of the title

        setup(420, 420, 500, 100)
        hideturtle()
        tracer(False)

        for key in ["r", "R"]:
            onkey(self.startGame, key)
        for key in ["p", "P"]:
            onkey(self.togglePause, key)    
        listen()

        self.startGame()
        done()

    def togglePause(self):
        self.gamePaused = not self.gamePaused

        if not self.gamePaused:
            print("Game resumes!")
            self.messageTurtle.clear()
            self.roundOfMovement()
        else:
            print("Game paused!") 
            self.drawPauseMessage()   

    def drawBoard(self):
        bgcolor('black')
        for index in range(len(self.tiles)):
            tile = self.tiles[index]
            if tile > 0:
                x, y = getTilePosition(index)
                tileColor = self.tileColors[tile]
                drawSquare(self.mapTurtle, x, y, squareColor=tileColor)
                if tile == Tile.MINE.value:  # drawing mines
                    self.minesTurtle.up()
                    self.minesTurtle.goto(x+10, y+10)
                    self.minesTurtle.dot(10, "black")

    def valid(self, point):
        blockingTiles = [Tile.NO_TILE.value, Tile.RIVER.value, Tile.INDESTRUCTIBLE_BLOCK.value, Tile.DESTRUCTIBLE_BLOCK.value]
        index = offset(point)
        if self.tiles[index] in blockingTiles:
            return False
        index = offset(point + 19 - self.tankCentralization)
        if self.tiles[index] in blockingTiles:
            return False
        return point.x % 20 == self.tankCentralization or point.y % 20 == self.tankCentralization

    def drawExplosion(self, drawingTurtle, x, y, explosionIteration=0, maxIterations=3):
        explosionColors = ["red", "yellow", "orange"]
        explosionColor = explosionColors[explosionIteration % len(explosionColors)]
        offsets = [
            (0, 0),
            (2, 2), (-2, -2), (-2, 2), (2, -2),
            (4, 0), (0, 4), (-4, 0), (0, -4),
        ]
        for dx, dy in offsets:
            drawSquare(drawingTurtle, x + dx * (explosionIteration + 1), y + dy * (explosionIteration + 1), 2 + explosionIteration, explosionColor)
        if explosionIteration < maxIterations:
            ontimer(lambda: self.drawExplosion(drawingTurtle, x, y, explosionIteration + 1, maxIterations), 150)
        else:
            ontimer(drawingTurtle.clear, 200)

    def drawModalBackground(self, x, y, modalWidth, modalHeight, backgroundColor="white", borderColor="black"):
        self.messageTurtle.color(borderColor)
        self.messageTurtle.fillcolor(backgroundColor)
        self.messageTurtle.penup()
        self.messageTurtle.goto(x - modalWidth / 2, y - modalHeight / 2)
        self.messageTurtle.pendown()
        self.messageTurtle.begin_fill()
        for _ in range(2):
            self.messageTurtle.forward(modalWidth)
            self.messageTurtle.left(90)
            self.messageTurtle.forward(modalHeight)
            self.messageTurtle.left(90)

        self.messageTurtle.end_fill()
        self.messageTurtle.penup()

    def drawEndMessage(self, reason):
        message = f"Game Over!\n{reason}"
        submessage = "Press 'R' to restart"

        self.drawModalMessage(message, submessage)

    def drawPauseMessage(self):
        message = "Game Paused!"
        submessage = "Press 'P' to play"   

        self.drawModalMessage(message, submessage) 

    def drawModalMessage(self, message, submessage):
        self.drawModalBackground(0, 0, 350, 120)

        self.messageTurtle.goto(0, 0)
        self.messageTurtle.write(message, align="center", font=("Arial", 16, "bold"))

        self.messageTurtle.goto(0, -40)
        self.messageTurtle.write(submessage, align="center", font=("Arial", 12, "normal"))

    def startGame(self):
        if self.gameRunning:  # don't start game if it's already started
            return
        self.gameRunning = True
        self.tiles = list(self.initialTiles)  # restarting map to state before changes in game

        self.tankTurtle.clear()
        self.mapTurtle.clear()
        self.messageTurtle.clear()

        self.bullets = []
        self.firstTank = Tank(self, 40 + self.tankCentralization, 0 + self.tankCentralization, "dark green", 1, self.controls1, "Control_R", "Return")
        self.secondTank = Tank(self, -100 + self.tankCentralization, 100 + self.tankCentralization, "slate gray", 2, self.controls2, "Control_L", "Shift_L")

        self.drawBoard()
        ontimer(self.minesTurtle.clear, 5000)  # hiding mines after 5 seconds
        self.roundOfMovement()

    def stopGame(self, tanks, reason):
        self.gameRunning = False

        for tank in tanks:  # draw destroyed tanks
            tank.drawTank(True)

        ontimer(lambda r=reason: self.drawEndMessage(r), 2500)

    def tanksCollision(self, tank1, tank2, collisionThreshold=20):
        distanceBetweenTanks = abs(tank1.position - tank2.position)
        if distanceBetweenTanks < collisionThreshold:
            self.stopGame([tank1, tank2], "tanks collision. Everyone died")

    def processBulletCollision(self, bullet, tanks, tankSize=16):
        for tank in tanks:
            if tank != bullet.shooter and tank.position.x <= bullet.position.x <= tank.position.x + tankSize and tank.position.y <= bullet.position.y <= tank.position.y + tankSize:
                self.drawExplosion(Turtle(visible=False), bullet.position.x, bullet.position.y)
                tank.takeDamage(f"tank {tank.tankId} was shot down by tank {bullet.shooter.tankId}")
                self.bullets.remove(bullet)
                bullet.bulletTurtle.clear()
        bulletTileValue = self.tiles[offset(bullet.position)]
        if bulletTileValue in [Tile.INDESTRUCTIBLE_BLOCK.value, Tile.DESTRUCTIBLE_BLOCK.value]:
            bullet.bulletTurtle.clear()
            if bulletTileValue == Tile.DESTRUCTIBLE_BLOCK.value:
                self.tiles[offset(bullet.position)] = Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value
                x, y = getTilePosition(offset(bullet.position))
                drawSquare(self.mapTurtle, x, y, squareColor=self.tileColors[Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value])
            self.bullets.remove(bullet)

    def roundOfMovement(self):
        if self.gamePaused or not self.gameRunning:
            return

        self.tankTurtle.clear()
        self.firstTank.tankMovement()
        self.secondTank.tankMovement()
        self.firstTank.moveTank()
        self.secondTank.moveTank()
        self.tanksCollision(self.firstTank, self.secondTank)

        for bullet in self.bullets[:]:
            bullet.moveBullet()
            self.processBulletCollision(bullet, [self.firstTank, self.secondTank])

        update()
        if self.gameRunning:
            ontimer(self.roundOfMovement, 100)


class Bullet:
    def __init__(self, shooter, bulletSpeed=10):
        self.position = vector(shooter.position.x + 7, shooter.position.y + 7)  # plus 7 to make more or less shooting from the middle of the title
        self.direction = shooter.direction
        self.bulletSpeed = bulletSpeed
        self.shooter = shooter
        self.bulletTurtle = Turtle(visible=False)

    def moveBullet(self):
        self.bulletTurtle.clear()
        bulletOffsets = {
            90: vector(self.bulletSpeed, 0),
            180: vector(0, -self.bulletSpeed),
            270: vector(-self.bulletSpeed, 0),
            0: vector(0, self.bulletSpeed)
        }
        self.position.move(bulletOffsets[self.direction])
        drawSquare(self.bulletTurtle, self.position.x, self.position.y, 3, "red")


class Tank:
    def __init__(self, game, x, y, tankColor, tankId, moveControls, stoppingControl, shootingControl, hp=3):
        self.game = game
        self.position = vector(x, y)
        self.speed = vector(0, 0)
        self.direction = 0  # 0 - forward, 90 - right, 180 - backward, 270 - left
        self.tankColor = tankColor
        self.tankId = tankId
        self.moveControls = moveControls
        self.stoppingControl = stoppingControl
        self.shootingControl = shootingControl
        self.setControls()
        self.hp = hp
        self.keysPressed = {key: False for key in moveControls}
        self.hpTurtle = Turtle(visible=False)

    def takeDamage(self, reason):
        if self.hp > 0:
            self.hp -= 1
            print(f"Tank {self.tankId} HP: {self.hp}")
            if self.hp == 0:
                self.game.stopGame([self], reason)

    def change(self, tankSpeedDirection, angle=None):
        offsets = {
            90: vector(5, 0),  # right
            180: vector(0, -5),  # down
            270: vector(-5, 0),  # left
            0: vector(0, 5)  # up
        }
        if angle in offsets and self.game.valid(self.position + offsets[angle]):
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

    def moveTank(self):
        if self.game.valid(self.position + self.speed):
            self.position.move(self.speed)
        if self.game.tiles[offset(self.position)] == Tile.MINE.value:
            x, y = getTilePosition(offset(self.position))
            self.game.tiles[offset(self.position)] = Tile.ROAD.value
            drawSquare(self.game.mapTurtle, x, y, squareColor=self.game.tileColors[Tile.ROAD.value])
            self.game.drawExplosion(Turtle(visible=False), x+10, y+10)
            self.takeDamage("tank ran over a mine")
        elif self.game.tiles[offset(self.position)] == Tile.FOREST.value:
            self.hpTurtle.clear()  # tank hide in forest
        else:
            self.drawTank()

    def drawHP(self, hpColor="red"):
        self.hpTurtle.clear()
        x, y = self.position
        self.hpTurtle.up()
        self.hpTurtle.goto(x + 10, y + 25)
        self.hpTurtle.color(hpColor)
        self.hpTurtle.write(f"HP: {self.hp}", align="center", font=("Arial", 10, "bold"))

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
            drawSquare(self.game.tankTurtle, x + dx, y + dy, 4, self.tankColor)
            if tankDestroyed and index in [0, 3, 5, 6]:
                drawSquare(self.game.tankTurtle, x + dx, y + dy, 4, "black")
        """Draw hull."""
        hullOffsets = {0: (4, 1), 90: (1, 4), 180: (4, 7), 270: (7, 4)}
        drawSquare(self.game.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 8, self.tankColor)
        if tankDestroyed:
            drawSquare(self.game.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 2, "black", "")
            drawSquare(self.game.tankTurtle, x + hullOffsets[angle][0]+4, y + hullOffsets[angle][1], 2, "black", "")
            drawSquare(self.game.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1]+4, 2, "black", "")
            drawSquare(self.game.tankTurtle, x + hullOffsets[angle][0]+2, y + hullOffsets[angle][1]+2, 2, "black", "")
            drawSquare(self.game.tankTurtle, x + hullOffsets[angle][0]+6, y + hullOffsets[angle][1]+4, 2, "black", "")
        """Draw cannon."""
        cannonOffsets = {
            0: [(7, 9), (7, 11), (7, 13)],
            90: [(9, 7), (11, 7), (13, 7)],
            180: [(7, 5), (7, 3), (7, 1)],
            270: [(5, 7), (3, 7), (1, 7)]
        }
        for dx, dy in cannonOffsets[angle]:
            drawSquare(self.game.tankTurtle, x + dx, y + dy, 2, self.tankColor)
        if tankDestroyed:
            drawSquare(self.game.tankTurtle, x + cannonOffsets[angle][1][0], y + cannonOffsets[angle][1][1], 2, "black")
        self.drawHP()

    def setControls(self):
        onkey(lambda: self.shoot(), self.shootingControl)
        onkey(lambda: self.change(vector(0, 0)), self.stoppingControl)
        for key, (tankSpeed, angle) in self.moveControls.items():
            onkey(lambda k=key: self.keyPressHandler(k), key)
            if len(key) == 1 and key.isalpha():
                onkey(lambda k=key: self.keyPressHandler(k), key.upper())

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
        bullet = Bullet(self)
        self.game.bullets.append(bullet)


Game(dafault_tiles, tileColors, "tanks_maps/map1.txt")
