import arcade
import graphics
from logic.defines import square_player_state

class Checker(arcade.ShapeElementList):
    def __init__(self):
        super().__init__()

    def update(self, board):
        width = graphics.defines.square.WIDTH
        heigth = graphics.defines.square.HEIGHT
        margin = graphics.defines.square.MARGIN

        for shape in self:
            self.remove(shape)

        for row in board.state:
            for square in row:
                if square.player_state == square_player_state.CHECKER_RED:
                    color = arcade.color.RED
                elif square.player_state == square_player_state.CHECKER_BLUE:
                    color = arcade.color.BLUE
                
                if square.player_state != square_player_state.EMPTY:
                    current_cir = arcade.create_ellipse_filled(
                        (margin + width) * (square.column-1) + margin + width // 2,
                        (margin + heigth) * (square.row-1) + margin + heigth // 2,
                        30,
                        30,
                        color
                    )
                    self.append(current_cir)