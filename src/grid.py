import pygame

pygame.init()


class Grid(object):
    """
    The Grid Class that manages the pieces in a list, `R` representing `Red`,
    `B` representing `Blue`, whitespace representing an empty slot.
    """
    def __init__(self, slot_w, cols=7, rows=6, pos=(0, 0)):
        """
        Initializes and setting up the List representing the game board,
        the surface to draw the pieces and board.

        :param slot_w: The width (including the margin) of each slot.
        :param cols: The number of columns in the board.
        :param rows: The number of rows in the board.
        :param pos: The position to draw the surface at, on the main window
            of the `Game` class.
        """
        self.slot_w = slot_w
        self.cols = cols
        self.rows = rows
        self.width = cols * slot_w
        self.height = rows * slot_w
        self.pos = pos

        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.surf = pygame.Surface((cols * slot_w, rows * slot_w))

    def __str__(self):
        """
        Get `self.grid` in String.

        :return: The stringified version of `self.grid` (str).
        """
        res = ''
        for row in self.grid:
            for s in row:
                if s == ' ':
                    res += '.'
                else:
                    res += str(s)
            res += '\n'
        return res

    def reset_grid(self):
        """
        Resets `self.grid`.

        :return: None
        """
        self.grid = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]

    def draw(self, surf):
        """
        Draws the board, the pieces and empty slots on `self.surf`,
        the draw `self.surf` on `surf` at `self.pos`.

        :param surf: The surface to draw `self.surf` on.
        :return: None
        """
        self.surf.fill((255, 234, 0))

        for r, row in enumerate(self.grid):
            for c, slot in enumerate(row):
                if slot == ' ':
                    pygame.draw.circle(
                        self.surf, (255, 255, 255),
                        (20 + c * self.slot_w, 20 + r * self.slot_w),
                        self.slot_w // 2 - 7
                    )
                elif slot == 'R':
                    pygame.draw.circle(
                        self.surf, (255, 0, 0),
                        (20 + c * self.slot_w, 20 + r * self.slot_w),
                        self.slot_w // 2 - 7
                    )
                elif slot == 'B':
                    pygame.draw.circle(
                        self.surf, (0, 0, 255),
                        (20 + c * self.slot_w, 20 + r * self.slot_w),
                        self.slot_w // 2 - 7
                    )

        surf.blit(self.surf, self.pos)

    def copy_grid(self):
        """
        Gets an copied `self.grid`.

        :return: copied `self.grid` (list).
        """
        return [row.copy() for row in self.grid]
