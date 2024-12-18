from turtle import Turtle
import random
from enum import Enum
from .draw import Draw
from .tile import Tile
from .utils import Vector


class BonusType(Enum):
    HEALTH = 1
    RELOAD = 2
    REGENERATION = 3
    SHIELD = 4
    ATTACK = 5
    SPEED = 6
    RAILGUN = 7
    ALL = 8


class Bonus:
    def __init__(self, game, bonusType, position):
        self.game = game
        self.bonusType = bonusType
        self.position = position
        self.bonusTurtle = Turtle(visible=False)
        self.drawBonus()

    def drawBonus(self):
        x, y, t = self.position.x, self.position.y, self.game.tileSize
        Draw.drawCircle(self.bonusTurtle, x+t//2, y+t//2, t*7//8, circleColor="light goldenrod yellow")
        if self.bonusType == BonusType.HEALTH:
            Draw.drawHearth(self.bonusTurtle, x+t*1//5, y+t*4//10, t*6//8, fillColor="red")
        elif self.bonusType == BonusType.RELOAD:
            Draw.drawSandglass(self.bonusTurtle, x, y, t)
        elif self.bonusType == BonusType.REGENERATION:
            Draw.drawRectangle(self.bonusTurtle, x+t//5, y+t*2//5, t*6//10, t//5, fillColor="red", borderColor="red")
            Draw.drawRectangle(self.bonusTurtle, x+t*2//5, y+t//5, t//5, t*6//10, fillColor="red", borderColor="red")
        elif self.bonusType == BonusType.SHIELD:
            Draw.drawShield(self.bonusTurtle, x, y, t)
        elif self.bonusType == BonusType.ATTACK:
            Draw.drawSkull(self.bonusTurtle, x, y, t)
        elif self.bonusType == BonusType.SPEED:
            Draw.drawChevronPattern(self.bonusTurtle, x+t*3//10, y+t*3//20, t//6, t//20, numberOfChevrons=3, fillColor="blue")
        elif self.bonusType == BonusType.RAILGUN:
            Draw.drawLightning(self.bonusTurtle, x+t*3//10, y+t*3//20, t/40, fillColor="gold", circuitColor="black")
        elif self.bonusType == BonusType.ALL:
            Draw.drawStar(self.bonusTurtle, x+t//8, y+t*5//8, t*6//8, fillColor="gold2", circuitColor="")

    @staticmethod
    def spawnBonus(game):
        if not game.gameRunning or not game.enableBonuses or len(game.bonuses) >= game.maxNumberOfBonuses:
            return
        availableBonusTypes = list(BonusType)
        if game.uniqueBonuses:
            existingBonusTypes = {bonus.bonusType for bonus in game.bonuses}
            availableBonusTypes = [bonusType for bonusType in BonusType if bonusType not in existingBonusTypes]
        if not availableBonusTypes:
            return
        bonusType = random.choice(availableBonusTypes)
        if bonusType == BonusType.ALL and random.randint(0, 1):  # to decrease chance of OP bonus ALL
            bonusType = random.choice(availableBonusTypes)
        possibleIndexes = [index for index, value in enumerate(game.tiles) if value == Tile.ROAD.value]
        occupiedIndexes = set()
        for tank in game.allTanks:
            occupiedIndexes.add(game.getTileIndexFromPoint(tank.position))
        for bonus in game.bonuses:
            occupiedIndexes.add(game.getTileIndexFromPoint(bonus.position))
        possibleIndexes = [idx for idx in possibleIndexes if idx not in occupiedIndexes]
        if not possibleIndexes:
            return
        randomIndex = random.choice(possibleIndexes)
        x, y = game.getTilePosition(randomIndex)
        position = Vector(x, y)
        bonus = Bonus(game, bonusType, position)
        game.bonuses.append(bonus)

    @staticmethod
    def tankIsOnBonus(tank, bonus, tileSize):
        tankRect = (tank.position.x, tank.position.y, int(tileSize*0.8), int(tileSize*0.8))
        bonusRect = (bonus.position.x, bonus.position.y, tileSize, tileSize)
        return Bonus.tankBonusOverlap(tankRect, bonusRect)

    @staticmethod
    def tankBonusOverlap(tankParameters, bonusParameters):
        x1, y1, w1, h1 = tankParameters
        x2, y2, w2, h2 = bonusParameters
        return not (x1 + w1 <= x2 or x1 >= x2 + w2 or y1 + h1 <= y2 or y1 >= y2 + h2)

    @staticmethod
    def activateBonus(tank, bonusType, amountTime=0):
        if bonusType == BonusType.HEALTH:
            tank.hp = min(tank.hp + 30, 2 * tank.game.basicHp)  # maximum hp is double base Hp
            if tank.hp > tank.maxHp:
                tank.maxHp = tank.hp
        elif bonusType == BonusType.RELOAD:
            tank.activeBonuses[BonusType.RELOAD] += amountTime or 10000
            tank.reloadingRemainingTime = 0
            tank.reloadingTime = max(200, tank.reloadingTime // 2)
        elif bonusType == BonusType.REGENERATION:
            tank.activeBonuses[BonusType.REGENERATION] += amountTime or 10000
        elif bonusType == BonusType.SHIELD:
            tank.activeBonuses[BonusType.SHIELD] += amountTime or 4000
            tank.indestructible = True
        elif bonusType == BonusType.ATTACK:
            tank.activeBonuses[BonusType.ATTACK] += amountTime or 5000
            tank.attack *= 2
        elif bonusType == BonusType.SPEED:
            tank.activeBonuses[BonusType.SPEED] += amountTime or 10000
            tank.teleportTankToMiddleTile()
            tank.speedRatio = 2
            tank.change(tank.speed, tank.direction)
        elif bonusType == BonusType.RAILGUN:
            tank.activeBonuses[BonusType.RAILGUN] += amountTime or 7000
            tank.railgunOn = True
        elif bonusType == BonusType.ALL:
            tank.activeBonuses[BonusType.ALL] = 5000
            for bType in BonusType:
                if bType != BonusType.ALL:
                    Bonus.activateBonus(tank, bType, 5000)
        else:
            print("Bonus activation not implemented yet")

    @staticmethod
    def updateActiveBonuses(tank):
        for bonusType, remainingTime in tank.activeBonuses.items():
            if remainingTime > 0:
                tank.activeBonuses[bonusType] -= 1000
                if tank.activeBonuses[bonusType] <= 0:
                    Bonus.deactivateBonus(tank, bonusType)
                elif bonusType == BonusType.REGENERATION:
                    tank.hp = min(tank.maxHp, tank.hp + int(0.1 * tank.maxHp))
        Bonus.displayActiveBonuses(tank)

    @staticmethod
    def deactivateBonus(tank, bonusType):
        if bonusType == BonusType.RELOAD:
            tank.reloadingTime = 2000
        elif bonusType == BonusType.SHIELD:
            tank.indestructible = False
        elif bonusType == BonusType.ATTACK:
            tank.attack = tank.defaultAttack
        elif bonusType == BonusType.SPEED:
            tank.teleportTankToMiddleTile()
            tank.speedRatio = 1
            tank.change(tank.speed/2, tank.direction)
        elif bonusType == BonusType.RAILGUN:
            tank.railgunOn = False
        tank.activeBonuses[bonusType] = 0

    @staticmethod
    def displayActiveBonuses(tank):
        if tank.bonusDisplayTurtle is None:
            return
        tank.bonusDisplayTurtle.clear()
        if tank.destroyed or tank.game.tiles[tank.game.getTileIndexFromPoint(tank.position)] == Tile.FOREST.value:
            return
        x, y = tank.position.x, tank.position.y + tank.game.tileSize + 10
        tank.bonusDisplayTurtle.up()
        tank.bonusDisplayTurtle.goto(x, y)
        bonusTexts = []
        if tank.activeBonuses[BonusType.ALL]:
            bonusTexts.append(f"All bonuses: {tank.activeBonuses[BonusType.ALL] // 1000}s")
        else:
            for bonusType, remainingTime in tank.activeBonuses.items():
                if remainingTime <= 0:
                    continue
                if bonusType == BonusType.RELOAD:
                    bonusName = "Reload Speed"
                elif bonusType == BonusType.REGENERATION:
                    bonusName = "Health Regen"
                elif bonusType == BonusType.SHIELD:
                    bonusName = "INDESTRUCTIBLE"
                elif bonusType == BonusType.ATTACK:
                    bonusName = "Double damage"
                elif bonusType == BonusType.SPEED:
                    bonusName = "Double speed"
                elif bonusType == BonusType.RAILGUN:
                    bonusName = "RAILGUN"
                else:
                    bonusName = "Unknown"
                secondsLeft = remainingTime // 1000
                bonusTexts.append(f"{bonusName}: {secondsLeft}s")
        if bonusTexts:
            tank.bonusDisplayTurtle.write('\n'.join(bonusTexts), align="left", font=("Arial", 8, "normal"))
