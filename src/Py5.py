import csv as xls
import math
import random
import re
from datetime import datetime as dt
from enum import Enum
from os import path
from typing import TypeVar, Union, Optional

from Arrays import Arrays
from Py5Vector import Py5Vector


class Py5:
    """ An all-in-one tool to do multiple tasks easier. Current version: *0.2.6-c*"""

    __author__ = "Shiromi"
    __version__ = "0.2.6-c"
    __copyright__ = "Copyright (c) 2020-2021 Shiromi"

    T = TypeVar('T', object, int, float, str)

    __PERLIN_Y_WRAP_B__ = 4
    __PERLIN_Y_WRAP__ = 1 << __PERLIN_Y_WRAP_B__
    __PERLIN_Z_WRAP_B__ = 8
    __PERLIN_Z_WRAP__ = 1 << __PERLIN_Z_WRAP_B__
    __PERLIN_SIZE__ = 4096

    __perlin_octaves__ = 4
    __perlin_amp_falloff__ = 0.5

    __perlin__ = None

    # static variables
    E = math.e
    PI = math.pi
    TWO_PI = TAU = 2 * PI
    HALF_PI = 0.5 * PI

    # math functions
    @staticmethod
    def half(x: float) -> float:
        return 0.5 * x

    @staticmethod
    def double(x: float) -> float:
        return 2 * x

    # used for changing modes
    class MODE(Enum):
        DEGREES = True
        RADIANS = False

    class COMPLEX(Enum):
        COMPLEX = True
        SIMPLE = False

    # default vars
    mode = MODE.RADIANS
    cx = COMPLEX.SIMPLE

    # Error classes
    class Py5InternalError(Exception):
        def __init__(self, message: str):
            super().__init__(f"Py5.Internals🌸 {message}")

    class Py5ValueError(Exception):
        def __init__(self, message: str):
            super().__init__(f"Value🌸 {message}")

    class Py5ModeError(Exception):
        def __init__(self, message: str):
            super().__init__(f"Mode🌸 {message}")

    class Py5Error(Exception):
        def __init__(self, message: str):
            super().__init__(f"Py5🌸 {message}")

    class Py5FriendlyError(Exception):
        def __init__(self, message: str):
            super().__init__(f"🌸 {message}")

    class Py5FileError(Exception):
        def __init__(self, message: str):
            super().__init__(f"File🌸 {message}")

    class Py5FileExtensionMismatchError(Exception):
        def __init__(self, message: str):
            super().__init__(f"Extension🌸 {message}")

    @staticmethod
    def deg(rad: float) -> float:
        """ Converts *radians* to *degrees*. """
        return rad * 180 / Py5.PI

    @staticmethod
    def rad(deg: float) -> float:
        """ Converts *degrees* to *radians*. """
        return deg * Py5.PI / 180

    @staticmethod
    def angle_mode(mode: MODE) -> None:
        """ Set mode to radians or degrees. Default is MODE.RADIANS"""
        if mode == Py5.mode:
            raise Py5.Py5ModeError(f"Mode already set to {mode}")
        Py5.mode = mode

    @staticmethod
    def complex_mode(cx: COMPLEX) -> None:
        """ Changes between complex and simple mode, default is *COMPLEX.DISABLED (Simple)*"""
        if cx == Py5.cx:
            raise Py5.Py5ModeError(f"Mode already set to {cx}")
        Py5.cx = cx

    @staticmethod
    def cos(n: float) -> float:
        """ Returns the cosine of the given value 'n' """
        return math.cos(n) if not Py5.mode else math.cos(Py5.rad(n))

    @staticmethod
    def sin(n: float) -> float:
        """ Returns the sine of the given value 'n'. """
        return math.sin(n) if not Py5.mode else math.sin(Py5.rad(n))

    @staticmethod
    def tan(n: float) -> float:
        """ Returns the tangent of the given value 'n'. """
        return math.tan(n) if not Py5.mode else math.tan(Py5.rad(n))

    @staticmethod
    def asin(n: float) -> float:
        """ Returns the arc sine of 'n'. """
        return math.asin(n) if not Py5.mode else math.asin(Py5.rad(n))

    @staticmethod
    def acos(n: float) -> float:
        """ Returns the arc cosine of 'n'. """
        return math.acos(n) if not Py5.mode else math.acos(Py5.rad(n))

    @staticmethod
    def atan(n: float) -> float:
        """ Returns the arc tangent of 'n'. """
        return math.atan(n) if not Py5.mode else math.atan(Py5.rad(n))

    @staticmethod
    def sinh(n: float) -> float:
        """ Returns the hyperbolic sine of 'n'. """
        return math.sinh(n) if not Py5.mode else math.sinh(Py5.rad(n))

    @staticmethod
    def cosh(n: float) -> float:
        """ Returns the hyperbolic cosine of 'n'. """
        return math.cosh(n) if not Py5.mode else math.cosh(Py5.rad(n))

    @staticmethod
    def tanh(n: float) -> float:
        """ Returns the hyperbolic tangent of 'n'. """
        return math.tanh(n) if not Py5.mode else math.tanh(Py5.rad(n))

    @staticmethod
    def asinh(n: float) -> float:
        """ Returns the inverse hyperbolic sine of 'n'. """
        return math.asinh(n) if not Py5.mode else math.asinh(Py5.rad(n))

    @staticmethod
    def acosh(n: float) -> float:
        """ Returns the inverse hyperbolic cosine of 'n'. """
        return math.acosh(n) if not Py5.mode else math.acosh(Py5.rad(n))

    @staticmethod
    def atanh(n: float) -> float:
        """ Returns the inverse hyperbolic tangent of 'n'. """
        return math.atanh(n) if not Py5.mode else math.atanh(Py5.rad(n))

    @staticmethod
    def atan2(x: float, y: float) -> float:
        """ Returns the arc tangent of x/y, """
        return math.atan2(x, y) if not Py5.mode else math.atan2(Py5.rad(x), Py5.rad(y))

    @staticmethod
    def pow(x: Union[float, int], n: Union[float, int]) -> float:
        """
        Returns the nth power of x,
        Alias: root(x, n)
        """
        return x**n

    @staticmethod
    def sqrt(x: Union[float, int]) -> Union[float, str]:
        """ Returns the square root of x. """
        if type(x) is int:
            x = float(x)
        if not Py5.cx:
            return math.sqrt(x)
        else:
            res = float(math.sqrt(abs(x)))
            if x < 0:
                res = str(res) + ' * i'
            return res

    @staticmethod
    def root(x: Union[float, int], n: int) -> Union[float, str]:
        """
        Returns the nth root of x.
        :param x Base
        :param n Denominator, exponent
        """
        if n == 2:
            return Py5.sqrt(x)
        else:
            res = Py5.pow(x, n)
            if not Py5.cx:
                return res
            else:
                return str(float(Py5.pow(abs(x), float(1/n)))) + " * i"

    @staticmethod
    def __scaled_cos__(n: float) -> float:
        return 0.5 * (1.0 * Py5.cos(n * Py5.PI))

    @staticmethod
    def abs(n: float) -> float:
        """ Returns the absolute value of 'n'. """
        return -n if n < 0 else n

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
    def dist(*args: float) -> float:
        """ Returns the distance between the given arguments. """
        if len(args) == 4:
            return Py5.__hypot2d__(args[2] - args[0], args[3] - args[1])
        elif len(args) == 6:
            return Py5.__hypot3d__(args[3] - args[0], args[4] - args[1], args[5] - args[2])
        else:
            raise Py5.Py5FriendlyError(f"Has to be of either length 4 or 6, got {len(args)} instead")

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
    def max(*args: float) -> float:
        """ Returns the maximum value from the given list. """
        record_index = 0
        for i in range(len(args)):
            if args[i] > args[record_index]:
                record_index = i

        return args[record_index]

    @staticmethod
    def min(*args: float) -> float:
        """ Returns the minimum value from the given list. """
        record_index = 0
        for i in range(len(args)):
            if args[i] < args[record_index]:
                record_index = i

        return args[record_index]

    @staticmethod
    def nf(n: float, left=0, right=0) -> str:
        """ Formats a number with the given amount of digits on either left or right. ``print(Py5.nf(20.2,
        right=2))`` """
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
        """ Formats a number to the thousand format. """
        neg = n < 0
        _n = str(n)[1:] if neg else str(n)
        try:
            decimal_index = _n.index('.')
        except ValueError:
            decimal_index = -1
        int_part = _n[0:decimal_index] if decimal_index != -1 else _n
        dec_part = _n[decimal_index + 1:] if decimal_index != -1 else ''
        string = '-' if neg else ''

        tmp = re.split(r"(?=(?:\d{3})*$)", int_part)

        tmp_string = ",".join(tmp)

        string += tmp_string[1:len(tmp_string) - 1]

        if decimal_index != -1:
            string += '.'
            string += dec_part

        return string

    @staticmethod
    def choice(*arr: T) -> T:
        """ Returns a random element from an array, same as *random.choice()* """
        i = random.randint(0, len(arr) - 1)
        return arr[i]

    @staticmethod
    def random(a: Union[int, float] = 0, b: Union[int, float] = 1) -> Union[int, float]:
        if a is int and b is int:
            if a == 0 and b == 1:
                return random.randint(0, 1)
            else:
                return random.randint(a, b)
        if a is float and b is float:
            if a == 0 and b == 1:
                return random.random()
            else:
                return random.random() * b + a

    @staticmethod
    def noise(x: float, y=0, z=0) -> float:
        """ Returns a random number from a given interval and seed. """
        if Py5.__perlin__ is None:
            Py5.__perlin__ = [Py5.random(0.0, 1.0) for _ in range(Py5.__PERLIN_SIZE__ + 1)]

        if x < 0:
            x = -x
        if y < 0:
            y = -y
        if z < 0:
            z = -z

        xi = Py5.floor(x)
        yi = Py5.floor(y)
        zi = Py5.floor(z)

        xf = x - xi
        yf = y - yi
        zf = z - zi

        r = 0
        ampl = 0.5

        for _ in range(Py5.__perlin_octaves__):
            of = xi + (yi << Py5.__PERLIN_Y_WRAP_B__) + (zi << Py5.__PERLIN_Z_WRAP_B__)

            rxf = Py5.__scaled_cos__(xf)
            ryf = Py5.__scaled_cos__(yf)

            n1 = Py5.__perlin__[of & Py5.__PERLIN_SIZE__]
            n1 += rxf * (Py5.__perlin__[(of + 1) & Py5.__PERLIN_SIZE__])
            n2 = Py5.__perlin__[(of + Py5.__PERLIN_Y_WRAP__) & Py5.__PERLIN_SIZE__]
            n2 += rxf * (Py5.__perlin__[(of + Py5.__PERLIN_Y_WRAP__ + 1) & Py5.__PERLIN_SIZE__] - n2)
            n1 += ryf * (n2 - n1)

            of += Py5.__PERLIN_Z_WRAP__
            n2 = Py5.__perlin__[of & Py5.__PERLIN_Z_WRAP__]
            n2 += rxf * (Py5.__perlin__[(of + 1) & Py5.__PERLIN_SIZE__] - n2)
            n3 = Py5.__perlin__[(of + Py5.__PERLIN_Y_WRAP__) & Py5.__PERLIN_Y_WRAP__]
            n3 += rxf * (Py5.__perlin__[(of + Py5.__PERLIN_Y_WRAP__ + 1) & Py5.__PERLIN_SIZE__] - n3)
            n2 += ryf * (n3 - n2)

            n1 += Py5.__scaled_cos__(zf) * (n2 - n1)

            r += n1 * ampl
            ampl *= Py5.__perlin_amp_falloff__
            xi <<= 1
            xf *= 2
            yi <<= 1
            yf *= 2
            zi <<= 1
            zf *= 2

            if xf >= 1.0:
                xi += 1
                xf -= 1

            if yf >= 1.0:
                yi += 1
                yf -= 1

            if zf >= 1.0:
                zi += 1
                zf -= 1

        return r

    @staticmethod
    def create_vector(x: float, y: float, z=0, w=0) -> Py5Vector:
        """ Creates a Vector with the given values. """
        return Py5Vector(x, y, z, w)

    @staticmethod
    def promise(func, on_success=None, on_error=None, exception: Exception = BaseException) -> any:
        def default_success() -> None:
            print("Success!")

        def default_error() -> None:
            print("Error!")

        try:
            x = func()
            if on_success is not None:
                on_success()
            else:
                default_success()
            return x
        except exception:
            if on_error is not None:
                on_error()
            else:
                default_error()

    class Debug(object):
        def __init__(self, func):
            self.func = func

        def __log_call__(self, *args, **kwargs) -> any:
            _now = dt.now()
            _hour: str = _now.hour if _now.hour > 10 else f"0{_now.hour}"
            _minute: str = _now.minute if _now.minute > 10 else f"0{_now.minute}"
            _second: str = _now.second if _now.second > 10 else f"0{_now.second}"

            print(f"{_hour}:{_minute}:{_second}: Executed: {self.func.__name__}"
                  f"\n\tArguments: {args}"
                  f"\n\tNamed Arguments: {kwargs}")

            return self.func(*args, **kwargs)

    @staticmethod
    def debug(func) -> any:
        """ Usage as a decorator to get the function name and parameters as debug info\n
        ``@Py5.debug def method_name(*args): pass`` """
        return Py5.Debug(func).__log_call__

    class Color(object):
        """ A color object which might be useful for *pygame*. """

        color: dict[str, float]

        def __init__(self, *args: float):
            """ Creates a new color object with 4 values: ``r,g,b,a``. """

            if type(args) is tuple:
                if len(args) == 1:
                    color_val = args[0] % 256
                    self.color = {"r": color_val, "g": color_val, "b": color_val, "a": 256}
                elif len(args) == 2:
                    color_val = args[0] % 256
                    alpha = args[1] % 256
                    self.color = {"r": color_val, "g": color_val, "b": color_val, "a": alpha}
                elif len(args) == 3:
                    self.color = {"r": args[0] % 256, "g": args[1] % 256, "b": args[2] % 256, "a": 255}
                elif len(args) == 4:
                    self.color = {"r": args[0] % 256, "g": args[1] % 256, "b": args[2] % 256, "a": args[3] % 256}
                else:
                    raise Py5.Py5Error(f"Expected between 1 or 4 arguments. Got {len(args)} instead")

        # readonly types
        @property
        def red(self) -> float:
            """ Gets the red value. """
            return self.color["r"]

        @property
        def green(self) -> float:
            """ Gets the green value. """
            return self.color["g"]

        @property
        def blue(self) -> float:
            """ Gets the blue value. """
            return self.color["b"]

        @property
        def alpha(self) -> float:
            """ Gets the alpha value. """
            return self.color["a"]

        def get(self) -> dict[str, float]:
            """ Returns the color object with all values. """
            return self.color

        def get_tuple(self) -> tuple[float, float, float, float]:
            """ Returns the color object as a tuple with all values. """
            return self.color["r"], self.color["g"], self.color["b"], self.color["a"]

    @staticmethod
    def color(*args: float) -> Color:
        """ Creates a new color object. """
        return Py5.Color(*args)

    @staticmethod
    def hex_color(hex_val: str) -> Color:
        """ Creates a new color object with given hex values. """
        if not hex_val.startswith('#'):
            raise AttributeError(f'Argument \'hex_val\' has to begin with \'#\', but got {hex_val[0]} instead.')
        args = hex_val[1:]
        if len(args) == 3:
            r = args[0]
            g = args[1]
            b = args[2]

            r += r
            g += g
            b += b

            return Py5.Color(int(r, 16), int(g, 16), int(b, 16), 255)
        elif len(args) == 4:
            r = args[0]
            g = args[1]
            b = args[2]
            a = args[3]

            r += r
            g += g
            b += b
            a += a

            return Py5.Color(int(r, 16), int(g, 16), int(b, 16), int(a, 16))
        elif len(args) == 6:
            r = args[0:1]
            g = args[2:3]
            b = args[4:5]

            return Py5.Color(int(r, 16), int(g, 16), int(b, 16), 255)
        elif len(args) == 8:
            r = args[0:1]
            g = args[2:3]
            b = args[4:5]
            a = args[6:7]

            return Py5.Color(int(r, 16), int(g, 16), int(b, 16), int(a, 16))

    @staticmethod
    def fill_array(arr: list, value: any = None) -> list:
        """ Fills an array with the given values. """
        return Arrays.fill(arr, value)

    @staticmethod
    def includes(array: list, value: any) -> bool:
        """ Checks if a list contains an element. """
        for elem in array:
            if elem == value:
                return True
        return False

    @staticmethod
    def parse_int(x: str) -> int:
        if not x.isdigit():
            raise Py5.Py5InternalError("Expected only digits, got alphanumerical string instead")
        return int(x)

    @staticmethod
    def parse_bool(x: Union[int, str]) -> bool:
        valid = [
            'true',
            '1',
            'false',
            '0'
        ]

        x = str(x) if x is int else x.lower()
        if x not in valid:
            raise Py5.Py5InternalError(f"Expected boolean value or 1 or 0, got {x}")

        return True if x.lower() == 'true' or x == '1' else False

    @staticmethod
    def available_methods(check: str = None) -> None:
        """ Prints the information for a function of this or one of it's subclasses. """
        py5_available = [
            "deg",
            "rad",
            "angle_mode",
            "cos",
            "sin",
            "tan",
            "asin",
            "acos",
            "atan",
            "sinh",
            "cosh",
            "tanh",
            "asinh",
            "acosh",
            "atanh",
            "atan2",
            "sqrt",
            "pow",
            "root",
            "abs",
            "ceil",
            "floor",
            "constrain",
            "dist",
            "exp",
            "lerp",
            "log",
            "mag",
            "fact",
            "map",
            "min",
            "nf",
            "num",
            "random",
            "choice",
            "noise",
            "create_vector",
            "color",
            "fill_array",
            "includes",
            "available_methods"
        ]
        py5color_available = [
            "red",
            "green",
            "blue",
            "alpha",
            "get"
        ]
        py5filereader_available = [
            "parse",
            "read"
        ]
        py5vector_available = [
            "add",
            "sub",
            "mult",
            "div",
            "scale",
            "get"
        ]
        arrays_available = [
            "fill"
        ]

        if check is None:
            py5_available_str = "\n\t".join(py5_available)
            py5filereader_available_str = "\n\t".join(py5filereader_available)
            py5color_available_str = "\n\t".join(py5color_available)
            py5vector_available_str = "\n\t".join(py5vector_available)
            arrays_available_str = "\n\t".join(arrays_available)

            print(f"Available methods for 'Py5':\n\t{py5_available_str}\n"
                  f"Available methods for 'Py5FileReader':\n\t{py5filereader_available_str}\n"
                  f"Available methods for 'Py5.Color':\n\t{py5color_available_str}\n"
                  f"Available methods for 'Py5Vector':\n\t{py5vector_available_str}\n"
                  f"Available methods for 'Arrays':\n\t{arrays_available_str}\n")
        else:
            if not Py5.includes(py5_available, check):
                if not Py5.includes(py5color_available, check):
                    if not Py5.includes(py5filereader_available, check):
                        if not Py5.includes(py5vector_available, check):
                            if not Py5.includes(arrays_available, check):
                                raise Py5.Py5InternalError(f"Method '{check}' is not defined.")
                            print(f"Method '{check}' is part of 'Arrays'")
                            help(getattr(Arrays, check))
                            return
                        print(f"Method '{check}' is part of 'Py5Vector'")
                        help(getattr(Py5Vector, check))
                        return
                    print(f"Method '{check}' is part of 'Py5FileReader'")
                    help(getattr(Py5FileReader, check))
                    return
                print(f"Method '{check}' is part of 'Py5.Color'")
                help(getattr(Py5.Color, check))
                return
            print(f"Method '{check}' is part of 'Py5'")
            help(getattr(Py5, check))


