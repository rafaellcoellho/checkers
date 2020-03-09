from typing import List


class Board:
    def __init__(self):
        from engine.checker import Checker as C
        from engine.defines import Players as P

        self.pieces: List[List] = [
            [C(P.P1, 1, 1), None, C(P.P1, 1, 3), None, C(P.P1, 1, 5), None, C(P.P1, 1, 7), None],
            [None, C(P.P1, 2, 2), None, C(P.P1, 2, 4), None, C(P.P1, 2, 6), None, C(P.P1, 2, 8)],
            [C(P.P1, 3, 1), None, C(P.P1, 3, 3), None, C(P.P1, 3, 5), None, C(P.P1, 3, 7), None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, C(P.P2, 6, 2), None, C(P.P1, 6, 4), None, C(P.P1, 6, 6), None, C(P.P1, 6, 8)],
            [C(P.P2, 7, 1), None, C(P.P2, 7, 3), None, C(P.P2, 7, 5), None, C(P.P2, 7, 7), None],
            [None, C(P.P2, 8, 2), None, C(P.P1, 8, 4), None, C(P.P1, 8, 6), None, C(P.P1, 8, 8)],
        ]
        self.active_player = P.P1

    def __repr__(self):
        return f"Board(pieces=%r)" % self.pieces

    def __str__(self):
        def format_lines(line):
            return "\n\t[" + ",".join(str(piece) for piece in line) + "]"

        lines = list(map(format_lines, self.pieces))
        return "[" + "".join(lines) + "\n]"
