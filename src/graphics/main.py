import arcade
from .grid import Grid
from .checker import Checker
from .defines import square

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

    def on_mouse_press(self, x, y, button, key_modifiers):
        column = int(x // (square.WIDTH + square.MARGIN))
        row = int(y // (square.HEIGHT + square.MARGIN))
        if self.board.moving_checker == None:
            self.board.calculate_possible_moves(row, column)
        else:
            if [row, column] in self.board.possible_moves:
                self.board.move(row,column)
            else:
                self.board.reset_possible_moves()
        print(row, column)
