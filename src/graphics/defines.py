from enum import IntEnum

class square(IntEnum):
    WIDTH = 70
    HEIGHT = 70
    MARGIN = 3

class window(IntEnum):
    WIDTH = (square.WIDTH + square.MARGIN) * 8 + square.MARGIN
    HEIGHT = (square.HEIGHT + square.MARGIN) * 8 + square.MARGIN

TITLE = 'checkers'  
