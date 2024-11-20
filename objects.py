#module that consists of every menu and game object that will be used
import pygame
from config import*
import time

class Button(): #Buttons will just be images
    def __init__(self, x, y, image, click, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))) #allows easy scaling of button
        self.click = pygame.transform.scale(click, (int(width * scale), int(height * scale))) #image when click
        self.rect = self.image.get_rect() #gets rect of image for the collider feature
        
        #takes a tuple and places rect on top of left of image, 
        # this is because of how pygame does its coordinates
        self.rect.topleft = (x,y) 

        self.clicked = False
       
    def clickCheck(self, surface):
        pos = pygame.mouse.get_pos() #get mouse position
        action = False
        if self.rect.collidepoint(pos): #checks mouse is over the button       
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #checks if mouse has been pressed and is not in clicked state
                
                self.clicked = True #do the things it needs to do
                action = True        
            if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
        return action
   


    def draw(self,surface):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos): #checks mouse is over the button
            surface.blit(self.click, (self.rect.x, self.rect.y))

                
                    
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y)) #draw button on screen
                
        

class Timer(): #Object for creating timers and cooldowns in attacks
    def __init__(self):
        self.time = time.time()
        self.tempTime = 0
    
    def startTimer(self):
        self.time = time.time()
        return self.time

    def executeTimer(self, start, number):
        self.tempTime = time.time()
        if self.tempTime - start > number:
            self.tempTime = 0
            return True
        else:
            return False




class Fighter(): #Refers to the fighters that the player will control
    def __init__(self, x,y):
        self.health = 100
        self.flip = False # For the x coordinate of attacking rect
        self.rect = pygame.Rect((x,y,96,192))
        self.vel_y = 0 #will be used for physics calculations
        self.jumping = False
        self.jumpTimer = Timer() # This is extremely botched and I know it is, I can only apologize for the grievous sins I'm committing.

        self.attackTimer = Timer()
        self.attackCount = 0
        self.attackType = 0
        self.attacking = False
      

        self.gravity = GRAVITY

        self.stun = False
     
    def drawHealthBar(self, health, screen, x, y):
        ratio = health  / 100
        pygame.draw.rect(screen, RED, (x-2, y-2, 405, 35))
        pygame.draw.rect(screen, DARK_GREEN, (x-2, y-2, 405*ratio, 35))
        pygame.draw.rect(screen, DARK_RED, (x, y, 400, 30))
        pygame.draw.rect(screen, GREEN, (x,y, 400 * ratio, 30))

    def move(self, screen, target):
        dx = 0
        dy = 0

        #get keypresses
        key = pygame.key.get_pressed()

        if self.attacking == False:

        #check for key to be pressed
            if key[pygame.K_a]:
                dx = -SPEED
                self.flip = True
            if key[pygame.K_d]:
                dx = SPEED
                self.flip = False

        #jumping
            if key[pygame.K_w] and not self.jumping: 
                self.gravity = GRAVITY
                self.vel_y = -40
                self.jumping = True
                self.jumpTimer.startTimer()


        #Attacks 1 - 4: Ground Attacks, 5: Jump Attack, 6: Parry
            if key[pygame.K_r] or key[pygame.K_t]: 
                if key[pygame.K_r] and self.vel_y != 0: #jumping attack
                    self.attackType = 5
                    self.attack(screen, target)
                
                elif key[pygame.K_t]:
                    self.attackType = 6
                    self.attack(screen, target)
                    
                elif key[pygame.K_r]:
                    
                    if self.attackCount == 0: #for the main bread and butter combo
                        if self.attackTimer.executeTimer(self.attackTimer.time,1):
                            self.attackCount += 1
                            self.attackType = 1
                            self.attack(screen, target)
                        else:
                            self.attackTimer.startTimer()


                    elif self.attackCount == 1:
                        if self.attackTimer.executeTimer(self.attackTimer.time,1):
                            self.attackCount += 1
                            self.attackType = 2
                            self.attack(screen, target)
                        else:
                            self.attackTimer.startTimer()

                    elif self.attackCount == 2:
                        if self.attackTimer.executeTimer(self.attackTimer.time,1):
                            self.attackCount += 1
                            self.attackType = 3
                            self.attack(screen, target)
                        else:
                            self.attackTimer.startTimer()

                    elif self.attackCount == 3:
                        if self.attackTimer.executeTimer(self.attackTimer.time,1):
                            self.attackCount = 0
                            self.attackType = 4
                            self.attack(screen, target)
                        else:
                            self.attackTimer.startTimer()
                

        
        #apply gravity
        self.vel_y += self.gravity
        dy += self.vel_y

        #for dashing
        if key[pygame.K_LSHIFT] and key[pygame.K_d]:
            dx += SPRINT
            self.attackCount = 0
        if key[pygame.K_LSHIFT] and key[pygame.K_a]:
            dx -= SPRINT
            self.attackCount = 0
            
        
        #ensure player remains on the screen
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left #insures that left side touches edge
        if self.rect.right + dx > WIN_WIDTH:
            dx = WIN_WIDTH - self.rect.right
        if self.rect.bottom + dy > WIN_HEIGHT - 126: #include the ground
            self.vel_y = 0
            dy = WIN_HEIGHT - 126 - self.rect.bottom
            self.gravity = GRAVITY
            self.push = 0
            
            if self.jumpTimer.executeTimer(self.jumpTimer.time,1) and self.jumping == True: #checks if the last time you pressed W is more than 1 seconds before you can jump again
                self.jumping = False

        #updates player position
        self.rect.x += dx
        self.rect.y += dy


    def draw(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.rect)
    

    def attack(self,screen, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height-100)
        pygame.draw.rect(screen, (0,0,255), attacking_rect)
        if attacking_rect.colliderect(target.rect): #checks if collision between rect
            target.health -= 10