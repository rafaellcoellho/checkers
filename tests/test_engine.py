from engine.defines import Players


def test_begin_with_player_one(board):
    assert board.active_player is Players.P1


def test_is_valid_selection(board):
    assert board.is_valid_selection(0, 0) is True
    assert board.is_valid_selection(7, 7) is False
    assert board.is_valid_selection(0, 1) is False

    board.active_player = Players.P2
    assert board.is_valid_selection(0, 0) is False
    assert board.is_valid_selection(7, 7) is True
    assert board.is_valid_selection(0, 1) is False
