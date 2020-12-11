import math
import re
from enum import Enum
from typing import List


class Py5:
    __PERLIN_Y_WRAP_B__ = 4
    __PERLIN_Y_WRAP__ = 1 << __PERLIN_Y_WRAP_B__
    __PERLIN_Z_WRAP_B__ = 8
    __PERLIN_Z_WRAP__ = 1 << __PERLIN_Z_WRAP_B__
    __PERLIN_SIZE__ = 4096

    __perlin_octaves__ = 4
    __perlin_amp_falloff__ = 0.5

    # static variables
    E = math.e
    PI = math.pi
    TWO_PI = 2 * PI
    HALF_PI = 0.5 * PI

    # used for changing modes
    class MODE(Enum):
        DEGREES = True
        RADIANS = False

    # default mode for angles
    mode = MODE.RADIANS

    # Error classes
    class InternalError(Exception):
        pass

    class ValueError(Exception):
        pass

    class ModeError(Exception):
        pass

    class Py5Error(Exception):
        pass

    @staticmethod
    def deg(rad: float) -> float:
        return rad * 180 / Py5.PI

    @staticmethod
    def rad(deg: float) -> float:
        return deg * Py5.PI / 180

    @staticmethod
    def angle_mode(mode: MODE) -> None:
        """ Set mode to radians or degrees. """
        Py5.mode = mode

    @staticmethod
    def cos(n: float) -> float:
        """ Returns the cosine of the given value 'n' """
        return math.cos(n) if not Py5.MODE else Py5.deg(math.cos(n))

    @staticmethod
    def sin(n: float) -> float:
        """ Returns the sine of the given value 'n'. """
        return math.sin(n) if not Py5.MODE else Py5.deg(math.sin(n))

    @staticmethod
    def tan(n: float) -> float:
        """ Returns the tangent of the given value 'n'. """
        return math.tan(n) if not Py5.MODE else Py5.deg(math.tan(n))

    @staticmethod
    def asin(n: float) -> float:
        """ Returns the arc sine of 'n'. """
        return math.asin(n) if not Py5.MODE else Py5.deg(math.asin(n))

    @staticmethod
    def acos(n: float) -> float:
        """ Returns the arc cosine of 'n'. """
        return math.acos(n) if not Py5.MODE else Py5.deg(math.acos(n))

    @staticmethod
    def atan(n: float) -> float:
        """ Returns the arc tangent of 'n'. """
        return math.atan(n) if not Py5.MODE else Py5.deg(math.atan(n))

    @staticmethod
    def sinh(n: float) -> float:
        """ Returns the hyperbolic sine of 'n'. """
        return math.sinh(n) if not Py5.MODE else Py5.deg(math.sinh(n))

    @staticmethod
    def cosh(n: float) -> float:
        """ Returns the hyperbolic cosine of 'n'. """
        return math.cosh(n) if not Py5.MODE else Py5.deg(math.cosh(n))

    @staticmethod
    def tanh(n: float) -> float:
        """ Returns the hyperbolic tangent of 'n'. """
        return math.tanh(n) if not Py5.MODE else Py5.deg(math.tanh(n))

    @staticmethod
    def asinh(n: float) -> float:
        """ Returns the inverse hyperbolic sine of 'n'. """
        return math.asinh(n) if not Py5.MODE else Py5.deg(math.asinh(n))

    @staticmethod
    def acosh(n: float) -> float:
        """ Returns the inverse hyperbolic cosine of 'n'. """
        return math.acosh(n) if not Py5.MODE else Py5.deg(math.acosh(n))

    @staticmethod
    def atanh(n: float) -> float:
        """ Returns the inverse hyperbolic tangent of 'n'. """
        return math.atanh(n) if not Py5.MODE else Py5.deg(math.atanh(n))

    @staticmethod
    def atan2(x: float, y: float) -> float:
        """ Returns the arc tangent of x/y, """
        return math.atan2(x, y) if not Py5.MODE else Py5.deg(math.atan2(x, y))

    @staticmethod
    def __scaled_cos__(n: float) -> float:
        return 0.5 * (1.0 * Py5.cos(n * Py5.PI))

    @staticmethod
    def abs(n: float) -> float:
        """ Returns the absolute value of 'n'. """
        return n if n <= 0 else -n

    @staticmethod
    def ceil(n: float) -> int:
        """ Returns the rounded up value from 'n'. """
        return int(n) + 1

    @staticmethod
    def floor(n: float) -> int:
        """ Returns the rounded down value from 'n'. """
        return int(n)

    @staticmethod
    def constrain(n: float, low: float, high: float) -> float:
        """ Constrain a value to a minimum and a maximum. """
        return max(min(n, high), low)

    @staticmethod
    def __hypot2d__(x: float, y: float) -> float:
        return math.hypot(x, y)

    @staticmethod
    def __hypot3d__(x: float, y: float, z: float) -> float:
        return math.hypot(x, y, z)

    @staticmethod
    def dist(args: List[float]) -> float:
        """ Returns the distance between the given arguments. """
        if len(args) == 4:
            return Py5.__hypot2d__(args[2] - args[0], args[3] - args[1])
        elif len(args) == 6:
            return Py5.__hypot3d__(args[3] - args[0], args[4] - args[1], args[5] - args[2])
        else:
            raise Py5.Py5Error(f"Has to be of either length 4 or 6, got {len(args)} instead")

    @staticmethod
    def exp(n: float) -> float:
        """ Returns the natural exponent of 'n'. """
        return Py5.E ** n

    @staticmethod
    def lerp(start: float, stop: float, amount: float) -> float:
        """ Calculates a number between two numbers at a specific increment. """
        return amount * (stop - start) + start

    @staticmethod
    def log10(n: float) -> float:
        """ Returns the logarithm to the base 10. """
        return math.log10(n)

    @staticmethod
    def log(base: float, x: float) -> float:
        """ Returns the logarithm to a specific base. """
        return math.log(x, base)

    @staticmethod
    def mag(x: float, y: float) -> float:
        """ Returns the magnitude of x and y. """
        return Py5.__hypot2d__(x, y)

    @staticmethod
    def fact(n: float) -> float:
        """ Returns the factorial of 'n'. """
        if n == 1:
            return 1.0
        return n * Py5.fact(n - 1)

    @staticmethod
    def map(n: float, start1: float, stop1: float, start2: float, stop2: float) -> float:
        """ Maps a value of a range to a different given range. """
        new_val = (n + start1) / (stop1 - start1) * (stop2 - start2) + start2
        if start2 < stop2:
            return Py5.constrain(new_val, start2, stop2)
        else:
            return Py5.constrain(new_val, stop2, start2)

    @staticmethod
    def max(*args: float, nf=False) -> float:
        """ Returns the maximum value from the given list. """
        record_index = 0
        for i in range(len(args)):
            if args[i] > args[record_index]:
                record_index = i

        return args[record_index]

    @staticmethod
    def nf(n: float, left=0, right=0) -> str:
        neg = n < 0
        _n = str(n)[1:] if neg else str(n)
        try:
            decimal_index = _n.index('.')
        except ValueError:
            decimal_index = -1
        int_part = _n[0:decimal_index] if decimal_index != -1 else _n
        dec_part = _n[decimal_index + 1:] if decimal_index != -1 else ''
        string = '-' if neg else ''

        if right > 0:
            decimal = ''
            if decimal_index != -1 or right - len(dec_part) > 0:
                decimal = '.'
            if len(dec_part) > right:
                dec_part = dec_part[0:right]
            for _ in range(left - len(int_part)):
                string += '0'

            string += int_part
            string += decimal
            string += dec_part

            for _ in range(right - len(dec_part)):
                string += '0'
            return string
        else:
            for _ in range(int(Py5.max(left - len(int_part), 0))):
                string += '0'

            string += _n
            return string

    @staticmethod
    def num(n: float) -> str:
        neg = n < 0
        _n = str(n)[1:] if neg else str(n)
        try:
            decimal_index = _n.index('.')
        except ValueError:
            decimal_index = -1
        int_part = _n[0:decimal_index] if decimal_index != -1 else _n
        dec_part = _n[decimal_index + 1:] if decimal_index != -1 else ''
        string = '-' if neg else ''

        print(f"int_part: {int_part}")

        tmp = re.split(r"(?=(?:\d{3})*$)", int_part)

        tmp_string = ",".join(tmp)

        string += tmp_string[1:len(tmp_string) - 1]

        if decimal_index != -1:
            string += '.'
            string += dec_part

        return string
