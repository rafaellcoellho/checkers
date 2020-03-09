from typing import List
from engine.checker import Checker
from engine.defines import Players


class Board:
    def __init__(self):

        self.pieces: List[List] = [[]]
        self.active_player = Players.P1

    def __repr__(self):
        return f"Board(state=%r)" % self.pieces

    def __str__(self):
        def format_lines(line):
            return "\n\t[" + ",".join(str(piece) for piece in line) + "]"

        lines = list(map(format_lines, self.pieces))
        return "[" + "".join(lines) + "\n]"
