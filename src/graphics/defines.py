from enum import IntEnum


class Square(IntEnum):
    WIDTH = 70
    HEIGHT = 70
    MARGIN = 3


class Window(IntEnum):
    WIDTH = (Square.WIDTH + Square.MARGIN) * 8 + Square.MARGIN
    HEIGHT = (Square.HEIGHT + Square.MARGIN) * 8 + Square.MARGIN


TITLE = 'checkers'
