from engine.defines import Players
from engine.utils import cn


def test_begin_with_player_one(initial_board):
    assert initial_board.active_player is Players.P1


def test_is_valid_selection(initial_board):
    assert initial_board.is_valid_selection(*cn("A1")) is True
    assert initial_board.is_valid_selection(*cn("H8")) is False
    assert initial_board.is_valid_selection(*cn("B1")) is False

    initial_board.active_player = Players.P2
    assert initial_board.is_valid_selection(*cn("A1")) is False
    assert initial_board.is_valid_selection(*cn("H8")) is True
    assert initial_board.is_valid_selection(*cn("B1")) is False


def test_game_winner(empty_board):
    from engine.checker import Checker

    empty_board.pieces[0][0] = Checker(Players.P1, *cn("A1"))
    assert empty_board.game_winner() is Players.P1

    empty_board.pieces[7][7] = Checker(Players.P2, *cn("H8"))
    assert empty_board.game_winner() is None

    empty_board.pieces[0][0] = None
    assert empty_board.game_winner() is Players.P2
