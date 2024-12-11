from turtle import ontimer, Terminator, onkey


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
