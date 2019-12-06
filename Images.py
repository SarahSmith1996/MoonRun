import pygame
import os
pygame.init()

#gets current working directory to access all files
os.chdir(os.path.dirname(os.path.realpath(__file__)))

night = pygame.image.load('starry.png') 
gameintro = pygame.image.load('intro.png') 
info1 = pygame.image.load('info1.png') 
info2 = pygame.image.load('info2.png') 

p1move = [pygame.image.load('p11.png'), pygame.image.load('p12.png'), pygame.image.load('p13.png'), pygame.image.load('p14.png'), pygame.image.load('p15.png'), pygame.image.load('p16.png'), pygame.image.load('p17.png'), pygame.image.load('p18.png')]
p2move = [pygame.image.load('p21.png'), pygame.image.load('p22.png'), pygame.image.load('p23.png'), pygame.image.load('p24.png'), pygame.image.load('p25.png'), pygame.image.load('p26.png'), pygame.image.load('p27.png'), pygame.image.load('p28.png')]
p1stand = pygame.image.load('p10.png')
p1jump = [pygame.image.load('p1j.png'),pygame.image.load('p1j2.png')]
p2stand = pygame.image.load('p20.png')
p2jump = [pygame.image.load('p2j.png'),pygame.image.load('p2j2.png')]