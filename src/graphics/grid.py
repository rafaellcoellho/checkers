import arcade
from .defines import square

class Grid(arcade.ShapeElementList):
    def __init__(self):
        super().__init__()

        is_black = True
        for row in range(8):
            for column in range(8):
                if is_black:
                    color = arcade.color.BLACK
                else:
                    color = arcade.color.WHITE
                is_black = not is_black

                current_rect = arcade.create_rectangle_filled(
                    (square.MARGIN + square.WIDTH) * column + square.MARGIN + square.WIDTH // 2,
                    (square.MARGIN + square.HEIGHT) * row + square.MARGIN + square.HEIGHT // 2,
                    square.WIDTH,
                    square.HEIGHT,
                    color
                )
                self.append(current_rect)
            is_black = not is_black