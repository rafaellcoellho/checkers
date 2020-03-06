import arcade
from .defines import Square
from logic.defines import SquareColor


class Grid(arcade.ShapeElementList):
    def __init__(self):
        super().__init__()

    def update(self, board):
        width = Square.WIDTH
        height = Square.HEIGHT
        margin = Square.MARGIN

        for shape in self:
            self.remove(shape)

        for row in board.state:
            for square in row:
                color = None
                if square.possible_move:
                    color = arcade.color.BLACK_LEATHER_JACKET
                elif square.color == SquareColor.WHITE:
                    color = arcade.color.WHITE
                elif square.color == SquareColor.BLACK:
                    color = arcade.color.BLACK

                current_rect = arcade.create_rectangle_filled(
                    (margin + width) * square.column + margin + width // 2,
                    (margin + height) * square.row + margin + height // 2,
                    float(width),
                    float(height),
                    color
                )
                self.append(current_rect)
