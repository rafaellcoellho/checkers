from typing import List


class Board:
    def __init__(self):
        from engine.checker import Checker as C
        from engine.defines import Players as P

        self.pieces: List[List[C]] = [
            [C(P.P1, 0, 0), None, C(P.P1, 0, 2), None, C(P.P1, 0, 4), None, C(P.P1, 0, 6), None],
            [None, C(P.P1, 1, 1), None, C(P.P1, 1, 3), None, C(P.P1, 1, 5), None, C(P.P1, 1, 7)],
            [C(P.P1, 2, 0), None, C(P.P1, 2, 2), None, C(P.P1, 2, 4), None, C(P.P1, 2, 6), None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, C(P.P2, 5, 1), None, C(P.P2, 5, 3), None, C(P.P2, 5, 5), None, C(P.P2, 5, 7)],
            [C(P.P2, 6, 0), None, C(P.P2, 6, 2), None, C(P.P2, 6, 4), None, C(P.P2, 6, 6), None],
            [None, C(P.P2, 7, 1), None, C(P.P2, 7, 3), None, C(P.P2, 7, 5), None, C(P.P2, 7, 7)],
        ]
        self.active_player = P.P1

    def __repr__(self):
        return f"Board(pieces=%r)" % self.pieces

    def __str__(self):
        def format_piece(piece):
            if piece is None:
                return "   "
            return str(piece)

        def format_lines(line):
            return "\n\t[" + ",".join(format_piece(piece) for piece in line) + "]"

        lines = list(map(format_lines, self.pieces))
        lines_reversed = list(reversed(lines))
        return "[" + "".join(lines_reversed) + "\n]"

    def is_valid_selection(self, from_row, from_col):
        board_selection = self.pieces[from_row][from_col]
        if board_selection is None:
            return False
        elif board_selection.player == self.active_player:
            return True
        else:
            return False

    def can_capture_piece(self, row, col):
        piece_to_capture = self.pieces[row][col]
        if piece_to_capture is None:
            return False
        elif piece_to_capture.player == self.active_player:
            return False
        else:
            return True

    def is_valid_p1_pawn_move(self, to_row, to_col, from_row, from_col):
        from engine.defines import Players

        if (to_row - from_row) == 1 and (to_col - from_col) == -1:
            return True
        elif (to_row - from_row) == 1 and (to_col - from_col) == 1:
            return True
        elif (to_row - from_row) == 2 and (to_col - from_col) == -2:  # try capture left
            return self.can_capture_piece(from_row + 1, from_col - 1, Players.P1)
        elif (to_row - from_row) == 2 and (to_col - from_col) == 2:  # try capture right
            return self.can_capture_piece(from_row + 1, from_col + 1, Players.P1)

        return False

    def is_valid_p2_pawn_move(self, to_row, to_col, from_row, from_col):
        from engine.defines import Players

        if (to_row - from_row) == -1 and (to_col - from_col) == -1:
            return True
        elif (to_row - from_row) == -1 and (to_col - from_col) == 1:
            return True
        elif (to_row - from_row) == -2 and (to_col - from_col) == -2:  # try capture left
            return self.can_capture_piece(from_row - 1, from_col - 1, Players.P2)
        elif (to_row - from_row) == -2 and (to_col - from_col) == 2:  # try capture right
            return self.can_capture_piece(from_row - 1, from_col + 1, Players.P2)

        return False

    def is_valid_pawn_move(self, from_row, from_col, to_row, to_col):
        from engine.defines import Players

        if self.pieces[to_row][to_col] is not None:
            return False

        if self.pieces[from_row][from_col].player == Players.P1:
            return self.is_valid_p1_pawn_move(to_row, to_col, from_row, from_col)

        if self.pieces[from_row][from_col].player == Players.P2:
            return self.is_valid_p2_pawn_move(to_row, to_col, from_row, from_col)

    def is_valid_king_move(self, from_row, from_col, to_row, to_col):
        row_direction = 1 if from_row < to_row else -1
        col_direction = 1 if from_col < to_col else -1

        board_row_coord = list(range(from_row, to_row, row_direction))[1:]
        board_col_coord = list(range(from_col, to_col, col_direction))[1:]
        board_coord = list(zip(board_row_coord, board_col_coord))
        board_values = [self.pieces[row][col] for row, col in board_coord]

        if all(piece is None for piece in board_values) is True:
            return True
        else:
            pieces_in_between = list([p for p in board_values if p is not None])
            enemy_pieces_in_between = list([p for p in pieces_in_between if p.player is not self.active_player])
            ally_pieces_in_between = list([p for p in pieces_in_between if p.player is self.active_player])

            if len(ally_pieces_in_between) > 0 or len(enemy_pieces_in_between) > 1:
                return False
            else:
                return True
