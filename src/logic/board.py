from .defines import SquarePlayerState, SquareColor
from .square import Square


class Board:
    def __init__(self):
        initial_state = []

        for row in range(8):
            initial_state.append([])
            for column in range(8):
                def is_even(x):
                    return x % 2 == 0

                player_state = SquarePlayerState.EMPTY

                if is_even(row) == is_even(column):
                    color = SquareColor.WHITE
                else:
                    color = SquareColor.BLACK
                    if row in [0, 1, 2]:
                        player_state = SquarePlayerState.CHECKER_BLUE
                    elif row in [5, 6, 7]:
                        player_state = SquarePlayerState.CHECKER_RED

                initial_state[row].append(
                    Square(row, column, color, player_state)
                )
        self.state = initial_state
        self.moving_checker = None
        self.possible_moves = None
        self.active_player = SquarePlayerState.CHECKER_BLUE

    def __repr__(self):
        output = ["[\n"]
        for row in self.state:
            output.append("\t[ ")
            for square in row:
                representation = []

                if square.color == SquareColor.WHITE:
                    representation.append("w")
                elif square.color == SquareColor.BLACK:
                    representation.append("b")

                if square.player_state == SquarePlayerState.CHECKER_BLUE:
                    representation.append(" cb")
                elif square.player_state == SquarePlayerState.CHECKER_RED:
                    representation.append(" cr")
                elif square.player_state == SquarePlayerState.EMPTY:
                    representation.append(" e")

                if square.possible_move:
                    representation.append(" pm")

                if square.column != 8:
                    representation.append(", ")

                output.append("".join(representation))
            output.append(" ]\n")
        output.append("]\n")
        return "".join(output)

    def calculate_possible_moves(self, row, column):
        self.reset_possible_moves()
        self.moving_checker = [row, column]
        self.possible_moves = []
        if self.state[row][column].king:
            print('Not implemented yet')
        else:
            if self.active_player == SquarePlayerState.CHECKER_BLUE:
                if row+1 <= 7 and column-1 >= 0:
                    self.possible_moves.append([row+1, column-1])
                    self.state[row+1][column-1].possible_move = True
                if row+1 <= 7 and column+1 <= 7:
                    self.possible_moves.append([row+1, column+1])
                    self.state[row+1][column+1].possible_move = True
            else:
                if row-1 <= 7 and column-1 >= 0:
                    self.possible_moves.append([row-1, column-1])
                    self.state[row-1][column-1].possible_move = True
                if row-1 <= 7 and column+1 <= 7:
                    self.possible_moves.append([row-1, column+1])
                    self.state[row-1][column+1].possible_move = True

    def reset_possible_moves(self):
        self.moving_checker = None
        self.possible_moves = None
        for row in self.state:
            for square in row:
                square.possible_move = False

    def move(self, to_row, to_column):
        from_row = self.moving_checker[0]
        from_column = self.moving_checker[1]
        print(f"Movendo {from_row},{from_column} para {to_row},{to_column}")

        player_state = self.state[from_row][from_column].player_state
        king = self.state[from_row][from_column].king

        self.state[from_row][from_column].player_state = SquarePlayerState.EMPTY
        self.state[from_row][from_column].king = False

        self.state[to_row][to_column].player_state = player_state
        self.state[to_row][to_column].king = king

        if self.active_player == SquarePlayerState.CHECKER_BLUE:
            self.active_player = SquarePlayerState.CHECKER_RED
        else:
            self.active_player = SquarePlayerState.CHECKER_BLUE
        self.reset_possible_moves()

    def is_active_player(self, row, column):
        return self.state[row][column].player_state == self.active_player

    def is_player(self, row, column):
        return self.state[row][column].player_state != SquarePlayerState.EMPTY

