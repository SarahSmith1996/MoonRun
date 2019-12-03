"""
-------------------------- MOON RUN -------------------------------

V 0.4:

NOTES:

set difficulty (worldvel) at beginning


TO DO: 
- obstacles, new sprites, title menu
- collision class (meteorite collision)
- highscores 
- pause menu: exit game, music?
- other items jetpack-boost?
- increase speed as game progresses (probably have to pass worldvel to draw functions)
- player dies when walking into obstacles? easier and maybe more fun, need spikes or sth
- Enter Name


Sarah:
- Sprites
- Physics Engine (player.move --> jump, falling meteorites)

Remmy: 
- Import title
- pause menu

Mohammad:
- Sprites
- Collisions/platforms

Jonas:
- Commenting -> OOP optimziation
- GIT repository
- scoreboard
- walking function


OPTIMIZE CODE:
- OOP optimization 
    - class variables change self to classname?
    - make player class subclass of element? maybe not
    - 'stuff' subclass of elements (draw function in element class)?
    - class for text with draw method??
- make reset function the general initializer of all game variables -> reset at the start of game (within menu)
- remove hardcoding
- sort code: global variables, databases, functions
- reduce image/sound sizes

- more counter digits
- align text with " size(text) -> (width, height) " https://stackoverflow.com/questions/25149892/how-to-get-the-width-of-text-using-pygame
    - also auto align on screen score with this
- max score?? 999.999?
- player shouldnt be able to run too far to the right
- change jump so player can jump on objects and item works


OPTIMIZE GAME:
- different sounds for both players?
- smoother walking with list index division
- add shooting star
- pause menu same key

TO FIX: 
- sounds drown each other out
- Esc before redraw window looks awkward
- hole sprite, so meteorites look better on top
- change meteor landing (according to worldvel)

"""


# general initiation
import pygame
import random

pygame.init()


#import os
#os.chdir(r'C:\Users\jonas\Desktop\MoonRun')


#general game values
worldvel = 8
pygame.display.set_caption("Moon Run")
clock = pygame.time.Clock()


#window
winwidth = 800
winheight = 400
window = pygame.display.set_mode((winwidth,winheight))

#fonts
font = 'pixel.otf'
smallfont = pygame.font.Font(font, 25)
bigfont = pygame.font.Font(font, 55)

#Colours
fontcolour = pygame.Color(255,201,14)
p1colour = pygame.Color('red')
p2colour = pygame.Color('blue')

#images
night = pygame.image.load('starry.png')

p1move = [pygame.image.load('p11.png'), pygame.image.load('p12.png')]
p2move = [pygame.image.load('p21.png'), pygame.image.load('p22.png')]
p1stand = pygame.image.load('p10.png')
p1jump = pygame.image.load('p1j.png')
p2stand = pygame.image.load('p20.png')
p2jump = pygame.image.load('p2j.png')


#sounds
jetpack = pygame.mixer.Sound('jetpack.wav')
death = pygame.mixer.Sound('death.wav')
step = pygame.mixer.Sound('step.wav')
fall = pygame.mixer.Sound('falling.wav')
crash = pygame.mixer.Sound('crash.wav')
select = pygame.mixer.Sound('selection.wav')
itemsound = pygame.mixer.Sound('item.wav')



