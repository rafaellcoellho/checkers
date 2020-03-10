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
        def format_lines(line):
            return "\n\t[" + ",".join(str(piece) for piece in line) + "]"

        lines = list(map(format_lines, self.pieces))
        return "[" + "".join(lines) + "\n]"

    def is_valid_selection(self, from_row, from_col):
        board_selection = self.pieces[from_row][from_col]
        if board_selection is None:
            return False
        elif board_selection.player == self.active_player:
            return True
        else:
            return False
