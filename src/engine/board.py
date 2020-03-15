from typing import List, Optional


class Board:
    def __init__(self):
        from engine.checker import Checker as C
        from engine.defines import Players as P

        self.pieces: List[List[Optional[C]]] = [
            [C(P.P1, 0, 0), None, C(P.P1, 0, 2), None, C(P.P1, 0, 4), None, C(P.P1, 0, 6), None],
            [None, C(P.P1, 1, 1), None, C(P.P1, 1, 3), None, C(P.P1, 1, 5), None, C(P.P1, 1, 7)],
            [C(P.P1, 2, 0), None, C(P.P1, 2, 2), None, C(P.P1, 2, 4), None, C(P.P1, 2, 6), None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, C(P.P2, 5, 1), None, C(P.P2, 5, 3), None, C(P.P2, 5, 5), None, C(P.P2, 5, 7)],
            [C(P.P2, 6, 0), None, C(P.P2, 6, 2), None, C(P.P2, 6, 4), None, C(P.P2, 6, 6), None],
            [None, C(P.P2, 7, 1), None, C(P.P2, 7, 3), None, C(P.P2, 7, 5), None, C(P.P2, 7, 7)],
        ]
        self.active_player = P.P1

    def __repr__(self):
        return f"Board(pieces=%r)" % self.pieces

    def __str__(self):
        def format_piece(piece):
            if piece is None:
                return "   "
            return str(piece)

        def format_lines(line):
            return "\n\t[" + ",".join(format_piece(piece) for piece in line) + "]"

        lines = list(map(format_lines, self.pieces))
        lines_reversed = list(reversed(lines))
        return "[" + "".join(lines_reversed) + "\n]"

    def is_valid_selection(self, from_row, from_col):
        board_selection = self.pieces[from_row][from_col]
        if board_selection is None:
            return False
        elif board_selection.player == self.active_player:
            return True
        else:
            return False

    def transfer_checker(self, from_row, from_col, to_row, to_col):
        moving_piece = self.pieces[from_row][from_col]
        moving_piece.row = to_row
        moving_piece.column = to_col
        self.pieces[from_row][from_col] = None
        self.pieces[to_row][to_col] = moving_piece

    def can_capture_piece(self, row, col, from_row, from_col, to_row, to_col, do_move=False):
        piece_to_capture = self.pieces[row][col]
        moving_piece = self.pieces[row][col]
        if piece_to_capture is None:
            return False
        elif piece_to_capture.player == self.active_player:
            return False
        else:
            if do_move:
                self.pieces[row][col] = None
                self.transfer_checker(from_row, from_col, to_row, to_col)

            return True

    def is_valid_p1_pawn_move(self, from_row, from_col, to_row, to_col, do_move=False):
        inputs = [from_row, from_col, to_row, to_col]

        if (to_row - from_row) == 1 and (to_col - from_col) == -1:
            if do_move:
                self.transfer_checker(*inputs)
            return True
        elif (to_row - from_row) == 1 and (to_col - from_col) == 1:
            if do_move:
                self.transfer_checker(*inputs)
            return True
        elif (to_row - from_row) == 2 and (to_col - from_col) == -2:    # try capture left
            return self.can_capture_piece(from_row + 1, from_col - 1, *inputs, do_move)
        elif (to_row - from_row) == 2 and (to_col - from_col) == 2:     # try capture right
            return self.can_capture_piece(from_row + 1, from_col + 1, *inputs, do_move)
        elif (to_row - from_row) == -2 and (to_col - from_col) == -2:   # try capture backwards left
            return self.can_capture_piece(from_row - 1, from_col - 1, *inputs, do_move)
        elif (to_row - from_row) == -2 and (to_col - from_col) == 2:    # try capture backwards right
            return self.can_capture_piece(from_row - 1, from_col + 1, *inputs, do_move)

        return False

    def is_valid_p2_pawn_move(self, from_row, from_col, to_row, to_col, do_move=False):
        inputs = [from_row, from_col, to_row, to_col]

        if (to_row - from_row) == -1 and (to_col - from_col) == -1:
            if do_move:
                self.transfer_checker(*inputs)
            return True
        elif (to_row - from_row) == -1 and (to_col - from_col) == 1:
            if do_move:
                self.transfer_checker(*inputs)
            return True
        elif (to_row - from_row) == -2 and (to_col - from_col) == -2:   # try capture left
            return self.can_capture_piece(from_row - 1, from_col - 1, *inputs, do_move)
        elif (to_row - from_row) == -2 and (to_col - from_col) == 2:    # try capture right
            return self.can_capture_piece(from_row - 1, from_col + 1, *inputs, do_move)
        elif (to_row - from_row) == 2 and (to_col - from_col) == -2:    # try capture backwards left
            return self.can_capture_piece(from_row + 1, from_col - 1, *inputs, do_move)
        elif (to_row - from_row) == 2 and (to_col - from_col) == 2:     # try capture backwards right
            return self.can_capture_piece(from_row + 1, from_col + 1, *inputs, do_move)

        return False

    def is_valid_pawn_move(self, from_row, from_col, to_row, to_col, do_move=False):
        from engine.defines import Players

        if self.pieces[from_row][from_col].player == Players.P1:
            return self.is_valid_p1_pawn_move(from_row, from_col, to_row, to_col, do_move)

        if self.pieces[from_row][from_col].player == Players.P2:
            return self.is_valid_p2_pawn_move(from_row, from_col, to_row, to_col, do_move)

    def is_valid_king_move(self, from_row, from_col, to_row, to_col, do_move=False):
        if to_row == from_row:
            return False
        elif to_col == from_col:
            return False

        if to_row > from_row and to_col > from_col:
            if (to_row - from_row) != (to_col - from_col):
                return False
        if to_row < from_row and to_col < from_col:
            if (from_row - to_row) != (from_col - to_col):
                return False
        if to_row < from_row and to_col > from_col:
            if (from_row - to_row) != (to_col - from_col):
                return False
        if to_row > from_row and to_col < from_col:
            if (to_row - from_row) != (from_col - to_col):
                return False

        row_direction = 1 if from_row < to_row else -1
        col_direction = 1 if from_col < to_col else -1

        board_row_coord = list(range(from_row, to_row, row_direction))[1:]
        board_col_coord = list(range(from_col, to_col, col_direction))[1:]
        board_coord = list(zip(board_row_coord, board_col_coord))
        board_values = [self.pieces[row][col] for row, col in board_coord]

        inputs = [from_row, from_col, to_row, to_col]
        if all(piece is None for piece in board_values) is True:
            if do_move:
                self.transfer_checker(*inputs)
            return True
        else:
            pieces_in_between = list([p for p in board_values if p is not None])
            enemy_pieces_in_between = list([p for p in pieces_in_between if p.player is not self.active_player])
            ally_pieces_in_between = list([p for p in pieces_in_between if p.player is self.active_player])

            if len(ally_pieces_in_between) > 0 or len(enemy_pieces_in_between) > 1:
                return False
            else:
                if do_move:
                    enemy_piece = enemy_pieces_in_between[0]
                    row = enemy_piece.row
                    col = enemy_piece.column
                    self.pieces[row][col] = None
                    self.transfer_checker(*inputs)
                return True

    def game_winner(self):
        from engine.defines import Players

        p1_pieces_count = 0
        p2_pieces_count = 0
        for lines in self.pieces:
            for piece in lines:
                if piece is not None:
                    if piece.player is Players.P1:
                        p1_pieces_count = p1_pieces_count+1
                    elif piece.player is Players.P2:
                        p2_pieces_count = p2_pieces_count+1

        if p1_pieces_count > 0 and p2_pieces_count == 0:
            return Players.P1
        elif p2_pieces_count > 0 and p1_pieces_count == 0:
            return Players.P2

        return None

    def move(self, from_row, from_col, to_row, to_col):

        inputs = [from_row, from_col, to_row, to_col]
        if all(7 >= i >= 0 for i in inputs) is not True:
            return False

        destination = self.pieces[to_row][to_col]
        if not self.is_valid_selection(from_row, from_col) or destination is not None:
            return False

        moving_piece = self.pieces[from_row][from_col]
        if moving_piece.king is True:
            return self.is_valid_king_move(*inputs, do_move=True)
        else:
            return self.is_valid_pawn_move(*inputs, do_move=True)

    def next_turn(self):
        from engine.defines import Players

        if self.active_player is Players.P1:
            self.active_player = Players.P2
        else:
            self.active_player = Players.P1
