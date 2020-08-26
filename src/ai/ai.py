from random import choice


class AI(object):
    """
    The AI for Connect Four.
    """

    def __init__(self, enemy):
        """
        Initializes the enemy (player) piece (`R` or `B`) and the AI's piece.

        :param enemy: the player's piece (`R` or `B`).
        """
        self.enemy = enemy
        self.piece = 'B' if enemy != 'B' else 'R'
        self.full_cols = []

    def get_next_col(self, game):
        """
        Calculates the column to place the next piece.
        The priorities list (from top to bottom):
         - The slot that the AI can win;
         - The slot that the player can win;
         - The slot that the AI can connect to 3;
         - The slot that the player can connect to 3;
         - Random between the middle three
         - Random between the left and the right

        :param game: The Game Object to check.
        :return: The best column to drop the piece.
        """
        p_win_cols = []
        force_cols = []
        p_force_cols = []

        for col in range(game.grid.cols):
            drop_res = game.drop_piece(col, False)

            if drop_res is False:
                continue

            copied_grid = game.grid.copy_grid()

            # if AI can win
            copied_grid[drop_res][col] = self.piece
            if game.check_if_win(drop_res, col, copied_grid) == self.piece:
                copied_grid[drop_res][col] = ' '
                return col

            # if Player can win
            copied_grid[drop_res][col] = self.enemy
            if game.check_if_win(drop_res, col, copied_grid) == self.enemy:
                copied_grid[drop_res][col] = ' '
                p_win_cols.append(col)

            # if AI can force
            copied_grid[drop_res][col] = self.piece
            if game.check_if_win(drop_res, col, copied_grid, 3) == self.piece:
                copied_grid[drop_res][col] = ' '
                force_cols.append(col)
                continue

            # if Player can force
            copied_grid[drop_res][col] = self.enemy
            if game.check_if_win(drop_res, col, copied_grid, 3) == self.enemy:
                copied_grid[drop_res][col] = ' '
                p_force_cols.append(col)

        if len(p_win_cols) != 0:
            return choice(p_win_cols)

        if len(force_cols) != 0:
            return choice(force_cols)

        if len(p_force_cols) != 0:
            return choice(p_force_cols)

        center_empties = [c for c in range(2, 5) if c not in self.full_cols]
        if len(center_empties) != 0:
            return choice(center_empties)

        return game.grid.cols - 1 if 0 in self.full_cols else 0

    def make_move(self, game):
        """
        Makes the best move on `game`.

        :param game: The Game Object to check.
        :return: None
        """
        dropped = False

        while not dropped:
            move = self.get_next_col(game)
            res = game.drop_piece(move)

            if res is not False:
                dropped = True
                winner = game.check_if_win(res, move, game.grid.grid)

                if winner is not False:
                    game.winner = winner

            else:
                self.full_cols.append(move)

        game.turn = game.player_turn
