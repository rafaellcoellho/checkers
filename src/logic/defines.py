from enum import IntEnum


class SquarePlayerState(IntEnum):
    EMPTY = 0
    CHECKER_RED = 1
    CHECKER_BLUE = 2


class SquareColor(IntEnum):
    BLACK = 0
    WHITE = 1
