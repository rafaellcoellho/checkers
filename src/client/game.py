import arcade
from enum import IntEnum
from engine.defines import Players
from engine.utils import cn, nc


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
        self.been_dragged = False

        x, y = self.get_coord()
        sprite_filename = ":resources:images/pinball/pool_cue_ball.png"
        if self.player == Players.P1:
            sprite_color = arcade.color.RED
        else:
            sprite_color = arcade.color.BLUE

        super().__init__(sprite_filename, center_x=x, center_y=y)
        self.color = sprite_color

    def get_coord(self):
        width = Square.WIDTH
        height = Square.HEIGHT
        margin = Square.MARGIN

        return (
            (margin + width) * self.column + margin + width // 2,
            (margin + height) * self.row + margin + height // 2
        )

    def belongs_to(self, p):
        return self.player == p

    def move(self, row, column):
        self.row = row
        self.column = column

    def update(self):
        if not self.been_dragged:
            x, y = self.get_coord()
            self.center_x = x
            self.center_y = y


class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title: str, player, client, receive_queue, turn_dialog):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        self.checkers_list = None
        self.checker = None
        self.dragged_checker = None

        self.tick = 0
        self.my_turn = True if player is Players.P1 else False
        self.turn_dialog = turn_dialog

        self.grid = None
        self.player = player
        self.client = client
        self.receive_queue = receive_queue

    def setup(self):
        self.grid = Grid()
        self.grid.create()

        self.checkers_list = arcade.SpriteList()

        player_1_starter_checker_pos = [
            (0, 0), (0, 2), (0, 4), (0, 6),
            (1, 1), (1, 3), (1, 5), (1, 7),
            (2, 0), (2, 2), (2, 4), (2, 6),
        ]
        for row, column in player_1_starter_checker_pos:
            self.checkers_list.append(
                Checker(Players.P1, row, column)
            )

        player_2_starter_checker_pos = [
            (5, 1), (5, 3), (5, 5), (5, 7),
            (6, 0), (6, 2), (6, 4), (6, 6),
            (7, 1), (7, 3), (7, 5), (7, 7),
        ]
        for row, column in player_2_starter_checker_pos:
            self.checkers_list.append(
                Checker(Players.P2, row, column)
            )

    def on_draw(self):
        arcade.start_render()
        self.grid.draw()

        self.checkers_list.draw()

    def on_update(self, delta_time: float):
        self.checkers_list.update()

        self.tick += delta_time
        if self.tick > 1.0:
            if self.receive_queue.empty() is False:
                message = self.receive_queue.get()

                command = message[:3]
                if command == "mov":
                    from_coord = message[4:6]
                    to_coord = message[7:9]

                    from_row, from_col, to_row, to_col = cn(from_coord, to_coord)

                    real_x = (Square.MARGIN + Square.WIDTH) * from_col + Square.MARGIN + Square.WIDTH // 2
                    real_y = (Square.MARGIN + Square.HEIGHT) * from_row + Square.MARGIN + Square.HEIGHT // 2

                    hit_sprites = arcade.get_sprites_at_point((real_x, real_y), self.checkers_list)

                    if len(hit_sprites) > 0:
                        checker = hit_sprites[0]
                        checker.move(to_row, to_col)
                elif command == "ytn":
                    self.my_turn = True
                    self.turn_dialog.is_my_turn()
                elif command == "ntn":
                    self.my_turn = False
                elif command == "rmv":
                    coord = message[4:6]
                    from_row, from_col = cn(coord)

                    real_x = (Square.MARGIN + Square.WIDTH) * from_col + Square.MARGIN + Square.WIDTH // 2
                    real_y = (Square.MARGIN + Square.HEIGHT) * from_row + Square.MARGIN + Square.HEIGHT // 2

                    hit_sprites = arcade.get_sprites_at_point((real_x, real_y), self.checkers_list)

                    if len(hit_sprites) > 0:
                        checker = hit_sprites[0]
                        checker.remove_from_sprite_lists()
                elif command == "kin":
                    coord = message[4:6]
                    from_row, from_col = cn(coord)

                    real_x = (Square.MARGIN + Square.WIDTH) * from_col + Square.MARGIN + Square.WIDTH // 2
                    real_y = (Square.MARGIN + Square.HEIGHT) * from_row + Square.MARGIN + Square.HEIGHT // 2

                    hit_sprites = arcade.get_sprites_at_point((real_x, real_y), self.checkers_list)

                    if len(hit_sprites) > 0:
                        checker = hit_sprites[0]
                        if checker.player == Players.P1:
                            checker.color = arcade.color.RED_DEVIL
                        else:
                            checker.color = arcade.color.BLUE_GREEN
                elif command == "win":
                    self.turn_dialog.show_message(" You Win ")
                elif command == "los":
                    self.turn_dialog.show_message("You Lost")

                else:
                    print(f"Unknown command {message}")

            self.tick = 0

    def on_mouse_press(self, x: float, y: float, button: int, key_modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT and self.my_turn is True:
            hit_sprites = arcade.get_sprites_at_point((x, y), self.checkers_list)

            if len(hit_sprites) > 0:
                checker = hit_sprites[0]

                if checker.belongs_to(self.player):
                    self.dragged_checker = checker
                    self.dragged_checker.been_dragged = True

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.dragged_checker is not None:
            self.dragged_checker.center_x = x
            self.dragged_checker.center_y = y

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT and self.dragged_checker is not None:
            row = int(y // (float(Square.HEIGHT + Square.MARGIN)))
            column = int(x // (float(Square.WIDTH + Square.MARGIN)))

            if 0 <= column <= 7 and 0 <= row <= 7:
                from_x, from_y = self.dragged_checker.get_coord()
                from_index = (
                    int(from_y // (float(Square.HEIGHT + Square.MARGIN))),
                    int(from_x // (float(Square.WIDTH + Square.MARGIN)))
                )
                to_index = (row, column)

                from_in_notation, to_in_notation = nc(from_index, to_index)

                self.dragged_checker.move(row, column)
                self.client.send_to_server(f"mov:{from_in_notation},{to_in_notation}")

            self.dragged_checker.been_dragged = False
            self.dragged_checker = None


class GameUi:
    def __init__(self, player, client, receive_queue):
        self.player = player
        self.client = client
        self.receive_queue = receive_queue

    def run(self):
        from client.dialogs import PassTurnDialog

        is_my_turn = True if self.player is Players.P1 else False
        turn_dialog = PassTurnDialog(self.client, is_my_turn)
        turn_dialog.run()

        game_window = GameWindow(
            Window.WIDTH,
            Window.HEIGHT,
            'checkers',
            self.player,
            self.client,
            self.receive_queue,
            turn_dialog
        )
        game_window.setup()
        arcade.run()
