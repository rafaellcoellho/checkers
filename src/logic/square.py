class Square:
    def __init__(self, row, column, color, player_state): 
        self.row = row
        self.column = column       
        self.color = color
        self.player_state = player_state
        self.possible_move = False
        self.king = False

    def __repr__(self):
        return f"Square(pos=[{self.row},{self.column}], color={self.color.name} state={self.player_state.name})"

    def __str__(self):
        short_player_name = {
            'EMPTY': ' ',
            'CHECKER_RED': 'R',
            'CHECKER_BLUE': 'B'
        }
        return f"  {'K' if self.king else ' '}{short_player_name[self.player_state.name]}  "
