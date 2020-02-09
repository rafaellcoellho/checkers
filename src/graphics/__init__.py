import arcade
from .main import Game
from .defines import window,TITLE

def run(board):
    game = Game(
        window.WIDTH,
        window.HEIGHT,
        TITLE,
        board
    )
    game.setup()
    arcade.run()