from .defines import square_player_state, square_color
from .square import Square

class Board():
    def __init__(self):
        initial_state = []

        is_black = True
        for row in range(8):
            initial_state.append([])
            for _ in range(8):
                if is_black:
                    color = square_color.BLACK
                else:
                    color = square_color.WHITE
                is_black = not is_black

                initial_state[row].append(
                    Square(color)
                )
            is_black = not is_black
        
        self.state = initial_state