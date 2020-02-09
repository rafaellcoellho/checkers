import arcade
from .defines import square

class Grid(arcade.ShapeElementList):
    def __init__(self):
        super().__init__()

        for row in range(8):
            for column in range(8):
                def is_even(x):
                    return x % 2 == 0

                if is_even(row) == is_even(column):
                    color = arcade.color.WHITE
                else:
                    color = arcade.color.BLACK

                current_rect = arcade.create_rectangle_filled(
                    (square.MARGIN + square.WIDTH) * column + square.MARGIN + square.WIDTH // 2,
                    (square.MARGIN + square.HEIGHT) * row + square.MARGIN + square.HEIGHT // 2,
                    square.WIDTH,
                    square.HEIGHT,
                    color
                )
                self.append(current_rect)