class player (object):

    def __init__(self,x,y,width,height,movelist,standimg,jumpimg,name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.movelist = movelist
        self.standimg = standimg
        self.jumpimg = jumpimg
        self.name = name

        self.vel = (5/4)*worldvel
        self.isJump = False
        self.jumpheight = 10
        self.jumpCount = self.jumpheight
        self.left = False
        self.step = 0
        self.move = False
        self.alive = True
        self.neg = 1

        #delete if not needed
        self.ontop = True
        self.maxvel = 2.5*worldvel
        
        self.maxjumpheight = 13

    def moving(self, direction):
        if direction == 0:
            self.left = True
            self.x -= self.vel
        else:
            self.left = False
            self.x += self.vel
        
        if not self.isJump:
            self.move = True
            step.play()

    def jump (self):
        if self.jumpCount >= -self.jumpheight:
            self.neg = 1
            if self.jumpCount < 0:
                self.neg = -1
            self.y -= (self.jumpCount **2) * 0.25 * self.neg
            self.jumpCount -= 0.5
            if self.neg == 1 and self.x>0: 
                jetpack.play()

        else:
            self.isJump = False
            self.jumpCount = self.jumpheight

    def draw(self, window):
        if self.move:
            if self.step + 1 > 8:
                self.step = 0
            if self.step < 4:
                if not self.left: 
                    window.blit(self.movelist[0], (self.x,self.y))
                else:
                    window.blit(pygame.transform.flip(self.movelist[0],1,0), (self.x,self.y))
                self.step += 1
            if self.step >= 4:
                if not self.left: 
                    window.blit(self.movelist[1], (self.x,self.y))
                else:
                    window.blit(pygame.transform.flip(self.movelist[1],1,0), (self.x,self.y))
                self.step += 1
        elif self.isJump and self.neg == 1:
            if not self.left:
                window.blit(self.jumpimg, (self.x,self.y))
            else: 
                window.blit(pygame.transform.flip(self.jumpimg,1,0), (self.x,self.y))
        else:
            if not self.left:
                window.blit(self.standimg, (self.x,self.y))
            else:
                window.blit(pygame.transform.flip(self.standimg,1,0), (self.x,self.y))
        
    def collision(self):
        """
        #above
        if self.x+self.width > other.x and self.x < other.x + other.width:
            if self.y >= other.y-other.height:
                self.ontop = True
        """
        #left

        #item
        for item in itemlist:
            if self.x > item.x and self.x < item.x + item.width:
                if self.y+self.height >= item.y:

                    if item.img == "item1.png":
                        if self.vel < self.maxvel:
                            self.vel += 4
                    else:
                        if self.jumpheight < self.maxjumpheight:
                            #self.jumpheight += 2    doesn't work, redo jump
                            print(self.jumpheight)
                    itemsound.play()
                    itemlist.pop(itemlist.index(item))



class element (object):

    def __init__(self,x,y,vel,img,width,height):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.width = width
        self.height = height


class backdrop (element):
    
    def draw(self, window):
        window.blit(pygame.image.load(self.img), (self.x,self.y))
        window.blit(pygame.image.load(self.img), (self.x+winwidth,self.y))
        if self.x > -winwidth:
            self.x -= self.vel
        else:
            self.x = 0
        
class stuff (element):

    def draw(self,window):
        window.blit(pygame.image.load(self.img),(self.x,self.y))

class Item (stuff):


    def draw(self,window,secimg):
        if (pygame.time.get_ticks()//500)%2: 
            window.blit(pygame.image.load(self.img),(self.x,self.y))
        else:
            window.blit(pygame.image.load(secimg),(self.x,self.y))

class Text: # creating the text class
    
    def __init__(self, x, y, text, font, fontsize, colour):
        self.x  = x
        self.y = y
        self.text = text
        self.fontsize = fontsize
        self.colour = colour
        self.font = pygame.font.Font(font, self.fontsize) # creating the font
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

"""
class scoreboard (object):
    LENGTH = 5

    def __init__(self,scoreList):
        self.scoreList = scoreList
    
    def addscore(self,newscore):
        for i in scoreList:
            if newscore > i:
                if i < LENGTH:

                scoreList[i] = newscore

    def reset(self):
"""

def redrawGameWindow():
    window.blit(night,(0,0)) #draws background (starry night)
    bd1.draw(window)
    bd2.draw(window)
    lunar.draw(window)
    pygame.draw.rect(window,(60,60,60),(0,winheight-20,winwidth,20)) #draws the floor
    for holes in holelist:
        holes.draw(window)
    for meteo in meteolist:
        meteo.draw(window)
    for item in itemlist:
        if item.img=="item1.png":
            otherimg = "item12.png"
        else:
            otherimg = "item22.png"
        item.draw(window,otherimg)
    for player in playerlist:
        player.draw(window)

def reset():
    global holelist
    global meteolist
    global gameovercount
    global winner
    global playtime
    global end
    global replay
    global playerlist
    global itemlist
    
    holelist=[]
    meteolist=[]
    itemlist=[]
    gameovercount=0
    winner=0
    playtime=0
    end = False
    replay = False
    for player in playerlist:
        player.alive = True
        player.y = winheight-player.height-16
        player.isJump = False
        player.jumpCount = 10
        player.neg = 1
        player.vel = (5/4)*worldvel

    player1.x = winwidth//2

    if twoplayer:
        player2.x = winwidth*(2/3)
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1,0.0)



#class instances
title = backdrop(0,0,worldvel/2,'starry.png',800,400)
bd1 = backdrop(0,0,worldvel/4,'hills_bg.png',800,400)
bd2 = backdrop(0,0,worldvel/2,'hills_fg.png',800,400)

lunar = stuff(winwidth*3,winheight-170,worldvel,'lunarmodule.png',160,160)

player1 = player(winwidth//2,winheight-80,64,64, p1move, p1stand, p1jump, 'Player 1')
player2 = player(winwidth*(2/3),winheight-80,64,64, p2move, p2stand, p2jump, 'Player 2')

#start conditions
itemlist=[]
holelist=[]
meteolist=[]
playerlist = [player1]
gameovercount = 0
winner = 0
playtime = 0
end = False
replay = False
menu = True
second_menu = False
twoplayer = False


#music for main game
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1,0.0)

#main game loop
run = True
while run:
    clock.tick(27)

    #leave game 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

            
    #game menu
    while menu:
        clock.tick(27)

        #leave game 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                menu = False
        
                
        title.draw(window)
        
        text = Text(winwidth//2, winheight//3, 'Moon run', font, 55, fontcolour)
        text.show_text()
        
        text2 = Text(winwidth//2, winheight//1.5, 'Press any key to begin', font, 25, fontcolour)
        text2.show_text()

        pygame.display.flip()


        for key in pygame.key.get_pressed():
            if key == True:
                menu = False
                second_menu = True
        
    while second_menu: # second menu loop
        
        title.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        text1 = Text(winwidth//2, winheight//3, '1 Player', font, 25, fontcolour) # 1 Player text
        text2 = Text(winwidth//2, winheight//2, '2 Player', font, 25, fontcolour) # 2 player text
        back = Text(winwidth//5, winheight//1.25, 'Back', font, 15, fontcolour) # Back button text
        text1.show_text() # method to show the text
        text2.show_text()
        back.show_text()
        pygame.display.flip()
        
        while text1.mouse_over(): # While loop for when the mouse is on top of the text
            text1 = Text(winwidth//2, winheight//3, '1 Player', font, 25, p1colour) # redraws the text but changes colour 
            title.draw(window)
            text1.show_text()
            text2.show_text()
            back.show_text()
            pygame.display.flip() # updates the display
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN: # if the mouse is clicked while on the text
                    select.play()
                    twoplayer = False
                    second_menu = False
                    
        while text2.mouse_over():
            text2 = Text(winwidth//2, winheight//2, '2 Player', font, 25, p2colour )  
            title.draw(window)
            text1.show_text()
            text2.show_text()
            back.show_text()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    select.play()
                    twoplayer = True
                    playerlist.append(player2)
                    second_menu = False
                    
        while back.mouse_over():
            back = Text(winwidth//5, winheight//1.25, 'Back', font, 15, pygame.Color('white'))
            title.draw(window)
            text1.show_text()
            text2.show_text()
            back.show_text()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    second_menu= False
                    menu = True
            
            
            

#game loop
    #default movement
    for player in playerlist:
        player.x -= worldvel
        player.collision()
    
    # lunar module regularly apperars
    if lunar.x > -6*winwidth:
        lunar.x -= worldvel
    else: 
        lunar.x = winwidth


    #remove holes
    for hole in holelist:
        if hole.x <= -hole.width:
            holelist.pop(holelist.index(hole))

    #make random holes in floor
    holeget=random.randint(0,50)
    if holeget == 0 and len(holelist)<1:
        x = stuff(winwidth+200,winheight-30,worldvel,'bigcrater.png',250,30)
        holelist += [x]
        
    for holes in holelist:
        holes.x -= holes.vel
    
    #remove meteor
    for meteo in meteolist:
        if meteo.x <= -meteo.width:
            meteolist.pop(meteolist.index(meteo))
   
    #create random meteorite 
    meteoget=random.randint(0,100)
    
    if meteoget == 0 and len(meteolist)<3:
        y = stuff(winwidth,0,worldvel,'meteorite.png',64,64)
        fall.play()
        meteolist += [y]   
        
    for meteo in meteolist:
        meteo.x -= meteo.vel
        if meteo.y == winheight - 80 - 4*meteo.vel:
            crash.play()
        if meteo.y < winheight - 80:
            meteo.y += 4*meteo.vel
        else:
            for hole in holelist:
                if meteo.x > hole.x and meteo.x < hole.x+hole.width-meteo.width:
                    meteo.y += 4*meteo.vel
            meteo.img='meteoriteb.png'

    #remove items
    for item in itemlist:
        if item.x <= -item.width:
            itemlist.pop(itemlist.index(item))

    #make random items
    itemget=random.randint(0,200)
    if itemget == 0 and len(itemlist)<1:
        x = Item(winwidth,winheight-60,worldvel,'item1.png',32,32)
        itemlist += [x]
    if itemget == 1 and len(itemlist)<1:
        x = Item(winwidth,winheight-60,worldvel,'item2.png',32,32)
        itemlist += [x]
        
    for item in itemlist:
        item.x -= item.vel


    #player control
    keys = pygame.key.get_pressed()

    #player 1 control
    if player1.alive:
        if keys[pygame.K_LEFT]:
            player1.moving(0)

        elif keys[pygame.K_RIGHT]:
            player1.moving(1)
        
        else: 
            player1.move = False

        if not player1.isJump:
            if keys[pygame.K_UP]:
                player1.isJump = True
                player1.move = False
            
        else:
            player1.jump()

    #player 2 control
    if twoplayer:
        if player2.alive:
            if keys[pygame.K_a]:
                player2.moving(0)

            elif keys[pygame.K_d]:
                player2.moving(1)
                
            else: 
                player2.move = False

            if not(player2.isJump):
                if keys[pygame.K_w]:
                    player2.isJump = True
                    player2.move = False
                    
            else:
                player2.jump()
    
    #pause game
    if keys[pygame.K_p]:
        select.play()
        pause = True
        while pause:
            clock.tick(27)
            
            #leave game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pause = False
            
            pygame.draw.rect(window,(20,20,20),(winwidth/2-200,winheight/2-100,400,200))
            pmsg = smallfont.render("Space to continue...", 1, (255,201,14))
            window.blit(pmsg, (250,250))
            
            pkeys = pygame.key.get_pressed()
            if pkeys[pygame.K_SPACE]:
                select.play()
                pause = False

            if pkeys[pygame.K_ESCAPE]:
                run = False
                pause = False

            pygame.display.update()
            continue

    #player death, fix issue: p2 can't move after p1 dies
    for player in playerlist:
        for hole in holelist:
            if player.x > hole.x + 5 and player.x < hole.x+250-player.width and player.y >= winheight-84:
                if player.alive:
                    death.play()
                player.alive = False
                player.y += 15

        if player.x <= -32 and player.alive:
            player.isJump = False #so that jetpack doesn't drown out death sound
            death.play()
            player.alive = False
            player.y += 2000


    #game over 
    
    if gameovercount > 10:
        end = True
    
    if not twoplayer:
        if not player1.alive:
            score = playtime
            gameovercount += 1
        if player1.alive:
            playtime += 1
            # more elegant but not resettable: playtime = pygame.time.get_ticks() // 1000 
        timer = smallfont.render(str(playtime).zfill(4), 1, (255,201,14))
        window.blit(timer, (705,20))
        pygame.display.update()

    else:
        if not player1.alive:
            if player2.alive:
                winner = player2
            gameovercount += 1
        if not player2.alive:
            if player1.alive:
                winner = player1
                gameovercount += 1
    
    #refresh screen
    redrawGameWindow()
    pygame.display.update()

    if end:
        pygame.mixer.music.load('gameover.mp3')
        pygame.mixer.music.play(-1,0.0)
    
        endrun = True
        while endrun:
            clock.tick(27)

            title.draw(window)
            gomsg = bigfont.render("Game Over", 1, (255,201,14))
            window.blit(gomsg, (220,100))
            keys = pygame.key.get_pressed()
            

            if winner != 0:
                winnername = smallfont.render("Winner:  "+winner.name, 1, (255,201,14))
                winner.move = True
                winner.left = False
                winner.x = winwidth/2 -winner.width/2
                winner.y = winheight/2
                winner.draw(window)
                #for still image:
                #window.blit(winner.standimg, (winwidth/2-winner.width/2, winheight/2))
                window.blit(winnername, (260,300))
            else:
                if not twoplayer:
                    newscore = smallfont.render("Your Score:  "+str(score).zfill(4), 1, (255,201,14))
                    window.blit(newscore, (260,300))
                else:
                    winnername = smallfont.render("Did you do that on purpose?", 1, (255,201,14))
                    window.blit(winnername, (180,300))
            pygame.display.update()
            
            if keys[pygame.K_r]:
                select.play()
                reset()
                endrun = False

            if keys[pygame.K_e]:
                select.play()
                reset()
                if len(playerlist)>1:
                    playerlist.pop()
                menu = True
                endrun = False

            if keys[pygame.K_ESCAPE]:
                run = False
                endrun = False

            #leave game 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endrun = False 
                    run = False

pygame.quit()