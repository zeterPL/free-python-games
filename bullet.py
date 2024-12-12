from turtle import Turtle
from draw import Draw
from tile import Tile
from utils import Utils, Vector


class Bullet:
    def __init__(self, shooter, bulletSpeed=None):
        self.position = Vector(shooter.position.x + int(0.35 * shooter.game.tileSize), shooter.position.y + int(0.35 * shooter.game.tileSize))
        self.direction = shooter.direction
        self.bulletSpeed = bulletSpeed if bulletSpeed else shooter.game.tileSize // 2
        self.shooter = shooter
        self.bulletTurtle = Turtle(visible=False)

    def moveBullet(self):
        self.bulletTurtle.clear()
        bulletDirectionMovements = {
            90: Vector(5, 0),
            180: Vector(0, -5),
            270: Vector(-5, 0),
            0: Vector(0, 5)
        }
        if self.shooter.railgunOn:
            self.position.move(bulletDirectionMovements[self.direction] * self.bulletSpeed / 5)
            while not Bullet.checkBulletHit(self.shooter.game, self):
                self.position.move(bulletDirectionMovements[self.direction] * self.shooter.speedRatio / 5)
                laserTurtle = Turtle(visible=False)
                Draw.drawSquare(laserTurtle, self.position.x, self.position.y, int(0.1 * self.shooter.game.tileSize), "blue", "")
                Utils.safeOntimer(laserTurtle.clear, 200)
            return True
        for _ in range(self.bulletSpeed//5):
            self.position.move(bulletDirectionMovements[self.direction] * self.shooter.speedRatio)
            if Bullet.checkBulletHit(self.shooter.game, self):
                Draw.drawSquare(self.bulletTurtle, self.position.x, self.position.y, int(0.15 * self.shooter.game.tileSize), "red")
                return True
        Draw.drawSquare(self.bulletTurtle, self.position.x, self.position.y, int(0.15 * self.shooter.game.tileSize), "red")
        return False

    @staticmethod
    def checkBulletHit(game, bullet):
        tankSize = 0.8 * game.tileSize
        if bullet.position.x < -game.gameWidth // 2 or bullet.position.x > game.gameWidth // 2 or bullet.position.y < -game.gameHeight // 2 or bullet.position.y > game.gameHeight // 2:
            return True
        for tank in game.allTanks:
            if tank != bullet.shooter and tank.position.x <= bullet.position.x <= tank.position.x + tankSize and tank.position.y <= bullet.position.y <= tank.position.y + tankSize:
                Draw.drawExplosion(game, bullet.position.x, bullet.position.y)
                tank.takeDamage(bullet.shooter.attack, f"tank {tank.tankId} was shot down by tank {bullet.shooter.tankId}")
                return True
        bulletTileValue = game.tiles[game.getTileIndexFromPoint(bullet.position)]
        if bulletTileValue in [Tile.INDESTRUCTIBLE_BLOCK.value, Tile.DESTRUCTIBLE_BLOCK.value]:
            if bulletTileValue == Tile.DESTRUCTIBLE_BLOCK.value:
                game.tiles[game.getTileIndexFromPoint(bullet.position)] = Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value
                x, y = game.getTilePosition(game.getTileIndexFromPoint(bullet.position))
                Draw.drawSquare(game.mapTurtle, x, y, game.tileSize, squareColor=game.tileColors[Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value])
            return True
        return False

    @staticmethod
    def processBulletsMovementsAndCollisions(game):
        for bullet in game.bullets[:]:
            hit = bullet.moveBullet()
            if hit:
                bullet.bulletTurtle.clear()
                game.bullets.remove(bullet)
                game.explosionSound.play()
