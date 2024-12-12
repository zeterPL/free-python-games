from turtle import bgcolor, Turtle
from utils import Utils
from tile import Tile


class Draw:
    @staticmethod
    def startDrawing(turtleObject, x, y, fillColor="", circuitColor="black", pensize=1):
        turtleObject.color(circuitColor)
        turtleObject.fillcolor(fillColor)
        turtleObject.pensize(pensize)
        turtleObject.up()
        turtleObject.goto(x, y)
        turtleObject.down()
        turtleObject.goto(x, y)  # Without it sometimes it's bugging and don't draw first circle
        turtleObject.begin_fill()

    @staticmethod
    def endDrawing(turtleObject):
        turtleObject.end_fill()
        turtleObject.up()

    @staticmethod
    def drawSquare(turtleObject, x, y, size, squareColor=None, circuitColor="black"):
        Draw.startDrawing(turtleObject, x, y, fillColor=squareColor, circuitColor=circuitColor)
        for count in range(4):
            turtleObject.forward(size)
            turtleObject.left(90)
        Draw.endDrawing(turtleObject)

    @staticmethod
    def drawRectangle(turtleObject, x, y, rectangleWidth, rectangleHeight, fillColor="white", borderColor="black", startDrawingFromMiddle=False, borderThickness=1):
        if startDrawingFromMiddle:
            x = x - rectangleWidth // 2
            y = y - rectangleHeight // 2
        Draw.startDrawing(turtleObject, x, y, fillColor=fillColor, circuitColor=borderColor, pensize=borderThickness)
        for _ in range(2):
            turtleObject.forward(rectangleWidth)
            turtleObject.left(90)
            turtleObject.forward(rectangleHeight)
            turtleObject.left(90)
        Draw.endDrawing(turtleObject)

    @staticmethod
    def drawCircle(turtleObject, x, y, circleSize, circleColor):
        Draw.startDrawing(turtleObject, x, y, fillColor=circleColor)
        turtleObject.dot(circleSize, circleColor)
        Draw.endDrawing(turtleObject)

    @staticmethod
    def drawHearth(turtleObject, x, y, size, fillColor="red", circuitColor="red"):
        Draw.startDrawing(turtleObject, x, y, fillColor=fillColor, circuitColor=circuitColor)
        turtleObject.left(140)
        turtleObject.circle(-size//4, 200)
        turtleObject.setheading(60)
        turtleObject.circle(-size//4, 200)
        turtleObject.forward(size//2)
        Draw.endDrawing(turtleObject)

    @staticmethod
    def drawStar(turtleObject, x, y, size, fillColor="gold", circuitColor=""):
        Draw.startDrawing(turtleObject, x, y, fillColor=fillColor, circuitColor=circuitColor)
        for _ in range(5):
            turtleObject.forward(size)
            turtleObject.right(144)
        Draw.endDrawing(turtleObject)

    @staticmethod
    def drawSingleChevron(turtleObject, x, y, size, fillColor="red", circuitColor=""):
        Draw.startDrawing(turtleObject, x, y, fillColor=fillColor, circuitColor=circuitColor)
        turtleObject.setheading(90)
        turtleObject.forward(size)
        turtleObject.right(45)
        turtleObject.forward(2*size)
        turtleObject.right(90)
        turtleObject.forward(2*size)
        turtleObject.right(45)
        turtleObject.forward(size)
        turtleObject.right(135)
        turtleObject.forward(2*size)
        turtleObject.left(90)
        turtleObject.forward(2*size)
        Draw.endDrawing(turtleObject)

    @staticmethod
    def drawChevronPattern(turtleObject, x, y, size, spaceBetweenChevrons, numberOfChevrons, fillColor="red", circuitColor=""):
        for _ in range(numberOfChevrons):
            Draw.drawSingleChevron(turtleObject, x, y, size, fillColor, circuitColor)
            y += size+spaceBetweenChevrons

    @staticmethod
    def drawSkull(turtleObject, x, y, squareSize, skullColor="light grey", eyesColor="black"):
        Draw.drawCircle(turtleObject, x+squareSize//2, y+squareSize*6//10, squareSize//2, skullColor)
        Draw.drawRectangle(turtleObject, x+squareSize*7//20, y+squareSize*43//80, squareSize//10, squareSize//10, fillColor=eyesColor)
        Draw.drawRectangle(turtleObject, x+squareSize*11//20, y+squareSize*43//80, squareSize//10, squareSize//10, fillColor=eyesColor)
        Draw.drawRectangle(turtleObject, x+squareSize*19//40, y+squareSize*7//16, squareSize//20, squareSize//20, fillColor=eyesColor)
        Draw.drawRectangle(turtleObject, x+squareSize*3//8, y+squareSize//4, squareSize//4, squareSize//6, fillColor=skullColor, borderColor="")

    @staticmethod
    def drawShield(turtleObject, x, y, squareSize, outerShieldColor="SlateGray4", innerShieldColor="saddle brown"):
        Draw.drawRectangle(turtleObject, x+squareSize*3//10, y+squareSize*7//20, squareSize*4//10, squareSize*4//10, fillColor=outerShieldColor, borderColor="")
        Draw.drawCircle(turtleObject, x+squareSize//2, y+squareSize*4//10, squareSize*4//10, circleColor=outerShieldColor)
        Draw.drawRectangle(turtleObject, x+squareSize*7//20, y+squareSize*8//20, squareSize*3//10, squareSize*3//10, fillColor=innerShieldColor, borderColor="")
        Draw.drawCircle(turtleObject, x+squareSize//2, y+squareSize*4//10, squareSize*3//10, circleColor=innerShieldColor)

    @staticmethod
    def drawSandglass(turtleObject, x, y, squareSize, glassColor="SpringGreen2", sandColor="red"):
        Draw.drawTriangle(turtleObject, x+squareSize*5//16, y+squareSize*6//8, squareSize*3//8, trianglePointedUp=False, fillColor=glassColor)
        Draw.drawTriangle(turtleObject, x+squareSize*5//16, y+squareSize//4, squareSize*3//8, fillColor=glassColor)
        Draw.drawTriangle(turtleObject, x+squareSize*4//10, y+squareSize*13//20, squareSize//5, trianglePointedUp=False, fillColor=sandColor)
        Draw.drawRectangle(turtleObject, x+squareSize*2//4, y+squareSize*5//16, squareSize//40, squareSize*3//16, fillColor=sandColor, borderColor="")
        Draw.drawRectangle(turtleObject, x+squareSize*15//32, y+squareSize*5//16, squareSize//8, squareSize*1//16, fillColor=sandColor, borderColor="")

    @staticmethod
    def drawLightning(turtleObject, x, y, t, fillColor="gold", circuitColor="black"):
        Draw.startDrawing(turtleObject, x, y, fillColor=fillColor, circuitColor=circuitColor)
        x, y = x + 5 * t, y + 12 * t
        turtleObject.goto(x, y)
        x, y = x - 4 * t, y
        turtleObject.goto(x, y)
        x, y = x + 3 * t, y + 12 * t
        turtleObject.goto(x, y)
        x, y = x + 14 * t, y
        turtleObject.goto(x, y)
        x, y = x - 9 * t, y - 10 * t
        turtleObject.goto(x, y)
        x, y = x + 5 * t, y
        turtleObject.goto(x, y)
        x, y = x - 14 * t, y - 14 * t
        turtleObject.goto(x, y)
        Draw.endDrawing(turtleObject)

    @staticmethod
    def drawTriangle(turtleObject, x, y, sideSize, trianglePointedUp=True, fillColor="red", circuitColor=""):
        Draw.startDrawing(turtleObject, x, y, fillColor=fillColor, circuitColor=circuitColor)
        for _ in range(3):
            turtleObject.forward(sideSize)
            if trianglePointedUp:
                turtleObject.left(120)
            else:
                turtleObject.right(120)
        Draw.endDrawing(turtleObject)

    @staticmethod
    def drawPortal(turtleObject, x, y, portalSize, numberOfLayers, portalColor, backgroundColor):
        for layer in range(numberOfLayers):
            Draw.drawCircle(turtleObject, x, y, portalSize, portalColor)
            Draw.drawCircle(turtleObject, x, y, int(portalSize - 2), backgroundColor)
            portalSize = max(int(0.5 * portalSize), 4)

    @staticmethod
    def drawBoard(game):
        Draw.drawSquare(game.mapTurtle, -game.gameWidth, -game.gameHeight, 2 * (game.gameWidth + game.gameHeight), "black")
        bgcolor('black')
        for index in range(len(game.tiles)):
            tile = game.tiles[index]
            if tile > 0:
                x, y = game.getTilePosition(index)
                tileColor = game.tileColors[tile]
                Draw.drawSquare(game.mapTurtle, x, y, game.tileSize, squareColor=tileColor)
                if tile == Tile.MINE.value:  # drawing mines
                    Draw.drawCircle(game.minesTurtle, x + game.tileSize // 2, y + game.tileSize // 2, game.tileSize // 2, "black")
                if tile == Tile.TELEPORT.value:  # drawing portals
                    Draw.drawPortal(game.mapTurtle, x + game.tileSize // 2, y + game.tileSize // 2, game.tileSize * 0.8, 5, "purple", "black")
        Draw.drawRectangle(game.mapTurtle, 0, 0, game.rows * game.tileSize, game.columns * game.tileSize, "", "white", True)  # drawing white circuit around board

    @staticmethod
    def drawExplosion(game, x, y, drawingTurtle=None, explosionIteration=0, maxIterations=3):
        drawingTurtle = drawingTurtle or Turtle(visible=False)
        explosionColors = ["red", "yellow", "orange"]
        explosionColor = explosionColors[explosionIteration % len(explosionColors)]
        t = game.tileSize // 20
        offsets = [(0, 0), (2 * t, 2 * t), (-2 * t, -2 * t), (-2 * t, 2 * t), (2 * t, -2 * t), (4 * t, 0), (0, 4 * t), (-4 * t, 0), (0, -4 * t)]
        for dx, dy in offsets:
            Draw.drawSquare(drawingTurtle, x + dx * (explosionIteration + t), y + dy * (explosionIteration + t), 2 * t + explosionIteration, explosionColor)
        if explosionIteration < maxIterations:
            Utils.safeOntimer(lambda: Draw.drawExplosion(game, x, y, drawingTurtle, explosionIteration + 1, maxIterations), 150)
        else:
            Utils.safeOntimer(drawingTurtle.clear, 200)

    @staticmethod
    def drawModalMessage(game, message, subMessage, x=0, y=0, modalWidth=350, modalHeight=120):
        game.messageTurtle.clear()
        Draw.drawRectangle(game.messageTurtle, x, y, modalWidth, modalHeight, "white", "black", True)
        Utils.writeText(game.messageTurtle, 0, 0, message)
        Utils.writeText(game.messageTurtle, 0, -40, subMessage, textFont=("Arial", 12, "normal"))

    @staticmethod
    def drawHP(tank, hpColor="red", bgColor="black"):
        tank.hpTurtle.clear()
        if tank.hp > 0:
            x, y = tank.position - tank.game.tankCentralization
            barWidth = tank.game.tileSize
            barHeight = tank.game.tileSize // 20 * 3
            baseHpRatio = min(tank.hp / tank.game.basicHp, 1)
            Draw.drawRectangle(tank.hpTurtle, x, y + tank.game.tileSize*1.2, barWidth, barHeight, bgColor)
            Draw.drawRectangle(tank.hpTurtle, x, y + tank.game.tileSize*1.2, barWidth*baseHpRatio, barHeight, hpColor)
            if tank.hp > tank.game.basicHp:
                additionalHpRatio = (tank.hp - tank.game.basicHp) / tank.game.basicHp
                Draw.drawRectangle(tank.hpTurtle, x, y + tank.game.tileSize * 1.2, barWidth*additionalHpRatio, barHeight, "purple", "")

    @staticmethod
    def drawReloadBar(tank, reloadColor="gold", bgColor="black"):
        if tank.reloadTurtle is None:
            return
        tank.reloadTurtle.clear()
        if tank.hp > 0:
            x, y = tank.position - tank.game.tankCentralization
            barWidth = tank.game.tileSize
            barHeight = tank.game.tileSize // 20 * 3
            reloadRatio = max(1 - (tank.reloadingRemainingTime / tank.reloadingTime), 0) if tank.reloadingTime > 0 else 1
            Draw.drawRectangle(tank.reloadTurtle, x, y + tank.game.tileSize, barWidth, barHeight, bgColor)
            Draw.drawRectangle(tank.reloadTurtle, x, y + tank.game.tileSize, barWidth * reloadRatio, barHeight, reloadColor)

    @staticmethod
    def drawTank(tank):
        tank.tankTurtle.clear()
        x, y = tank.position
        angle = tank.direction
        t = tank.game.tileSize // 20
        """Draw tracks."""
        trackOffsets = {
            0: [(0, 0), (0, 4 * t), (0, 8 * t), (0, 12 * t), (12 * t, 0), (12 * t, 4 * t), (12 * t, 8 * t), (12 * t, 12 * t)],
            90: [(0, 0), (4 * t, 0), (8 * t, 0), (12 * t, 0), (0, 12 * t), (4 * t, 12 * t), (8 * t, 12 * t), (12 * t, 12 * t)],
            180: [(0, 0), (0, 4 * t), (0, 8 * t), (0, 12 * t), (12 * t, 0), (12 * t, 4 * t), (12 * t, 8 * t), (12 * t, 12 * t)],
            270: [(0, 0), (4 * t, 0), (8 * t, 0), (12 * t, 0), (0, 12 * t), (4 * t, 12 * t), (8 * t, 12 * t), (12 * t, 12 * t)]
        }
        for index, (dx, dy) in enumerate(trackOffsets[angle]):
            Draw.drawSquare(tank.tankTurtle, x + dx, y + dy, 4 * t, tank.tankColor)
            if tank.destroyed and index in [0, t, 5, t]:
                Draw.drawSquare(tank.tankTurtle, x + dx, y + dy, 4 * t, "black")
        """Draw hull."""
        hullOffsets = {0: (4 * t, t), 90: (t, 4 * t), 180: (4 * t, 7 * t), 270: (7 * t, 4 * t)}
        Draw.drawSquare(tank.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 8 * t, tank.tankColor)
        if tank.destroyed:
            Draw.drawSquare(tank.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1], 2 * t, "black", "")
            Draw.drawSquare(tank.tankTurtle, x + hullOffsets[angle][0] + 4 * t, y + hullOffsets[angle][1], 2 * t, "black", "")
            Draw.drawSquare(tank.tankTurtle, x + hullOffsets[angle][0], y + hullOffsets[angle][1] + 4 * t, 2 * t, "black", "")
            Draw.drawSquare(tank.tankTurtle, x + hullOffsets[angle][0] + 2 * t, y + hullOffsets[angle][1] + 2 * t, 2 * t, "black", "")
            Draw.drawSquare(tank.tankTurtle, x + hullOffsets[angle][0] + 6 * t, y + hullOffsets[angle][1] + 4 * t, 2 * t, "black", "")
        """Draw cannon."""
        cannonOffsets = {
            0: [(7 * t, 9 * t), (7 * t, 11 * t), (7 * t, 13 * t)],
            90: [(9 * t, 7 * t), (11 * t, 7 * t), (13 * t, 7 * t)],
            180: [(7 * t, 5 * t), (7 * t, 3 * t), (7 * t, t)],
            270: [(5 * t, 7 * t), (3 * t, 7 * t), (t, 7 * t)]
        }
        for dx, dy in cannonOffsets[angle]:
            Draw.drawSquare(tank.tankTurtle, x + dx, y + dy, 2 * t, tank.tankColor)
        if tank.destroyed:
            Draw.drawSquare(tank.tankTurtle, x + cannonOffsets[angle][1][0], y + cannonOffsets[angle][1][1], 2 * t, "black")
        Draw.drawHP(tank)
        Draw.drawReloadBar(tank)
