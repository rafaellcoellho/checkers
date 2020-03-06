import arcade
from .defines import Square
from logic.defines import SquarePlayerState


class Checker(arcade.ShapeElementList):
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
                if square.player_state == SquarePlayerState.CHECKER_RED:
                    color = arcade.color.RED
                elif square.player_state == SquarePlayerState.CHECKER_BLUE:
                    color = arcade.color.BLUE
                
                if square.player_state != SquarePlayerState.EMPTY:
                    current_cir = arcade.create_ellipse_filled(
                        (margin + width) * square.column + margin + width // 2,
                        (margin + height) * square.row + margin + height // 2,
                        30,
                        30,
                        color
                    )
                    self.append(current_cir)
