import pygame

pygame.init()


def force_win(game, winner):
    """
    Force `winner` to win.

    :param game: An instance of `Game` to set the winner.
    :param winner: `R` for Red or `B` for Blue.
    :return: None
    """
    game.winner = winner


def force_draw(game):
    """
    Force `game` to get a draw.

    :param game: An instance of `Game` to get a draw
    :return: None
    """
    for r in range(game.grid.rows):
        for c in range(game.grid.cols):
            game.grid.grid[r][c] = 'R'


def play_sound(sound):
    """
    Play `sound`.

    :param sound: An instance of `pygame.mixer.Sound`.
    :return: None
    """
    pygame.mixer.Sound.play(sound)
