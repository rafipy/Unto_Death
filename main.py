import pygame
import pygame_textinput
from sprites import* 
from config import*
from objects import*

#creating a class for game so everything looks cleaner
#its very possible for me to not use one but I saw a youtube video like this and I enjoyed what they did
#note for self ALWAYS CD FINALPROJECT WHEN RESTARTING TERMINAL


class Game:
    def __init__(self):
        pygame.init()
        #creating the screen here, most of the settings will be controlled in config
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.state = "menu"
        self.clock = pygame.time.Clock() # This will be for FPS.
        self.FPS = 60
        

        pygame.display.set_caption("Unto Death")
        self.fontH1 = pygame.font.Font("font\SuperPixel-m2L8j.ttf", 64)
        self.fontp= pygame.font.Font("font\SuperPixel-m2L8j.ttf", 16)
        self.running = True 
    
    def drawText(self, text, font, color, x, y): #Function to show text on the screen on a given coordinate.
        img = font.render(text, True, color) #second is anti aliasing
        self.screen.blit(img, (x,y)) #displays the font on x,y
    
    
    def mainMenu(self):
        self.screen.fill((50,25,25))
        
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

        self.clock.tick(self.FPS)

        self.screen.blit(BG, (0, 0))
        fighter_1.drawHealthBar(fighter_1.health, self.screen, 20, 20)
        fighter_2.drawHealthBar(fighter_2.health, self.screen, WIN_WIDTH - 400 - 20, 20)

        #establish control
        fighter_1.move(self.screen, fighter_2)
        fighter_2.move(self.screen, fighter_1)
        
        fighter_1.update()
        fighter_2.update()
        
        fighter_1.draw(self.screen)
        fighter_2.draw(self.screen)

        pygame.display.update()
    
    def connectLAN(self):
        
        # But more customization possible: Pass your own font object
        font = pygame.font.SysFont("Consolas", 55)
        
        # Create own manager with custom input validator
        manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) == )
        
        # Pass these to constructor
        textinput = pygame_textinput.TextInputVisualizer(manager=manager, font_object=font)
        
        # Customize much more
  
        textinput.cursor_blink_interval = 400 # blinking interval in ms
        textinput.antialias = False
        textinput.font_color = WHITE
        pygame.key.set_repeat(200, 25)
        
        
        while True:
            self.screen.fill((50,50, 100))
            
            self.drawText("Enter Server IP!", self.fontH1, WHITE, (WIN_WIDTH//2) - 360, WIN_HEIGHT//2 - 250)
            
            events = pygame.event.get() #Gets keys yuh
            
            textinput.update(events)
     
        
            screen.blit(textinput.surface, ((WIN_WIDTH//2) - 150,  WIN_HEIGHT//2 ))
        
            
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    print(f"User pressed enter! Input so far: {textinput.value}")
                    
            pygame.display.update()
        
        
    
    
       


game = Game()


while game.running:
    for event in pygame.event.get(): #checks through all the events in pygame and breaks the loop if QUIT is pressed
        if event.type == pygame.QUIT:
            game.running=False
    
    if game.state == "menu":
        game.mainMenu()
    elif game.state == "local":
        game.localBattle()
    elif game.state == "lan":
        game.connectLAN()
    

pygame.quit()