import pytest
from engine.board import Board

@pytest.fixture
def board():
    return Board()


@pytest.fixture
def board_simplified():
    from engine.checker import Checker as C
    from engine.defines import Players as P

    sb = Board()
    sb.pieces = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, C(P.P2, 3, 1), None, C(P.P1, 3, 3), None, None, None, None],
        [None, None,      C(P.P2, 4, 2), None, C(P.P1, 4, 4), None, None, None],
        [None, None, None,          C(P.P1, 5, 3), None, C(P.P2, 5, 5), None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
    ]

    return sb
