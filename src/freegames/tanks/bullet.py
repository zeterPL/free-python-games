from turtle import Turtle, ontimer
from freegames import vector
from graphics import drawSquare

class Bullet:
    def __init__(self, bulletPosition, direction, owner, bulletSpeed=10):
        self.position = vector(bulletPosition.x + 7, bulletPosition.y + 7)
        self.direction = direction
        self.bulletSpeed = bulletSpeed
        self.owner = owner
        self.bulletTurtle = Turtle(visible=False)  
        self.bulletTurtle.hideturtle()
        self.bulletTurtle.up()

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
        color = explosionColors[explosionIteration % len(explosionColors)]
        offsets = [
            (0, 0), (2, 2), (-2, -2), (-2, 2), (2, -2),
            (4, 0), (0, 4), (-4, 0), (0, -4),
        ]
        for dx, dy in offsets:
            drawSquare(
                self.bulletTurtle,
                x + dx * (explosionIteration + 1),
                y + dy * (explosionIteration + 1),
                2 + explosionIteration,
                color
            )
        if explosionIteration < maxIterations:
            ontimer(
                lambda: self.drawExplosion(x, y, explosionIteration + 1, maxIterations),
                150
            )
        else:
            ontimer(self.bulletTurtle.clear, 200)
