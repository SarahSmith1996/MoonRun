"""
-------------------------- MOON RUN -------------------------------


NOTES:

    IDEAS:
    - Enter Name
    - add shooting star
    - spikey objects/aliens that kill on contact


    OPTIMIZE CODE:
    - OOP optimization 
        - class variables change self to classname?
        - 'stuff' subclass of elements (draw function in element class)?
    - make reset function the general initializer of all game variables -> reset at the start of game (within menu)
    - remove hardcoding
    - sort code: global variables, databases, functions
    - sounds drown each other out
    - change hole sprite, so meteorites look better on top


"""


# general initiation
import pygame
import random
import pickle
import os
import Sounds
import Display
import Player


pygame.init()

#gets current working directory to access all files
os.chdir(os.path.dirname(os.path.realpath(__file__)))


#general game values
worldvel = 8
maxscore = 999999
pygame.display.set_caption("Moon Run")
clock = pygame.time.Clock()

gamewin = Display.Screen(800, 400)
window = gamewin.create_window()

vsmallfont = Display.Fonts()
vsmallfont.font_size(15)
smallfont = Display.Fonts()
smallfont.font_size(25)
bigfont = Display.Fonts()
bigfont.font_size(55)
fontcolour = Display.Fonts()
fontcolour.fonts_colours(255,201,14)

sky = GameProperties.Images()
backgroundimg = GameProperties.Images()


