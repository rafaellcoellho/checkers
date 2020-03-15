def cn(origin: str, destination: str = None):
    col_char, row_char = origin
    from_row = int(row_char) - 1
    from_col = ord(col_char) - 65

    if destination is None:
        return [from_row, from_col]

    col_char, row_char = destination
    to_row = int(row_char) - 1
    to_col = ord(col_char) - 65

    return [from_row, from_col, to_row, to_col]
