from turtle import ontimer, Terminator, onkey, setup
from tkinter import Tk


class Utils:
    @staticmethod
    def safeOntimer(function, delay, *args, **kwargs):
        try:
            ontimer(lambda: function(*args, **kwargs), delay)
        except Terminator:
            pass

    @staticmethod
    def conditionalExecution(condition, function, *args, **kwargs):
        conditionResult = condition() if callable(condition) else condition
        if conditionResult:
            return function(*args, **kwargs)

    @staticmethod
    def activateKeys(keyBindings):
        for func, key in keyBindings:
            onkey(func, key)

    @staticmethod
    def deactivateKeys(keys):
        for key in keys:
            onkey(None, key)  # type: ignore

    @staticmethod
    def writeText(turtleObject, x, y, message, textAlign="center", textFont=("Arial", 16, "bold"), textColor="black"):
        turtleObject.color(textColor)
        turtleObject.goto(x, y)
        turtleObject.write(message, align=textAlign, font=textFont)

    @staticmethod
    def debugPrintActualHpSituation(func):
        def wrapper(self, *args, **kwargs):
            if hasattr(self, 'tankId') and hasattr(self, 'hp') and self.tankId in [0, 1]:
                print(f"TankId={self.tankId} hp={self.hp} before damage:")
            result = func(self, *args, **kwargs)
            if hasattr(self, 'tankId') and hasattr(self, 'hp') and self.tankId in [0, 1]:
                print(f"TankId={self.tankId} hp={self.hp} after damage")
            return result
        return wrapper

    @staticmethod
    def setupGameOnScreen(gameWidth, gameHeight, centerGame=False, optionalStartX=0, optionalStartY=0):
        if centerGame:
            root = Tk()
            root.withdraw()
            screenWidth = root.winfo_screenwidth()
            screenHeight = root.winfo_screenheight()
            xPosition = (screenWidth - gameWidth) // 2
            yPosition = (screenHeight - gameHeight) // 2
            # print(f"{screenWidth=} {screenHeight=} {xPosition=} {yPosition=}")
            setup(width=gameWidth, height=gameHeight, startx=xPosition, starty=yPosition)
            root.destroy()
        else:
            startX = optionalStartX if optionalStartX is not None else 0
            startY = optionalStartY if optionalStartY is not None else 0
            setup(gameWidth, gameHeight, startX, startY)

