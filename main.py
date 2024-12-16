import pygame
from pygame import mixer
import pygame_textinput
from sprites import* 
from config import*
from objects import*
from deprecated.network import Network

clientNumber = 0

#creating a class for game so everything looks cleaner
#its very possible for me to not use one but I saw a youtube video like this and I enjoyed what they did
#note for self ALWAYS CD FINALPROJECT WHEN RESTARTING TERMINAL


class Game:
    def __init__(self):
        mixer.pre_init(44100, -16, 6, 2048)
        mixer.init()
        pygame.init()

        #creating the screen here, most of the settings will be controlled in config
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.state = "menu"
        self.clock = pygame.time.Clock() # This will be for FPS.
        self.FPS = 60
        
        self.introCount = 3
        self.lastCountUpdate = pygame.time.get_ticks()
        self.score = [0, 0]
        self.roundOver = False
        self.roundOverCD = 2000
        self.roundOverTime = 0

        self.fighter_1 = Fighter(200, 431, False, FIGHTER1_DATA, FIGHTER1_SHEET, FIGHTER_ANIMS, 1, SFX)
        self.fighter_2 = Fighter(1000, 431, True, FIGHTER2_DATA, FIGHTER2_SHEET, FIGHTER_ANIMS, 2, SFX)

        pygame.display.set_caption("Unto Death")
        self.fontH1 = pygame.font.Font("font\SuperPixel-m2L8j.ttf", 64)
        self.fontp= pygame.font.Font("font\SuperPixel-m2L8j.ttf", 16)
        self.gameFont = pygame.font.Font("font\PixelifySans-Bold.ttf", 25)
        self.roundFont = pygame.font.Font("font\PixelifySans-Bold.ttf", 128)
        self.running = True 

    
    def drawText(self, text, font, color, x, y): #Function to show text on the screen on a given coordinate.
        img = font.render(text, True, color) #second is anti aliasing
        self.screen.blit(img, (x,y)) #displays the font on x,y

    def reset(self):
        self.fighter_1 = Fighter(200, 431, False, FIGHTER1_DATA, FIGHTER1_SHEET, FIGHTER_ANIMS, 1, SFX)
        self.fighter_2 = Fighter(1000, 431, True, FIGHTER2_DATA, FIGHTER2_SHEET, FIGHTER_ANIMS, 2, SFX)
    
    
    def mainMenu(self):
        self.screen.fill((50,25,25))
        MENU_MUSIC.play()

        self.drawText("Unto Death", self.fontH1, WHITE, (WIN_WIDTH//2) - 250, WIN_HEIGHT//2 - 250)
        self.drawText("An Indie Game by Rafie Mustika Ramasna", self.fontp, WHITE, (WIN_WIDTH//2) - 225, WIN_HEIGHT//2 - 150)
        
        START.draw(self.screen)
        MULTI.draw(self.screen)
 
        pygame.display.update()

        if START.clickCheck(self.screen) == True:

            self.state = "local"

        if MULTI.clickCheck(self.screen) == True:
            self.state = "lan"
       

    def localBattle(self):
        MENU_MUSIC.stop()

        channel2 = pygame.mixer.Channel(1)
        channel2.set_volume(50)
        channel2.queue(BATTLE_MUSIC)
       
        

        self.clock.tick(self.FPS)
        self.screen.blit(BG, (0, 0))
        self.fighter_1.update()
        self.fighter_2.update()
        self.fighter_1.draw(self.screen)
        self.fighter_2.draw(self.screen)

    
        
        if self.introCount <= 0:
            if self.roundOver == False:
                self.fighter_1.move(self.fighter_2)
                self.fighter_2.move(self.fighter_1)
            
        else:
            self.drawText(str(self.introCount),self.roundFont, WHITE, WIN_WIDTH//2 - 30, WIN_HEIGHT//2 - 200)
            if (pygame.time.get_ticks() - self.lastCountUpdate) >= 1000:
                self.introCount -= 1
                self.lastCountUpdate = pygame.time.get_ticks() #updates the timer to check if the time has passed 1000ms

        self.fighter_1.drawHealthBar(self.fighter_1.health, self.screen, 20, 20)
        self.fighter_2.drawHealthBar(self.fighter_2.health, self.screen, WIN_WIDTH - 400 - 20, 20)
        self.drawText("P1: " + str(self.score[0]), self.gameFont, WHITE, 20, 60)
        self.drawText("P2: " + str(self.score[1]),self.gameFont, WHITE, WIN_WIDTH - 400 - 20, 60)
        
        if self.score[0] == 3:
            self.roundOverTime = pygame.time.get_ticks()
            self.drawText("PLAYER ONE WINS", self.fontH1, WHITE, (WIN_WIDTH//2) - 400, WIN_HEIGHT//2 - 250)
            if pygame.time.get_ticks() - self.roundOverTime > self.roundOverCD:
                self.roundOver = False
                self.introCount = 3
                self.score[0] = 0
                self.score[1] = 0
                self.reset()
            
      
        elif self.score[1] == 3:
            self.roundOverTime = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.roundOverTime > self.roundOverCD:
                self.drawText("PLAYER TWO WINS", self.fontH1, WHITE, (WIN_WIDTH//2) - 400, WIN_HEIGHT//2 - 250)
                self.roundOver = False
                self.introCount = 3
                self.score[0] = 0
                self.score[1] = 0
                self.reset()
            
        else:
            if self.roundOver == False:
                if self.fighter_1.alive == 0:
                    self.score[1] += 1
                    self.roundOver = True
                    self.roundOverTime = pygame.time.get_ticks()
                elif self.fighter_2.alive == 0:
                    self.score[0] += 1
                    self.roundOver = True
                    self.roundOverTime = pygame.time.get_ticks()
            else:
                self.drawText("ROUND END", self.fontH1, WHITE, (WIN_WIDTH//2) - 252, WIN_HEIGHT//2 - 250)
                
                if pygame.time.get_ticks() - self.roundOverTime > self.roundOverCD:
                    self.roundOver = False
                    self.introCount = 3
                    #resetting position
                    self.reset()


        pygame.display.update()

    # def LANBattle(self):
    #     run = True
    #     n = Network()
    #     p = n.getP()


    #     while run:
    #         self.clock.tick(self.FPS)
    #         p2 = n.send(p)
    #         self.screen.blit(BG, (0, 0))

    #         p.move(p2)

    #         pygame.display.update()
    
    # def connectLAN(self):
    #     n = Network()
    #     while True:
    #         check = n.wait()

    #         print(check[0])

game = Game()


while game.running:
    for event in pygame.event.get(): #checks through all the events in pygame and breaks the loop if QUIT is pressed
        if event.type == pygame.QUIT:
            game.running=False
    
    if game.state == "menu":
        game.mainMenu()
    elif game.state == "local":
        game.localBattle()

    

pygame.quit()