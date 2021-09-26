import pygame
import json
import random
from pygame.locals import *

screen_width = 800
screen_height = 600

pygame.init()

score = random.randint(1,1000)

screen = pygame.display.set_mode((screen_width, screen_height))

running = True

black = (0,0,0)

hide = pygame.Surface((50, 50))
hide.fill((0, 255, 0)) #RGBA sequence
hide_centre = (0,0)
hide_rect = hide.get_rect()

arrow = pygame.image.load("arrow.png").convert()
arrow = pygame.transform.smoothscale(arrow, (60, 80))
arrow = pygame.transform.rotate(arrow, 90)
arrow.set_colorkey(black)

surf1_font = pygame.font.Font('Retro Gaming.ttf', 32)
text1 = surf1_font.render('Play', True, (0,255,0))
textRect1 = text1.get_rect()
textRect1.center = (400,25)
textRect1_y = textRect1.y

surf2_font = pygame.font.Font('Retro Gaming.ttf', 32)
text2 = surf2_font.render('Retry', True, (0,255,0))
textRect2 = text2.get_rect()
textRect2.center = (400,175)
textRect2_y = textRect2.y

surf3_font = pygame.font.Font('Retro Gaming.ttf', 32)
text3 = surf3_font.render('Exit', True, (0,255,0))
textRect3 = text3.get_rect()
textRect3.center = (400,325)
textRect3_y = textRect3.y

surf4 = pygame.Surface((50,50))
surf4.fill((0,0,0))
surf4_centre = (0,0)
surf4_rect = surf4.get_rect()
x = 550
y = 450
wheatx = 10
wheaty = 0
arrow_surf = arrow.copy()
arrow_rect = (x,y)

text = ''

class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super(Arrow, self).__init__()
        self.surf = arrow_surf.copy()
        self.rect = self.surf.get_rect()  
    # Move the sprite based on user keypresses
    
    def update(self, pressed_keys):
        global wheaty
        if wheaty + 5 < textRect1_y:
            wheaty = textRect1_y - 5
        if wheaty + 5 > textRect3_y:
            wheaty = textRect3_y - 5
    
    def select(self):
        global surf1_centre, surf2_centre, surf3_centre, wheaty
        if wheaty+5 == textRect1_y:
            print('Play')
        elif wheaty+5 == textRect2_y:
            print('retry')
        elif wheaty+5 == textRect3_y:
            print('exit')

arrow = Arrow()

while running:  
    # look at every event in the queue
    for event in pygame.event.get():
        # did the user press a key?
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                wheaty +=150
            elif event.key == K_UP:
                wheaty -= 150
            elif event.key == K_RETURN:
                arrow.select()
            # was it the escape key?
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(text)
                with open('Highscores.json') as f:
                    f
                text = ''
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode

    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    arrow.update(pressed_keys)
    # sets background to white
    screen.fill((255,255,255))

    txt_surface = surf1_font.render(text, True, (0,255,0))
    # Resize the box if the text is too long.
    width = max(200, txt_surface.get_width()+10)
    surf4_rect.w = width
    surf4_rect.y = y
    # Blit the text.
    screen.blit(txt_surface, (surf4_rect.x+5, surf4_rect.y+5))
    # Blit the input_box rect.
    pygame.draw.rect(screen, (0,255,0), surf4_rect, 1)


    # makes a square thats 50 pixels wide and 50 pixels tall    

    # jet_alive = pygame.image.load("jet.png").convert()
    # jet_alive = pygame.transform.smoothscale(jet_alive, (30, 23))
    # jet_alive = pygame.transform.rotate(jet_alive, 270)
    # jet_alive.set_colorkey((0, 0, 0), RLEACCEL)

    # life1 = jet_alive.copy()
    # life1rect = (150,100)  
    # 

    # life2 = jet_alive.copy()
    # life2rect = (200,100)  
    # screen.blit(life2, life2rect)

    # life3 = jet_alive.copy()
    # life3rect = (250,100)  
    # screen.blit(life3, life3rect)

    # life4 = jet_dead.copy()
    # life4rect = (300,100)  
    # screen.blit(life4, life4rect)

    # life5 = jet_dead.copy()
    # life5rect = (350,100)  
    # screen.blit(life5, life5rect)

    # pygame.display.set_caption('Show Text')
    # font = pygame.font.Font('Retro Gaming.ttf', 32)
    # text = font.render('Lives: 1', True, (0,255,0), (0,0,255))
    # textRect = text.get_rect()
    # set the center of the rectangular object.
    # textRect.center = (screen_width // 2, screen_height // 2)
    #making the block called surf black in colour 

    # puts the square called surf in the middle of the screen 
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    # screen.blit(surf4, surf4_centre)
    screen.blit(arrow_surf, (wheatx, wheaty))
    # screen.blit(text, textRect)
    pygame.display.flip()