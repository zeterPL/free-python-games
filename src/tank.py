from turtle import Turtle
import random
from collections import deque
from .bullet import Bullet
from .tile import Tile
from .bonus import Bonus, BonusType
from .draw import Draw
from .utils import Utils, Vector


class Tank:
    def __init__(self, game, x, y, tankColor, tankId, moveControls, stoppingControl, shootingControl, hp=None, attack=None):
        self.game = game
        self.position = Vector(x, y)
        self.speed = Vector(0, 0)
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
        self.defaultAttack = self.attack
        self.tankTurtle = Turtle(visible=False)
        self.hpTurtle = Turtle(visible=False)
        self.reloadTurtle = Turtle(visible=False)
        self.bonusDisplayTurtle = Turtle(visible=False)
        self.reloadingTime = 2000  # value in milliseconds
        self.reloadingRemainingTime = 0
        self.loaded = True
        self.destroyed = False
        self.deathReason = ""
        self.activeBonuses = {bonusType: 0 for bonusType in BonusType}
        self.indestructible = False
        self.railgunOn = False

    def delete(self):
        self.tankTurtle = None
        self.hpTurtle = None
        self.reloadTurtle = None
        self.bonusDisplayTurtle = None
        Utils.deactivateKeys([self.stoppingControl, self.shootingControl] + list(self.moveControls.keys()))

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
        if not self.destroyed and self.game.valid(newPosition) and wantMove and not Tank.tanksCollision(self.game, self, newPosition, int(self.game.tileSize * 0.8)):
            self.position = newPosition

        for bonus in self.game.bonuses[:]:
            if bonus.tankIsOnBonus(self, bonus, self.game.tileSize):
                bonus.activateBonus(self, bonus.bonusType)
                self.game.bonuses.remove(bonus)
                bonus.bonusTurtle.clear()

        centralizedPosition = self.position + int(self.game.tileSize * 0.4)
        tileIndex = self.game.getTileIndexFromPoint(centralizedPosition)
        tileValue = self.game.tiles[tileIndex]
        if tileValue == Tile.MINE.value:
            x, y = self.game.getTilePosition(tileIndex)
            self.game.tiles[tileIndex] = Tile.ROAD.value
            Draw.drawSquare(self.game.mapTurtle, x, y, self.game.tileSize, squareColor=self.game.tileColors[Tile.ROAD.value])
            Draw.drawExplosion(self.game, x + self.game.tileSize // 2, y + self.game.tileSize // 2)
            self.takeDamage(random.randint(self.game.basicAttack//2, self.game.basicAttack*2), f"tank {self.tankId} ran over a mine")
        elif tileValue == Tile.TELEPORT.value:
            self.teleportTankThroughTeleport()
        elif tileValue == Tile.FOREST.value:  # tank hide in forest
            self.tankTurtle.clear()
            self.hpTurtle.clear()
            self.reloadTurtle.clear()
            self.bonusDisplayTurtle.clear()
        else:
            Draw.drawTank(self)
            Bonus.displayActiveBonuses(self)

    def teleportTankThroughTeleport(self):
        index = self.game.getTileIndexFromPoint(self.position)
        row, column = divmod(index, self.game.columns)
        newRow = row if self.speed.x else self.game.rows - row - 1 if self.speed.y > 0 else self.game.rows - row
        newColumn = column if self.speed.y else self.game.columns - column - 1 if self.speed.x > 0 else self.game.columns - column - 2
        potentialIndex = newRow * self.game.rows + newColumn
        newIndex = Tank.getClosestAvailableIndex(self.game, potentialIndex, index+1)
        self.position = Vector(*self.game.getTilePosition(newIndex)) + self.game.tankCentralization
        self.hp = max(1, int(0.9 * self.hp))
        self.game.teleportSound.play()

    @staticmethod
    def getClosestAvailableIndex(game, newIndex, repeatingIndex):
        if Tank.checkIfIndexAvailableForTankTeleport(game, newIndex, [repeatingIndex]):
            return newIndex
        visited = {newIndex}
        queue = deque([newIndex])
        while queue:
            current = queue.popleft()
            currentRow, currentColumn = divmod(current, game.columns)
            for deltaRow, deltaColumn in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighborRow = currentRow + deltaRow
                neighborColumn = currentColumn + deltaColumn
                if 0 <= neighborRow < game.rows and 0 <= neighborColumn < game.columns:
                    neighborIndex = neighborRow * game.columns + neighborColumn
                    if neighborIndex not in visited:
                        visited.add(neighborIndex)
                        if Tank.checkIfIndexAvailableForTankTeleport(game, neighborIndex, [repeatingIndex]):
                            return neighborIndex
                        queue.append(neighborIndex)
        print("Not found available index, so teleport just to not available place to die.")
        return newIndex  # If no available index was found return newIndex anyway

    @staticmethod
    def checkIfIndexAvailableForTankTeleport(game, newIndex, blockedIndex):
        if (newIndex not in blockedIndex
                and game.tiles[newIndex] in [Tile.ROAD.value, Tile.FOREST.value, Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value, Tile.MINE.value]
                and newIndex not in game.occupiedTilesByEnemies
                and newIndex != game.getTileIndexFromPoint(game.firstTank.position)
                and (game.secondTank is None or newIndex != game.getTileIndexFromPoint(game.secondTank.position))):
            return True
        return False

    def teleportTankToMiddleTile(self):
        tileIndex = self.game.getTileIndexFromPoint(self.position)
        dx = (self.game.getTilePosition(tileIndex)[0] + self.game.tankCentralization) - self.position.x
        dy = (self.game.getTilePosition(tileIndex)[1] + self.game.tankCentralization) - self.position.y
        if abs(dx) > self.game.tileSize // 2:
            self.position = Vector(self.game.getTilePosition(tileIndex)[0] + self.game.tankCentralization + self.game.tileSize, self.game.getTilePosition(tileIndex)[1] + self.game.tankCentralization)
        elif abs(dy) > self.game.tileSize // 2:
            self.position = Vector(self.game.getTilePosition(tileIndex)[0] + self.game.tankCentralization, self.game.getTilePosition(tileIndex)[1] + self.game.tankCentralization + self.game.tileSize)
        else:
            self.position = Vector(self.game.getTilePosition(tileIndex)[0] + self.game.tankCentralization, self.game.getTilePosition(tileIndex)[1] + self.game.tankCentralization)

    def setControls(self):
        keyBindings = [(self.shoot, self.shootingControl), (lambda: self.change(Vector(0, 0)), self.stoppingControl)]
        for key in self.moveControls.keys():
            keyBindings.append((lambda k=key: self.keyPressHandler(k), key))
        Utils.activateKeys(keyBindings)

    def keyPressHandler(self, key):
        self.keysPressed[key] = True

    def tankMovement(self):
        for key, (tankSpeed, angle) in self.moveControls.items():
            if self.keysPressed[key]:
                if self.change(tankSpeed, angle) != -1:
                    for k in self.keysPressed:
                        self.keysPressed[k] = False

    def shoot(self):
        if self.game.gamePaused or not self.loaded or self.destroyed:
            return
        bullet = Bullet(self)
        self.game.bullets.append(bullet)
        self.loaded = False
        self.reloadingRemainingTime = self.reloadingTime
        self.updateReload()  # Start updating the reload bar
        if not self.railgunOn:
            self.game.laserShootSound.play()
        else:
            self.game.railgunSound.play()

    def updateReload(self):
        if self.game.gamePaused:
            Utils.safeOntimer(self.updateReload, 100)
            return
        if self.reloadingRemainingTime > 0:
            self.reloadingRemainingTime -= 100  # Decrease remaining time
            Utils.safeOntimer(self.updateReload, 100)  # Update every 100ms
        else:
            self.loaded = True
        if self.game.tiles[self.game.getTileIndexFromPoint(self.position + int(self.game.tileSize * 0.4))] != Tile.FOREST.value:
            Draw.drawReloadBar(self)

    # @Utils.debugPrintActualHpSituation
    def takeDamage(self, amount, reason):
        if not self.destroyed and not self.indestructible:
            self.hp -= amount
            if self.hp <= 0:
                self.destroyed = True
                self.deathReason = reason
                Draw.drawTank(self)
            self.game.damageSound.play()

    @staticmethod
    def tanksCollision(game, tankChecking, tankCheckingPosition=None, collisionThreshold=20):
        tankCheckingPosition = tankCheckingPosition or tankChecking.position
        for otherTank in game.allTanks:
            distanceBetweenTanks = abs(tankCheckingPosition - otherTank.position)
            if otherTank != tankChecking and distanceBetweenTanks < collisionThreshold and tankChecking.speed != Vector(0, 0):
                if not otherTank.destroyed:  # to improve gameplay collision with destroyed tank won't take damage
                    tankChecking.takeDamage(otherTank.attack//20, f"tank {tankChecking.tankId} collide with tank {otherTank.tankId}")
                    otherTank.takeDamage(tankChecking.attack//20, f"tank {otherTank.tankId} collide with tank {tankChecking.tankId}")
                tankChecking.speed = Vector(0, 0)
                return True
        return False
