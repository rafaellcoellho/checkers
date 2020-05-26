import arcade
from enum import IntEnum


class Square(IntEnum):
    WIDTH = 70
    HEIGHT = 70
    MARGIN = 3


class Window(IntEnum):
    WIDTH = (Square.WIDTH + Square.MARGIN) * 8 + Square.MARGIN
    HEIGHT = (Square.HEIGHT + Square.MARGIN) * 8 + Square.MARGIN


class Players(IntEnum):
    P1 = 1
    P2 = 2


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

    def create(self):
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


class Checker(arcade.Sprite):
    def __init__(self, player, initial_row: int, initial_column: int, is_king: bool = False):
        self.row = initial_row
        self.column = initial_column
        self.player = player
        self.is_king = is_king

        x, y = self.get_top_left_coord()
        sprite_filename = ":resources:images/pinball/pool_cue_ball.png"
        if self.player == Players.P1:
            sprite_color = arcade.color.RED
        else:
            sprite_color = arcade.color.BLUE

        super().__init__(sprite_filename, center_x=x, center_y=y)
        self.color = sprite_color

    def get_top_left_coord(self):
        width = Square.WIDTH
        height = Square.HEIGHT
        margin = Square.MARGIN

        return (
            (margin + width) * self.column + margin + width // 2,
            (margin + height) * self.row + margin + height // 2
        )

    def move(self, row, column):
        self.row = row
        self.column = column

    def update(self):
        x, y = self.get_top_left_coord()
        self.center_x = x
        self.center_y = y


class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title: str, board):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        self.checkers_list = None
        self.checker = None

        self.grid = None
        self.board = board

    def setup(self):
        self.grid = Grid()
        self.grid.create()

        self.checker = Checker(Players.P1, 7, 0)

        self.checkers_list = arcade.SpriteList()
        self.checkers_list.append(self.checker)

    def on_draw(self):
        arcade.start_render()
        self.grid.draw()

        self.checkers_list.draw()

    def on_update(self, delta_time: float):
        self.checkers_list.update()

    def on_mouse_press(self, x: float, y: float, button: int, key_modifiers: int):
        column = int(x // (float(Square.WIDTH + Square.MARGIN)))
        row = int(y // (float(Square.HEIGHT + Square.MARGIN)))

        self.checkers_list[0].move(row, column)
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
