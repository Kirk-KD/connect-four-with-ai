import pygame
from .image import Image
from .text import Text

pygame.init()


class Prompt(Image):
    """
    The Class Prompt that shows some text on top of an
    image as background.
    """
    def __init__(self, size, msg, footer):
        """
        Initializes and sets the background image.

        :param size: The size of the prompt.
        :param msg: The message to show.
        """
        super().__init__('./sprites/win_prompt_bg.png', size)
        self.msg = msg
        self.text = Text(self.msg, 23)
        self.footer = footer
        self.footer_text = Text(self.footer, 13)

    def draw(self, surf, pos):
        """
        Draws `self.text` on `surf` at `pos` and calls `draw()` of `Image`.

        :param surf: The surface to draw `self.text` on.
        :param pos: The position to draw the whole prompt at.
        :return: None
        """
        super().draw(surf, pos)
        self.text.draw(
            surf, (
                self.size[0] // 2 - self.text.surf.get_width() // 2 + pos[0],
                self.size[1] // 2 - self.text.surf.get_height() // 2 + pos[1] - 10
            )
        )
        self.footer_text.draw(
            surf, (
                self.size[0] // 2 - self.footer_text.surf.get_width() // 2 + pos[0],
                self.size[1] - 20 + pos[1]
            )
        )
