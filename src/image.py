import pygame

pygame.init()


class Image(object):
    """
    The Image Class to store and draw a loaded image.
    """
    def __init__(self, path, size=None):
        """
        Define the image from `path` and resize to `size` if `size`
        is not None.

        :param path: The path of the image.
        :param size: The size to resize the image to; If `size`
            is None (default) then the image will keep its original
            size.
        """
        self.ori_img = pygame.image.load(path)
        self.size = size if size else self.ori_img.get_size()
        self.img = pygame.transform.scale(self.ori_img, self.size)

    def draw(self, surf, pos):
        """
        Draws `self.img` at `pos` on `surf`.

        :param surf: The surface to draw `self.img` on.
        :param pos: The position to draw `self.img` at.
        :return: None
        """
        surf.blit(self.img, pos)
