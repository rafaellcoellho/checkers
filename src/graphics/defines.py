from enum import IntEnum

class window(IntEnum):
    WIDTH = 560
    HEIGHT = 560

class square(IntEnum):
    WIDTH = window.WIDTH / 8
    HEIGHT = window.HEIGHT / 8



TITLE = 'checkers'  
