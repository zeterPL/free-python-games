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
    def __init__(self, game, bonus_type, position):
        self.game = game
        self.bonus_type = bonus_type
        self.position = position
        self.bonusTurtle = Turtle(visible=False)
        self.drawBonus()

    def drawBonus(self):
        # x, y = self.position.x + self.game.tileSize // 2, self.position.y + self.game.tileSize // 2
        # if self.bonus_type == BonusType.HEALTH:
        #     color = "red"
        #     shape = "circle"
        # elif self.bonus_type == BonusType.SHOOTING_SPEED:
        #     color = "blue"
        #     shape = "square"
        # else:
        #     color = "white"
        #     shape = "circle"
        # self.bonusTurtle.up()
        # self.bonusTurtle.goto(x, y)
        # self.bonusTurtle.shape(shape)
        # self.bonusTurtle.color(color)
        # self.bonusTurtle.shapesize(self.game.tileSize / 20)
        # self.bonusTurtle.showturtle()

        # self.game.drawStar(self.bonusTurtle, self.position.x+1, self.position.y+self.game.tileSize*5//8, self.game.tileSize-1, fillColor="gold2", circuitColor="")
        # self.game.drawHearth(self.bonusTurtle, self.position.x + self.game.tileSize//8, self.position.y + self.game.tileSize*3//8, self.game.tileSize, fillColor="red", circuitColor="")

        Draw.drawRectangle(self.bonusTurtle, self.position.x+self.game.tileSize*1//8, self.position.y+self.game.tileSize*3//8, self.game.tileSize*6//8, self.game.tileSize*2//8, fillColor="red", borderColor="red")
        Draw.drawRectangle(self.bonusTurtle, self.position.x+self.game.tileSize*3//8, self.position.y+self.game.tileSize*1//8, self.game.tileSize*2//8, self.game.tileSize*6//8, fillColor="red", borderColor="red")
