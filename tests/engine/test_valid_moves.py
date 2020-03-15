import pytest
from engine.defines import Players
from engine.utils import cn


def test_is_valid_pawn_basic_move(initial_board):
    # Normal moves
    assert initial_board.is_valid_pawn_move(*cn("C3", "B4")) is True
    assert initial_board.is_valid_pawn_move(*cn("C3", "C4")) is False
    assert initial_board.is_valid_pawn_move(*cn("C3", "D4")) is True
    assert initial_board.is_valid_pawn_move(*cn("C3", "B2")) is False
    assert initial_board.is_valid_pawn_move(*cn("C3", "C2")) is False
    assert initial_board.is_valid_pawn_move(*cn("C3", "D2")) is False
    assert initial_board.is_valid_pawn_move(*cn("C3", "B3")) is False
    assert initial_board.is_valid_pawn_move(*cn("C3", "D3")) is False
    # Weird moves
    assert initial_board.is_valid_pawn_move(*cn("C3", "C5")) is False
    assert initial_board.is_valid_pawn_move(*cn("C3", "D8")) is False

    # Normal moves
    assert initial_board.is_valid_pawn_move(*cn("B6", "A5")) is True
    assert initial_board.is_valid_pawn_move(*cn("B6", "B5")) is False
    assert initial_board.is_valid_pawn_move(*cn("B6", "C5")) is True
    assert initial_board.is_valid_pawn_move(*cn("B6", "A7")) is False
    assert initial_board.is_valid_pawn_move(*cn("B6", "B7")) is False
    assert initial_board.is_valid_pawn_move(*cn("B6", "C7")) is False
    assert initial_board.is_valid_pawn_move(*cn("B6", "A6")) is False
    assert initial_board.is_valid_pawn_move(*cn("B6", "C6")) is False
    # Weird moves
    assert initial_board.is_valid_pawn_move(*cn("B6", "G1")) is False
    assert initial_board.is_valid_pawn_move(*cn("B6", "E5")) is False


@pytest.mark.parametrize("players", [(Players.P1, Players.P2), (Players.P2, Players.P1)])
def test_is_valid_pawn_capture_move(empty_board, players):
    from engine.checker import Checker

    empty_board.active_player = players[0]
    empty_board.pieces[4][4] = Checker(players[0], *cn("E5"))
    empty_board.pieces[5][5] = Checker(players[1], *cn("F6"))
    empty_board.pieces[5][3] = Checker(players[0], *cn("D6"))
    empty_board.pieces[3][3] = Checker(players[1], *cn("D4"))
    empty_board.pieces[3][5] = Checker(players[0], *cn("F4"))

    assert empty_board.is_valid_pawn_move(*cn("E5", "F6")) is False
    assert empty_board.is_valid_pawn_move(*cn("E5", "G7")) is True
    assert empty_board.is_valid_pawn_move(*cn("E5", "D6")) is False
    assert empty_board.is_valid_pawn_move(*cn("E5", "C7")) is False
    assert empty_board.is_valid_pawn_move(*cn("E5", "D4")) is False
    assert empty_board.is_valid_pawn_move(*cn("E5", "C3")) is True
    assert empty_board.is_valid_pawn_move(*cn("E5", "F4")) is False
    assert empty_board.is_valid_pawn_move(*cn("E5", "G3")) is False


@pytest.mark.parametrize("players", [(Players.P1, Players.P2), (Players.P2, Players.P1)])
def test_is_valid_king_move(empty_board, players):
    from engine.checker import Checker

    empty_board.active_player = players[0]
    empty_board.pieces[4][0] = Checker(players[0], *cn("A5"))
    # Normal moves
    assert empty_board.is_valid_king_move(*cn("A5", "D8")) is True
    assert empty_board.is_valid_king_move(*cn("A5", "A7")) is False
    assert empty_board.is_valid_king_move(*cn("A5", "C5")) is False
    assert empty_board.is_valid_king_move(*cn("A5", "C3")) is True
    assert empty_board.is_valid_king_move(*cn("A5", "A3")) is False
    # Weird moves
    assert empty_board.is_valid_king_move(*cn("A5", "D6")) is False
    assert empty_board.is_valid_king_move(*cn("A5", "F6")) is False
    assert empty_board.is_valid_king_move(*cn("A5", "B8")) is False

    empty_board.pieces[6][2] = Checker(players[1], *cn("C7"))
    assert empty_board.is_valid_king_move(*cn("A5", "D8")) is True

    empty_board.pieces[5][1] = Checker(players[0], *cn("B6"))
    assert empty_board.is_valid_king_move(*cn("A5", "D8")) is False

    empty_board.active_player = players[1]
    empty_board.pieces[3][7] = Checker(players[1], *cn("H4"))
    # Normal moves
    assert empty_board.is_valid_king_move(*cn("H4", "E1")) is True
    assert empty_board.is_valid_king_move(*cn("H4", "H2")) is False
    assert empty_board.is_valid_king_move(*cn("H4", "F4")) is False
    assert empty_board.is_valid_king_move(*cn("H4", "F6")) is True
    assert empty_board.is_valid_king_move(*cn("H4", "H6")) is False
    # Weird moves
    assert empty_board.is_valid_king_move(*cn("H4", "B2")) is False
    assert empty_board.is_valid_king_move(*cn("H4", "C3")) is False
    assert empty_board.is_valid_king_move(*cn("H4", "D6")) is False

    empty_board.pieces[1][4] = Checker(players[0], *cn("F2"))
    assert empty_board.is_valid_king_move(*cn("H4", "E1")) is True

    empty_board.pieces[2][6] = Checker(players[1], *cn("G3"))
    assert empty_board.is_valid_king_move(*cn("H4", "E1")) is False
