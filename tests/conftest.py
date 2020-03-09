import pytest


@pytest.fixture
def board():
    from engine.board import Board
    return Board()
