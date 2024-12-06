from turtle import Turtle
from enum import Enum
from draw import Draw


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
            # Draw.drawHearth(self.bonusTurtle, self.position.x + self.game.tileSize//8, self.position.y + self.game.tileSize*3//8, self.game.tileSize, fillColor="red", circuitColor="")
            Draw.drawHearth(self.bonusTurtle, self.position.x + self.game.tileSize * 1 // 5, self.position.y + self.game.tileSize * 4 // 10, self.game.tileSize * 6 // 8, fillColor="red")
        elif self.bonusType == BonusType.RELOAD:
            Draw.drawSandglass(self.bonusTurtle, self.position.x, self.position.y, self.game.tileSize)
        elif self.bonusType == BonusType.REGENERATION:
            # Draw.drawRectangle(self.bonusTurtle, self.position.x+self.game.tileSize*1//8, self.position.y+self.game.tileSize*3//8, self.game.tileSize*6//8, self.game.tileSize*2//8, fillColor="red", borderColor="red")
            # Draw.drawRectangle(self.bonusTurtle, self.position.x+self.game.tileSize*3//8, self.position.y+self.game.tileSize*1//8, self.game.tileSize*2//8, self.game.tileSize*6//8, fillColor="red", borderColor="red")
            Draw.drawRectangle(self.bonusTurtle, self.position.x+self.game.tileSize//5, self.position.y+self.game.tileSize*2//5, self.game.tileSize*6//10, self.game.tileSize//5, fillColor="red", borderColor="red")
            Draw.drawRectangle(self.bonusTurtle, self.position.x+self.game.tileSize*2//5, self.position.y+self.game.tileSize//5, self.game.tileSize//5, self.game.tileSize * 6 // 10, fillColor="red", borderColor="red")
        elif self.bonusType == BonusType.SHIELD:
            Draw.drawShield(self.bonusTurtle, self.position.x, self.position.y, self.game.tileSize)
        elif self.bonusType == BonusType.ATTACK:
            Draw.drawSkull(self.bonusTurtle, self.position.x, self.position.y, self.game.tileSize)
        elif self.bonusType == BonusType.SPEED:
            # Draw.drawChevronPattern(self.bonusTurtle, self.position.x+self.game.tileSize*9//40, self.position.y, self.game.tileSize//5, self.game.tileSize//20, numberOfChevrons=3, fillColor="blue")
            Draw.drawChevronPattern(self.bonusTurtle, self.position.x+self.game.tileSize*3//10, self.position.y+self.game.tileSize*3//20, self.game.tileSize//6, self.game.tileSize//20, numberOfChevrons=3, fillColor="blue")
        elif self.bonusType == BonusType.ALL:
            Draw.drawStar(self.bonusTurtle, self.position.x+self.game.tileSize//8, self.position.y+self.game.tileSize*5//8, self.game.tileSize*6//8, fillColor="gold2", circuitColor="")

        # Draw.drawTriangle(self.bonusTurtle, self.position.x+self.game.tileSize*5//16, self.position.y+self.game.tileSize*6//8, self.game.tileSize*3//8, trianglePointedUp=False, fillColor="SpringGreen2")
        # Draw.drawTriangle(self.bonusTurtle, self.position.x+self.game.tileSize*5//16, self.position.y+self.game.tileSize//4, self.game.tileSize*3//8, fillColor="SpringGreen2")
        # Draw.drawTriangle(self.bonusTurtle, self.position.x+self.game.tileSize*7//16, self.position.y+self.game.tileSize*5//8, self.game.tileSize//8, trianglePointedUp=False, fillColor="red")
        # Draw.drawRectangle(self.bonusTurtle, self.position.x+self.game.tileSize*19//40, self.position.y+self.game.tileSize*5//16, self.game.tileSize//20, self.game.tileSize*3//16, fillColor="red", borderColor="")

        # Draw.drawTriangle(self.bonusTurtle, self.position.x + self.game.tileSize * 5 // 16, self.position.y + self.game.tileSize * 6 // 8, self.game.tileSize * 3 // 8, trianglePointedUp=False, fillColor="SpringGreen2")
        # Draw.drawTriangle(self.bonusTurtle, self.position.x + self.game.tileSize * 5 // 16, self.position.y + self.game.tileSize // 4, self.game.tileSize * 3 // 8, fillColor="SpringGreen2")
        # Draw.drawTriangle(self.bonusTurtle, self.position.x + self.game.tileSize * 4 // 10, self.position.y + self.game.tileSize * 7 // 10, self.game.tileSize // 5, trianglePointedUp=False, fillColor="red")
        # Draw.drawRectangle(self.bonusTurtle, self.position.x + self.game.tileSize * 19 // 40, self.position.y + self.game.tileSize * 5 // 16, self.game.tileSize // 20, self.game.tileSize * 3 // 16, fillColor="red", borderColor="")
