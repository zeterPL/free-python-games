from turtle import ontimer, Terminator, onkey, setup, Screen
from tkinter import Tk
import collections.abc
import math


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
        screen = Screen()
        screen.title("Tanks Battle Game")
        screen._root.iconbitmap("assets/icons/tank.ico")

    @staticmethod
    def floor(value, size, offset=200):
        """Floor of `value` given `size` and `offset`.

        The floor function is best understood with a diagram of the number line::

             -200  -100    0    100   200
            <--|--x--|-----|--y--|--z--|-->

        The number line shown has offset 200 denoted by the left-hand tick mark at
        -200 and size 100 denoted by the tick marks at -100, 0, 100, and 200. The
        floor of a value is the left-hand tick mark of the range where it lies. So
        for the points show above: ``floor(x)`` is -200, ``floor(y)`` is 0, and
        ``floor(z)`` is 100.

        >>> Utils.floor(10, 100)
        0.0
        >>> Utils.floor(120, 100)
        100.0
        >>> Utils.floor(-10, 100)
        -100.0
        >>> Utils.floor(-150, 100)
        -200.0
        >>> Utils.floor(50, 167)
        -33.0
        """
        return float(((value + offset) // size) * size - offset)


class Vector(collections.abc.Sequence):
    """Two-dimensional Vector.

    Vectors can be modified in-place.

    >>> v = Vector(0, 1)
    >>> v.move(1)
    >>> v
    Vector(1, 2)
    >>> v.rotate(90)
    >>> v
    Vector(-2.0, 1.0)

    """

    # pylint: disable=invalid-name
    PRECISION = 6

    __slots__ = ('_x', '_y', '_hash')

    def __init__(self, x, y):
        """Initialize Vector with coordinates: x, y.

        >>> v = Vector(1, 2)
        >>> v.x
        1
        >>> v.y
        2

        """
        self._hash = None
        self._x = round(x, self.PRECISION)
        self._y = round(y, self.PRECISION)

    @property
    def x(self):
        """X-axis component of Vector.

        >>> v = Vector(1, 2)
        >>> v.x
        1
        >>> v.x = 3
        >>> v.x
        3

        """
        return self._x

    @x.setter
    def x(self, value):
        if self._hash is not None:
            raise ValueError('cannot set x after hashing')
        self._x = round(value, self.PRECISION)

    @property
    def y(self):
        """Y-axis component of Vector.

        >>> v = Vector(1, 2)
        >>> v.y
        2
        >>> v.y = 5
        >>> v.y
        5

        """
        return self._y

    @y.setter
    def y(self, value):
        if self._hash is not None:
            raise ValueError('cannot set y after hashing')
        self._y = round(value, self.PRECISION)

    def __hash__(self):
        """v.__hash__() -> hash(v)

        >>> v = Vector(1, 2)
        >>> h = hash(v)
        >>> v.x = 2
        Traceback (most recent call last):
            ...
        ValueError: cannot set x after hashing

        """
        if self._hash is None:
            pair = (self.x, self.y)
            self._hash = hash(pair)
        return self._hash

    def set(self, other):
        """Set Vector x, y to other x, y.

        >>> a = Vector(0, 0)
        >>> b = Vector(1, 2)
        >>> a.set(b)
        >>> a
        Vector(1, 2)

        """
        self.x = other.x
        self.y = other.y

    def __len__(self):
        """v.__len__() -> len(v)

        >>> v = Vector(1, 2)
        >>> len(v)
        2

        """
        return 2

    def __getitem__(self, index):
        """v.__getitem__(v, i) -> v[i]

        >>> v = Vector(3, 4)
        >>> v[0]
        3
        >>> v[1]
        4
        >>> v[2]
        Traceback (most recent call last):
            ...
        IndexError

        """
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError

    def copy(self):
        """Return copy of Vector.

        >>> v = Vector(1, 2)
        >>> w = v.copy()
        >>> v is w
        False

        """
        type_self = type(self)
        return type_self(self.x, self.y)

    def __eq__(self, other):
        """v.__eq__(w) -> v == w

        >>> v = Vector(1, 2)
        >>> w = Vector(1, 2)
        >>> v == w
        True

        """
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):
        """v.__ne__(w) -> v != w

        >>> v = Vector(1, 2)
        >>> w = Vector(3, 4)
        >>> v != w
        True

        """
        if isinstance(other, Vector):
            return self.x != other.x or self.y != other.y
        return NotImplemented

    def __iadd__(self, other):
        """v.__iadd__(w) -> v += w

        >>> v = Vector(1, 2)
        >>> w = Vector(3, 4)
        >>> v += w
        >>> v
        Vector(4, 6)
        >>> v += 1
        >>> v
        Vector(5, 7)

        """
        if self._hash is not None:
            raise ValueError('cannot add Vector after hashing')
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        return self

    def __add__(self, other):
        """v.__add__(w) -> v + w

        >>> v = Vector(1, 2)
        >>> w = Vector(3, 4)
        >>> v + w
        Vector(4, 6)
        >>> v + 1
        Vector(2, 3)
        >>> 2.0 + v
        Vector(3.0, 4.0)

        """
        copy = self.copy()
        return copy.__iadd__(other)

    __radd__ = __add__

    def move(self, other):
        """Move Vector by other (in-place).

        >>> v = Vector(1, 2)
        >>> w = Vector(3, 4)
        >>> v.move(w)
        >>> v
        Vector(4, 6)
        >>> v.move(3)
        >>> v
        Vector(7, 9)

        """
        self.__iadd__(other)

    def __isub__(self, other):
        """v.__isub__(w) -> v -= w

        >>> v = Vector(1, 2)
        >>> w = Vector(3, 4)
        >>> v -= w
        >>> v
        Vector(-2, -2)
        >>> v -= 1
        >>> v
        Vector(-3, -3)

        """
        if self._hash is not None:
            raise ValueError('cannot subtract Vector after hashing')
        if isinstance(other, Vector):
            self.x -= other.x
            self.y -= other.y
        else:
            self.x -= other
            self.y -= other
        return self

    def __sub__(self, other):
        """v.__sub__(w) -> v - w

        >>> v = Vector(1, 2)
        >>> w = Vector(3, 4)
        >>> v - w
        Vector(-2, -2)
        >>> v - 1
        Vector(0, 1)

        """
        copy = self.copy()
        return copy.__isub__(other)

    def __imul__(self, other):
        """v.__imul__(w) -> v *= w

        >>> v = Vector(1, 2)
        >>> w = Vector(3, 4)
        >>> v *= w
        >>> v
        Vector(3, 8)
        >>> v *= 2
        >>> v
        Vector(6, 16)

        """
        if self._hash is not None:
            raise ValueError('cannot multiply Vector after hashing')
        if isinstance(other, Vector):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self

    def __mul__(self, other):
        """v.__mul__(w) -> v * w

        >>> v = Vector(1, 2)
        >>> w = Vector(3, 4)
        >>> v * w
        Vector(3, 8)
        >>> v * 2
        Vector(2, 4)
        >>> 3.0 * v
        Vector(3.0, 6.0)

        """
        copy = self.copy()
        return copy.__imul__(other)

    __rmul__ = __mul__

    def scale(self, other):
        """Scale Vector by other (in-place).

        >>> v = Vector(1, 2)
        >>> w = Vector(3, 4)
        >>> v.scale(w)
        >>> v
        Vector(3, 8)
        >>> v.scale(0.5)
        >>> v
        Vector(1.5, 4.0)

        """
        self.__imul__(other)

    def __itruediv__(self, other):
        """v.__itruediv__(w) -> v /= w

        >>> v = Vector(2, 4)
        >>> w = Vector(4, 8)
        >>> v /= w
        >>> v
        Vector(0.5, 0.5)
        >>> v /= 2
        >>> v
        Vector(0.25, 0.25)

        """
        if self._hash is not None:
            raise ValueError('cannot divide Vector after hashing')
        if isinstance(other, Vector):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other
        return self

    def __truediv__(self, other):
        """v.__truediv__(w) -> v / w

        >>> v = Vector(1, 2)
        >>> w = Vector(3, 4)
        >>> w / v
        Vector(3.0, 2.0)
        >>> v / 2
        Vector(0.5, 1.0)

        """
        copy = self.copy()
        return copy.__itruediv__(other)

    def __neg__(self):
        """v.__neg__() -> -v

        >>> v = Vector(1, 2)
        >>> -v
        Vector(-1, -2)

        """
        # pylint: disable=invalid-unary-operand-type
        copy = self.copy()
        copy.x = -copy.x
        copy.y = -copy.y
        return copy

    def __abs__(self):
        """v.__abs__() -> abs(v)

        >>> v = Vector(3, 4)
        >>> abs(v)
        5.0

        """
        return (self.x**2 + self.y**2) ** 0.5

    def rotate(self, angle):
        """Rotate Vector counter-clockwise by angle (in-place).

        >>> v = Vector(1, 2)
        >>> v.rotate(90)
        >>> v == Vector(-2, 1)
        True

        """
        if self._hash is not None:
            raise ValueError('cannot rotate Vector after hashing')
        radians = angle * math.pi / 180.0
        cosine = math.cos(radians)
        sine = math.sin(radians)
        x = self.x
        y = self.y
        self.x = x * cosine - y * sine
        self.y = y * cosine + x * sine

    def __repr__(self):
        """v.__repr__() -> repr(v)

        >>> v = Vector(1, 2)
        >>> repr(v)
        'Vector(1, 2)'

        """
        type_self = type(self)
        name = type_self.__name__
        return '{}({!r}, {!r})'.format(name, self.x, self.y)
