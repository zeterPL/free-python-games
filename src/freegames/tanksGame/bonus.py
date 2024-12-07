from turtle import Turtle
import random
from enum import Enum
from freegames import vector
from draw import Draw
from tile import Tile


class BonusType(Enum):
    HEALTH = 1
    RELOAD = 2
    REGENERATION = 3
    SHIELD = 4
    ATTACK = 5
    SPEED = 6
    ALL = 7


class Bonus:
    def __init__(self, game, bonusType, position):
        self.game = game
        self.bonusType = bonusType
        self.position = position
        self.bonusTurtle = Turtle(visible=False)
        self.drawBonus()

    def drawBonus(self):
        Draw.drawCircle(self.bonusTurtle, self.position.x+self.game.tileSize//2, self.position.y+self.game.tileSize//2, self.game.tileSize*7//8, circleColor="light goldenrod yellow")
        if self.bonusType == BonusType.HEALTH:
            Draw.drawHearth(self.bonusTurtle, self.position.x + self.game.tileSize * 1 // 5, self.position.y + self.game.tileSize * 4 // 10, self.game.tileSize * 6 // 8, fillColor="red")
        elif self.bonusType == BonusType.RELOAD:
            Draw.drawSandglass(self.bonusTurtle, self.position.x, self.position.y, self.game.tileSize)
        elif self.bonusType == BonusType.REGENERATION:
            Draw.drawRectangle(self.bonusTurtle, self.position.x+self.game.tileSize//5, self.position.y+self.game.tileSize*2//5, self.game.tileSize*6//10, self.game.tileSize//5, fillColor="red", borderColor="red")
            Draw.drawRectangle(self.bonusTurtle, self.position.x+self.game.tileSize*2//5, self.position.y+self.game.tileSize//5, self.game.tileSize//5, self.game.tileSize * 6 // 10, fillColor="red", borderColor="red")
        elif self.bonusType == BonusType.SHIELD:
            Draw.drawShield(self.bonusTurtle, self.position.x, self.position.y, self.game.tileSize)
        elif self.bonusType == BonusType.ATTACK:
            Draw.drawSkull(self.bonusTurtle, self.position.x, self.position.y, self.game.tileSize)
        elif self.bonusType == BonusType.SPEED:
            Draw.drawChevronPattern(self.bonusTurtle, self.position.x+self.game.tileSize*3//10, self.position.y+self.game.tileSize*3//20, self.game.tileSize//6, self.game.tileSize//20, numberOfChevrons=3, fillColor="blue")
        elif self.bonusType == BonusType.ALL:
            Draw.drawStar(self.bonusTurtle, self.position.x+self.game.tileSize//8, self.position.y+self.game.tileSize*5//8, self.game.tileSize*6//8, fillColor="gold2", circuitColor="")

    @staticmethod
    def spawnBonus(game):
        if not game.gameRunning or not game.enableBonuses or len(game.bonuses) >= game.maxNumberOfBonuses:
            return
        bonusType = random.choice(list(BonusType))
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
        position = vector(x, y)
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
            tank.hp += 30
            if tank.hp > tank.maxHp:
                tank.maxHp = tank.hp
        elif bonusType == BonusType.RELOAD:
            tank.activeBonuses[BonusType.RELOAD] += amountTime or 10000
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
            tank.teleportToMiddleTile()
            tank.speedRatio = 2
            tank.change(tank.speed, tank.direction)
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
                    tank.hp = min(tank.maxHp, tank.hp + 0.1 * tank.maxHp)
                    tank.drawHP()
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
            tank.teleportToMiddleTile()
            tank.speedRatio = 1
            tank.change(tank.speed/2, tank.direction)
        tank.activeBonuses[bonusType] = 0

    @staticmethod
    def displayActiveBonuses(tank):
        tank.bonusDisplayTurtle.clear()
        if tank.destroyed:
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
                else:
                    bonusName = "Unknown"
                secondsLeft = remainingTime // 1000
                bonusTexts.append(f"{bonusName}: {secondsLeft}s")
        if bonusTexts:
            tank.bonusDisplayTurtle.write('\n'.join(bonusTexts), align="left", font=("Arial", 8, "normal"))
