import arcade
from enum import IntEnum


class Square(IntEnum):
    WIDTH = 70
    HEIGHT = 70
    MARGIN = 3


class Window(IntEnum):
    WIDTH = (Square.WIDTH + Square.MARGIN) * 8 + Square.MARGIN
    HEIGHT = (Square.HEIGHT + Square.MARGIN) * 8 + Square.MARGIN


class Grid(arcade.ShapeElementList):
    def __init__(self):
        super().__init__()
        self.board_layout = [
            ["B", "W", "B", "W", "B", "W", "B", "W"],
            ["W", "B", "W", "B", "W", "B", "W", "B"],
            ["B", "W", "B", "W", "B", "W", "B", "W"],
            ["W", "B", "W", "B", "W", "B", "W", "B"],
            ["B", "W", "B", "W", "B", "W", "B", "W"],
            ["W", "B", "W", "B", "W", "B", "W", "B"],
            ["B", "W", "B", "W", "B", "W", "B", "W"],
            ["W", "B", "W", "B", "W", "B", "W", "B"],
        ]

    def update(self):
        width = Square.WIDTH
        height = Square.HEIGHT
        margin = Square.MARGIN

        for shape in self:
            self.remove(shape)

        for row_index, row in enumerate(self.board_layout):
            for column_index, square in enumerate(row):
                color = None
                if square == "W":
                    color = arcade.color.WHITE
                elif square == "B":
                    color = arcade.color.BLACK

                current_rect = arcade.create_rectangle_filled(
                    (margin + width) * column_index + margin + width // 2,
                    (margin + height) * row_index + margin + height // 2,
                    float(width),
                    float(height),
                    color
                )
                self.append(current_rect)


class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title: str, board):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        self.grid = None
        self.board = board

    def setup(self):
        self.grid = Grid()

    def on_update(self, delta_time: float):
        self.grid.update()

    def on_draw(self):
        arcade.start_render()
        self.grid.draw()

    def on_mouse_press(self, x: float, y: float, button: int, key_modifiers: int):
        column = int(x // (float(Square.WIDTH + Square.MARGIN)))
        row = int(y // (float(Square.HEIGHT + Square.MARGIN)))

        print(column, row)


class GameUi:
    def __init__(self, board=None):
        self.board = board

    def run(self):
        game_window = GameWindow(
            Window.WIDTH,
            Window.HEIGHT,
            'checkers',
            self.board
        )
        game_window.setup()
        arcade.run()
