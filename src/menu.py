from .text import Text
from .constants import *
from .util import play_sound


class Menu(object):
    """
    The Menu Class that allows player to choose between playing
    with an AI or another player.
    """
    def __init__(self, win_width, win_height):
        """
        Initializes the window and other class variables.

        :param win_width: The width of the window.
        :param win_height: The height of the window.
        """
        self.win_width = win_width
        self.win_height = win_height
        self.surf = pygame.display.set_mode((self.win_width, self.win_height))
        self.running = False

        self.title_text = Text('Connect Four!', 53)
        self.pvc_text = Text('[s] Single Player', 37, (255, 171, 54))
        self.pvp_text = Text('[d] Double Player', 37, (255, 171, 54))

        self.return_game = None

    def main_loop(self):
        """
        The main loop of Menu. Runs ss long as `self.running` is True.

        :return: None
        """
        while self.running:
            self.event_listener()
            self.surf.fill((255, 255, 255))

            self.draw_title()
            self.draw_pvc_op()
            self.draw_pvp_op()

            pygame.display.update()

    def event_listener(self):
        """
        Detects Exit and Key Press events. When `S` or `D` key is pressed,
        `self.return_game` will be set to an Game object.

        :return: None
        """
        from .game import Game

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.stop()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_s:
                    play_sound(SOUND_CLICK)
                    self.return_game = Game(WIDTH, HEIGHT, (255, 255, 255), with_ai=True)
                    self.stop()
                elif e.key == pygame.K_d:
                    play_sound(SOUND_CLICK)
                    self.return_game = Game(WIDTH, HEIGHT, (255, 255, 255), with_ai=False)
                    self.stop()

    def draw_title(self):
        """
        Draws `self.title_text`.

        :return: None
        """
        self.title_text.draw(
            self.surf, (self.win_width // 2 - self.title_text.surf.get_width() // 2, 20)
        )

    def draw_pvc_op(self):
        """
        Draws `self.pvc_text`.

        :return: None
        """
        self.pvc_text.draw(
            self.surf, (self.win_width // 2 - self.pvc_text.surf.get_width() // 2, 130)
        )

    def draw_pvp_op(self):
        """
        Draws `self.pvp_text`.

        :return: None
        """
        self.pvp_text.draw(
            self.surf, (self.win_width // 2 - self.pvp_text.surf.get_width() // 2, 205)
        )

    def start(self):
        """
        Sets the title and start the main loop.

        :return: None
        """
        pygame.display.set_caption('Connect Four!')
        pygame.display.set_icon(ICON)
        self.running = True
        self.main_loop()

    def stop(self):
        """
        Stops the main loop by setting `self.running` to False.

        :return: None
        """
        self.running = False


def new_game_from_menu():
    menu = Menu(WIDTH, HEIGHT)
    menu.start()

    if menu.return_game:
        game = menu.return_game
        game.start()
