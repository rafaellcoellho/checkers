import arcade
from .main import Game
from .defines import Window, TITLE


def run(board):
    game = Game(
        Window.WIDTH,
        Window.HEIGHT,
        TITLE,
        board
    )
    game.setup()
    arcade.run()
