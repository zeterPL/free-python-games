class Draw:
    @staticmethod
    def startDrawing(turtleObject, x, y, fillColor="", circuitColor="black", pensize=1):
        turtleObject.color(circuitColor)
        turtleObject.fillcolor(fillColor)
        turtleObject.pensize(pensize)
        turtleObject.up()
        turtleObject.goto(x, y)
        turtleObject.down()
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
        Draw.startDrawing(turtleObject, x, y)
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
    def drawTriangle(turtleObject, x, y, sideSize, trianglePointedUp=False, fillColor="red", circuitColor=""):
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
