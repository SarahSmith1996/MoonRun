import pygame
pygame.init()

class Display ():
    
    def __init__(self, width=800, height=400):

        self.winwidth = width
        self.winheight = height

class Screen (Display):
    
    def __init__(self):
        super().__init__()


    def create_window (self):
        return pygame.display.set_mode((self.winwidth,self.winheight))

class Text(Display): #### creating the text class 
    
    def __init__(self, x, y, text, font, fontsize, colour, window):
        self.x  = x
        self.y = y
        self.text = text
        self.fontsize = fontsize
        self.colour = colour
        self.window = window
        self.font = pygame.font.Font(font, self.fontsize) # creating the font
        self.textsurf = self.font.render(self.text, True, self.colour) # creating the text surface
        self.rect = self.textsurf.get_rect() # creating the rectangle for the text

    
    def show_text(self): # method to show the text
        self.rect.center = (self.x,self.y) # Puts the center of the text at the x and y co ordinates
        self.window.blit(self.textsurf,self.rect) # prints one surface onto another
        
    def mouse_over(self): # checks whether the mouse is over a the text
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

class Fonts (Display):

    
       
    def font_size (self, size):
        self.size = size
        return pygame.font.Font(self.font,self.size)

    def fonts_colours (self, red, blue, green):
        self.red, self.green, self.blue = red, green, blue
        return pygame.Color(self.red, self.blue, self.green)

class Colours (Display):
    
    fontcolour = pygame.Color(255,201,14)
    white = pygame.Color('white')
    black = pygame.Color('black')
    p1colour = pygame.Color('red')
    p2colour = pygame.Color('blue')

class Images (Display):
    
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

class Background (Images):

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
        if self.x > -self.winwidth:
            self.x -= self.vel
        else:
            self.x = 0
        
class BackgroundObjects (Background):
    # displayobjects
    def draw(self,window):
        window.blit(pygame.image.load(self.img),(self.x,self.y))

class Items (BackgroundObjects):

    def __init__(self,x,y,vel,img,width,height):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.width = width
        self.height = height

    def draw(self,window,secimg):
        if (pygame.time.get_ticks()//500)%2: 
            window.blit(pygame.image.load(self.img),(self.x,self.y))
        else:
            window.blit(pygame.image.load(secimg),(self.x,self.y))