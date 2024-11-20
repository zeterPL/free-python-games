from turtle import Turtle, onkey
from freegames import vector
from graphics import drawSquare
from tiles import tiles, Tile, getTilePosition, tileColors
from game_utils import valid, offset
from constants import tankCentralization

class Tank:
    def __init__(self, x, y, tankColor, tankId, moveControls,
                 stoppingControl, shootingControl, tankTurtle, hp=3):
        self.position = vector(x, y)
        self.speed = vector(0, 0)
        self.direction = 0
        self.tankColor = tankColor
        self.tankId = tankId
        self.moveControls = moveControls
        self.stoppingControl = stoppingControl
        self.shootingControl = shootingControl
        self.tankTurtle = tankTurtle
        self.setControls()
        self.hp = hp
        self.keysPressed = {key: False for key in moveControls}
        self.hpTurtle = Turtle(visible=False)
        self.hpTurtle.up()
        self.hpTurtle.hideturtle()
        self.hpTurtle.color("red")

    def drawHP(self):
        self.hpTurtle.clear()
        x, y = self.position
        self.hpTurtle.goto(x + 10, y + 25)
        self.hpTurtle.write(f"HP: {self.hp}", align="center",
                            font=("Arial", 10, "bold"))

    def takeDamage(self):
        self.hp -= 1
        if self.hp <= 0:
            from main import stopGame
            stopGame([self], f"Czołg {self.tankId} został zniszczony")
        else:
            print(f"Czołg {self.tankId} HP: {self.hp}")

    def change(self, tankSpeedDirection, angle=None):
        offsets = {
            90: vector(5, 0),
            180: vector(0, -5),
            270: vector(-5, 0),
            0: vector(0, 5)
        }
        if angle in offsets and valid(self.position + offsets[angle]):
            self.speed = tankSpeedDirection
            self.direction = angle
            return 0
        if tankSpeedDirection.x == 0 and tankSpeedDirection.y == 0:
            self.speed = tankSpeedDirection
            return 1
        if self.speed.x == 0 and self.speed.y == 0 and angle is not None:
            self.direction = angle
            return 2
        return -1

    def move(self):
        if valid(self.position + self.speed):
            self.position.move(self.speed)
        if tiles[offset(self.position)] == Tile.MINE.value:
            x, y = getTilePosition(offset(self.position))
            drawSquare(self.tankTurtle, x, y,
                       squareColor=tileColors[Tile.MINE.value])
            from main import stopGame
            stopGame([self], "Czołg wjechał na minę")
        elif tiles[offset(self.position)] == Tile.FOREST.value:
            pass  # Czołg ukrywa się w lesie
        else:
            self.drawTank()

    def drawTank(self, tankDestroyed=False):
        x, y = self.position
        angle = self.direction
        # Rysowanie gąsienic
        trackOffsets = {
            0: [(0, 0), (0, 4), (0, 8), (0, 12), (12, 0), (12, 4), (12, 8), (12, 12)],
            90: [(0, 0), (4, 0), (8, 0), (12, 0), (0, 12), (4, 12), (8, 12), (12, 12)],
            180: [(0, 0), (0, 4), (0, 8), (0, 12), (12, 0), (12, 4), (12, 8), (12, 12)],
            270: [(0, 0), (4, 0), (8, 0), (12, 0), (0, 12), (4, 12), (8, 12), (12, 12)]
        }
        for index, (dx, dy) in enumerate(trackOffsets[angle]):
            drawSquare(self.tankTurtle, x + dx, y + dy, 4, self.tankColor)
            if tankDestroyed and index in [0, 3, 5, 6]:
                drawSquare(self.tankTurtle, x + dx, y + dy, 4, "black")
        # Rysowanie kadłuba
        hullOffsets = {0: (4, 1), 90: (1, 4), 180: (4, 7), 270: (7, 4)}
        drawSquare(self.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 8, self.tankColor)
        if tankDestroyed:
            drawSquare(self.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 2, "black", "")
            drawSquare(self.tankTurtle, x + hullOffsets[angle][0]+4, y + hullOffsets[angle][1], 2, "black", "")
            drawSquare(self.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1]+4, 2, "black", "")
            drawSquare(self.tankTurtle, x + hullOffsets[angle][0]+2, y + hullOffsets[angle][1]+2, 2, "black", "")
            drawSquare(self.tankTurtle, x + hullOffsets[angle][0]+6, y + hullOffsets[angle][1]+4, 2, "black", "")
        # Rysowanie działa
        cannonOffsets = {
            0: [(7, 9), (7, 11), (7, 13)],
            90: [(9, 7), (11, 7), (13, 7)],
            180: [(7, 5), (7, 3), (7, 1)],
            270: [(5, 7), (3, 7), (1, 7)]
        }
        for dx, dy in cannonOffsets[angle]:
            drawSquare(self.tankTurtle, x + dx, y + dy, 2, self.tankColor)
        if tankDestroyed:
            drawSquare(self.tankTurtle, x + cannonOffsets[angle][1][0], y + cannonOffsets[angle][1][1], 2, "black")

    def setControls(self):
        onkey(lambda: self.shoot(), self.shootingControl)
        onkey(lambda: self.change(vector(0, 0)), self.stoppingControl)
        for key in self.moveControls:
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
        from bullet import Bullet
        from main import bullets
        bullet = Bullet(self.position, self.direction, self)
        bullets.append(bullet)
