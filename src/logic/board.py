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

                if is_even(row) == is_even(column):
                    color = square_color.WHITE
                else:
                    color = square_color.BLACK

                initial_state[row].append(
                    Square(row+1, column+1, color)
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
                
                if square.column != 8:
                    representation.append(", ")

                output.append("".join(representation))
            output.append(" ]\n")
        output.append("]\n")
        return "".join(output)