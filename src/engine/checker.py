from typing import Tuple
from engine.defines import Players


class Checker:
    def __init__(self, player: Players, pos: Tuple):
        self.row, self.column = pos
        self.player = player
        self.king = False

    def __repr__(self):
        return f"Checker(belongs_to={self.player.name}," \
               f"{'king' if self.king else 'pawn'}," \
               f"pos={chr(self.column+64)}{self.row})"

    def __str__(self):
        return f"{self.player.name}" \
               f"{'K' if self.king else 'P'}"
