def test_begin_with_player_one(board):
    from engine.defines import Players

    assert board.active_player is Players.P1
