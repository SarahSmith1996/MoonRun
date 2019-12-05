import pygame
pygame.init()
class GameProperties:
    pass

class Images (GameProperties):
    
    def __init__(self):
        pass

    imgdict = {"night": pygame.image.load('starry.png'),
            "background": pygame.image.load('hills_bg.png'),
            "info1": pygame.image.load('info1.png'),
            "info2" : pygame.image.load('info2.png'), 
            "p1move" : [pygame.image.load('p11.png'), pygame.image.load('p12.png'),\
                        pygame.image.load('p13.png'), pygame.image.load('p14.png'), \
                        pygame.image.load('p15.png'), pygame.image.load('p16.png'),\
                        pygame.image.load('p17.png'), pygame.image.load('p18.png')], 
            "p2move" : [pygame.image.load('p21.png'), pygame.image.load('p22.png'),\
                        pygame.image.load('p23.png'), pygame.image.load('p24.png'),\
                        pygame.image.load('p25.png'), pygame.image.load('p26.png'), \
                        pygame.image.load('p27.png'), pygame.image.load('p28.png')],
            "p1stand" : pygame.image.load('p10.png'),
            "p1jump" : [pygame.image.load('p1j.png'),pygame.image.load('p1j2.png')],
            "p2stand" : pygame.image.load('p20.png'),
            "p2jump" : [pygame.image.load('p2j.png'),pygame.image.load('p2j2.png')]}

    def get_image (self, imgname):
        self.imgname = imgname
        if self.imgname in self.imgdict:
            return self.imgdict[self.imgname]

class Sounds (GameProperties):

    jetpack = pygame.mixer.Sound('jetpack.wav')
    death = pygame.mixer.Sound('death.wav')
    step = pygame.mixer.Sound('step.wav')
    fall = pygame.mixer.Sound('falling.wav')
    crash = pygame.mixer.Sound('crash.wav')
    select = pygame.mixer.Sound('selection.wav')
    itemsound = pygame.mixer.Sound('item.wav')