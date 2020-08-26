import pygame

pygame.init()


class Text(object):
    """
    The Class Text that holds a text surface.
    """
    def __init__(self, text, size, color=(0, 0, 0)):
        """
        Initializes text, text size, font and text surface.

        :param text: The text on the text surface.
        :param size: The font size.
        :param color: Text color.
        """
        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont('Comic Sans MS', size)
        self.surf = self.font.render(self.text, False, color)

    def draw(self, surf, pos):
        """
        Draws `self.surf` on `surf` at `pos`.

        :param surf: The surface to draw `self.surf` on.
        :param pos: The position to draw `self.surf` at.
        :return: None
        """
        surf.blit(self.surf, pos)
