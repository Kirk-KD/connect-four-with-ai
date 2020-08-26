import pygame

pygame.init()

WIDTH = 500
HEIGHT = 450
ICON = pygame.image.load('./sprites/c4_icon.png')

SOUND_DROP = pygame.mixer.Sound('./sounds/drop.wav')
SOUND_WIN = pygame.mixer.Sound('./sounds/win.wav')
SOUND_CLICK = pygame.mixer.Sound('./sounds/click.wav')
