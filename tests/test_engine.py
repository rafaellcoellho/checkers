import pytest
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


def test_is_valid_pawn_move(board, board_simplified):
    assert board.is_valid_pawn_move(2, 2, 3, 1) is True     # C3 -> B4 valid
    assert board.is_valid_pawn_move(2, 2, 3, 2) is False    # C3 -> C4 invalid
    assert board.is_valid_pawn_move(2, 2, 3, 3) is True     # C3 -> D4 valid
    assert board.is_valid_pawn_move(2, 2, 1, 1) is False    # C3 -> B2 invalid
    assert board.is_valid_pawn_move(2, 2, 1, 2) is False    # C3 -> C2 invalid
    assert board.is_valid_pawn_move(2, 2, 1, 3) is False    # C3 -> D2 invalid
    assert board.is_valid_pawn_move(2, 2, 2, 1) is False    # C3 -> B3 invalid
    assert board.is_valid_pawn_move(2, 2, 2, 3) is False    # C3 -> D3 invalid

    assert board.is_valid_pawn_move(5, 1, 4, 0) is True     # B6 -> A5 valid
    assert board.is_valid_pawn_move(5, 1, 4, 1) is False    # B6 -> B5 invalid
    assert board.is_valid_pawn_move(5, 1, 4, 2) is True     # B6 -> C5 valid
    assert board.is_valid_pawn_move(5, 1, 6, 0) is False    # B6 -> A7 invalid
    assert board.is_valid_pawn_move(5, 1, 6, 1) is False    # B6 -> B7 invalid
    assert board.is_valid_pawn_move(5, 1, 6, 2) is False    # B6 -> C7 invalid
    assert board.is_valid_pawn_move(5, 1, 5, 0) is False    # B6 -> A6 invalid
    assert board.is_valid_pawn_move(5, 1, 5, 2) is False    # B6 -> C6 invalid

    assert board_simplified.is_valid_pawn_move(4, 4, 5, 5) is False    # E5 -> F6 invalid because enemy pawn is there
    assert board_simplified.is_valid_pawn_move(4, 4, 6, 6) is True     # E5 -> G7 valid because enemy pawn is there
    assert board_simplified.is_valid_pawn_move(4, 4, 5, 3) is False    # E5 -> D6 invalid because allied pawn is there
    assert board_simplified.is_valid_pawn_move(4, 4, 6, 2) is False    # E5 -> C7 invalid because allied pawn is there

    assert board_simplified.is_valid_pawn_move(4, 2, 3, 1) is False    # C5 -> B4 invalid because allied pawn is there
    assert board_simplified.is_valid_pawn_move(4, 2, 2, 0) is False    # C5 -> A3 invalid because allied pawn is there
    assert board_simplified.is_valid_pawn_move(4, 2, 3, 3) is False    # C5 -> D4 invalid because enemy pawn is there
    assert board_simplified.is_valid_pawn_move(4, 2, 2, 4) is True    # C5 -> E3 valid because enemy pawn is there
