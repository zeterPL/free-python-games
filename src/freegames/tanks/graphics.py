from turtle import Turtle

def drawSquare(turtleObject, x, y, size=20, squareColor=None,
               circuitColor="black"):
    """Rysuje kwadrat w punkcie (x, y)."""
    if circuitColor:
        turtleObject.color(circuitColor)
    else:
        turtleObject.color("")
    turtleObject.fillcolor(squareColor)
    turtleObject.up()
    turtleObject.goto(x, y)
    turtleObject.down()
    turtleObject.begin_fill()
    for _ in range(4):
        turtleObject.forward(size)
        turtleObject.left(90)
    turtleObject.end_fill()
