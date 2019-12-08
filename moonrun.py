"""
-------------------------- MOON RUN -------------------------------
Created by: Remigius Ezeabasili, Jonas Kohl, Sarah Smith, Mohammad Yazdani
Music by: Eric Skiff

"""


# general initiation
import pygame
import random
import pickle
import os

pygame.init()

#gets current working directory to access all files
os.chdir(os.path.dirname(os.path.realpath(__file__)))


#general game values
pygame.display.set_caption("Moon Run")
clock = pygame.time.Clock()     # Used to track time in the game 
worldvel = 8    # Velocity of sidescroll
maxscore = 999999


#window
winwidth = 800  # Display window width
winheight = 400     # Display window height 

window = pygame.display.set_mode((winwidth,winheight))
pFloorpos = winheight-87
pOntoppos = winheight-87-64

#fonts
font = 'font2.ttf' 

#Colours
fontcolour = pygame.Color(255,201,14)   # Yellow font colour 
white = pygame.Color('white')      
black = pygame.Color('black')         
p1colour = pygame.Color('red')      
p2colour = pygame.Color('blue')  


#images
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


#sounds
introsound = pygame.mixer.Sound('intro.wav')
start = pygame.mixer.Sound('start.wav') 
hover = pygame.mixer.Sound('hover.wav')
jetpack = pygame.mixer.Sound('jetpack.wav') 
death = pygame.mixer.Sound('death.wav') 
step = pygame.mixer.Sound('step.wav') 
fall = pygame.mixer.Sound('falling.wav') 
crash = pygame.mixer.Sound('crash.wav') 
select = pygame.mixer.Sound('selection.wav') 
itemsound = pygame.mixer.Sound('item.wav') 
speed = pygame.mixer.Sound('speed.wav') 



