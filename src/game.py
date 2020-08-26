"""
TODO:
    - winning prompt              [DONE]
    - basic computer AI           [DONE]
    - main menu                   [DONE]
    - doc string                  [DONE]
    - draw detection              [DONE]
    - icon                        [DONE]
    - sound effects               [DONE]
"""

from .grid import Grid
from .prompt import Prompt
from .text import Text
from .menu import new_game_from_menu

from .util import *
from .constants import *

from .ai.ai import AI

pygame.init()


class Game(object):
    """
    The Game Class that stores in-game data and
    manages the game (winning, losing, restarting, etc.).
    """

    def __init__(self, win_width, win_height, bg_color, player_turn='R', with_ai=False):
        """
        Initializing and setting initial value of in-game data.

        :param win_width: The width of game window.
        :param win_height: The height of game window.
        :param bg_color: The color to fill the screen every frame.
        :param player_turn: Player's turn; `R`=Red, `B`=Blue.
        :param with_ai: True=PvC, False=PvP
        """
        # dimensions
        self.win_width = win_width
        self.win_height = win_height
        self.bg_color = bg_color
        self.surf = self.create_window()

        # game grid
        self.grid = Grid(40)
        self.grid.pos = (
            self.win_width // 2 - self.grid.width // 2,
            self.win_height // 2 - self.grid.height // 2
        )

        # game status
        self.playing = False
        self.paused = False
        self.player_turn = player_turn
        self.turn = player_turn

        # in game data
        self.drop_col = 0
        self.winner = None

        # AI
        self.ai = AI('R') if with_ai else None

    # MAIN GAME
    def game_loop(self):
        """
        The main game loop that updates screen, handles events with `self.event_listener()`
        and keeps looping until `self.playing` is False.

        :return: None
        """
        while self.playing:
            self.event_listener()

            if self.paused:
                pygame.display.update()
                continue

            self.surf.fill(self.bg_color)

            self.draw_esc_exit()
            self.draw_next_piece()
            self.grid.draw(self.surf)

            if self.winner:
                self.paused = True
                self.draw_win_prompt()
                play_sound(SOUND_WIN)

            elif self.check_if_draw():
                self.paused = True
                self.draw_win_prompt(draw=True)

            elif self.turn != self.player_turn and self.ai:
                self.ai.make_move(self)

            pygame.display.update()

    def event_listener(self):
        """
        Listens to events and handles pausing, quiting, etc.

        :return: None
        """
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.stop()

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not self.winner:
                    dropped_row = self.drop_piece(self.drop_col, True)
                    if dropped_row is not None:
                        winner = self.check_if_win(dropped_row, self.drop_col, self.grid.grid)
                        if winner:
                            self.winner = winner

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    play_sound(SOUND_CLICK)
                    self.stop()
                    self.grid.reset_grid()
                    new_game_from_menu()
                elif e.key == pygame.K_SPACE:
                    if self.winner is not None or self.check_if_draw():
                        play_sound(SOUND_CLICK)
                        self.paused = False
                        self.winner = None
                        self.grid.reset_grid()

    # DRAW
    def draw_win_prompt(self, draw=False):
        """
        Draws a prompt showing who has won when there is a winner.

        :return: None
        """
        p = Prompt(
            None, f'{"RED" if self.winner == "R" else "BLUE"} WINS!' if not draw else 'DRAW!',
            'PRESS [SPACE] TO PLAY AGAIN'
        )
        p.draw(self.surf, (self.win_width // 2 - 150, self.win_height - 80))

    def draw_next_piece(self):
        """
        Draws the floating piece showing which column the
        piece will drop in; Column got from `self.mouse_x_to_col`.

        :return: None
        """
        self.drop_col = self.mouse_x_to_col()
        pygame.draw.circle(
            self.surf, (255, 0, 0) if self.turn == 'R' else (0, 0, 255),
            (
                self.drop_col * self.grid.slot_w + self.grid.pos[0] + 20,
                self.grid.pos[1] - 30
            ),
            self.grid.slot_w // 2 - 7
        )

    def draw_esc_exit(self):
        text = Text('[ESC] EXIT TO MENU', 13, (0, 0, 0))
        text.draw(self.surf, (10, 5))

    # CHECK
    def check_if_win(self, row, col, grid: list, target=4):
        """
        Checks if there is a winner from `grid[row][col]`, win if
        there are horizontally, vertically or diagonally `target`
        pieces of the same color.

        :param row: The row of the piece.
        :param col: The column of the piece.
        :param grid: The grid the piece is in.
        :param target: How many pieces of the same color is required to win.
        :return: False (bool) if `grid`[`row`][`col`] is whitespace or there is
            no winner. Otherwise return `B` (str) if Blue has won, `R` (str) if Red.
        """
        piece = grid[row][col]

        if piece == ' ':
            return False

        # check row
        this_row = 1
        r = row + 1
        while r < self.grid.rows:
            if grid[r][col] == piece:
                this_row += 1
                r += 1
                if this_row >= target:
                    return piece
            else:
                break
        r = row - 1
        while r >= 0:
            if grid[r][col] == piece:
                this_row += 1
                r -= 1
                if this_row >= target:
                    return piece
            else:
                break

        # check col
        this_col = 1
        c = col + 1
        while c < self.grid.cols:
            if grid[row][c] == piece:
                this_col += 1
                c += 1
                if this_col >= target:
                    return piece
            else:
                break
        c = col - 1
        while c >= 0:
            if grid[row][c] == piece:
                this_col += 1
                c -= 1
                if this_col >= target:
                    return piece
            else:
                break

        # check LL-UR
        this_llur = 1
        c = col + 1
        r = row - 1
        while c < self.grid.cols and r >= 0:
            if grid[r][c] == piece:
                this_llur += 1
                if this_llur >= target:
                    return piece
                c += 1
                r -= 1
            else:
                break
        c = col - 1
        r = row + 1
        while c >= 0 and r < self.grid.rows:
            if grid[r][c] == piece:
                this_llur += 1
                if this_llur >= target:
                    return piece
                c -= 1
                r += 1
            else:
                break

        # check UL-LR
        this_ullr = 1
        c = col + 1
        r = row + 1
        while c < self.grid.cols and r < self.grid.rows:
            if grid[r][c] == piece:
                this_ullr += 1
                if this_ullr >= target:
                    return piece
                c += 1
                r += 1
            else:
                break
        c = col - 1
        r = row - 1
        while c >= 0 and r >= 0:
            if grid[r][c] == piece:
                this_ullr += 1
                if this_ullr >= target:
                    return piece
                c -= 1
                r -= 1
            else:
                break

        return False

    def check_if_draw(self):
        for r, row in enumerate(self.grid.grid):
            for c, slot in enumerate(row):
                # if t := self.check_if_win(r, c, self.grid.grid):
                #     self.winner = t
                #     return False
                if slot == ' ':
                    return False
        return True

    # ACTION
    def drop_piece(self, drop_col, drop=True):
        """
        Drops a piece in `drop_col`.

        :param drop_col: The column the piece has to be dropped in.
        :param drop: Actually drop the piece.
        :return: False (bool) if the column is full, otherwise the
            row the piece landed in (int).
        """
        for r, row in enumerate(self.grid.grid):
            if row[drop_col] != ' ':
                if r - 1 < 0:  # if col is full
                    return False

                if drop:
                    play_sound(SOUND_DROP)
                    self.grid.grid[r - 1][drop_col] = self.turn
                    if self.turn == 'R':
                        self.turn = 'B'
                    elif self.turn == 'B':
                        self.turn = 'R'
                    # self.turn = 'B' if self.turn == 'R' else 'B'
                return r - 1

        if drop:
            play_sound(SOUND_DROP)
            self.grid.grid[-1][drop_col] = self.turn
            if self.turn == 'R':
                self.turn = 'B'
            elif self.turn == 'B':
                self.turn = 'R'
            # self.turn = 'B' if self.turn == 'R' else 'B'
        return len(self.grid.grid) - 1

    def create_window(self):
        """
        Creates a window.

        :return: The window (pygame.Surface).
        """
        return pygame.display.set_mode((self.win_width, self.win_height))

    # TOOL
    def mouse_x_to_col(self):
        """
        Gets the column based on mouseX.

        :return: column (int)
        """
        mouse_x = pygame.mouse.get_pos()[0]

        if mouse_x < self.grid.pos[0]:
            col = 0
        elif mouse_x > self.grid.pos[0] + self.grid.width:
            col = self.grid.cols - 1
        else:
            col = (mouse_x - self.grid.pos[0]) // self.grid.slot_w

        return col

    # GAME CONTROL
    def start(self):
        """
        Starts the game by setting `self.playing` to True and calling
        `self.game_loop`.

        :return: None
        """
        pygame.display.set_caption(f'Connect Four! - {"Single" if self.ai else "Double"} Player')
        pygame.display.set_icon(ICON)
        self.playing = True
        self.game_loop()

    def stop(self):
        """
        Stops the game by setting `self.playing` to False.

        :return: None
        """
        self.playing = False
