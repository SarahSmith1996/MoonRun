import pygame
import random
import pickle
import os

pygame.init()

os.chdir(os.path.dirname(os.path.realpath(__file__)))
pygame.display.set_caption("Moon Run")
clock = pygame.time.Clock()     # Used to track time in the game 


winwidth = 800  # Display window width
winheight = 400     # Display window height 

window = pygame.display.set_mode((winwidth,winheight))

font = 'pixel.otf' 

class Text: # creating the text class 
    
    def __init__(self, x, y, text, font, fontsize, colour):
        self.x  = x
        self.y = y
        self.text = text
        self.fontsize = fontsize
        self.colour = colour
        self.font = pygame.font.SysFont("Arial",self.fontsize) # creating the font
        self.textsurf = self.font.render(self.text, True, self.colour) # creating the text surface
        self.rect = self.textsurf.get_rect() # creating the rectangle for the text

    
    def show_text(self): # method to show the text
        self.rect.center = (self.x,self.y) # Puts the center of the text at the x and y co ordinates
        window.blit(self.textsurf,self.rect) # prints one surface onto another
        
    def mouse_over(self): # checks whether the mouse is over a the text
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False


#main game loop
run = True
while run:
    clock.tick(27)
    keys = pygame.key.get_pressed()

    #leave game 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    Test = Text(winwidth//2, winheight//2, "Test",font, 100, pygame.Color('white'))
    Test.show_text()
    pygame.display.update()

pygame.quit()