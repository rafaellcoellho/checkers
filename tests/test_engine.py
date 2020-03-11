import pytest
from engine.defines import Players


def _(origin: str, destination: str=None):

    col_char, row_char = origin
    from_row = int(row_char) - 1
    from_col = ord(col_char) - 65

    if destination is None:
        return [from_row, from_col]

    col_char, row_char = destination
    to_row = int(row_char) - 1
    to_col = ord(col_char) - 65

    return [from_row, from_col, to_row, to_col]


def test_begin_with_player_one(initial_board):
    assert initial_board.active_player is Players.P1


def test_is_valid_selection(initial_board):
    assert initial_board.is_valid_selection(*_("A1")) is True
    assert initial_board.is_valid_selection(*_("H8")) is False
    assert initial_board.is_valid_selection(*_("B1")) is False

    initial_board.active_player = Players.P2
    assert initial_board.is_valid_selection(*_("A1")) is False
    assert initial_board.is_valid_selection(*_("H8")) is True
    assert initial_board.is_valid_selection(*_("B1")) is False


def test_is_valid_pawn_basic_move(initial_board):
    assert initial_board.is_valid_pawn_move(*_("C3", "B4")) is True
    assert initial_board.is_valid_pawn_move(*_("C3", "C4")) is False
    assert initial_board.is_valid_pawn_move(*_("C3", "D4")) is True
    assert initial_board.is_valid_pawn_move(*_("C3", "B2")) is False
    assert initial_board.is_valid_pawn_move(*_("C3", "C2")) is False
    assert initial_board.is_valid_pawn_move(*_("C3", "D2")) is False
    assert initial_board.is_valid_pawn_move(*_("C3", "B3")) is False
    assert initial_board.is_valid_pawn_move(*_("C3", "D3")) is False

    assert initial_board.is_valid_pawn_move(*_("B6", "A5")) is True
    assert initial_board.is_valid_pawn_move(*_("B6", "B5")) is False
    assert initial_board.is_valid_pawn_move(*_("B6", "C5")) is True
    assert initial_board.is_valid_pawn_move(*_("B6", "A7")) is False
    assert initial_board.is_valid_pawn_move(*_("B6", "B7")) is False
    assert initial_board.is_valid_pawn_move(*_("B6", "C7")) is False
    assert initial_board.is_valid_pawn_move(*_("B6", "A6")) is False
    assert initial_board.is_valid_pawn_move(*_("B6", "C6")) is False


def test_is_valid_pawn_capture_move(empty_board):
    from engine.checker import Checker
    from engine.defines import Players

    empty_board.pieces[4][4] = Checker(Players.P1, *_("E5"))
    empty_board.pieces[5][5] = Checker(Players.P2, *_("F6"))
    empty_board.pieces[5][3] = Checker(Players.P1, *_("D6"))

    assert empty_board.is_valid_pawn_move(*_("E5", "F6")) is False
    assert empty_board.is_valid_pawn_move(*_("E5", "G7")) is True
    assert empty_board.is_valid_pawn_move(*_("E5", "D6")) is False
    assert empty_board.is_valid_pawn_move(*_("E5", "C7")) is False

    empty_board.pieces[4][2] = Checker(Players.P2, *_("C5"))
    empty_board.pieces[3][1] = Checker(Players.P2, *_("A3"))
    empty_board.pieces[3][3] = Checker(Players.P1, *_("D4"))

    assert empty_board.is_valid_pawn_move(*_("C5", "B4")) is False
    assert empty_board.is_valid_pawn_move(*_("C5", "A3")) is False
    assert empty_board.is_valid_pawn_move(*_("C5", "D4")) is False
    assert empty_board.is_valid_pawn_move(*_("C5", "E3")) is True


@pytest.mark.parametrize("players", [(Players.P1, Players.P2), (Players.P2, Players.P1)])
def test_detect_chips_between(empty_board, players):
    from engine.checker import Checker

    # Player 1
    empty_board.pieces[4][0] = Checker(players[0], *_("A5"))
    assert empty_board.no_chips_between(*_("A5", "D8")) is True

    empty_board.pieces[2][6] = Checker(players[1], *_("C7"))
    assert empty_board.no_chips_between(*_("A5", "D8")) is True

    empty_board.pieces[5][1] = Checker(players[0], *_("B6"))
    assert empty_board.no_chips_between(*_("A5", "D8")) is False

    # Player 2
    empty_board.pieces[3][7] = Checker(players[1], *_("H4"))
    assert empty_board.no_chips_between(*_("H4", "E1")) is True

    empty_board.pieces[1][4] = Checker(players[0], *_("F2"))
    assert empty_board.no_chips_between(*_("H4", "E1")) is True

    empty_board.pieces[2][6] = Checker(players[1], *_("G3"))
    assert empty_board.no_chips_between(*_("H4", "E1")) is False
