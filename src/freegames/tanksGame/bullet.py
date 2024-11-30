from turtle import Turtle
from freegames import vector


class Bullet:
    def __init__(self, shooter, bulletSpeed=None):
        self.position = vector(shooter.position.x + int(0.35 * shooter.game.tileSize), shooter.position.y + int(0.35 * shooter.game.tileSize))
        self.direction = shooter.direction
        self.bulletSpeed = bulletSpeed if bulletSpeed else shooter.game.tileSize // 2
        self.shooter = shooter
        self.bulletTurtle = Turtle(visible=False)
    #
    # def __del__(self):
    #     self.bulletTurtle.clear()
    #     del self.bulletTurtle

    def moveBullet(self):
        self.bulletTurtle.clear()
        bulletDirectionMovements = {
            90: vector(self.bulletSpeed, 0),
            180: vector(0, -self.bulletSpeed),
            270: vector(-self.bulletSpeed, 0),
            0: vector(0, self.bulletSpeed)
        }
        self.position.move(bulletDirectionMovements[self.direction])
        self.shooter.game.drawSquare(self.bulletTurtle, self.position.x, self.position.y, int(0.15 * self.shooter.game.tileSize), "red")
