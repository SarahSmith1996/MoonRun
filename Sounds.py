import pygame
import os
pygame.init()

#gets current working directory to access all files
os.chdir(os.path.dirname(os.path.realpath(__file__)))


jetpack = pygame.mixer.Sound('jetpack.wav')
death = pygame.mixer.Sound('death.wav')
step = pygame.mixer.Sound('step.wav')
fall = pygame.mixer.Sound('falling.wav')
crash = pygame.mixer.Sound('crash.wav')
select = pygame.mixer.Sound('selection.wav')
itemsound = pygame.mixer.Sound('item.wav')