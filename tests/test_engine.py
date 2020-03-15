import pytest
from engine.defines import Players


def _(origin: str, destination: str = None):
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
    # Normal moves
    assert initial_board.is_valid_pawn_move(*_("C3", "B4")) is True
    assert initial_board.is_valid_pawn_move(*_("C3", "C4")) is False
    assert initial_board.is_valid_pawn_move(*_("C3", "D4")) is True
    assert initial_board.is_valid_pawn_move(*_("C3", "B2")) is False
    assert initial_board.is_valid_pawn_move(*_("C3", "C2")) is False
    assert initial_board.is_valid_pawn_move(*_("C3", "D2")) is False
    assert initial_board.is_valid_pawn_move(*_("C3", "B3")) is False
    assert initial_board.is_valid_pawn_move(*_("C3", "D3")) is False
    # Weird moves
    assert initial_board.is_valid_pawn_move(*_("C3", "C5")) is False
    assert initial_board.is_valid_pawn_move(*_("C3", "D8")) is False

    # Normal moves
    assert initial_board.is_valid_pawn_move(*_("B6", "A5")) is True
    assert initial_board.is_valid_pawn_move(*_("B6", "B5")) is False
    assert initial_board.is_valid_pawn_move(*_("B6", "C5")) is True
    assert initial_board.is_valid_pawn_move(*_("B6", "A7")) is False
    assert initial_board.is_valid_pawn_move(*_("B6", "B7")) is False
    assert initial_board.is_valid_pawn_move(*_("B6", "C7")) is False
    assert initial_board.is_valid_pawn_move(*_("B6", "A6")) is False
    assert initial_board.is_valid_pawn_move(*_("B6", "C6")) is False
    # Weird moves
    assert initial_board.is_valid_pawn_move(*_("B6", "G1")) is False
    assert initial_board.is_valid_pawn_move(*_("B6", "E5")) is False


@pytest.mark.parametrize("players", [(Players.P1, Players.P2), (Players.P2, Players.P1)])
def test_is_valid_pawn_capture_move(empty_board, players):
    from engine.checker import Checker

    empty_board.active_player = players[0]
    empty_board.pieces[4][4] = Checker(players[0], *_("E5"))
    empty_board.pieces[5][5] = Checker(players[1], *_("F6"))
    empty_board.pieces[5][3] = Checker(players[0], *_("D6"))
    empty_board.pieces[3][3] = Checker(players[1], *_("D4"))
    empty_board.pieces[3][5] = Checker(players[0], *_("F4"))

    assert empty_board.is_valid_pawn_move(*_("E5", "F6")) is False
    assert empty_board.is_valid_pawn_move(*_("E5", "G7")) is True
    assert empty_board.is_valid_pawn_move(*_("E5", "D6")) is False
    assert empty_board.is_valid_pawn_move(*_("E5", "C7")) is False
    assert empty_board.is_valid_pawn_move(*_("E5", "D4")) is False
    assert empty_board.is_valid_pawn_move(*_("E5", "C3")) is True
    assert empty_board.is_valid_pawn_move(*_("E5", "F4")) is False
    assert empty_board.is_valid_pawn_move(*_("E5", "G3")) is False


@pytest.mark.parametrize("players", [(Players.P1, Players.P2), (Players.P2, Players.P1)])
def test_is_valid_king_move(empty_board, players):
    from engine.checker import Checker

    empty_board.active_player = players[0]
    empty_board.pieces[4][0] = Checker(players[0], *_("A5"))
    # Normal moves
    assert empty_board.is_valid_king_move(*_("A5", "D8")) is True
    assert empty_board.is_valid_king_move(*_("A5", "A7")) is False
    assert empty_board.is_valid_king_move(*_("A5", "C5")) is False
    assert empty_board.is_valid_king_move(*_("A5", "C3")) is True
    assert empty_board.is_valid_king_move(*_("A5", "A3")) is False
    # Weird moves
    assert empty_board.is_valid_king_move(*_("A5", "D6")) is False
    assert empty_board.is_valid_king_move(*_("A5", "F6")) is False
    assert empty_board.is_valid_king_move(*_("A5", "B8")) is False

    empty_board.pieces[6][2] = Checker(players[1], *_("C7"))
    assert empty_board.is_valid_king_move(*_("A5", "D8")) is True

    empty_board.pieces[5][1] = Checker(players[0], *_("B6"))
    assert empty_board.is_valid_king_move(*_("A5", "D8")) is False

    empty_board.active_player = players[1]
    empty_board.pieces[3][7] = Checker(players[1], *_("H4"))
    # Normal moves
    assert empty_board.is_valid_king_move(*_("H4", "E1")) is True
    assert empty_board.is_valid_king_move(*_("H4", "H2")) is False
    assert empty_board.is_valid_king_move(*_("H4", "F4")) is False
    assert empty_board.is_valid_king_move(*_("H4", "F6")) is True
    assert empty_board.is_valid_king_move(*_("H4", "H6")) is False
    # Weird moves
    assert empty_board.is_valid_king_move(*_("H4", "B2")) is False
    assert empty_board.is_valid_king_move(*_("H4", "C3")) is False
    assert empty_board.is_valid_king_move(*_("H4", "D6")) is False

    empty_board.pieces[1][4] = Checker(players[0], *_("F2"))
    assert empty_board.is_valid_king_move(*_("H4", "E1")) is True

    empty_board.pieces[2][6] = Checker(players[1], *_("G3"))
    assert empty_board.is_valid_king_move(*_("H4", "E1")) is False


def test_game_winner(empty_board):
    from engine.checker import Checker

    empty_board.pieces[0][0] = Checker(Players.P1, *_("A1"))
    assert empty_board.game_winner() is Players.P1

    empty_board.pieces[7][7] = Checker(Players.P2, *_("H8"))
    assert empty_board.game_winner() is None

    empty_board.pieces[0][0] = None
    assert empty_board.game_winner() is Players.P2
