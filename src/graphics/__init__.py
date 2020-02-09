import arcade
from .main import Game
from .defines import window,TITLE

def run():
    game = Game(
        window.WIDTH,
        window.HEIGHT,
        TITLE
    )
    game.setup()
    arcade.run()