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


def nc(origin: (int, int), destination: (int, int) = None):
    row, column = origin
    from_column_char = chr(65 + column)
    from_row_char = str(row + 1)

    if destination is None:
        return f"{from_column_char}{from_row_char}"

    row, column = destination
    to_column_char = chr(65 + column)
    to_row_char = str(row + 1)

    return (
        f"{from_column_char}{from_row_char}",
        f"{to_column_char}{to_row_char}"
    )