class player (object):

    def __init__(self,x,y,width,height,movelist,standimg,jumpimg,name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.movelist = movelist    # Sprite images for movement
        self.standimg = standimg    # Standing image of player
        self.jumpimg = jumpimg      # Jumping image of player
        self.name = name

        self.vel = worldvel+2  # Allows player to move in the world
        self.isJump = False
        self.jumpheight = 10
        self.jumpCount = self.jumpheight
        self.fallCount = 0
        self.left = False
        self.step = 0 
        self.move = False
        self.alive = True

        self.leftof = False
        self.rightof = False
        self.ontop = False
        self.floorpos = pFloorpos
        self.col = False    # Collision detection 

        self.speedboost = 0
        self.maxspeedboost = 6
        self.maxjumpheight = 16


    def moving(self, leftB, rightB, jumpB):

        self.platform()
        #default movement
        self.x -= worldvel
        self.collision()

        #gravity 
        if self.alive:
            falldistance= (self.fallCount**2) * 0.25
            if self.y + falldistance <= self.floorpos:
                if self.jumpCount == 0:
                    self.y += falldistance
                    self.fallCount += 0.5
                else:
                    if self.jumpCount == self.jumpheight and self.y < pFloorpos and not self.isJump:
                        if not self.ontop:
                            self.y += 8
                    
            else:
                if self.jumpCount < self.jumpheight:  
                    self.y = self.floorpos
                    self.isJump = False
                    self.jumpCount = self.jumpheight
                    self.fallCount = 0

        #controls
        if self.alive:
            if leftB and not self.rightof:
                self.left = True  ## Can move left 
                self.x -= self.vel ## Create an offset
                if not self.isJump:  
                    self.move = True  
                    step.play()

            elif rightB and not self.leftof:
                self.left = False
                if self.x <= winwidth:
                    self.x += self.vel
                if not self.isJump:
                    self.move = True
                    step.play()
            
            else: 
                self.move = False

            if not self.isJump:
                if jumpB:
                    self.isJump = True
                    self.move = False
                
            else:
                self.jump()
    
    def jump (self):

        if self.jumpCount > 0:
            self.y -= 8
            self.jumpCount -= 0.5
            jetpack.play()

    def draw(self, window): # Draw function used to implement sprite animation 
        if self.move:
            if self.step + 1 > 16: 
                self.step = 0
            if not self.left: 
                window.blit(self.movelist[self.step//2], (self.x,self.y))   # Integer division the number of steps to determine which sprite image to use 
            else: 
                window.blit(pygame.transform.flip(self.movelist[self.step//2],1,0), (self.x,self.y))
            self.step += 1
        elif self.isJump and self.jumpCount > 0:
            if not self.left:
                if pygame.time.get_ticks()%2 == 0:
                    window.blit(self.jumpimg[0], (self.x,self.y))
                else:
                    window.blit(self.jumpimg[1], (self.x,self.y))
            else: 
                if pygame.time.get_ticks()%2 == 0:
                    window.blit(pygame.transform.flip(self.jumpimg[0],1,0), (self.x,self.y))
                else:
                    window.blit(pygame.transform.flip(self.jumpimg[1],1,0), (self.x,self.y))
        else:   # Player standing still
            if not self.left:
                window.blit(self.standimg, (self.x,self.y))
            else:
                window.blit(pygame.transform.flip(self.standimg,1,0), (self.x,self.y))
    
   
    def collision(self):

        # Collision with item 
        for item in itemlist:
            if  item.x < self.x + self.width//2 < item.x + item.width:
                if self.y+self.height >= item.y:

                    if item.img == "item1.png":
                        if self.speedboost < self.maxspeedboost:
                            self.speedboost += 2

                    else:
                        if self.jumpheight < self.maxjumpheight:
                            self.jumpheight += 2
                    itemsound.play()
                    itemlist.pop(itemlist.index(item))   

        if not self.col:
            self.leftof = False
            self.rightof = False
        self.col = False

        #player death
        for hole in holelist:
            if self.x > hole.x + 5 and self.x < hole.x+hole.width-self.width and self.y >= winheight-91:
                if self.alive:
                    pygame.mixer.Channel(1).play(death)
                self.alive = False
                self.y += 15

        if self.x <= -50 and self.alive:
            self.isJump = False #so that jetpack doesn't drown out death sound
            pygame.mixer.Channel(1).play(death)
            self.alive = False
            self.y += 2000

    def platform(self):

        # interaction with meteor
        for meteo in meteolist:
            if not meteo.inhole:
                if meteo.x < self.x + self.width - 20 < meteo.x + meteo.width and self.y + self.height > meteo.y + 10:
                    self.leftof = True
                    self.col = True
                elif meteo.x < self.x < meteo.x + meteo.width and self.y + self.height > meteo.y + 10 : 
                    self.rightof = True
                    self.col = True

                if meteo.x <= self.x+self.width//2 <= meteo.x+meteo.width+10:
                    self.ontop = True
                    self.floorpos = pOntoppos
        if not self.ontop:
            self.floorpos = pFloorpos
        self.ontop = False
        

class element (object):

    def __init__(self,x,y,vel,img,width,height):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.width = width
        self.height = height


class backdrop (element):   # Class for dynamic background in both menu and gameplay
    
    def draw(self, window):
        window.blit(pygame.image.load(self.img), (self.x,self.y)) 
        window.blit(pygame.image.load(self.img), (self.x+winwidth,self.y))  # Creates 2 images, one following from the other. Allows for sidescrolling of background
        if self.x > -winwidth: 
            self.x -= self.vel
        else:
            self.x = 0
        
class displayObject (element):  

    def draw(self,window):
        window.blit(pygame.image.load(self.img),(self.x,self.y))

# class Background (Images):

#     def __init__(self,x,y,vel,img,width,height):
        
#         self.x = x
#         self.y = y
#         self.vel = vel
#         self.img = img
#         self.width = width
#         self.height = height
#         worldvel = 8

# class Backdrop (Background):
    
#     def draw(self, window):
#         window.blit(pygame.image.load(self.img), (self.x,self.y))
#         window.blit(pygame.image.load(self.img), (self.x+self.winwidth,self.y))
#         if self.x > -self.winwidth:
#             self.x -= self.vel
#         else:
#             self.x = 0
        
# class BackgroundObjects (Background):
#     # displayobjects
#     def draw(self,window):
#         window.blit(pygame.image.load(self.img),(self.x,self.y))

# class Items (BackgroundObjects):

#     def __init__(self,x,y,vel,img,width,height):
#         self.x = x
#         self.y = y
#         self.vel = vel
#         self.img = img
#         self.width = width
#         self.height = height

#     def draw(self,window,secimg):
#         if (pygame.time.get_ticks()//500)%2: 
#             window.blit(pygame.image.load(self.img),(self.x,self.y))
#         else:
#             window.blit(pygame.image.load(secimg),(self.x,self.y))

# class Meteorite (displayObject):

#     inhole = False 

#     def animate(self):
#         #meteorite animation    
#         if self.y == winheight - 80 - 32:  # Determines y postion to play meteorite sound
#             crash.play() # Plays crash sound
            
#         if self.y < winheight - 80: 
#             self.y += 32
#         else:
#             for hole in holelist:
#                 if self.x > hole.x and self.x < hole.x+hole.width-self.width:   # Condition to check meteor is within hole 
#                     self.y += 32 # Allows meteor to fall through hole 
#                     self.inhole = True 
#             self.img='meteoriteb.png'   # Loads image of meteorite making collision with the ground
    

# class Item (displayObject):


#     def draw(self,window,secimg):
#         if (pygame.time.get_ticks()//500)%2: 
#             window.blit(pygame.image.load(self.img),(self.x,self.y))
#         else:
#             window.blit(pygame.image.load(secimg),(self.x,self.y))

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


class scoreboard (object):
    LENGTH = 4      # 5 High scores 

    def __init__(self,scoreList):
        self.scoreList = scoreList
    
    def addscore(self,newscore):    # Method that allows a new score to be added
        if newscore >= maxscore:
            newscore = maxscore     # If current score is the highest score
        self.scoreList += [newscore]    # Adds new score to list
        self.scoreList = sorted(self.scoreList,reverse=True)    # Sorted and reverse used to order scorelist in descending order
        self.scoreList.pop(self.LENGTH+1)
        if newscore in self.scoreList:
            return True
        else:
            return False


    def reset(self):
        for i in range(self.LENGTH+1):
            self.scoreList[i] = 0


def introPlay():
    incount = 0
    global intro
    global run
    while intro:
        clock.tick(27)
        incount += 1
        window.blit(gameintro, (0,0))

        mask = pygame.Surface((winwidth, winheight))
        mask = mask.convert()
        mask.fill(black)
        mask.set_alpha(255-10*incount)      # Gradually decreases transparency of black screen to load in logo 
        window.blit(mask, (0, 0))           
        if incount == 20:
            introsound.play()
            presents = Text(winwidth//2, winheight//2+50, "presents", font, 15, (255,255,255))  # Text alignment for presents subtext 
            presents.show_text()
        pygame.display.update()
        if incount >= 60:
            intro = False
            pygame.mixer.music.load('music.mp3')
            pygame.mixer.music.play(-1,0.0)
        #leave game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                run = False


def startScreen():
    #game menu
    global menu
    global second_menu
    global run
    while menu:
        clock.tick(27)  # Frame rate

        #leave game 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                menu = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                start.play()
                menu = False
                second_menu = True
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                else:
                    start.play()
                    second_menu = True
                    menu = False
        title.draw(window)
    
        text = Text(winwidth//2, winheight//3, 'MOON RUN', font, 55, fontcolour)
        text.show_text() 
        if (pygame.time.get_ticks()//500)%2:
            begincolour = fontcolour
        else:
            begincolour = white
        text2 = Text(winwidth//2, winheight//1.5, 'Press any key to begin', font, 25, begincolour)
        text2.show_text()

        pygame.display.update()

def playerSelect():
    global run
    global second_menu
    global twoplayer
    instruc = False
    while second_menu: # second menu loop
        
        title.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        text1 = Text(winwidth//2, winheight//3, '1 Player [1]', font, 25, fontcolour) # 1 Player text
        text2 = Text(winwidth//2, winheight//2, '2 Player [2]', font, 25, fontcolour) # 2 player text
        text1.show_text() # method to show the text
        text2.show_text()
        pygame.display.update()
        keys=pygame.key.get_pressed()

        if keys[pygame.K_2]:
            select.play()
            twoplayer = True
            playerlist.append(player2)
            instruc = True
            second_menu = False
        
        if keys[pygame.K_1]:
            select.play()
            twoplayer = False
            instruc = True
            second_menu = False
        
        if keys[pygame.K_ESCAPE]:
            run = False
            second_menu = False
    
        # For mouse over text sound
        soundtrigger = False
        if text1.mouse_over() or text2.mouse_over():
            soundtrigger = True
            if soundtrigger == True:
                hover.play()               # Sound can be changed if necessary
                soundtrigger = False
        
        text1ctrl = True
        while text1.mouse_over() and text1ctrl: # While loop for when the mouse is on top of the text
            text1 = Text(winwidth//2, winheight//3, '1 Player [1]', font, 25, p1colour) # redraws the text but changes colour 
            title.draw(window)
            text1.show_text()
            text2.show_text()
            pygame.display.update() # updates the display
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key != pygame.K_2: # if the mouse is clicked while on the text
                    select.play()
                    twoplayer = False
                    instruc = True
                    second_menu = False
                    text1ctrl = False
        
        text2ctrl = True            
        while text2.mouse_over() and text2ctrl:
            text2 = Text(winwidth//2, winheight//2, '2 Player [2]', font, 25, p2colour )  
            title.draw(window)
            text1.show_text()
            text2.show_text()
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key != pygame.K_1:
                    select.play()
                    twoplayer = True
                    playerlist.append(player2)
                    instruc = True
                    second_menu = False
                    text2ctrl = False
    if instruc:
        instructionloop(twoplayer)

def instructionloop(twoplayer): # Instruction page before game starts
    trigger = True
    global run
    while trigger:
        clock.tick(27)
        title.draw(window)
        if twoplayer:
            window.blit(info2, (0,0))       # If 2 player selected then loads info page for 2 players
        else:
            window.blit(info1, (0,0))       # If 1 player selected then loads infopage for 1 player
        pygame.display.update()            

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                trigger = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:     # User presses space to proceed to game 
                    select.play()
                    trigger = False


def pauseMenu():    # Pause Menu during gameplay 
    pause = True
    global run
    while pause:
        clock.tick(27)
        
        #leave game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pause = False
        
        # Continue and Retry prompts 
        contmsg = Text(winwidth//2, winheight//2, 'Continue [C]', font, 35, fontcolour)     
        retrymsg = Text(winwidth//2, winheight//1.5, 'Restart [R]', font, 35, fontcolour)
        contmsg.show_text()
        retrymsg.show_text()
        pygame.display.flip()
        
        contctrl = True
        while contmsg.mouse_over() and contctrl:
            contmsg = Text(winwidth//2, winheight//2, 'Continue [C]', font, 35, white)
            contmsg.show_text()
            retrymsg.show_text()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    select.play()
                    pause = False
                    contctrl = False

        retryctrl = True            
        while retrymsg.mouse_over() and retryctrl:
            retrymsg = Text(winwidth//2, winheight//1.5, 'Restart [R]', font, 35, white)   
            retrymsg.show_text()
            contmsg.show_text()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    select.play()
                    reset()
                    pause = False
                    retryctrl = False
        
        pkeys = pygame.key.get_pressed()
        if pkeys[pygame.K_c]:
            select.play()
            pause = False

        if pkeys[pygame.K_r]:
            select.play()
            reset()
            pause = False

        pygame.display.update()

def endScreen():
    global menu
    global run
    global endcredits
    global winner
    pygame.mixer.music.load('gameover.mp3')
    pygame.mixer.music.play(-1,0.0)

    endrun = True
    while endrun:
        clock.tick(27)

        title.draw(window)
        gomsg = Text(winwidth//2, 100, "Game Over", font, 55, fontcolour)
        gomsg.show_text()
        goprompt = Text(winwidth//2, 350, \
            "Restart [R]        High Score[H]        Main Menu[E]        Exit[ESC]", font, 15, fontcolour)
        goprompt.show_text()
            
       
        
        keys = pygame.key.get_pressed()

        if winner != 0:
            
            winnername = Text(winwidth//2, 300, "Winner {}".format(winner.name), font, 25, fontcolour) 
            winner.move = True
            winner.left = False
            winner.x = winwidth/2 -winner.width/2
            winner.y = winheight/2
            winner.draw(window)
            winnername.show_text()
            
        else:
            if not twoplayer:
                if newhigh:
                    congratulations = Text(winwidth//2, 260, "New high score".format(str(myscore).zfill(4)), font, 25, p1colour)
                    if (pygame.time.get_ticks()//500)%2: 
                        congratulations.show_text()
                newscore = Text(winwidth//2, 300, "Your score: {}".format(str(myscore).zfill(4)), font, 25, white)
                newscore.show_text()
                
            else:
                winnername = Text(winwidth//2, 300, "Did you do that on purpose?", font, 25, fontcolour)
                winnername.show_text()
                
        
        
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

        if keys[pygame.K_h]:
            pygame.draw.rect(window,(fontcolour),(winwidth/2-250,0,500,400))
            linecount = 0
            hiscores = Text(winwidth//2, 100, "High Scores:", font, 25, black) 
            hiscores.show_text()
            
            for score in highscore.scoreList:
                linecount += 1
                i = Text(winwidth//2, 100+linecount*40, str(linecount)+". . . . . . . ." +str(score).zfill(6), font, 25, black)
                i.show_text()
            pygame.display.update()
        
        if keys[pygame.K_0]:
            highscore.reset()

        if keys[pygame.K_ESCAPE]:
            start.play()
            run = False
            endrun = False
            endcredits = True
        
        pygame.display.update()

        #leave game 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endrun = False 
                run = False

def creditScene():
    global run
    global endcredits
    endcount = 0
    while endcredits and endcount <300:
        
        credit = ["Moon Run","","Game and visuals:","",\
            "Remigius Ezeabasili", "Jonas Kohl", "Sarah Smith",\
            "Mohammad Yazdani","","Music:","",\
            "Eric Skiff - HHavok-intro / Ascending - Resistor Anthems", \
            "Available for free at    http://EricSkiff.com/music","",\
            "Sounds:      BitKits free VST","", "2019"]
        title.draw(window)
        linecount = 0
        for line in credit:
            linecount += 20
            i = Text(winwidth//2, 20+linecount, line, font, 15, fontcolour)
            i.show_text()

        pygame.display.update() 
        endcount += 1

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endcredits = False
                    run = False


def redrawGameWindow():     # Function used to draw game's objects  
    window.blit(night,(0,0)) #draws background (starry night)
    bd1.draw(window)
    pygame.draw.rect(window,(60,60,60),(0,winheight-20,winwidth,20)) #draws the floor
    for holes in holelist:
        holes.draw(window)
    for meteo in meteolist:
        meteo.animate()
        meteo.draw(window)
    for item in itemlist:
        if item.img=="item1.png":
            otherimg = "item12.png"
        else:
            otherimg = "item22.png"
        item.draw(window,otherimg)
    for player in playerlist:
        player.draw(window)

def createAndMove(typ,lst,listLimit,randLimit):
    for obj in lst:
        if obj.x <= -obj.width:
            lst.pop(lst.index(obj))

    #make random objects
    objget=random.randint(0,randLimit)
    if objget == 0 and len(lst)<listLimit:
        if typ == "h":
            x = displayObject(winwidth+200,winheight-30,worldvel,'bigcrater.png',250,30)
        elif typ == "m":
            x = Meteorite(winwidth,0,worldvel,'meteorite.png',64,64)
            fall.play()
        elif typ == "i":
            if pygame.time.get_ticks()%2 == 0:
                x = Item(winwidth,winheight-60,worldvel,'item1.png',32,32)
            else:
                x = Item(winwidth,winheight-60,worldvel,'item2.png',32,32)
        #add to objectlist
        lst += [x]
    #move objects at their velocity
    for obj in lst:
        obj.x -= worldvel


def reset():
    global worldvel
    global holelist
    global meteolist
    global gameovercount
    global winner
    global playtime
    global end
    global replay
    global playerlist
    global itemlist
    global highget
    global newhigh
    global speedcount
    
    worldvel = 8
    holelist=[]
    meteolist=[]
    itemlist=[]
    gameovercount=0
    winner=0
    playtime=0
    speedcount = 0
    highget = True
    end = False
    replay = False
    for player in playerlist:
        player.alive = True
        player.y = winheight-player.height-16
        player.isJump = False
        player.ontop = False
        player.leftof = False
        player.rightof = False
        player.speedboost = 0
        player.jumpheight = 10
        player.jumpCount = player.jumpheight
        player.neg = 1
        player.vel = (5/4)*worldvel

    player1.x = winwidth//2

    if twoplayer:
        player2.x = winwidth*(2/3)
    
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1,0.0)


#class instances
title = backdrop(0,0,worldvel/2,'starry.png',800,400)
bd1 = backdrop(0,0,worldvel/8,'hills_bg.png',800,400)

player1 = player(winwidth//2,pFloorpos,71,71, p1move, p1stand, p1jump, 'Player 1')
player2 = player(winwidth*(2/3),pFloorpos,71,71, p2move, p2stand, p2jump, 'Player 2')



#start conditions



itemlist=[]
holelist=[]
meteolist=[]
allobjlist = [itemlist,holelist,meteolist]
playerlist = [player1]
gameovercount = 0
winner = 0
playtime = 0
speedcount = 0
intro = True
end = False
replay = False
menu = True
endcredits = False
second_menu = False
twoplayer = False
highget = True
newhigh = False
firstrun = True



#loads highscores from file
try:
    file = open("highscore.hs","rb")
    highscore = pickle.load(file)
    file.close()
except FileNotFoundError:
    highscore = scoreboard([0,0,0,0,0])
except EOFError:
    highscore = scoreboard([0,0,0,0,0])



#main game loop
run = True
while run:
    clock.tick(27)
    keys = pygame.key.get_pressed()

    #leave game 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    introPlay()
    startScreen()
    playerSelect()
    """
    #randomly generate and move holes, meteors and items. 
    createAndMove('h',holelist,1,50)
    createAndMove('m',meteolist,1,100)
    createAndMove('i',itemlist,1,300)
    """       
    
    #player control
    player1.moving(keys[pygame.K_LEFT],keys[pygame.K_RIGHT],keys[pygame.K_UP])
    if twoplayer:
        player2.moving(keys[pygame.K_a],keys[pygame.K_d],keys[pygame.K_w])

    #pause game
    if keys[pygame.K_p]:
        select.play()
        pauseMenu()

    #speed up
    speedcount += 1
    if speedcount % 500 == 0:
        worldvel *= 1.5
        speed.play()
    player1.vel = worldvel+2 + player1.speedboost
    player2.vel = worldvel+2 + player2.speedboost
    bd1.vel = worldvel/8

    #game over conditions
    if gameovercount > 20:
        end = True
    
    if not twoplayer:
        if not player1.alive:
            myscore = playtime
            gameovercount += 1
            if highget:
                newhigh = highscore.addscore(myscore)
                highget = False
        if player1.alive:
            playtime += 1 

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
    if not menu and not second_menu and run:

        
        redrawGameWindow() 
        if not twoplayer:
            timer = Text(winwidth//2, 40, str(playtime).zfill(4), font, 25, fontcolour)
            timer.show_text()
        pygame.display.update() 

    if end:
        endScreen() 
    
    if endcredits:
        creditScene()
    

#write the highscores into a file
file = open("highscore.hs","wb")
pickle.dump(highscore,file)
file.close()

pygame.quit()
