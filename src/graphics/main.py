import arcade
from .grid import Grid
from .checker import Checker
from .defines import Square


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
        column = int(x // (float(Square.WIDTH + Square.MARGIN)))
        row = int(y // (float(Square.HEIGHT + Square.MARGIN)))

        if self.board.moving_checker is None:
            if self.board.is_active_player(row, column):
                self.board.calculate_possible_moves(row, column)
        else:
            if [row, column] in self.board.possible_moves:
                self.board.move(row, column)
            else:
                self.board.reset_possible_moves()
