from .defines import square_player_state, square_color
from .square import Square

class Board():
    def __init__(self):
        initial_state = []

        for row in range(8):
            initial_state.append([])
            for column in range(8):
                def is_even(x):
                    return x % 2 == 0

                player_state = square_player_state.EMPTY

                if is_even(row) == is_even(column):
                    color = square_color.WHITE
                else:
                    color = square_color.BLACK
                    if row in [0, 1, 2]:
                        player_state = square_player_state.CHECKER_BLUE
                    elif row in [5, 6, 7]:
                        player_state = square_player_state.CHECKER_RED

                initial_state[row].append(
                    Square(row+1, column+1, color, player_state)
                )
        self.state = initial_state
    
    def __repr__(self):
        output = ["[\n"]
        for row in self.state:
            output.append("\t[ ")
            for square in row:
                representation = []
                if square.color == square_color.WHITE:
                    representation.append("w")
                elif square.color == square_color.BLACK:
                    representation.append("b")

                if square.player_state == square_player_state.CHECKER_BLUE:
                    representation.append(" cb")
                elif square.player_state == square_player_state.CHECKER_RED:
                    representation.append(" cr")
                
                if square.column != 8:
                    representation.append(", ")

                output.append("".join(representation))
            output.append(" ]\n")
        output.append("]\n")
        return "".join(output)