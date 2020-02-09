import arcade
import graphics
from logic.defines import square_color

class Grid(arcade.ShapeElementList):
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
                if square.color == square_color.WHITE:
                    color = arcade.color.WHITE
                elif square.color == square_color.BLACK:
                    color = arcade.color.BLACK

                current_rect = arcade.create_rectangle_filled(
                    (margin + width) * (square.column-1) + margin + width // 2,
                    (margin + heigth) * (square.row-1) + margin + heigth // 2,
                    width,
                    heigth,
                    color
                )
                self.append(current_rect)