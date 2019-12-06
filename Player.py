import pygame
pygame.init()

class Player (object):

    def __init__(self,x,y,width,height,movelist,standimg,jumpimg,name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.movelist = movelist
        self.standimg = standimg
        self.jumpimg = jumpimg
        self.name = name

class PlayerMovement(Player): 
    
    worldvel = 8
    vel = worldvel+2
    isJump = False
    jumpheight = 10
    jumpCount = jumpheight
    left = False
    step = 0
    move = False
    alive = True
    neg = 1

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

        self.maxvel = 2.5*worldvel
        
        self.maxjumpheight = 13

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
