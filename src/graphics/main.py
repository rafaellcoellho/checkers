import arcade
from .defines import square,window

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()

        # Desenha tabuleiro
        for i in range(1, 8):
            arcade.draw_line(
                square.WIDTH*i, 0,
                square.WIDTH*i, window.HEIGHT,
                arcade.color.BLACK, 3
            )
            arcade.draw_line(
                0, square.HEIGHT*i,
                window.WIDTH, square.HEIGHT*i,
                arcade.color.BLACK, 3
            )


    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        pass

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass
