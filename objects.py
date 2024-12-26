#module that consists of every menu and game object that will be used

import pygame
from config import*
import time


class Button: #Buttons will just be images
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

class Timer: #Object for creating timers and cooldowns in attacks
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


class Fighter:
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps, player, soundData):
        self.flip = flip  # For the x coordinate of attacking rect

        self.vel_y = 0  # will be used for physics calculations
        self.jumping = False
        self.running = False
        self.rolling = False
        self.hit = False
        self.alive = True

        self.speed = SPEED
        self.gravity = GRAVITY

        self.rect = pygame.Rect(x, y, 80, 120)
        self.parry = pygame.Rect(0, 0, 0, 0)

        self.stunTime = 0
        self.jumpTime = 0
        self.attackTime = 0
        self.rollTime = 0

        self.attacking = False

        self.size = data[0]
        self.scale = data[1]
        self.offset = data[2]


        self.action = 6
        self.frameIndex = 0
        self.animationList = self.animationCreate(sprite_sheet, animation_steps)
        self.image = self.animationList[self.action][self.frameIndex]

        self.health = 100
        self.stun = False

        self.player = player  # checks which player they are

 
        self.attackSFX = soundData[0]
        self.parrySFX = soundData[1]
        self.deathSFX = soundData[2]
        self.rollSFX = soundData[3]
        self.jumpSFX = soundData[4]

        
        

    def animationCreate(self, sprite_sheet, animation_steps):
        # extract images from sprite sheet
        animation_list = []  # The actual list containing all the elements
        for y, animation in enumerate(
                animation_steps):  # This function same as adding y each time animation steps goes on but cooler, this for loop is just for extracting.
            tempImgList = []

            for x in range(animation):
                tempImg = sprite_sheet.subsurface(x * self.size[1], y * self.size[0], self.size[1],
                                                  self.size[0])  # take a part of the image
                tempImgList.append(
                    pygame.transform.scale(tempImg, (self.size[1] * self.scale, self.size[0] * self.scale)))

            animation_list.append(tempImgList)

        return animation_list

    def drawHealthBar(self, health, screen, x, y):
        ratio = health / 100
        pygame.draw.rect(screen, RED, (x - 2, y - 2, 405, 35))
        pygame.draw.rect(screen, DARK_GREEN, (x - 2, y - 2, 405 * ratio, 35))
        pygame.draw.rect(screen, DARK_RED, (x, y, 400, 30))
        pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip,
                                    False)  # flip horizontal if self flip 1 then it will be true.

        screen.blit(img, (
            self.rect.x - (self.offset[self.flip][0] * self.scale),
            self.rect.y - (self.offset[self.flip][1] * self.scale)))

    def update(self):  # updates sprite
        # check action before running
        animationCooldown = 50

        if self.health <= 0:
            self.deathSFX.play()
            self.health = 0
            self.alive = False
            self.updateAction(3)
            

        elif self.hit == True:
            animationCooldown = 150
            self.updateAction(4)

        elif self.stun == True:
            animationCooldown = 200
            self.updateAction(4)
            self.stunTime = pygame.time.get_ticks()



        elif self.attacking == True:
            animationCooldown = 150

            if self.attack_type == 1:
                self.updateAction(0)

            elif self.attack_type == 2:

                self.updateAction(1)


        elif self.jumping == True:
            animationCooldown = 100
            self.updateAction(6)

        elif self.rolling == True:
            self.updateAction(7)

        elif self.running == True:

            self.updateAction(8)

        else:
            self.updateAction(5)

        self.image = self.animationList[self.action][self.frameIndex]

        if pygame.time.get_ticks() - self.updateTime > animationCooldown:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()
        # checks if animation has ended
        if self.frameIndex >= len(self.animationList[self.action]):

            if self.alive == False:
                self.frameIndex = len(self.animationList[self.action]) - 1

            else:

                self.frameIndex = 0

                # check if attack is executed
                if self.stun == True:
                    if pygame.time.get_ticks() - self.stunTime > 500:
                        self.stun = False
                        self.stunTime = pygame.time.get_ticks()
                

                elif self.action == 0 or self.action == 1:
                    if pygame.time.get_ticks() - self.attackTime > 70:
                        self.attacking = False
                    
                elif self.action == 7:
                    self.rolling = False
                    self.parry = pygame.Rect(0, 0, 1.5 * self.rect.width, self.rect.height)
                    


                elif self.action == 4:
                    if pygame.time.get_ticks() - self.stunTime > 500:
                        self.hit = False
                        self.attacking = False
                

    def updateAction(self, newAction):
        # checks if current action is different to previous one
        if newAction != self.action:
            self.action = newAction
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()



    def move(self,  target):
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # get key presses
        key = pygame.key.get_pressed()
        #
        if self.hit == False and self.stun == False and self.attacking == False:

            # check for key to be pressed
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -self.speed
                    self.running = True

                if key[pygame.K_d]:
                    dx = self.speed
                    self.running = True

                if key[pygame.K_q] and pygame.time.get_ticks() - self.rollTime > 3000:

                    self.roll()
                    self.rollTime = pygame.time.get_ticks()

                # jumping
                if key[pygame.K_w] and not self.jumping:
                        self.jumpSFX.play()
                        self.vel_y = -35
                        self.jumping = True
                        self.jumpTime = pygame.time.get_ticks()
                # Attacks
                if (key[pygame.K_r] or key[pygame.K_t]) and pygame.time.get_ticks() - self.attackTime > 1000:
                    self.attack(target)
                    if key[pygame.K_t]:
                        self.attack_type = 2
                        self.attackTime = pygame.time.get_ticks()
                    elif key[pygame.K_r]:
                        self.attack_type = 1
                        self.attackTime = pygame.time.get_ticks()
                # for dashing
                if key[pygame.K_LSHIFT] and key[pygame.K_d]:
                    dx += SPRINT
                    self.attackCount = 0
                    self.dashing = True
                if key[pygame.K_LSHIFT] and key[pygame.K_a]:
                    dx -= SPRINT
                    self.attackCount = 0
                    self.dashing = True
           

            elif self.player == 2:
                if self.hit == False:
                    if key[pygame.K_LEFT]:
                        dx = -self.speed
                        self.running = True

                    if key[pygame.K_RIGHT]:
                        dx = self.speed
                        self.running = True

                    if key[pygame.K_QUOTE] and pygame.time.get_ticks() - self.rollTime > 3000:
                        self.roll()
                        self.rollTime = pygame.time.get_ticks()

                    # jumping
                    if key[pygame.K_UP] and not self.jumping:
                        self.jumpSFX.play()
                        self.vel_y = -35
                        self.jumping = True
                        self.jumpTime = pygame.time.get_ticks()
                        

                    # Attacks
                    if (key[pygame.K_SLASH] or key[pygame.K_PERIOD]) and  pygame.time.get_ticks() - self.attackTime > 1000:
                        self.attack(target)
                        if key[pygame.K_SLASH]:
                            self.attack_type = 2
                            self.attackTime = pygame.time.get_ticks()
                        elif key[pygame.K_PERIOD]:
                            self.attack_type = 1
                            self.attackTime = pygame.time.get_ticks()

                    # for dashing
                    if key[pygame.K_RSHIFT] and key[pygame.K_RIGHT]:
                        dx += SPRINT
                        self.attackCount = 0
                        self.dashing = True

                    if key[pygame.K_RSHIFT] and key[pygame.K_LEFT]:
                        dx -= SPRINT
                        self.attackCount = 0
                        self.dashing = True

            # apply gravity
            self.vel_y += GRAVITY
            dy += self.vel_y

            # ensure player remains on the screen
            if self.rect.left + dx < 0:
                dx = 0 - self.rect.left  # insures that left side touches edge
            if self.rect.right + dx > WIN_WIDTH:
                dx = WIN_WIDTH - self.rect.right
            if self.rect.bottom + dy > WIN_HEIGHT - 126:  # include the ground
                self.vel_y = 0
                dy = WIN_HEIGHT - 126 - self.rect.bottom
                self.jumping = False
                self.jumpTime = pygame.time.get_ticks()

            # ensure players are facing one another
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            # updates player position
            self.rect.x += dx
            self.rect.y += dy

    def roll(self):
  
        self.rolling = True
        pygame.mixer.find_channel().play(self.rollSFX) #we do this instead of the usual because better sound quality from a channel and auto makes it so you can run several things at once!
        self.parry = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                1.5 * self.rect.width, self.rect.height)

    def attack(self, target):
        self.attacking = True
        pygame.mixer.find_channel().play(self.attackSFX)
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                     2 * self.rect.width,
                                     self.rect.height)  # self.flip will make the box behind by moving x axis
        


        if attacking_rect.colliderect(target.rect):  # checks if collision between rect
            target.health -= 10
            target.hit = True
            target.stunTime = pygame.time.get_ticks()

        if attacking_rect.colliderect(target.parry):
            self.stun = True
            pygame.mixer.find_channel().play(self.parrySFX)
            print("Stunned!")

                
          
