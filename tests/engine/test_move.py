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


def test_move_invalid_index(empty_board):
    empty_board.active_player = Players.P1
    empty_board.pieces[3][3] = Checker(Players.P1, *cn("D4"))
    assert empty_board.move(*cn("D4", "A9")) is False
    assert empty_board.move(*cn("I1", "E5")) is False


@pytest.mark.parametrize("info", [{"player": Players.P1, "coord": "E5"}, {"player": Players.P2, "coord": "C3"}])
def test_move_pawn(empty_board, info):
    empty_board.active_player = info["player"]
    moving_piece = Checker(info["player"], *cn("D4"))

    empty_board.pieces[3][3] = moving_piece
    assert empty_board.move(*cn("D4", info["coord"])) is True
    assert empty_board.pieces[3][3] is None

    row, col = cn(info["coord"])
    assert empty_board.pieces[row][col] is moving_piece
    assert moving_piece.row == row
    assert moving_piece.column == col


@pytest.mark.parametrize("players", [(Players.P1, Players.P2), (Players.P2, Players.P1)])
def test_capture_pawn(empty_board, players):
    empty_board.active_player = players[0]

    moving_piece = Checker(players[0], *cn("D4"))
    empty_board.pieces[3][3] = moving_piece

    empty_board.pieces[4][4] = Checker(players[1], *cn("E5"))

    assert empty_board.move(*cn("D4", "F6")) is True
    assert empty_board.pieces[3][3] is None
    assert empty_board.pieces[5][5] is moving_piece
    assert moving_piece.row == 5
    assert moving_piece.column == 5
    assert empty_board.pieces[4][4] is None


