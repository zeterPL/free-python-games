from turtle import Turtle, onkey, ontimer
from freegames import vector
import random
from bullet import Bullet
from tile import Tile
from bonus import Bonus
from draw import Draw


class Tank:
    def __init__(self, game, x, y, tankColor, tankId, moveControls, stoppingControl, shootingControl, hp=None, attack=None):
        self.game = game
        self.position = vector(x, y)
        self.speed = vector(0, 0)
        self.tankSpeedValue = self.game.tankSpeedValue
        self.speedRatio = 1
        self.direction = 0  # 0 - forward, 90 - right, 180 - backward, 270 - left
        self.tankColor = tankColor
        self.tankId = tankId
        self.moveControls = moveControls
        self.stoppingControl = stoppingControl
        self.shootingControl = shootingControl
        self.setControls()
        self.keysPressed = {key: False for key in moveControls}
        self.hp = hp or self.game.basicHp
        self.maxHp = hp or self.game.basicHp
        self.attack = attack or self.game.basicAttack
        self.tankTurtle = Turtle(visible=False)
        self.hpTurtle = Turtle(visible=False)
        self.reloadTurtle = Turtle(visible=False)
        self.bonusDisplayTurtle = Turtle(visible=False)
        self.reloadingTime = 2000  # value in milliseconds
        self.reloadingRemainingTime = 0
        self.loaded = True
        self.destroyed = False
        self.deathReason = ""
        self.activeBonuses = {}
        self.indestructible = False

    def takeDamage(self, amount, reason):
        if not self.destroyed and not self.indestructible:
            self.hp -= amount
            if self.hp <= 0:
                self.destroyed = True
                self.deathReason = reason
                self.drawTank()
            self.game.damageSound.play()

    def change(self, tankSpeedDirection, angle=None):
        if self.destroyed:
            return
        if angle is not None and self.game.valid(self.position + tankSpeedDirection * self.speedRatio):
            self.speed = tankSpeedDirection * self.speedRatio
            self.direction = angle
            return 0
        # stop tank
        if tankSpeedDirection.x == 0 and tankSpeedDirection.y == 0:
            self.speed = tankSpeedDirection * self.speedRatio
            self.direction = angle or self.direction
            return 1
        # if tank was stopped before then he can turn in any direction
        if self.speed.x == 0 and self.speed.y == 0 and angle is not None:
            self.direction = angle
            return 2
        # if tank move in wrong direction, where he can't go
        return -1

    def moveTank(self, wantMove=True):
        newPosition = self.position + self.speed
        if not self.destroyed and self.game.valid(newPosition) and wantMove and not self.game.tanksCollision(self, newPosition, int(self.game.tileSize * 0.8)):
            self.position = newPosition

        for bonus in self.game.bonuses[:]:
            if bonus.tankIsOnBonus(self, bonus, self.game.tileSize):
                bonus.activateBonus(self, bonus)
                self.game.bonuses.remove(bonus)
                bonus.bonusTurtle.clear()

        centralizedPosition = self.position + int(self.game.tileSize * 0.4)
        tileIndex = self.game.getTileIndexFromPoint(centralizedPosition)
        tileValue = self.game.tiles[tileIndex]
        if tileValue == Tile.MINE.value:
            x, y = self.game.getTilePosition(tileIndex)
            self.game.tiles[tileIndex] = Tile.ROAD.value
            Draw.drawSquare(self.game.mapTurtle, x, y, self.game.tileSize, squareColor=self.game.tileColors[Tile.ROAD.value])
            self.game.drawExplosion(Turtle(visible=False), x + self.game.tileSize // 2, y + self.game.tileSize // 2)
            self.takeDamage(random.randint(self.game.basicAttack//2, self.game.basicAttack*2), f"tank {self.tankId} ran over a mine")
        elif tileValue == Tile.TELEPORT.value:
            if self.speed.x:
                self.position -= vector(self.speed.x//abs(self.speed.x)*self.game.tileSize*(self.game.columns-2), 0)
            else:
                self.position -= vector(0, self.speed.y//abs(self.speed.y)*self.game.tileSize*(self.game.rows-2))
        elif tileValue == Tile.FOREST.value:  # tank hide in forest
            self.tankTurtle.clear()
            self.hpTurtle.clear()
            self.reloadTurtle.clear()
            self.bonusDisplayTurtle.clear()
        else:
            self.drawTank()

    def drawHP(self, hpColor="red", bgColor="black"):
        self.hpTurtle.clear()
        if self.hp > 0:
            x, y = self.position - self.game.tankCentralization
            barWidth = self.game.tileSize
            barHeight = self.game.tileSize // 20 * 3
            hpRatio = self.hp / self.maxHp
            Draw.drawRectangle(self.hpTurtle, x, y + self.game.tileSize*1.2, barWidth, barHeight, bgColor)
            Draw.drawRectangle(self.hpTurtle, x, y + self.game.tileSize*1.2, barWidth*hpRatio, barHeight, hpColor)

    def drawReloadBar(self, reloadColor="gold", bgColor="black"):
        self.reloadTurtle.clear()
        if self.hp > 0:
            x, y = self.position - self.game.tankCentralization
            barWidth = self.game.tileSize
            barHeight = self.game.tileSize // 20 * 3
            reloadRatio = 1 - (self.reloadingRemainingTime / self.reloadingTime) if self.reloadingTime > 0 else 1
            Draw.drawRectangle(self.reloadTurtle, x, y + self.game.tileSize, barWidth, barHeight, bgColor)
            Draw.drawRectangle(self.reloadTurtle, x, y + self.game.tileSize, barWidth * reloadRatio, barHeight, reloadColor)

    def drawTank(self):
        self.tankTurtle.clear()
        x, y = self.position
        angle = self.direction
        t = self.game.tileSize // 20
        """Draw tracks."""
        trackOffsets = {
            0: [(0, 0), (0, 4 * t), (0, 8 * t), (0, 12 * t), (12 * t, 0), (12 * t, 4 * t), (12 * t, 8 * t), (12 * t, 12 * t)],
            90: [(0, 0), (4 * t, 0), (8 * t, 0), (12 * t, 0), (0, 12 * t), (4 * t, 12 * t), (8 * t, 12 * t), (12 * t, 12 * t)],
            180: [(0, 0), (0, 4 * t), (0, 8 * t), (0, 12 * t), (12 * t, 0), (12 * t, 4 * t), (12 * t, 8 * t), (12 * t, 12 * t)],
            270: [(0, 0), (4 * t, 0), (8 * t, 0), (12 * t, 0), (0, 12 * t), (4 * t, 12 * t), (8 * t, 12 * t), (12 * t, 12 * t)]
        }
        for index, (dx, dy) in enumerate(trackOffsets[angle]):
            Draw.drawSquare(self.tankTurtle, x + dx, y + dy, 4 * t, self.tankColor)
            if self.destroyed and index in [0, t, 5, t]:
                Draw.drawSquare(self.tankTurtle, x + dx, y + dy, 4 * t, "black")
        """Draw hull."""
        hullOffsets = {0: (4 * t, t), 90: (t, 4 * t), 180: (4 * t, 7 * t), 270: (7 * t, 4 * t)}
        Draw.drawSquare(self.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 8 * t, self.tankColor)
        if self.destroyed:
            Draw.drawSquare(self.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 2 * t, "black", "")
            Draw.drawSquare(self.tankTurtle, x + hullOffsets[angle][0] + 4 * t, y + hullOffsets[angle][1], 2 * t, "black", "")
            Draw.drawSquare(self.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1] + 4 * t, 2 * t, "black", "")
            Draw.drawSquare(self.tankTurtle, x + hullOffsets[angle][0] + 2 * t, y + hullOffsets[angle][1] + 2 * t, 2 * t, "black", "")
            Draw.drawSquare(self.tankTurtle, x + hullOffsets[angle][0] + 6 * t, y + hullOffsets[angle][1] + 4 * t, 2 * t, "black", "")
        """Draw cannon."""
        cannonOffsets = {
            0: [(7 * t, 9 * t), (7 * t, 11 * t), (7 * t, 13 * t)],
            90: [(9 * t, 7 * t), (11 * t, 7 * t), (13 * t, 7 * t)],
            180: [(7 * t, 5 * t), (7 * t, 3 * t), (7 * t, t)],
            270: [(5 * t, 7 * t), (3 * t, 7 * t), (t, 7 * t)]
        }
        for dx, dy in cannonOffsets[angle]:
            Draw.drawSquare(self.tankTurtle, x + dx, y + dy, 2 * t, self.tankColor)
        if self.destroyed:
            Draw.drawSquare(self.tankTurtle, x + cannonOffsets[angle][1][0], y + cannonOffsets[angle][1][1], 2 * t, "black")
        self.drawHP()
        self.drawReloadBar()
        Bonus.displayActiveBonuses(self)

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

    def shoot(self):
        if not self.loaded or self.destroyed:
            return
        bullet = Bullet(self)
        self.game.bullets.append(bullet)
        self.loaded = False
        self.reloadingRemainingTime = self.reloadingTime
        self.updateReload()  # Start updating the reload bar
        self.game.laserShootSound.play()

    def updateReload(self):
        if self.reloadingRemainingTime > 0:
            self.reloadingRemainingTime -= 100  # Decrease remaining time
            ontimer(self.updateReload, 100)  # Update every 100ms
        else:
            self.loaded = True
        if self.game.tiles[self.game.getTileIndexFromPoint(self.position + int(self.game.tileSize * 0.4))] != Tile.FOREST.value:
            self.drawReloadBar()
