import pygame
pygame.init()

class Sounds (GameProperties):

    jetpack = pygame.mixer.Sound('jetpack.wav')
    death = pygame.mixer.Sound('death.wav')
    step = pygame.mixer.Sound('step.wav')
    fall = pygame.mixer.Sound('falling.wav')
    crash = pygame.mixer.Sound('crash.wav')
    select = pygame.mixer.Sound('selection.wav')
    itemsound = pygame.mixer.Sound('item.wav')