import pygame
pygame.init()
class Display ():
    pass

class Screen (Display):

    def __init__(self, width, height):

        self.winwidth = width
        self.winheight = height
    
    def create_window (self):
        return pygame.display.set_mode((self.winwidth,self.winheight))

class Fonts (Display):

    font = 'pixel.otf'
       
    def font_size (self, size):
        self.size = size
        return pygame.font.Font(self.font,self.size)

    def fonts_colours (self, red, blue, green):
        self.red, self.green, self.blue = red, green, blue
        return pygame.Color(self.red, self.blue, self.green)

class Colours (Display):

    white = pygame.Color('white')
    black = pygame.Color('black')
    p1colour = pygame.Color('red')
    p2colour = pygame.Color('blue')

class Background (Screen):

    def __init__(self,x,y,vel,img,width,height):
        
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.width = width
        self.height = height
        worldvel = 8

class Backdrop (Background):
    
    def draw(self, window):
        window.blit(pygame.image.load(self.img), (self.x,self.y))
        window.blit(pygame.image.load(self.img), (self.x+winwidth,self.y))
        if self.x > -winwidth:
            self.x -= self.vel
        else:
            self.x = 0
        
class BackgroundObjects (Background):
    # displayobjects
    def draw(self,window):
        window.blit(pygame.image.load(self.img),(self.x,self.y))