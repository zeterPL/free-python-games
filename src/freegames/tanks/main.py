from turtle import (setup, hideturtle, tracer, listen, onkey, update,
                    ontimer, done, bgcolor, Turtle, mainloop)
from tank import Tank
from bullet import Bullet
from tiles import tiles, tileColors, getTilePosition, Tile
from graphics import drawSquare
from game_utils import offset
from constants import tankCentralization
from freegames import vector

bullets = []
gameRunning = True

mapTurtle = Turtle(visible=False)
tankTurtle = Turtle(visible=False)
gameOverTurtle = Turtle(visible=False)
gameOverTurtle.up()
gameOverTurtle.hideturtle()
gameOverTurtle.color("red")

controls1 = {
    "Up": (vector(0, 5), 0),
    "Down": (vector(0, -5), 180),
    "Left": (vector(-5, 0), 270),
    "Right": (vector(5, 0), 90)
}
controls2 = {
    "w": (vector(0, 5), 0),
    "s": (vector(0, -5), 180),
    "a": (vector(-5, 0), 270),
    "d": (vector(5, 0), 90)
}

def drawBoard():
    bgcolor('black')
    for index, tile in enumerate(tiles):
        if tile > 0:
            x, y = getTilePosition(index)
            tileColor = tileColors[tile]
            drawSquare(mapTurtle, x, y, squareColor=tileColor)
            if tile == Tile.MINE.value:
                mapTurtle.goto(x + 10, y + 10)
                mapTurtle.dot(10, "black")

def startGame():
    global firstTank, secondTank, bullets, gameRunning
    bullets = []
    gameRunning = True
    tankTurtle.clear()
    mapTurtle.clear()
    gameOverTurtle.clear()
    firstTank = Tank(40 + tankCentralization, 0 + tankCentralization,
                     "dark green", 1, controls1, "Control_R", "Return", tankTurtle)
    secondTank = Tank(-100 + tankCentralization, 100 + tankCentralization,
                      "slate gray", 2, controls2, "Control_L", "Shift_L", tankTurtle)
    drawBoard()
    move()

def drawModalBackground(x, y, width, height, color="white",
                        border_color="black"):
    gameOverTurtle.color(border_color)
    gameOverTurtle.fillcolor(color)
    gameOverTurtle.penup()
    gameOverTurtle.goto(x - width / 2, y - height / 2)
    gameOverTurtle.pendown()
    gameOverTurtle.begin_fill()
    for _ in range(2):
        gameOverTurtle.forward(width)
        gameOverTurtle.left(90)
        gameOverTurtle.forward(height)
        gameOverTurtle.left(90)
    gameOverTurtle.end_fill()
    gameOverTurtle.penup()

def hideGameElements():
    tankTurtle.clear()
    for bullet in bullets:
        bullet.bulletTurtle.clear()
    firstTank.hpTurtle.clear()
    secondTank.hpTurtle.clear()

def stopGame(tanks, reason):
    global gameRunning
    gameRunning = False
    hideGameElements()
    drawModalBackground(0, 0, 300, 150)
    gameOverTurtle.goto(0, 20)
    message = f"Koniec Gry!\n{reason}"
    gameOverTurtle.write(message, align="center",
                         font=("Arial", 16, "bold"))
    gameOverTurtle.goto(0, -40)
    gameOverTurtle.write("Naciśnij 'R', aby zrestartować", align="center",
                         font=("Arial", 12, "normal"))
    for tank in tanks:
        tank.drawTank(True)
        print(f"Gra zakończona, czołg {tank.tankId} przegrał: {reason}.")

def tanksCollision(tank1, tank2, collisionThreshold=20):
    distanceBetweenTanks = abs(tank1.position - tank2.position)
    if distanceBetweenTanks < collisionThreshold:
        stopGame([tank1, tank2], "Kolizja czołgów. Wszyscy zginęli.")

def checkBulletCollision(bullet, tanks, tankSize=16):
    for tank in tanks:
        if (tank != bullet.owner and
            tank.position.x <= bullet.position.x <= tank.position.x + tankSize
            and tank.position.y <= bullet.position.y <= tank.position.y + tankSize):
            bullet.drawExplosion(bullet.position.x, bullet.position.y)
            tank.takeDamage()
            return True
    bulletTileValue = tiles[offset(bullet.position)]
    if bulletTileValue in [Tile.INDESTRUCTIBLE_BLOCK.value,
                           Tile.DESTRUCTIBLE_BLOCK.value]:
        bullet.bulletTurtle.clear()
        if bulletTileValue == Tile.DESTRUCTIBLE_BLOCK.value:
            tiles[offset(bullet.position)] = Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value
            x, y = getTilePosition(offset(bullet.position))
            drawSquare(mapTurtle, x, y,
                       squareColor=tileColors[Tile.DESTROYED_DESTRUCTIBLE_BLOCK.value])
        return True
    return False

def stopGame(tanks, reason):
    global gameRunning
    gameRunning = False
    hideGameElements()
    drawModalBackground(0, 0, 300, 150)
    gameOverTurtle.goto(0, 20)
    message = f"Koniec Gry!\n{reason}"
    gameOverTurtle.write(message, align="center",
                         font=("Arial", 16, "bold"))
    gameOverTurtle.goto(0, -40)
    gameOverTurtle.write("Naciśnij 'R', aby zrestartować", align="center",
                         font=("Arial", 12, "normal"))
    for tank in tanks:
        tank.drawTank(True)
        print(f"Gra zakończona, czołg {tank.tankId} przegrał: {reason}.")

def move():
    if not gameRunning:
        return
    tankTurtle.clear()
    firstTank.tankMovement()
    secondTank.tankMovement()
    firstTank.move()
    secondTank.move()
    firstTank.drawHP()
    secondTank.drawHP()
    tanksCollision(firstTank, secondTank)
    for bullet in bullets[:]:
        bullet.move()
        if checkBulletCollision(bullet, [firstTank, secondTank]):
            bullets.remove(bullet)
    update()
    if gameRunning:
        ontimer(move, 100)

def setupRestart():
    onkey(startGame, "r")
    listen()

setup(420, 420, 500, 100)
hideturtle()
tracer(False)
setupRestart()
startGame()
mainloop()
