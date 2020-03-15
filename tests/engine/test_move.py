import pytest
from engine.defines import Players
from engine.checker import Checker
from engine.utils import cn


@pytest.mark.parametrize("players", [(Players.P1, Players.P2), (Players.P2, Players.P1)])
def test_move_to_occupied_square(empty_board, players):
    empty_board.active_player = players[0]
    empty_board.pieces[3][3] = Checker(players[0], *cn("D4"))
    empty_board.pieces[4][4] = Checker(players[0], *cn("E5"))
    assert empty_board.move(*cn("D4", "E5")) is False