class Py5FileType(Enum):
    """ The file extensions currently compatible with *Py5*. """

    CONFIGURATION_SETTINGS = "ini"
    TEXT = "txt"
    XML = "xml"
    EXCEL_SPREADSHEET = "csv"
    MARKDOWN = "md"


class Py5FileReader:
    """ Allows the user to read and parse files. """

    @staticmethod
    def parse(file: str, ext: Py5FileType = Py5FileType.TEXT) -> \
            Union[dict[str, Union[str, dict]], list[Union[str, dict]]]:
        """
        Parses code files such as xml and ini to a dictionary.
        :raises Py5FileError If the file is not existing.
        :param file: The path to the file.
        :param ext: The file extension.
        :return: The contents.
        """
        if not path.isfile(file):
            raise Py5.Py5FileError(f"No such file, open '{file}'")
        file = open(file, "r")
        search = re.search
        regex_match = re.match
        if ext == Py5FileType.CONFIGURATION_SETTINGS:
            value = {}
            section = None
            for line in file:
                if search(r'^\s*([^=]+?)\s*=\s*(.*?)\s*$', line, re.M):
                    match = regex_match(r'^\s*([^=]+?)\s*=\s*(.*?)\s*$', line, re.M)
                    if section is not None:
                        value[section][match[1]] = match[2]
                    else:
                        value[match[1]] = match[2]
                elif search(r'^\s*\[\s*([^\]]*)\s*\]\s*$', line, re.M):
                    match = regex_match(r'^\s*\[\s*([^\]]*)\s*\]\s*$', line, re.M)
                    value[match[1]] = {}
                    section = match[1]
            return value
        elif ext == Py5FileType.TEXT:
            value = []
            for line in file:
                value.append(line.replace("\n", ""))
            return value
        elif ext == Py5FileType.XML:
            values = {}
            # Work in progress, adding in v0.5a
            return values
        elif ext == Py5FileType.MARKDOWN:
            values = {}
            compare = {
                "h1": r"(?P<h1>^#)",
                "h2": r"(?P<h2>^#{2})",
                "h3": r"(?P<h3>^#{3})",
                "h4": r"(?P<h4>^#{4})",
                "i": r"[\*_]([^\*_]+)[\*_]$",
                "b": r"[\*_]{2}([^\*_]+)[\*_]{2}$",
                "strikethrough": r"~{2}([^~]+)~{2}$",
                "code": r"`([^`]+)`$"
            }

    @staticmethod
    def read(file: str, line: Optional[int] = None,
             delimiter: str = "\n", ext: Union[str, Py5FileType] = Py5FileType.TEXT) -> Union[list[str], str]:

        """
        Reads the specified file and returns its content in a list form.
        :raises Py5FileError If the specified file isn't existing.
        :raises Py5Error If the line index is beyond the maximum lines of the file.
        :raises Py5FileExtensionMismatchError If the given extension isn't compatible with the current version of Py5.
        :param file: The path to the file.
        :param line: Reads only specified line, **works only for text-type files**.
        :param delimiter: Removes the end of the line if not specified, **works only for text-type files**.
        :param ext: The file extension.
        :return: The file contents.
        """

        def read_csv(csv: str) -> list[str]:
            l: list[str] = []
            csv = open(csv)
            r = xls.reader(csv)
            for csv_ln in r:
                l.append(str(csv_ln))
            csv.close()
            return l

        def read_xml(xml: str) -> list[str]:
            l: list[str] = []
            xml = open(xml)
            for xml_ln in xml:
                l.append(re.search(r"<([^>]+)>", xml_ln)[0])
            xml.close()
            return l

        def read_md(md: str) -> list[str]:
            l: list[str] = []
            md = open(md)
            for md_ln in md:
                l.append(re.sub(r"^\s+", "", md_ln).strip("\n"))
            md.close()
            return l

        def read_txt(txt: str, ln: Optional[int] = None, limiter: str = "\n") -> Union[str, list[str]]:
            data: list[str] = []
            f = open(txt)
            current_line = 0
            for f_ln in f:
                current_line += 1
                data.append(f_ln.strip(limiter).replace("\t", ""))
                if ln is not None:
                    if current_line == ln:
                        return f_ln
            if ln is not None:
                if current_line < ln:
                    raise Py5.Py5Error(f"Line number out of range.\nmaximum={current_line}; given={ln}")
            f.close()
            return data

        def read_ini(ini: str) -> list[str]:
            l: list[str] = []
            ini = open(ini)
            for ini_ln in ini:
                l.append(ini_ln.strip("\n"))
            ini.close()
            return l

        if not path.isfile(file):
            raise Py5.Py5FileError(f"No such file, open '{file}'")

        extension: str
        if type(ext) is str:
            extension = ext
        else:
            extension = ext.value

        extension = extension.lower()

        if extension == 'txt':
            return read_txt(file, line, delimiter)
        elif extension == 'csv':
            return read_csv(file)
        elif extension == 'xml':
            return read_xml(file)
        elif extension == 'md':
            return read_md(file)
        elif extension == 'ini':
            return read_ini(file)
        else:
            error_msg = str(list(map(lambda x: x.name, Py5FileType.__members__.values()))).strip('[]')
            raise Py5.Py5FileExtensionMismatchError(f"Expected one of {error_msg}, got '{extension}' instead.")