#Colours
fontcolour = pygame.Color(255,201,14)
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
        self.movelist = movelist
        self.standimg = standimg
        self.jumpimg = jumpimg
        self.name = name

        self.vel = worldvel+2
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


    
    #delete self.left
    def moving(self, leftB, rightB, jumpB):
        
        if self.alive:
            if leftB:
                self.left = True
                self.x -= self.vel
                if not self.isJump:
                    self.move = True
                    step.play()

            elif rightB:
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
            if self.step + 1 > 16:
                self.step = 0
            if not self.left: 
                window.blit(self.movelist[self.step//2], (self.x,self.y))
            else:
                window.blit(pygame.transform.flip(self.movelist[self.step//2],1,0), (self.x,self.y))
            self.step += 1
        elif self.isJump and self.neg == 1:
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
        else:
            if not self.left:
                window.blit(self.standimg, (self.x,self.y))
            else:
                window.blit(pygame.transform.flip(self.standimg,1,0), (self.x,self.y))
    
    #should maybe move to item class, ideally use sprites instead
    def collision(self):

        #item
        for item in itemlist:
            if self.x > item.x and self.x < item.x + item.width:
                if self.y+self.height >= item.y:

                    if item.img == "item1.png":
                        if self.vel < self.maxvel:
                            self.vel += 4
                            print ("Speed up!")
                    else:
                        if self.jumpheight < self.maxjumpheight:
                            #self.jumpheight += 2    doesn't work, redo jump
                            print("Jetpack boost!")
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
        
class displayObject (element):

    def draw(self,window):
        window.blit(pygame.image.load(self.img),(self.x,self.y))


class Item (displayObject):


    def draw(self,window,secimg):
        if (pygame.time.get_ticks()//500)%2: 
            window.blit(pygame.image.load(self.img),(self.x,self.y))
        else:
            window.blit(pygame.image.load(secimg),(self.x,self.y))

class scoreboard (object):
    LENGTH = 4

    def __init__(self,scoreList):
        self.scoreList = scoreList
    
    def addscore(self,newscore):
        if newscore >= maxscore:
            newscore = maxscore
        self.scoreList += [newscore]
        self.scoreList = sorted(self.scoreList,reverse=True)
        self.scoreList.pop(self.LENGTH+1)

    def reset(self):
        for i in range(self.LENGTH):
            self.scoreList[i] = 0


def redrawGameWindow():
    window.blit((sky.get_image("night")),(0,0)) #draws background (starry night)
    bd1.draw(window)
    #bd2.draw(window)
    lunar.draw(window)
    pygame.draw.rect(window,(60,60,60),(0,winheight-20,winwidth,20)) #draws the floor
    for holes in holelist:
        holes.draw(window)
    for meteo in meteolist:
        meteo.draw(window)
    for item in itemlist:
        if Items.img=="item1.png":
            otherimg = "item12.png"
        else:
            otherimg = "item22.png"
        Items.draw(window,otherimg)
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
            x = displayObject(winwidth,0,worldvel,'meteorite.png',64,64)
            fall.play()
        elif typ == "i":
            if pygame.time.get_ticks()%2 == 0:
                x = Items(winwidth,winheight-60,worldvel,'item1.png',32,32)
            else:
                x = Items(winwidth,winheight-60,worldvel,'item2.png',32,32)
        #add to objectlist
        lst += [x]
    #move objects at their velocity
    for obj in lst:
        obj.x -= worldvel

def instructionloop(twoplayer):
    trigger = True
    
    while trigger:
        clock.tick(27)
        title.draw(window)
        if twoplayer:
            window.blit(info2, (0,0))
            window.blit((GameProperties.Images.get_images("info1")),(0,0))
        else:
            window.blit(info1, (0,0))
        pygame.display.update()            

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                global run
                run = False
                trigger = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    select.play()
                    trigger = False
            window.blit((GameProperties.Images.get_images("info2")), (0,0))
        

class Text: #### creating the text class 
    
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
        player.jumpCount = 10
        player.neg = 1
        player.vel = (5/4)*worldvel

    player1.x = winwidth//2

    if twoplayer:
        player2.x = winwidth*(2/3)
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1,0.0)


#class instances

title = Display.Backdrop(0,0,worldvel/2,sky.get_image("night"),800,400)
bd1 = Display.Backdrop(0,0,worldvel/8,backgroundimg.get_image("background"),800,400)
#bd2 = backdrop(0,0,worldvel/4,'hills_fg.png',800,400)

lunar = Display.BackgroundObjects(winwidth*3,winheight-170,worldvel,'lunarmodule.png',160,160)

player1 = player(winwidth//2,winheight-85,71,71, (GameProperties.Images.get_image("p1move")), \
    (GameProperties.Images.get_images("p1stand")), (GameProperties.Images.get_image("p1jump")), 'Player 1')
player2 = player(winwidth*(2/3),winheight-85,71,71, (GameProperties.Images.get_image("p2move")), \
    (GameProperties.Images.get_images("p2stand")), (GameProperties.Images.get_image("p2jump")), 'Player 2')

#loads highscores from file
try:
    file = open("highscore.hs","rb")
    highscore = pickle.load(file)
    file.close()
except FileNotFoundError:
    highscore = scoreboard([0,0,0,0,0])
except EOFError:
    highscore = scoreboard([0,0,0,0,0])


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
firstrun = True

#music for main game


#main game loop
run = True
while run:
    incount = 0
    while intro:
        clock.tick(27)
        incount += 1
        window.blit(gameintro, (0,0))

        mask = pygame.Surface((winwidth, winheight))
        mask = mask.convert()
        mask.fill(black)
        mask.set_alpha(255-10*incount)
        window.blit(mask, (0, 0))
        if incount == 20:
            introsound.play()
            presents = Text(winwidth//2, winheight//2+50, "presents", font, 15, (255,255,255))
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
        
        text = Text(winwidth//2, winheight//3, 'MOON RUN', font, 55, fontcolour)
        text.show_text()
        
        text2 = Text(winwidth//2, winheight//1.5, 'Press any key to begin', font, 25, fontcolour)
        text2.show_text()

        pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONDOWN:
            menu = False
            second_menu = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            else:
                start.play()
                second_menu = True
            menu = False
            
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
            instructionloop(twoplayer)
            second_menu = False
        
        if keys[pygame.K_1]:
            select.play()
            twoplayer = False
            instructionloop(twoplayer)
            second_menu = False
        
        if keys[pygame.K_ESCAPE]:
            run = False
            second_menu = False
        
        text1ctrl = True
        while text1.mouse_over() and text1ctrl: # While loop for when the mouse is on top of the text
            text1 = Text(winwidth//2, winheight//3, '1 Player [1]', font, 25, p1colour) # redraws the text but changes colour 
            title.draw(window)
            text1.show_text()
            text2.show_text()
            pygame.display.update() # updates the display
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN: # if the mouse is clicked while on the text
                    select.play()
                    twoplayer = False
                    instructionloop(twoplayer)
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
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    select.play()
                    twoplayer = True
                    playerlist.append(player2)
                    instructionloop(twoplayer)
                    second_menu = False
                    text2ctrl = False
                    
            
    #default movement
    for player in playerlist:
        player.x -= worldvel
        player.collision()
    
    # lunar module regularly apperars
    if lunar.x > -6*winwidth:
        lunar.x -= worldvel
    else: 
        lunar.x = winwidth
    
    #randomly generate and move holes, meteors and items
    createAndMove('h',holelist,1,50)
    createAndMove('m',meteolist,3,100)
    createAndMove('i',itemlist,1,200)
        
    #meteorite animation    
    for meteo in meteolist:
        if meteo.y == winheight - 80 - 32:
            crash.play()
        if meteo.y < winheight - 80:
            meteo.y += 32
        else:
            for hole in holelist:
                if meteo.x > hole.x and meteo.x < hole.x+hole.width-meteo.width:
                    meteo.y += 32
            meteo.img='meteoriteb.png'
    
    #player control
    keys = pygame.key.get_pressed()
    player1.moving(keys[pygame.K_LEFT],keys[pygame.K_RIGHT],keys[pygame.K_UP])
    if twoplayer:
        player2.moving(keys[pygame.K_a],keys[pygame.K_d],keys[pygame.K_w])

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
                reset()
                pause = False

            pygame.display.update()
            continue

    #player death
    for player in playerlist:
        for hole in holelist:
            if player.x > hole.x + 5 and player.x < hole.x+hole.width-player.width and player.y >= winheight-91:
                if player.alive:
                    death.play()
                player.alive = False
                player.y += 15

        if player.x <= -50 and player.alive:
            player.isJump = False #so that jetpack doesn't drown out death sound
            death.play()
            player.alive = False
            player.y += 2000

    #speed up
    speedcount += 1
    if speedcount % 500 == 0:
        worldvel *= 1.5
        speed.play()
    player1.vel = worldvel+2
    player2.vel = worldvel+2
    bd1.vel = worldvel/8
    #bd2.vel = worldvel/4

    #game over 
    
    if gameovercount > 20:
        end = True
    
    if not twoplayer:
        if not player1.alive:
            myscore = playtime
            gameovercount += 1
            if highget:
                highscore.addscore(myscore)
                highget = False
        if player1.alive:
            playtime += 1 

        if run:
            timer = smallfont.render(str(playtime).zfill(4), 1, (255,201,14))
            window.blit(timer, (winwidth-timer.get_width()-20,20))
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
    
    #refresh screen#
    if not menu and not second_menu and run:
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
            window.blit(gomsg, (winwidth//2-gomsg.get_width()//2,100))
            goprompt = vsmallfont.render ("Restart [R]                           High Score[H]                           Main Menu[E]                           Exit[ESC]", 1,(255,201,14))
            window.blit (goprompt, (winwidth//2-goprompt.get_width()//2,350))
            
            
            keys = pygame.key.get_pressed()

            if winner != 0:
                winnername = smallfont.render("Winner:  "+winner.name, 1, (fontcolour))
                winner.move = True
                winner.left = False
                winner.x = winwidth/2 -winner.width/2
                winner.y = winheight/2
                winner.draw(window)
                window.blit(winnername, (winwidth//2-winnername.get_width()//2,300))
            else:
                if not twoplayer:
                    newscore = smallfont.render("Your Score:  "+str(myscore).zfill(4), 1, (255,255,255))
                    window.blit(newscore, (winwidth//2-newscore.get_width()//2,250))
                else:
                    winnername = smallfont.render("Did you do that on purpose?", 1, (fontcolour))
                    window.blit(winnername, (winwidth//2-winnername.get_width()//2,300))
            
            
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
                pygame.draw.rect(window,(fontcolour),(winwidth/2-200,0,400,400))
                linecount = 0
                window.blit(smallfont.render("High Scores:", 1, (0,0,0)), (290,100))
                for score in highscore.scoreList:
                    linecount += 1
                    window.blit(smallfont.render(str(linecount)+" . . . . . . . "+str(score).zfill(6), 1, (0,0,0)), (290,100+linecount*40))

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



file = open("highscore.hs","wb")
pickle.dump(highscore,file)
file.close()

pygame.quit()
