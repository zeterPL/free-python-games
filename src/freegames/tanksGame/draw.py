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
    def drawSingleChevron(turtleObject, x, y, size, fillColor="red", circuitColor=""):
        Draw.startDrawing(turtleObject, x, y, fillColor=fillColor, circuitColor=circuitColor)
        print(f"{turtleObject.position()=}")
        turtleObject.setheading(90)
        turtleObject.forward(size)
        turtleObject.right(45)
        turtleObject.forward(2*size)
        turtleObject.right(90)
        turtleObject.forward(2*size)
        print(f"{turtleObject.position()=}")
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
        # Draw.drawCircle(turtleObject, x+squareSize//2, y+squareSize*2//3, squareSize//2, skullColor)
        # Draw.drawRectangle(turtleObject, x+squareSize*7//20, y+squareSize*6//10, squareSize//10, squareSize//10, fillColor=eyesColor)
        # Draw.drawRectangle(turtleObject, x+squareSize*11//20, y+squareSize*6//10, squareSize//10, squareSize//10, fillColor=eyesColor)
        # Draw.drawRectangle(turtleObject, x+squareSize*19//40, y+squareSize*5//10, squareSize//20, squareSize//20, fillColor=eyesColor)
        # Draw.drawRectangle(turtleObject, x+squareSize*3//8, y+squareSize//4, squareSize//4, squareSize//6, fillColor=skullColor, borderColor="")

        # Draw.drawCircle(turtleObject, x+squareSize//2, y+squareSize//2, squareSize//2, skullColor)
        # Draw.drawRectangle(turtleObject, x+squareSize*3//8, y+squareSize//6, squareSize//4, squareSize//6, fillColor=skullColor, borderColor="")
        # Draw.drawRectangle(turtleObject, x+squareSize*7//20, y+squareSize*13//30, squareSize//10, squareSize//10, fillColor=eyesColor)
        # Draw.drawRectangle(turtleObject, x+squareSize*11//20, y+squareSize*13//30, squareSize//10, squareSize//10, fillColor=eyesColor)
        # Draw.drawRectangle(turtleObject, x+squareSize*19//40, y+squareSize//3, squareSize//20, squareSize//20, fillColor=eyesColor)

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
        # Draw.drawTriangle(turtleObject, x+squareSize*4//10, y+squareSize*7//10, squareSize//5, trianglePointedUp=False, fillColor=sandColor)
        # Draw.drawRectangle(turtleObject, x+squareSize*19//40, y+squareSize*5//16, squareSize//20, squareSize*3//16, fillColor=sandColor, borderColor="")
        Draw.drawTriangle(turtleObject, x+squareSize*4//10, y+squareSize*13//20, squareSize//5, trianglePointedUp=False, fillColor=sandColor)
        Draw.drawRectangle(turtleObject, x+squareSize*2//4, y+squareSize*5//16, squareSize//40, squareSize*3//16, fillColor=sandColor, borderColor="")
        Draw.drawRectangle(turtleObject, x+squareSize*15//32, y+squareSize*5//16, squareSize//8, squareSize*1//16, fillColor=sandColor, borderColor="")

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
