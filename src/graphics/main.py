import arcade
from .grid import Grid
from .checker import Checker

class Game(arcade.Window):
    def __init__(self, width, height, title, board):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        
        self.grid = None
        self.players = None
        self.board = board

    def setup(self):
        print(self.board)
        self.grid = Grid()
        self.players = Checker()

    def on_update(self, delta_time):
        self.grid.update(self.board)
        self.players.update(self.board)

    def on_draw(self):
        arcade.start_render()
        self.grid.draw()
        self.players.draw()

    def on_key_press(self, key, key_modifiers):
        pass

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass
