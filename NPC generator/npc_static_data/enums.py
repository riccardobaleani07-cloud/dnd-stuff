from enum import IntEnum, Enum, auto

class Size(IntEnum):
    ATOMIC = -5 # not an official size category, it is like a real size average atom
    NANOMETRIC = -4 # not an official size category, it is like a real size average virus
    MICROSCOPIC = -3 # not an official size category, it is like a real size average bacterium
    VISIBLE = -2 # not an official size category, it is like a real size average fly, it is big enought to be seen by the naked eye
    VERY_TINY = -1 # not an official size category, it is like a real size lizard or small mouse
    TINY = 0
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    HUGE = 4
    GARGANTUAN = 5
    COLOSSAL = 6 # not an official size category, it is like a very large ship or a small mountain/island, cannot be seen from orbit
    LARGE_COLOSSAL = 7 # not an official size category, it is like a large mountain, an asteroid or a small proto-planet, cannot be seen from space, but it's visible from orbit
    PLANETARY = 8 # not an official size category, it is like a large proto-planet or a small planet, can be seen from space and orbit
    LARGE_PLANETARY = 9 # not an official size category, it is like a large planet or a small star, can be seen from space and orbit
    STELLAR = 10 # not an official size category, it is like a small-star, can be seen from space and orbit
    LARGE_STELLAR = 11 # not an official size category, it is like a large star, can be seen from  deep space
    TINY_GALACTICAL = 12 # not an official size category, it is less than a tiny galaxy, can be seen from deep space
    GALACTICAL = 13 # not an official size category, it is like a galaxy, can be seen from deep space

class SocialLevel(Enum):
    ROYAL = auto()
    NOBLE = auto()
    COMMONER = auto()
    PEASANT = auto()
    SLAVE = auto()

class Wealth(IntEnum):
    POOR = 0
    MODEST = 1
    WEALTHY = 2
    RICH = 3
    OPULENT = 4

class MagicSource(IntEnum):
    NONE = 0
    INNATE = 1
    LEARNED = 2

class ArmorType(IntEnum):
    UNARMORED = 0
    LIGHT = 1
    MEDIUM = 2
    HEAVY = 3

