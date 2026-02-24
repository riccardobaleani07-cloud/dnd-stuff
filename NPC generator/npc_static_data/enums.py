from enum import IntEnum, Enum, auto

class Size(IntEnum):
    TINY = 0
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    HUGE = 4
    GARGANTUAN = 5

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

