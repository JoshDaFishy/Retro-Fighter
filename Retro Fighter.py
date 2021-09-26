import random
import pygame
import time
import json
import operator
from pygame.constants import K_SPACE
from pygame.locals import *
from pygame.math import Vector2

screen_width = 800
screen_height = 600

pygame.init()
pygame.mixer.init()

enemy_Timer = 2500

screen = pygame.display.set_mode((screen_width, screen_height))

spawn_time = random.randint(100000,120000)

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, enemy_Timer)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 5000)

PowerUpSpawn = pygame.USEREVENT + 3
pygame.time.set_timer(PowerUpSpawn, spawn_time)

ShotCooldown = pygame.USEREVENT + 4
pygame.time.set_timer(ShotCooldown, 10)

shot_cooldown_time = 500
score_gap = 10000
bind = ''     

shot_delay = False
start_menu_active = True
scores_menu_active = False
retry_menu_active_highscore = False
retry_menu_active = False
added = False
invincible = False
border = True
settings_menu = False
active = False
Arrow_moved = False
running = False
gameStarted = False
shotEnded = True

with open('assets/data/Highscores.json','r') as f:
    Scores = json.load(f)

with open('assets/data/keybinds.json','r') as f:
    Keybinds = json.load(f)
    bindup = Keybinds["bindup"]
    binddown = Keybinds["binddown"]
    bindleft = Keybinds["bindleft"]
    bindright = Keybinds["bindright"]
    bindfire = Keybinds["bindfire"]

logo_font = pygame.font.Font('assets/fonts/AerologicaRegular.ttf', 110)
font64 = pygame.font.Font('assets/fonts/Retro Gaming.ttf', 64)
font48 = pygame.font.Font('assets/fonts/Retro Gaming.ttf', 48)
font32 = pygame.font.Font('assets/fonts/Retro Gaming.ttf', 32)
font25 = pygame.font.Font('assets/fonts/Retro Gaming.ttf', 25)

missile_sound = pygame.mixer.Sound("assets/sfx/Missilesfx.ogg")
plane_explode_sound = pygame.mixer.Sound("assets/sfx/planeexplode.ogg")
explode_sound = pygame.mixer.Sound("assets/sfx/ExplodeSFX.ogg")

player_surf = pygame.image.load("assets/images/jet.png").convert()
weapon_surf = pygame.image.load("assets/images/missile.png").convert_alpha()
Enemy1weapon_surf = pygame.image.load("assets/images/blueRocketSprite.png")
Enemy1weapon_surf = pygame.transform.rotate(Enemy1weapon_surf, 90)
Enemy2weapon_surf = pygame.image.load("assets/images/Enemy2MissileSprite.png").convert_alpha()
AutoFire = pygame.image.load("assets/images/Mushroom.png").convert()
explode1 = pygame.image.load("assets/images/explode1.png").convert_alpha()
explode2 = pygame.image.load("assets/images/explode2.png").convert_alpha()
jet_alive = pygame.image.load("assets/images/jet.png").convert()
jet_dead = pygame.image.load("assets/images/jet_nolife.png").convert()
arrow = pygame.image.load("assets/images/arrow.png").convert()
enemy1_surf = pygame.image.load("assets/images/helicopter.png").convert()
enemy2_surf = pygame.image.load("assets/images/helicopter2.png").convert()
enemy3_surf = pygame.image.load("assets/images/sheepboss.png").convert()
boss_surf = pygame.image.load("assets/images/BossSprite.png").convert_alpha()
enemy3withWeapon_surf = pygame.image.load("assets/images/armedSheepBoss.png").convert()
cloud_surf = pygame.image.load("assets/images/cloud.png").convert()
laserChargePt1_surf = pygame.image.load("assets/images/SheepCannonCharge1.png").convert()
laserChargePt2_surf = pygame.image.load("assets/images/SheepCannonCharge2.png").convert()
laserChargePt3_surf = pygame.image.load("assets/images/SheepCannonCharge3.png").convert()
laserChargePt4_surf = pygame.image.load("assets/images/SheepCannonCharge4.png").convert()
laseFirePt1_surf = pygame.image.load("assets/images/SheepCannonFire1.png").convert()
laseFirePt2_surf = pygame.image.load("assets/images/SheepCannonFire2.png").convert()
laseFirePt3_surf = pygame.image.load("assets/images/SheepCannonFire3.png").convert()
laseFirePt4_surf = pygame.image.load("assets/images/SheepCannonFire4.png").convert()
up1_surf = pygame.image.load("assets/images/1upMushroom.png").convert_alpha()

def sort_scores(Scores):
    return {k: v for k, v in sorted(Scores.items(), key=operator.itemgetter(1), reverse=True)[:10]}


Scores = sort_scores(Scores)

black = (0,0,0)
white = (255,255,255)

changesurf = pygame.Surface((800, 600))
changesurf.fill((0,0,0))
changesurfrect = changesurf.get_rect()  

power = 1

change = font48.render('Press your chosen key', True, (0,255,0))
changeRect = change.get_rect()
changeRect.center = (400,200)
changeRect_y = changeRect.y

text1 = font48.render('Play', True, (0,255,0))
textRect1 = text1.get_rect()
textRect1.center = (400,200)
textRect1_y = textRect1.y

logo = logo_font.render('RETRO FIGHTER', True, (0,255,0))
logo_rect = logo.get_rect()
logo_rect.center = (400,50)
logo_rect_y = logo_rect.y

text2 = font48.render('Scores', True, (0,255,0))
textRect2 = text2.get_rect()
textRect2.center = (400,400)
textRect2_y = textRect2.y

enterText = font32.render('Submit Name', True, (0,255,0))
enterTextRect = enterText.get_rect()
enterTextRect.center = (400,250)
enterTextRect_y = enterTextRect.y

highscoreText = font32.render('New highscore! Please enter your name', True, (0,255,0))
highscoreTextRect = highscoreText.get_rect()
highscoreTextRect.center = (400,100)
highscoreTextRect_y = highscoreTextRect.y

settingsText = font48.render('Settings', True, (0,255,0))
settingsTextRect = settingsText.get_rect()
settingsTextRect.center = (400,300)
settingsTextRect_y = settingsTextRect.y

text3 = font48.render('Exit', True, (0,255,0))
textRect3 = text3.get_rect()
textRect3.center = (400,550)
textRect3_y = textRect3.y

backText = font32.render('back', True, (0,255,0))
backRect = backText.get_rect()

Retry = font64.render('Retry', True, (0,255,0))
Retry_rect = Retry.get_rect()
Retry_rect.center = (400,325)
Retry_rect_y = Retry_rect.y


rebindupText = font25.render('Change "Move Up" key?', True, (0,255,0))
rebindupTextRect = rebindupText.get_rect()
rebindupTextRect.center = (400,25)
rebindupTextRect_y = 25

rebinddownText = font25.render('Change "Move Down" key?', True, (0,255,0))
rebinddownTextRect = rebinddownText.get_rect()
rebinddownTextRect.center = (400,120)
rebinddownTextRect_y = 120

rebindleftText = font25.render('Change "Move Left" key?', True, (0,255,0))
rebindleftTextRect = rebindleftText.get_rect()
rebindleftTextRect.center = (400,220)
rebindleftTextRect_y = 220

rebindrightText = font25.render('Change "Move Right" key?', True, (0,255,0))
rebindrightTextRect = rebindrightText.get_rect()
rebindrightTextRect.center = (400,320)
rebindrightTextRect_y = 320

rebindfireText = font25.render('Change "Fire" key?', True, (0,255,0))
rebindfireTextRect = rebindfireText.get_rect()
rebindfireTextRect.center = (400,420)
rebindfiretTextRect_y = 420

resetdefaultText = font25.render('Reset set key bindings to default?', True, (0,255,0))
resetdefaultTextRect = resetdefaultText.get_rect()
resetdefaultTextRect.center = (400,510)
resetdefaultTextRect_y = 510

missile_sound.set_volume(0.1)

cloud_surf = pygame.transform.smoothscale(cloud_surf, (129, 96))
cloud_surf.set_colorkey((0, 0, 0), RLEACCEL)

up1_surf = pygame.transform.smoothscale(up1_surf, (44, 47))
up1_surf.set_colorkey((0, 0, 0, ), RLEACCEL)

enemy1_surf = pygame.transform.smoothscale(enemy1_surf, (110, 90))
enemy1_surf.set_colorkey((0, 0, 0), RLEACCEL)
enemy1_surf = pygame.transform.flip(enemy1_surf, True, False)

enemy2_surf = pygame.transform.smoothscale(enemy2_surf, (73, 60))
enemy2_surf.set_colorkey((0, 0, 0), RLEACCEL)

enemy3_surf = pygame.transform.smoothscale(enemy3_surf, (110, 90))
enemy3_surf.set_colorkey((0, 0, 0), RLEACCEL)

laserChargePt1_surf = pygame.transform.smoothscale(laserChargePt1_surf, (92, 74))
laserChargePt1_surf.set_colorkey((0, 0, 0), RLEACCEL)
laserChargePt2_surf = pygame.transform.smoothscale(laserChargePt2_surf, (97, 103))
laserChargePt2_surf.set_colorkey((0, 0, 0), RLEACCEL)
laserChargePt3_surf = pygame.transform.smoothscale(laserChargePt3_surf, (96, 100))
laserChargePt3_surf.set_colorkey((0, 0, 0), RLEACCEL)

laserChargePt4_surf = pygame.transform.smoothscale(laserChargePt4_surf, (356, 186))
laserChargePt4_surf.set_colorkey((0, 0, 0), RLEACCEL)

laseFirePt1_surf = pygame.transform.smoothscale(laseFirePt1_surf, (574, 202))
laseFirePt1_surf.set_colorkey((0, 0, 0), RLEACCEL)
laseFirePt2_surf = pygame.transform.smoothscale(laseFirePt2_surf, (573, 208))
laseFirePt2_surf.set_colorkey((0, 0, 0), RLEACCEL)
laseFirePt3_surf = pygame.transform.smoothscale(laseFirePt3_surf, (573, 217))
laseFirePt3_surf.set_colorkey((0, 0, 0), RLEACCEL)
laseFirePt4_surf = pygame.transform.smoothscale(laseFirePt4_surf, (561, 211))
laseFirePt4_surf.set_colorkey((0, 0, 0), RLEACCEL)



Enemy1weapon_surf = pygame.transform.smoothscale(Enemy1weapon_surf, (43, 28))
Enemy1weapon_surf.set_colorkey((255, 255, 255), RLEACCEL)

weapon_surf = pygame.transform.smoothscale(weapon_surf, (51, 24))
weapon_surf.set_colorkey((255, 255, 255), RLEACCEL)

boss_surf = pygame.transform.smoothscale(boss_surf, (100, 100))
boss_surf.set_colorkey((255, 0, 0), RLEACCEL)
# boss_surf.set_colorkey(boss_surf.get_at((0,0)))

player_surf = pygame.transform.smoothscale(player_surf, (79, 46))
player_surf.set_colorkey((0, 0, 0), RLEACCEL)
player_surf = pygame.transform.flip(player_surf, True, False)

AutoFire = pygame.transform.smoothscale(AutoFire, (60, 50))
AutoFire.set_colorkey(AutoFire.get_at((0,0)))

explode1 = pygame.transform.smoothscale(explode1, (38, 41))
# explode1.set_colorkey(pygame.Color(166, 0, 0))
explode1.set_colorkey(explode1.get_at((0,0)))

enemy3withWeapon_surf = pygame.transform.smoothscale(enemy3withWeapon_surf, (110, 90))
# explode1.set_colorkey(pygame.Color(166, 0, 0))
enemy3withWeapon_surf.set_colorkey(enemy3withWeapon_surf.get_at((0,0)))

explode2 = pygame.transform.smoothscale(explode2,(40,40))
# explode2.set_colorkey(pygame.Color(164, 0, 0))
explode2.set_colorkey(explode2.get_at((0,0)))

explodes = [explode1,explode2]


jet_alive = pygame.transform.smoothscale(jet_alive, (30, 23))
jet_alive = pygame.transform.rotate(jet_alive, 270)
jet_alive.set_colorkey((0, 0, 0), RLEACCEL)

jet_dead = pygame.transform.smoothscale(jet_dead, (30, 23))
jet_dead = pygame.transform.rotate(jet_dead, 270)
jet_dead.set_colorkey((0, 0, 0), RLEACCEL)


arrow = pygame.transform.smoothscale(arrow, (60, 80))
arrow = pygame.transform.rotate(arrow, 90)
arrow.set_colorkey(black)

Enemy2weapon_surf = pygame.transform.smoothscale(Enemy2weapon_surf, (43, 28))






text_field = ''
surf4 = pygame.Surface((50,50))
surf4.fill((0,0,0))
surf4_centre = (400,450)
surf4_rect = surf4.get_rect()


x = 550
y = 450
wheatx = 10
wheaty = 0
arrow_rect = (x,y)
arrow_surf = arrow.copy()


playerx = 0
playery = 0

arrow_index = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.enemyspawn_timer = 2600
        self.target_second = 30
        self.surf = player_surf.copy()
        self.rect = self.surf.get_rect()  
        self.hp = 3
        self.lives = 3
        self.score = 00000
        self.prev_score = 00000
        self.trackable_rect = self.surf.get_rect()
        self.timerStarted = False
        self.difficultyLevel = 0
        self.bossBattle = False
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        global enemy_Timer
        if gameStarted == True and self.timerStarted == False:
            self.startTimer = time.time()
            self.timerStarted = True
        self.timer_pause = time.time()
        self.current_time = self.timer_pause - self.startTimer
        if round(self.current_time) == self.target_second:
            print("Difficulty level UP")
            self.target_second += 30
            if enemy_Timer > 1500:
                enemy_Timer -= 250
                pygame.time.set_timer(ADDENEMY, enemy_Timer)
            if self.bossBattle == False:
                self.difficultyLevel += 1 
                print(f"the game is getting more difficult. difficulty level: {self.difficultyLevel} The enemy spawn timer is at {enemy_Timer}")
            if self.difficultyLevel % 3 == 0:
                new_boss = Boss()
                boss.add(new_boss)
                all_sprites.add(new_boss)
                self.difficultyLevel += 1
                self.bossBattle = True
        if pressed_keys[bindup]:
            self.rect.move_ip(0, -10)
        if pressed_keys[binddown]:
            self.rect.move_ip(0, 10)
        if pressed_keys[bindleft]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[bindright]:
            self.rect.move_ip(10, 0)  
        # Keep player on the screen
        if self.rect.left < 0 and border == True:
            self.rect.left = 0
        if self.rect.right > screen_width and border == True:
            self.rect.right = screen_width
        if self.rect.right > screen_width-200 and border == True and self.bossBattle == True:
            self.rect.right = screen_width-200
        if self.rect.top <= 0 and border == True:
            self.rect.top = 0
        if self.rect.bottom >= screen_height and border == True:
            self.rect.bottom = screen_height
        self.trackable_rect = self.surf.get_rect()
        if self.score % 10000 == 0 and self.score > 0:
            self.score = self.score + 100
            self.lives = self.lives + 1
    def explode(self):
        global prev_player_rect_x, prev_player_rect_y
        if self.hp <=0:
            new_explode = Explode(prev_player_rect_x,prev_player_rect_y,True)
            explosions.add(new_explode)
            all_sprites.add(new_explode)

player = Player()

text = font32.render(str(player.score).zfill(7), True, (255,255,255))
textRect = text.get_rect()
textRect.center = (400,23)

wing = 1

class Lives(pygame.sprite.Sprite):
    def __init__(self, Alive, x, y):
        super(Lives, self).__init__()
        self.surf = jet_alive.copy()
        self.image_choice = 2
        self.rect = (x,y)


    def swap_life(self, Switch):
        if Switch == True:
            self.surf = jet_alive.copy()
        elif Switch == False:
            self.surf = jet_dead.copy()



class Missile(pygame.sprite.Sprite):
    def __init__(self, wing):
        global invincible, playerx, playery
        super(Missile, self).__init__()
        self.surf = weapon_surf.copy()
        self.weapon_damage = 1
        missile_sound.play()
        if wing == 1:
            if invincible == False:
                self.rect = self.surf.get_rect(
                    center=(
                        player.rect.x,
                        player.rect.y 
                    )
                ) 
            elif invincible == True:
                self.rect = self.surf.get_rect(
                    center=(
                        playerx,
                        playery
                    )
                )      

        elif wing == 2:
            if invincible == False:
                self.rect = self.surf.get_rect(
                    center=(
                        player.rect.x,
                        player.rect.y+45
                    )
                ) 
            elif invincible == True:
                self.rect = self.surf.get_rect(
                    center=(
                        playerx,
                        playery+45
                    )
                )      

        self.speed = 5
    def update(self):
        self.rect.move_ip(self.speed,0)
        if self.rect.right > screen_width:
            self.kill()
        
        enemies_collided = pygame.sprite.spritecollide(self, enemy1, False)
        enemies_collided += pygame.sprite.spritecollide(self, enemy2, False)
        enemies_collided += pygame.sprite.spritecollide(self, enemy3, False)
        enemies_collided += pygame.sprite.spritecollide(self, boss, False)
        enemies_collided += pygame.sprite.spritecollide(self, enemy1shots, False)
        enemies_collided += pygame.sprite.spritecollide(self, enemy2shots, False)
        if len(enemies_collided) > 0:
            self.kill()
            missile_sound.stop()
            explode_sound.play()
            for sprite in enemies_collided:
                sprite.explode()


class Explode(pygame.sprite.Sprite):
    def __init__(self, coords_x, coords_y, plane):
        global active, playerx, playery 
        timer_start = time.time()
        super(Explode, self).__init__()
        self.surf = explode1.copy()
        self.image_choice = 2
        active = True
        self.plane_mode = False
        if plane == True:
            self.plane_mode = True
            playerx = coords_x
            playery = coords_y
            player.rect.x = 10000
            player.rect.y = 10000
            self.rect = self.surf.get_rect()
            self.rect.center=(
                (coords_x+40),
                (coords_y+40)
            )
        else:
            self.rect = self.surf.get_rect(
            center=(
                (coords_x+40),
                (coords_y+40)
            )
        ) 
        self.timer_start = time.time()
        
        self.stage = 0

    def image_change(self):
        global prev_player_rect_x, prev_player_rect_y, border, invincible, playerx, playery
        
        self.timer_pause = time.time()
        self.current_time = self.timer_pause - self.timer_start
        if self.plane_mode == False:
            if self.current_time >= 0.25 and self.stage == 0:
                self.surf = explode2.copy()
                self.stage += 1
            
            elif self.current_time >= 0.5 and self.stage == 1:
                self.surf = explode1.copy()
                self.stage += 1
            
            elif self.current_time >= 0.75 and self.stage == 2:
                self.surf = explode2.copy()
                self.stage += 1
            
            elif self.current_time >= 1.0 and self.stage == 3:
               self.kill()
               self.stage += 1
        
        if self.plane_mode == True:
            if self.current_time >= 1.0 and self.stage == 0:
                self.surf = explode2.copy()
                self.stage += 1
            elif self.current_time >=2.0 and self.stage == 1:
                self.surf = explode1.copy()
                self.stage += 1
            elif self.current_time >=3.0 and self.stage == 2:
                self.surf = explode2.copy()
                self.stage += 1
            elif self.current_time >= 4.0 and self.stage == 3:
                invincible = True
                self.rect.center = (10000,10000)
                player.rect.x = playerx
                player.rect.y = playery
                border = True
                self.stage += 1
            elif self.current_time >= 4.3 and self.stage == 4:
                border = False
                playerx = player.rect.x
                playery = player.rect.y
                player.rect.x = 10000
                player.rect.y = 10000
                self.stage += 1
            elif self.current_time >=4.6 and self.stage == 5:
                border = True
                player.rect.x = playerx + (player.rect.x - 10000)
                player.rect.y = playery + (player.rect.y - 10000)
                self.stage += 1
            elif self.current_time >=4.9 and self.stage == 6:
                border = False
                playerx = player.rect.x
                playery = player.rect.y
                player.rect.x = 10000
                player.rect.y = 10000
                self.stage += 1
            elif self.current_time >= 5.2 and self.stage == 7:
                border = True
                player.rect.x = playerx + (player.rect.x - 10000)
                player.rect.y = playery + (player.rect.y - 10000)
                self.stage += 1
            elif self.current_time >= 5.5 and self.stage == 8:
                border = False
                playerx = player.rect.x
                playery = player.rect.y
                player.rect.x = 10000
                player.rect.y = 10000
                self.stage += 1
            elif self.current_time >=5.8 and self.stage == 9:
                border = True
                player.rect.x = playerx + (player.rect.x - 10000)
                player.rect.y = playery + (player.rect.y - 10000)
                self.stage += 1
            elif self.current_time >=6.1 and self.stage == 10:
                border = False
                playerx = player.rect.x
                playery = player.rect.y
                player.rect.x = 10000
                player.rect.y = 10000
                self.stage += 1
            elif self.current_time >= 6.4 and self.stage == 11:
                border = True
                player.rect.x = playerx + (player.rect.x - 10000)
                player.rect.y = playery + (player.rect.y - 10000)
                self.stage += 1
            elif self.current_time >= 6.7 and self.stage == 12:
                border = False
                playerx = player.rect.x
                playery = player.rect.y
                player.rect.x = 10000
                player.rect.y = 10000
                self.stage += 1
            elif self.current_time >=7.0 and self.stage == 13:
                border = True
                player.rect.x = playerx + (player.rect.x - 10000)
                player.rect.y = playery + (player.rect.y - 10000)
                invincible = False
                self.kill()
                self.stage += 1
    
    def update(self):
        self.image_change()

explosions = pygame.sprite.Group()
enemy1 = pygame.sprite.Group()
enemy2 = pygame.sprite.Group()
enemy3 = pygame.sprite.Group()
boss = pygame.sprite.Group()
clouds = pygame.sprite.Group()
playershots = pygame.sprite.Group()
enemy1shots = pygame.sprite.Group()
enemy2shots = pygame.sprite.Group()
enemy3laser = pygame.sprite.Group()
powerups = pygame.sprite.Group()
bossHpBar = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

live1 = Lives(True,645,10)
live2 = Lives(True,675,10)
live3 = Lives(True,705,10)
live4 = Lives(False,735,10)
live5 = Lives(False,765,10)



class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy1, self).__init__()
        global enemy1Counter
        self.surf = enemy1_surf.copy()
        self.enemy_health = 1
        self.enemy_health += player.difficultyLevel
        if self.enemy_health > 3:
            self.enemy_health = 3
        self.enemy_damage = 1
        self.hasWeapon = False
        self.fire_second = 2
        self.angle = 0
        enemy1Counter += 1
        if enemy1Counter % 10 == 0:
            self.hasWeapon = True
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20,  screen_width + 100),
                random.randint(0,screen_height),

            )
        )
        self.speed = random.randint(2,10)
        if self.hasWeapon == True:
            self.speed = random.randint(2,3)
        self.startTimer = time.time()
    def explode(self):
        explode_sound.set_volume(0.11)
        explode_sound.play()
        new_explode = Explode(self.rect.x,self.rect.y, False)
        explosions.add(new_explode)
        all_sprites.add(new_explode)
        self.kill()
        player.score = player.score + 3000
    def update(self):
        global invincible
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()
        elif pygame.sprite.spritecollideany(player, enemy1):
            if invincible == False:
                player.hp = player.hp-self.enemy_damage
                self.kill()
            plane_explode_sound.set_volume(0.3)
            plane_explode_sound.play()

        self.timer_pause = time.time()
        self.current_time = self.timer_pause - self.startTimer
        # print(round(self.current_time))
        if round(self.current_time) == self.fire_second and self.hasWeapon == True:
            self.fire_second += 4

            for angle in range(-60, 60 + 1, 20):
                new_shot = Enemy1Missile(self.rect.x, self.rect.centery, angle)
                enemy1shots.add(new_shot)
                all_sprites.add(new_shot)
        # elif pygame.sprite.groupcollide(shots, enemy1, False, False)
    
class Enemy1Missile(pygame.sprite.Sprite):
    def __init__(self, locationX, locationY, angle):
        super(Enemy1Missile, self).__init__()
        self.surf = Enemy1weapon_surf.copy()
        self.surf = pygame.transform.rotate(self.surf, -angle)
        self.velocity = Vector2(-1, 0)
        self.velocity.rotate_ip(angle)
        self.locationX = locationX
        self.locationY = locationY
        self.weapon_damage = 1
        missile_sound.play()
        missile_sound.play()
        missile_sound.play()
        missile_sound.play()
        self.rect = self.surf.get_rect(
                center=(
                    self.locationX,
                    self.locationY
                )
            )
        self.pos = Vector2(self.rect.x, self.rect.y)
        self.speed = 5
    def update(self):
        global invincible
        self.pos += (self.speed * self.velocity)
        self.rect.x, self.rect.y = self.pos
        if self.rect.right > screen_width:
            self.kill()
        
        # player_collided = pygame.sprite.spritecollide(self, player, False)
        player_collided = self.rect.colliderect(player.rect)
        if player_collided == True and invincible == False:
            self.kill()
            missile_sound.stop()
            explode_sound.play()
            player.hp -= 1
    
    def explode(self):
        explode_sound.set_volume(0.09)
        explode_sound.play()
        self.weapon_damage = self.weapon_damage - 1
        player.score = player.score + 100
        explode_sound.set_volume(0.11)
        explode_sound.play()
        new_explode = Explode(self.rect.x-20,self.rect.y-20, False)
        explosions.add(new_explode)
        all_sprites.add(new_explode)
        self.kill()
        player.score = player.score + 350

enemy1Counter = 0
enemy2Counter = 0
enemy3Counter = 0

class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy2, self).__init__()
        global enemy2Counter
        self.hasWeapon = False
        enemy2Counter += 1
        if enemy2Counter % 3 == 0:
            self.hasWeapon = True

        self.wing = 1
        self.surf = enemy2_surf.copy()
        self.enemy_health = 2
        self.enemy_health += player.difficultyLevel
        if self.enemy_health > 4:
            self.enemy_health = 4
        self.enemy_damage = 2
        self.fire_second = 2
        self.startTimer = time.time()
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20,  screen_width + 100),
                random.randint(0,screen_height),

            )
        )
        self.speed = random.randint(2,10)
        if self.hasWeapon == True:
            self.speed = random.randint(2,3)




    def explode(self):
        explode_sound.set_volume(0.09)
        explode_sound.play()
        self.enemy_health = self.enemy_health - 1
        self.enemy_damage = self.enemy_damage - 1
        player.score = player.score + 100
        if self.enemy_health <=0:
            explode_sound.set_volume(0.11)
            explode_sound.play()
            new_explode = Explode(self.rect.x,self.rect.y, False)
            explosions.add(new_explode)
            all_sprites.add(new_explode)
            self.kill()
            player.score = player.score + 350

    def update(self):
        global invincible
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()
        elif pygame.sprite.spritecollideany(player, enemy2):
            if invincible == False:
                self.kill()
                player.hp = player.hp-self.enemy_damage
                plane_explode_sound.set_volume(0.3)
                plane_explode_sound.play()
        self.timer_pause = time.time()
        self.current_time = self.timer_pause - self.startTimer
        if round(self.current_time) == self.fire_second and self.hasWeapon == True:
            self.fire_second += 2
            new_shot = Enemy2Missile(self.wing, self.rect.x, self.rect.y)
            if self.wing == 1:
                self.wing = 2
            else:
                self.wing = 1
            enemy2shots.add(new_shot)
            all_sprites.add(new_shot)


class Enemy2Missile(pygame.sprite.Sprite):
    def __init__(self, wing, locationX, locationY):
        super(Enemy2Missile, self).__init__()
        self.surf = Enemy2weapon_surf.copy()
        self.weapon_damage = 1
        missile_sound.play()
        if wing == 1:
            self.rect = self.surf.get_rect(
                center=(
                    locationX,
                    locationY 
                )
            )    
        elif wing == 2:
            self.rect = self.surf.get_rect(
                center=(
                    locationX,
                    locationY+50
                )
            ) 
        self.speed = 5
    def update(self):
        global invincible
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right > screen_width:
            self.kill()
        
        # player_collided = pygame.sprite.spritecollide(self, player, False)
        player_collided = self.rect.colliderect(player.rect)
        if player_collided == True and invincible == False:
            self.kill()
            missile_sound.stop()
            explode_sound.play()
            player.hp -= 1
    
    def explode(self):
        explode_sound.set_volume(0.09)
        explode_sound.play()
        self.weapon_damage = self.weapon_damage - 1
        player.score = player.score + 100
        explode_sound.set_volume(0.11)
        explode_sound.play()
        new_explode = Explode(self.rect.x-20,self.rect.y-20, False)
        explosions.add(new_explode)
        all_sprites.add(new_explode)
        self.kill()
        player.score = player.score + 350
            
enemy3id = 1
class Enemy3(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy3, self).__init__()
        global enemy3Counter, enemy3id
        self.surf = enemy3_surf.copy()
        self.hasWeapon = False
        self.enemy_health = 3
        self.enemy_health += player.difficultyLevel
        self.enemy_damage = 3
        if self.enemy_health > 6:
            self.enemy_health = 6
        self.id = enemy3id
        enemy3id += 1
        enemy3Counter += 1
        if enemy3Counter % 3 == 0:
            self.hasWeapon = True
            self.surf = enemy3withWeapon_surf.copy()
            self.shotFired = False
        self.startTimer = time.time()
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20,  screen_width + 100),
                random.randint(0,screen_height),

            )
        )
        self.speed = random.randint(2,10)
        if self.hasWeapon == True:
            self.speed = 3
    
    def explode(self):
        self.enemy_health = self.enemy_health - 1
        self.enemy_damage = self.enemy_damage - 1
        explode_sound.set_volume(0.09)
        explode_sound.play()
        player.score = player.score + 100
        if self.enemy_health <=0:
            explode_sound.set_volume(0.11)
            explode_sound.play()
            new_explode = Explode(self.rect.x,self.rect.y, False)
            explosions.add(new_explode)
            all_sprites.add(new_explode)
            self.kill()
            player.score = player.score + 450

    def update(self):
        global invincible
        self.timer_pause = time.time()
        self.current_time = self.timer_pause - self.startTimer
        if round(self.current_time) == 3 and self.hasWeapon == True:
            self.speed = 0
        if round(self.current_time) == 5 and self.hasWeapon == True and self.shotFired == False:
            new_shot = Enemy3Cannon(self.rect.x, self.rect.y, self.id, False)
            enemy3laser.add(new_shot)
            all_sprites.add(new_shot)
            self.shotFired = True
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()
        elif pygame.sprite.spritecollideany(player, enemy3):
            if invincible == False:
                self.kill()
                player.hp = player.hp-self.enemy_damage
            plane_explode_sound.set_volume(0.3)
            plane_explode_sound.play()
        if  round(self.current_time) == 10 and self.hasWeapon == True:
            self.speed = -3
        if round(self.current_time) == 11.5 and self.hasWeapon == True:
            self.kill()

class Enemy3Cannon(pygame.sprite.Sprite):
    def __init__(self, locationX, locationY,enemy3id, bossMode):
        super(Enemy3Cannon, self).__init__()
        self.surf = laserChargePt1_surf.copy()   
        self.locationX = locationX
        self.locationY = locationY
        self.id = enemy3id
        self.timerStart = time.time()
        self.weapon_damage = 1
        self.stage = 0
        self.rect = self.surf.get_rect(
            center=(
                locationX-45,
                locationY+30
            )
        )
        self.speed = 0
        self.bossMode = bossMode
        self.startTime = time.time()
    def update(self):
        global enemy3
        self.Animation()
        if self.bossMode:
            pass
        else:
            for sprite in enemy3:
                if sprite.id == self.id:
                    print('sheep is still alive')
                    break
            else:
                print("I am ded")
                self.kill()
    def Animation(self):
        global invincible
        global shotEnded
        self.timer_pause = time.time()
        self.current_time = self.timer_pause - self.timerStart
        if self.current_time >= 0.00 and self.stage == 0:
            self.stage += 1
            self.rect = self.surf.get_rect(
            center=(
                self.locationX-45,
                self.locationY+45
                )
            )
            print("the gun is in stage 1 charging")
            self.surf = laserChargePt1_surf.copy()
        elif self.current_time >= 0.25 and self.stage == 1:
            self.stage += 1
            self.rect = self.surf.get_rect(
            center=(
                self.locationX-45,
                self.locationY+25
                )
            )
            print("the gun is in stage 2 charging")
            self.surf = laserChargePt2_surf.copy()  
        elif self.current_time >= 0.50 and self.stage == 2:
            self.stage += 1
            print("the gun is in stage 3 charging")
            self.surf = laserChargePt3_surf.copy()
        elif self.current_time >= 0.75 and self.stage == 3:
            self.stage += 1 
            self.rect = self.surf.get_rect(
            center=(
                self.locationX-45,
                self.locationY+45
                )
            ) 
            self.surf = laserChargePt1_surf.copy()   
        elif self.current_time >= 1.00 and self.stage == 4:
            self.stage += 1
            print("the gun is in stage 2 charging")
            self.surf = laserChargePt2_surf.copy()
        elif self.current_time >= 1.25 and self.stage == 5:
            self.stage += 1
            print("the gun is in stage 3 charging")
            self.surf = laserChargePt3_surf.copy()  
        elif self.current_time >= 1.50 and self.stage == 6:
            self.stage += 1
            self.rect = self.surf.get_rect(
                center=(
                    self.locationX,
                    self.locationY
                )
            )   
            print("the gun is in stage 1 firing")
            self.surf = laseFirePt1_surf.copy()   
            self.rect.x = 0  
        elif self.current_time >= 1.75 and self.stage == 7:
            self.stage += 1
            print("the gun is in stage 2 firing")
            self.surf = laseFirePt2_surf.copy()
        elif self.current_time >= 2 and self.stage == 8:
            self.stage += 1
            print("the gun is in stage 3 firing")
            self.surf = laseFirePt3_surf.copy()   
        elif self.current_time >= 2.25 and self.stage == 9:
            self.stage += 1
            print("the gun is in stage 4 firing")
            self.surf = laseFirePt4_surf.copy()  
        elif self.current_time >= 2.50 and self.stage == 10:
            self.stage += 1
            print("the gun is in stage 1 shooting")
            self.surf = laseFirePt1_surf.copy()
        elif self.current_time >= 2.75 and self.stage == 11:
            self.stage += 1    
            print("the gun is in stage 2 shooting")  
            self.surf = laseFirePt2_surf.copy()     
        elif self.current_time >= 3.00 and self.stage == 12:
            self.stage += 1    
            print("the gun is in stage 3 shooting") 
            self.surf = laseFirePt3_surf.copy()  
        elif self.current_time >= 3.25 and self.stage == 13:
            self.stage += 1     
            print("the gun is in stage 4 shooting") 
            self.surf = laseFirePt4_surf.copy()
        elif self.current_time >= 3.50 and self.stage == 14:
            self.stage += 1
            print("the gun is in stage 1 shooting")
            self.surf = laseFirePt1_surf.copy()
        elif self.current_time >= 3.75 and self.stage == 15:
            self.stage += 1    
            print("the gun is in stage 2 shooting")  
            self.surf = laseFirePt2_surf.copy()     
        elif self.current_time >= 4.00 and self.stage == 16:
            self.stage += 1    
            print("the gun is in stage 3 shooting") 
            self.surf = laseFirePt3_surf.copy()  
        elif self.current_time >= 4.25 and self.stage == 17:
            self.stage += 1     
            print("the gun is in stage 4 shooting") 
            self.surf = laseFirePt4_surf.copy()  
        elif self.current_time >= 4.50 and self.stage == 18:
            self.kill()
            shotEnded = False  
        if self.stage >= 8:
            player_collided = self.rect.colliderect(player.rect)
            if player_collided == True and invincible == False:
                explode_sound.play()
                player.hp -= 3  
         

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        print("the boss has spawned")
        self.total_Health = 7
        self.total_Health += player.difficultyLevel + 1
        self.enemy_health = 7
        self.enemy_health += player.difficultyLevel + 1
        new_bar = BossHealthBar(self.total_Health, self)
        bossHpBar.add(new_bar)
        self.surf = boss_surf.copy()
        self.enemy_damage = 3
        self.attackMode = 1
        self.speed = 3
        self.speedX = 0
        self.speedY = 3
        self.wing = 1
        self.shotsFired = 0
        self.targetSecond = 6
        self.targetSecond2 = 6
        self.startAttack = False
        self.fire_second = 2
        self.shootmode2Bool = False
        self.startTimer = time.time()
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20,  screen_width + 100),
                random.randint(0,screen_height),

            )
        )

    def explode(self):
        global bossHpBar
        self.enemy_health = self.enemy_health - 1
        self.enemy_damage = self.enemy_damage - 1
        explode_sound.set_volume(0.09)
        explode_sound.play()
        player.score = player.score + 100
        if self.enemy_health <=0:
            explode_sound.set_volume(0.11)
            explode_sound.play()
            new_explode = Explode(self.rect.x,self.rect.y, False)
            explosions.add(new_explode)
            all_sprites.add(new_explode)
            self.kill()
            for sprite in bossHpBar:
                sprite.kill()
            player.bossBattle = False
            player.score = player.score + 450

    def update(self):
        global invincible, bossBar_centre, bossHpBar
        player_collided = self.rect.colliderect(player.rect)
        if player_collided:
            self.enemy_health -= player.hp
            missile_sound.stop()
            explode_sound.play()
            player.hp -= 3
        self.timer_pause = time.time()
        self.current_time = self.timer_pause - self.startTimer
        # print(f"time is{round(self.current_time)}. Target second is {self.fire_second}")
        if self.current_time >= self.fire_second:
            if self.shootmode2Bool == False:
                self.fire_second += 1.5
                # print("the timer is set to 1.5")
            else:
                self.fire_second += 0.5
                # print("the timer is set to 0.5")
            new_shot = Enemy2Missile(self.wing, self.rect.x, self.rect.y)
            # print("I am shooting a missile")
            if self.wing == 1:
                self.wing = 2
            else:
                self.wing = 1
            enemy2shots.add(new_shot)
            all_sprites.add(new_shot)
        if self.startAttack:
            self.attack()
        if round(self.current_time) < 3:
            self.rect.move_ip(-self.speed,0)
        if round(self.current_time) > 3:
            self.speedX = 0
            self.rect.move_ip(self.speedX, self.speedY)
            if self.rect.top < 0:
                self.speedY = 3
            if self.rect.bottom > 600:
                self.speedY = -3
        # print(f"{round(self.current_time)} and the target is {self.targetSecond} the attack is {self.startAttack}")
        if self.current_time >= self.targetSecond:
            self.startAttack = True
            # self.shootmode2Bool = True
            # self.attackMode = random.randint(1,3)
            # print(self.attackMode)
        if self.rect.right < 0:
            self.kill()
            for sprite in bossHpBar:
                sprite.kill()

        elif pygame.sprite.spritecollideany(player, enemy3):
            if invincible == False:
                self.kill()
                for sprite in bossHpBar:
                    sprite.kill()
                player.hp = player.hp-self.enemy_damage
            # plane_explode_sound.set_volume(0.3)
            # plane_explode_sound.play()
        # print(self.attackMode)
        bossHpBar.update(self.rect.x,self.rect.y)
        bossBar_centre = ( 
            (self.rect.x-15),
            (self.rect.y-20)
        )
    def attack(self):
        self.timer_pause = time.time()
        self.current_time = self.timer_pause - self.startTimer
        if self.attackMode == 1:
            if round(self.current_time) == self.targetSecond2 and self.shotsFired < 3:
                self.shootMode1(power)
                self.targetSecond2 += 1
                self.shotsFired += 1
            elif self.shotsFired >= 3:
                self.shotsFired = 0
                self.startAttack = False
                self.targetSecond += 6
                self.targetSecond2 += 6
                self.attackMode = 2
        elif self.attackMode == 2:
            self.shootmode2Bool = True
            if round(self.current_time) == self.targetSecond2 and self.shotsFired < 2:
                self.shootMode1(power)
                self.targetSecond2 += 1
                self.shotsFired += 1
            else:
                if self.shotsFired >= 2:
                    self.shotsFired = 0
                    self.startAttack = False
                    self.targetSecond += 6
                    self.targetSecond2 += 6
                    self.shootmode2Bool = False
                    self.attackMode = 3
                    print(self.attackMode)
                    # self.attackMode = random.randint(1,3)
        elif self.attackMode == 3:
            print(f"{round(self.current_time)} and the target is {self.targetSecond2}")
            print("I am trying to start")
            if round(self.current_time) == self.targetSecond2 and self.shotsFired <= 1:
                self.shootMode1(power)
                self.targetSecond2 += 4
                self.shotsFired += 1
                # print("attack mode 3!!")
            elif round(self.current_time) >= self.targetSecond2 and self.shotsFired >= 1:
                new_shot = Enemy3Cannon(self.rect.x, self.rect.y, 0, True)
                enemy3laser.add(new_shot)
                all_sprites.add(new_shot)
                self.shotsFired = 0
                self.startAttack = False
                self.targetSecond += 6
                self.targetSecond2 += 6
                self.attackMode = 1
            
    def shootMode1(self,power):
        for angle in range(-60, 60 + 1, 20):
            new_shot = Enemy1Missile(self.rect.x, self.rect.centery, angle)
            enemy1shots.add(new_shot)
            all_sprites.add(new_shot)

    def shootMode3(self):
        new_shot = Enemy3Cannon(self.rect.x, self.rect.y)
        enemy3laser.add(new_shot)
        all_sprites.add(new_shot)


class BossHealthBar(pygame.sprite.Sprite):
    def __init__(self, maxBossHp, sprite):
        super(BossHealthBar, self).__init__()
        self.surf = pygame.Surface((110, 15))
        self.surf.fill((0,255,0))
        self.rect = ( 
            (200),
            (40)
        )
        self.bossMaxHp = maxBossHp
        print("Bossbarinit = ",self.bossMaxHp)
        self.sprite = sprite
    def update(self, bossX, bossY):
        self.bossHp = self.sprite.enemy_health
        # print(str(self.bossHp) + ', ' + str(self.bossMaxHp))
        self.widthOfGreen = (self.bossHp / self.bossMaxHp)*110
        # print(self.bossHp/self.bossMaxHp)
        self.surf = pygame.Surface((self.widthOfGreen, 15))
        self.surf.fill((0,255,0)) 
        self.rect = ( 
            (bossX-15),
            (bossY-20)
        )
        


bossbar = pygame.Surface((110, 15))
bossbar.fill((255,0,0))
bossBar_centre = ( 
    (110),
    (15)
)

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = cloud_surf.copy()
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        self.enabled = False
        super(PowerUp, self).__init__()

        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height),
            )
        )
    
    def start_powerup_action(self):
        pass

    def update(self):
        if not self.enabled:
            self.rect.move_ip(-15,0)
            if self.rect.right < 0:
                self.kill()
        
            if pygame.sprite.collide_rect(self, player):
                self.rect.move_ip(-screen_width, -screen_height)
                self.start_powerup_action()

class AutoFirePowerUp(PowerUp):
    def __init__(self):
        self.surf = AutoFire.copy()
        super().__init__()
    
    def start_powerup_action(self):
        self.enabled = True
        self.start_time = time.time()
    
    def update(self):
        global shot_delay, wing, shot_cooldown_timea
        super().update()
        if self.enabled:
            if time.time() - self.start_time > 5:
                self.enabled = False
                shot_cooldown_time = 500
                self.kill()
            
            if not shot_delay:
                shot_cooldown_time = 175
                pygame.time.set_timer(ShotCooldown, shot_cooldown_time)
                shot_delay = True
                new_shot = Missile(wing)
                if wing == 1:
                    wing = 2
                else:
                    wing = 1
                playershots.add(new_shot)
                all_sprites.add(new_shot)

class ExtraLifePowerUp(PowerUp):
    def __init__(self):
        self.surf = up1_surf.copy()
        super().__init__()
    
    def start_powerup_action(self):
        self.enabled = True
        self.start_time = time.time()
    
    def update(self):
        super().update()
        if self.enabled:
            if player.lives == 5:
                player.hp = 3
                player.score = player.score + 5000
                self.enabled = False
            elif player.lives < 5:
                player.lives = player.lives + 1
                player.hp = 3
                self.enabled = False

class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super(Arrow, self).__init__()
        self.surf = arrow_surf.copy()
        self.surf = arrow.copy()
        self.rect = self.surf.get_rect()  
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        pass
    def select(self):
        global surf1_centre, surf2_centre, surf3_centre, wheaty, start_menu_active, running, scores_menu_active, game_active, retry_menu_active, exitRect3_y, retry_menu_active_highscore, border
        if wheaty+5 == textRect1_y:
            print('Play')
            start_menu_active = False
            running = True
        elif wheaty+5 == textRect2_y:
            print('scores')
            start_menu_active = False
            scores_menu_active = True
        elif wheaty+5 == textRect3_y:
            print('exit')
            running = False
            start_menu_active = False
            game_active = False
            scores_menu_active = False
        elif wheaty+30 == 200:
            print('retry')
            running = True
            start_menu_active = False
            game_active = True
            scores_menu_active = False
            retry_menu_active = False
            player.bossBattle = False
            border = True
            player.lives = 3
            player.score = 0
            player.hp = 3
            player.surf = player_surf.copy()
            player.rect = player.surf.get_rect()
            for sprite in all_sprites:
                    sprite.kill()
        elif wheaty+5 == exitRect3_y:
            print('exit')
            running = False
            start_menu_active = False
            game_active = False
            scores_menu_active = False
            retry_menu_active_highscore = False
            retry_menu_active = False
        elif wheaty+5 == backRect.y:
            print('back')
            scores_menu_active = False
            start_menu_active = True
            wheaty = 0

arrow_sprite = Arrow()
# Setup the clock for a decent framerate
clock = pygame.time.Clock()
exitRect3_y = 500
bar1colour = (0,255,0)
bar2colour = (0,255,0)
bar3colour = (0,255,0)
game_active = True
pygame.mixer.music.load("assets/sfx/AirWolf.mp3")
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(loops=-1)
while game_active:
    while start_menu_active:
        screen.fill(black)
        for event in pygame.event.get():
            # did the user press a key?
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                   arrow_index += 1
                elif event.key == K_UP:
                    arrow_index -= 1
                elif event.key == K_RETURN:
                    if arrow_index == 0:
                        print('play')
                        running = True
                        start_menu_active = False
                        game_active = True
                        scores_menu_active = False
                        retry_menu_active = False
                        retry_menu_active_highscore = False
                    elif arrow_index == 1:
                        print('settings')
                        running = False
                        start_menu_active = False
                        game_active = False
                        scores_menu_active = False
                        retry_menu_active = False
                        retry_menu_active_highscore = False
                        settings_menu = True
                        arrow_index = 0
                    elif arrow_index == 2:
                            print('scores')
                            running = False
                            start_menu_active = False
                            game_active = True
                            scores_menu_active = True
                            retry_menu_active = False
                            retry_menu_active_highscore = False
                    elif arrow_index == 3:
                            print('exit')
                            running = False
                            start_menu_active = False
                            game_active = False
                            scores_menu_active = False
                            retry_menu_active = False
                            retry_menu_active_highscore = False
                # was it the escape key?
                if event.key == K_ESCAPE:
                    running = False
                    start_menu_active = False
                    game_active = False
                    scores_menu_active = False
                    retry_menu_active_highscore = False
            elif event.type == QUIT:
                running = False
                start_menu_active = False
                game_active = False
                retry_menu_active_highscore = False
        pressed_keys = pygame.key.get_pressed()
        if arrow_index > 3:
            arrow_index = 0
        if arrow_index < 0:
            arrow_index = 3
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)
        screen.blit(text3, textRect3)
        screen.blit(settingsText, settingsTextRect)
        screen.blit(logo, logo_rect)
        screen.blit(arrow, (wheatx, [textRect1.y, settingsTextRect_y, textRect2.y, textRect3.y][arrow_index]))
        pygame.display.flip()
        clock.tick(30)
    while settings_menu:
        rebindupTextRect_y = 25
        rebinddownTextRect_y = 120
        rebindleftTextRect_y = 220
        rebindrightTextRect_y = 320
        rebindfiretTextRect_y = 420
        resetdefaultTextRect_y = 510
        screen.fill(black)
        for event in pygame.event.get():
            # did the user press a key?
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if arrow_index == 0:
                        print('Change Move Up')
                        rebind = True
                        while rebind:
                            rebindupTextRect.y = 10000
                            rebinddownTextRect.y = 10000
                            rebindleftTextRect.y = 10000
                            rebindrightTextRect.y = 10000
                            rebindfireTextRect.y = 10000
                            resetdefaultTextRect.y = 10000
                            screen.blit(backText, (350,550))
                            screen.blit(rebindupText, rebindupTextRect)
                            screen.blit(rebinddownText, rebinddownTextRect)
                            screen.blit(rebindleftText, rebindleftTextRect)
                            screen.blit(rebindrightText, rebindrightTextRect)
                            screen.blit(rebindfireText, rebindfireTextRect)
                            screen.blit(resetdefaultText, resetdefaultTextRect)
                            screen.blit(change, changeRect)
                            pygame.display.flip()
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == K_ESCAPE:
                                        rebind = False
                                        rebindupTextRect.y = 25
                                        rebinddownTextRect.y = 120
                                        rebindleftTextRect.y = 220
                                        rebindrightTextRect.y = 320
                                        rebindfireTextRect.y = 420
                                        resetdefaultTextRect.y = 510
                                    elif event.key == K_RETURN:
                                        print('That is not a valid key option')
                                    else:
                                        bindup = event.key
                                        print(repr(bindup),K_e)
                                        print(pygame.key.name(bindup))
                                        Keybinds["bindup"] = bindup
                                        with open('assets/data/keybinds.json', 'w') as f:
                                            json.dump(Keybinds,f)
                                        rebind = False
                                        rebindupTextRect.y = 25
                                        rebinddownTextRect.y = 120
                                        rebindleftTextRect.y = 220
                                        rebindrightTextRect.y = 320
                                        rebindfireTextRect.y = 420
                                        resetdefaultTextRect.y = 510
                    elif arrow_index == 1:
                        print('Change Move Down')
                        rebind = True
                        while rebind:
                            rebindupTextRect.y = 10000
                            rebinddownTextRect.y = 10000
                            rebindleftTextRect.y = 10000
                            rebindrightTextRect.y = 10000
                            rebindfireTextRect.y = 10000
                            resetdefaultTextRect.y = 10000
                            screen.blit(backText, (350,550))
                            screen.blit(rebindupText, rebindupTextRect)
                            screen.blit(rebinddownText, rebinddownTextRect)
                            screen.blit(rebindleftText, rebindleftTextRect)
                            screen.blit(rebindrightText, rebindrightTextRect)
                            screen.blit(rebindfireText, rebindfireTextRect)
                            screen.blit(resetdefaultText, resetdefaultTextRect)
                            screen.blit(change, changeRect)
                            pygame.display.flip()
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == K_ESCAPE:
                                        rebind = False
                                        rebindupTextRect.y = 25
                                        rebinddownTextRect.y = 120
                                        rebindleftTextRect.y = 220
                                        rebindrightTextRect.y = 320
                                        rebindfireTextRect.y = 420
                                        resetdefaultTextRect.y = 510
                                    elif event.key == K_RETURN:
                                        print('That is not a valid key option')
                                    else:
                                        binddown = event.key
                                        print(repr(binddown),K_e)
                                        print(pygame.key.name(binddown))
                                        Keybinds["binddown"] = binddown
                                        with open('assets/data/keybinds.json', 'w') as f:
                                            json.dump(Keybinds,f)
                                        rebind = False
                                        rebindupTextRect.y = 25
                                        rebinddownTextRect.y = 120
                                        rebindleftTextRect.y = 220
                                        rebindrightTextRect.y = 320
                                        rebindfireTextRect.y = 420
                                        resetdefaultTextRect.y = 510
                    elif arrow_index == 2:
                        print('Change Move Left')
                        rebind = True
                        while rebind:
                            rebindupTextRect.y = 10000
                            rebinddownTextRect.y = 10000
                            rebindleftTextRect.y = 10000
                            rebindrightTextRect.y = 10000
                            rebindfireTextRect.y = 10000
                            resetdefaultTextRect.y = 10000
                            screen.blit(backText, (350,550))
                            screen.blit(rebindupText, rebindupTextRect)
                            screen.blit(rebinddownText, rebinddownTextRect)
                            screen.blit(rebindleftText, rebindleftTextRect)
                            screen.blit(rebindrightText, rebindrightTextRect)
                            screen.blit(rebindfireText, rebindfireTextRect)
                            screen.blit(resetdefaultText, resetdefaultTextRect)
                            screen.blit(change, changeRect)
                            pygame.display.flip()
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == K_ESCAPE:
                                        rebind = False
                                        rebindupTextRect.y = 25
                                        rebinddownTextRect.y = 120
                                        rebindleftTextRect.y = 220
                                        rebindrightTextRect.y = 320
                                        rebindfireTextRect.y = 420
                                        resetdefaultTextRect.y = 510
                                    elif event.key == K_RETURN:
                                        print('That is not a valid key option')
                                    else:
                                        bindleft = event.key
                                        print(repr(bindleft),K_e)
                                        print(pygame.key.name(bindleft))
                                        Keybinds["bindleft"] = bindleft
                                        with open('assets/data/keybinds.json', 'w') as f:
                                            json.dump(Keybinds,f)
                                        rebind = False
                                        rebindupTextRect.y = 25
                                        rebinddownTextRect.y = 120
                                        rebindleftTextRect.y = 220
                                        rebindrightTextRect.y = 320
                                        rebindfireTextRect.y = 420
                                        resetdefaultTextRect.y = 510
                    elif arrow_index == 3:
                        print('Change Move Right')
                        rebind = True
                        while rebind:
                            rebindupTextRect.y = 10000
                            rebinddownTextRect.y = 10000
                            rebindleftTextRect.y = 10000
                            rebindrightTextRect.y = 10000
                            rebindfireTextRect.y = 10000
                            resetdefaultTextRect.y = 10000
                            screen.blit(backText, (350,550))
                            screen.blit(rebindupText, rebindupTextRect)
                            screen.blit(rebinddownText, rebinddownTextRect)
                            screen.blit(rebindleftText, rebindleftTextRect)
                            screen.blit(rebindrightText, rebindrightTextRect)
                            screen.blit(rebindfireText, rebindfireTextRect)
                            screen.blit(resetdefaultText, resetdefaultTextRect)
                            screen.blit(change, changeRect)
                            pygame.display.flip()
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == K_ESCAPE:
                                        rebind = False
                                        rebindupTextRect.y = 25
                                        rebinddownTextRect.y = 120
                                        rebindleftTextRect.y = 220
                                        rebindrightTextRect.y = 320
                                        rebindfireTextRect.y = 420
                                        resetdefaultTextRect.y = 510
                                    elif event.key == K_RETURN:
                                        print('That is not a valid key option')
                                    else:
                                        bindright = event.key
                                        print(repr(bindright),K_e)
                                        print(pygame.key.name(bindright))
                                        Keybinds["bindright"] = bindright
                                        with open('assets/data/keybinds.json','w') as f:
                                            json.dump(Keybinds,f)
                                        rebind = False
                                        rebindupTextRect.y = 25
                                        rebinddownTextRect.y = 120
                                        rebindleftTextRect.y = 220
                                        rebindrightTextRect.y = 320
                                        rebindfireTextRect.y = 420
                                        resetdefaultTextRect.y = 510
                    elif arrow_index == 4:
                        print('Change Fire button')
                        rebind = True
                        while rebind:
                            rebindupTextRect.y = 10000
                            rebinddownTextRect.y = 10000
                            rebindleftTextRect.y = 10000
                            rebindrightTextRect.y = 10000
                            rebindfireTextRect.y = 10000
                            resetdefaultTextRect.y = 10000
                            screen.blit(backText, (350,550))
                            screen.blit(rebindupText, rebindupTextRect)
                            screen.blit(rebinddownText, rebinddownTextRect)
                            screen.blit(rebindleftText, rebindleftTextRect)
                            screen.blit(rebindrightText, rebindrightTextRect)
                            screen.blit(rebindfireText, rebindfireTextRect)
                            screen.blit(resetdefaultText, resetdefaultTextRect)
                            screen.blit(change, changeRect)
                            pygame.display.flip()
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == K_ESCAPE:
                                        rebind = False
                                        rebindupTextRect.y = 25
                                        rebinddownTextRect.y = 120
                                        rebindleftTextRect.y = 220
                                        rebindrightTextRect.y = 320
                                        rebindfireTextRect.y = 420
                                        resetdefaultTextRect.y = 510
                                    elif event.key == K_RETURN:
                                        print('That is not a valid key option')
                                    else:
                                        bindfire = event.key
                                        print(repr(bindfire),K_e)
                                        print(pygame.key.name(bindfire))
                                        Keybinds["bindfire"] = bindfire
                                        with open('assets/data/keybinds.json', 'w') as f:
                                            json.dump(Keybinds,f)
                                        rebind = False
                                        rebindupTextRect.y = 25
                                        rebinddownTextRect.y = 120
                                        rebindleftTextRect.y = 220
                                        rebindrightTextRect.y = 320
                                        rebindfireTextRect.y = 420
                                        resetdefaultTextRect.y = 510
                    elif arrow_index == 5:
                        print('Reset key binds to default')
                        bindup = K_UP
                        binddown = K_DOWN
                        bindleft = K_LEFT
                        bindright = K_RIGHT
                        bindfire = K_SPACE
                        Keybinds["bindup"] = bindup
                        Keybinds["binddown"] = binddown
                        Keybinds["bindleft"] = bindleft
                        Keybinds["bindright"] = bindright
                        Keybinds["bindfire"] = bindfire
                        with open('assets/data/keybinds.json','w') as f:
                            json.dump(Keybinds,f)
                    elif arrow_index == 6:
                        print('back')
                        running = False
                        start_menu_active = True
                        game_active = True
                        scores_menu_active = False
                        retry_menu_active = False
                        retry_menu_active_highscore = False
                        settings_menu = False
                        arrow_index = 0
                elif event.key == K_DOWN:
                   arrow_index += 1
                elif event.key == K_UP:
                    arrow_index -= 1
                # was it the escape key?
                elif event.key == K_ESCAPE:
                    running = False
                    start_menu_active = False
                    game_active = False
                    scores_menu_active = False
                    retry_menu_active_highscore = False
                    settings_menu = False
            elif event.type == QUIT:
                running = False
                start_menu_active = False
                game_active = False
                scores_menu_active = False
                retry_menu_active_highscore = False
                settings_menu = False
        pressed_keys = pygame.key.get_pressed()
        arrow_sprite.update(pressed_keys)
        # screen.blit(score_text, score_rect)
        if arrow_index > 6:
            arrow_index = 0
        if arrow_index < 0:
            arrow_index = 6
        screen.blit(backText, (350,550))
        screen.blit(rebindupText, rebindupTextRect)
        screen.blit(rebinddownText, rebinddownTextRect)
        screen.blit(rebindleftText, rebindleftTextRect)
        screen.blit(rebindrightText, rebindrightTextRect)
        screen.blit(rebindfireText, rebindfireTextRect)
        screen.blit(resetdefaultText, resetdefaultTextRect)
        screen.blit(arrow, (wheatx, [rebindupTextRect_y, rebinddownTextRect_y, rebindleftTextRect_y, rebindrightTextRect_y, rebindfiretTextRect_y, resetdefaultTextRect_y, 550][arrow_index]))
        pygame.display.flip()
        clock.tick(30)
    while scores_menu_active:
        # if wheaty + 5 < textRect1_y:
        #     wheaty = textRect1_y - 5
        # if wheaty + 5 > textRect3_y:
        #     wheaty = textRect3_y - 5
        screen.fill(black)
        wheaty = 550   
        score_text = pygame.Surface((screen_width, 500), pygame.SRCALPHA, 32).convert_alpha()
        score_rect = score_text.get_rect()

        offset = 0
        padding = 150
        
        def add_score(name, value):
            name_surface = font32.render(name, True, (0,255,0))
            name_rect = name_surface.get_rect()
            score_text.blit(name_surface, (score_rect.left + padding, offset))

            value_surface = font32.render(str(value), True, (0,255,0))
            value_rect = value_surface.get_rect()
            score_text.blit(value_surface, (score_rect.right - value_rect.width - padding, offset))
        
        add_score("Name", "Scores")
        offset += 32

        for name, value in Scores.items():
            add_score(name, value)
            offset += 32
        
        score_rect.centerx = 400
        score_rect.top = 100
        backRect.center = (400,575)
        for event in pygame.event.get():
            # did the user press a key?
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    arrow_sprite.select()
                # was it the escape key?
                if event.key == K_ESCAPE:
                    running = False
                    start_menu_active = False
                    game_active = False
                    scores_menu_active = False
                    retry_menu_active_highscore = False
            elif event.type == QUIT:
                running = False
                start_menu_active = False
                game_active = False
                scores_menu_active = False
                retry_menu_active_highscore = False
        scorerect_y = score_rect.y
        pressed_keys = pygame.key.get_pressed()
        arrow_sprite.update(pressed_keys)
        screen.blit(score_text, score_rect)
        screen.blit(backText, backRect)
        screen.blit(arrow, (wheatx, wheaty))
        pygame.display.flip()
        clock.tick(30)
    while running:
        if gameStarted == False:
            gameStarted = True
        # look at every event in the queue
        for event in pygame.event.get():
            # did the user press a key?
            if event.type == ShotCooldown:
                shot_delay = False
            if event.type == KEYDOWN:
                # was it the escape key?
                if event.key == K_ESCAPE:
                    running = False
                    start_menu_active = False
                    game_active = False
                    scores_menu_active = False
                    retry_menu_active_highscore = False
                elif event.key == bindfire and not shot_delay:
                    pygame.time.set_timer(ShotCooldown, shot_cooldown_time)
                    shot_delay = True
                    new_shot = Missile(wing)
                    if wing == 1:
                        wing = 2
                    else:
                        wing = 1
                    playershots.add(new_shot)
                    all_sprites.add(new_shot)
            elif event.type == QUIT:
                running = False
                start_menu_active = False
                game_active = False
                scores_menu_active = False
                retry_menu_active_highscore = False
            # add new enemy
            elif event.type == ADDENEMY and player.bossBattle == False:
                # create new enemy
                spawn = random.randint(1,100)
                if spawn <=65:   
                    new_enemy1 = Enemy1()
                    enemy1.add(new_enemy1)
                    all_sprites.add(new_enemy1)
                elif spawn >65 and spawn <90:
                    new_enemy2 = Enemy2()
                    enemy2.add(new_enemy2)
                    all_sprites.add(new_enemy2)
                else:
                    new_enemy3 = Enemy3()
                    enemy3.add(new_enemy3)
                    all_sprites.add(new_enemy3)
                    # Add a new cloud?
            elif event.type == ADDCLOUD:
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
            elif event.type == PowerUpSpawn:
                # Create the new cloud and add it to sprite groups
                chosen_power_up = random.randint(0,2)
                if chosen_power_up == 0:
                    print('I am 0')
                    new_power_up = AutoFirePowerUp()
                    powerups.add(new_power_up)
                    all_sprites.add(new_power_up)
                elif chosen_power_up == 1:
                    print('I am 1')
                    new_power_up = ExtraLifePowerUp()
                    powerups.add(new_power_up)
                    all_sprites.add(new_power_up)
                elif chosen_power_up > 1:
                    print("drop bomb")
        if player.lives == 5:
            live1.swap_life(True)
            live2.swap_life(True)
            live3.swap_life(True)
            live4.swap_life(True)
            live5.swap_life(True)
        elif player.lives == 4:
            live1.swap_life(True)
            live2.swap_life(True)
            live3.swap_life(True)
            live4.swap_life(True)
            live5.swap_life(False)
        elif player.lives == 3:
            live1.swap_life(True)
            live2.swap_life(True)
            live3.swap_life(True)
            live4.swap_life(False)
            live5.swap_life(False)
        elif player.lives == 2:
            live1.swap_life(True)
            live2.swap_life(True)
            live3.swap_life(False)
            live4.swap_life(False)
            live5.swap_life(False)
        elif player.lives == 1:
            live1.swap_life(True)
            live2.swap_life(False)
            live3.swap_life(False)
            live4.swap_life(False)
            live5.swap_life(False)
        elif player.lives == 0:
            live1.swap_life(False)
            live2.swap_life(False)
            live3.swap_life(False)
            live4.swap_life(False)
            live5.swap_life(False)


        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        explosions.update()
        enemy1.update()
        enemy2.update()
        enemy3.update()
        boss.update()
        clouds.update()
        playershots.update()
        enemy1shots.update()
        enemy2shots.update()
        enemy3laser.update()
        powerups.update()
        
        if player.score // score_gap > player.prev_score // score_gap:
            if player.lives == 5:
                # spawn random power up
                new_power_up = AutoFirePowerUp()
                powerups.add(new_power_up)
                all_sprites.add(new_power_up)
            elif player.lives < 5:
                player.lives = player.lives + 1

        text = font32.render(str(player.score).zfill(7), True, (255,255,255))

        player.prev_score = player.score

        # sets background to white
        screen.fill((135, 206, 250))

        if player.hp <= 0:
            if player.lives > 0:
                # plane_explode_sound.set_volume(1)
                # plane_explode_sound.play()
                prev_player_rect_x = player.rect.x
                prev_player_rect_y = player.rect.y
                player.rect.x = 1000
                player.rect.y = 1000
                border = False
                player.lives = player.lives - 1
                player.explode()
                print(player.lives, " lives left")
                player.hp = 3

            if player.lives <= 0:
                player.kill()
                # explosions.kill()
                # enemy1.kill()
                # enemy2.kill()
                # enemy3.kill()
                # clouds.kill()
                # shots.kill()
                # powerups.kill()

                running = False
                biggest_key = (max(Scores.items(), key=operator.itemgetter(1))[0])
                if player.score > Scores[biggest_key]:
                    retry_menu_active_highscore = True
                else:
                    retry_menu_active = True


        elif player.hp == 1:
            bar1colour = (0,255,0)
            bar2colour = (255,0,0)
            bar3colour = (255,0,0)
        elif player.hp == 2:
            bar1colour = (0,255,0)
            bar2colour =(0,255,0)
            bar3colour = (255,0,0)
        elif player.hp ==3:
            bar1colour = (0,255,0)
            bar2colour = (0,255,0)
            bar3colour = (0,255,0)
        elif player.hp <= 0:
            bar1colour = (255,0,0)
            bar2colour = (255,0,0)
            bar3colour = (255,0,0)
        
        hp_bar1 = pygame.Surface((25, 17))
        hp_bar1.fill(bar1colour)
        hp_bar1_centre = ( 
            (15),
            (16)
        )
        

        
        hp_bar2 = pygame.Surface((25, 17))
        hp_bar2.fill(bar2colour)
        hp_bar2_centre = ( 
            (40),
            (16)
        )
        

        
        hp_bar3 = pygame.Surface((25,17))
        hp_bar3.fill(bar3colour)
        hp_bar3_centre = ( 
            (65),
            (16)
        )
        # Check if any enemies have collided with the player
        # Draw all sprites

        if player.bossBattle == True:
            screen.blit(bossbar,bossBar_centre)
            for entity in bossHpBar:
                screen.blit(entity.surf, entity.rect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        # puts the square called surf in the middle of the screen 

        screen.blit(player.surf,player.rect)
        screen.blit(live1.surf,live1.rect)
        screen.blit(live2.surf,live2.rect)
        screen.blit(live3.surf,live3.rect)
        screen.blit(live4.surf,live4.rect)
        screen.blit(live5.surf,live5.rect)
        screen.blit(hp_bar1,hp_bar1_centre)
        screen.blit(hp_bar2,hp_bar2_centre)
        screen.blit(hp_bar3,hp_bar3_centre)
        screen.blit(text, textRect)
        pygame.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        clock.tick(30)
    while retry_menu_active:
        screen.fill(black)
        if Arrow_moved == False:
            wheaty = 170
            Arrow_moved = True
        Retry_rect.center = (400,200)
        Retry_rect_y = Retry_rect.y
        for event in pygame.event.get():
            # did the user press a key?
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    wheaty +=325
                elif event.key == K_UP:
                    wheaty -= 325
                if event.key == K_ESCAPE:
                    running = False
                    start_menu_active = False
                    game_active = False
                    scores_menu_active = False
                    retry_menu_active = False
            if event.type == pygame.KEYDOWN:
                    if event.key == K_RETURN:
                        arrow_sprite.select()
                # was it the escape key?
            elif event.type == QUIT:
                running = False
                start_menu_active = False
                game_active = False
                retry_menu_active = False
        txt_surface = font48.render(text_field, True, (0,255,0))
        # Resize the box if the text is too long.
        # Blit the text.
        # Blit the input_box rect.
        if wheaty < Retry_rect_y + 11:
            wheaty = Retry_rect_y + 11
        if wheaty > exitRect3_y - 5:
            wheaty = exitRect3_y - 5
        screen.blit(arrow, (wheatx, wheaty))
        screen.blit(Retry, Retry_rect)
        screen.blit(text3, (315,exitRect3_y))
        pygame.display.flip()
        clock.tick(30)
        # this makes the square a bit off centre. This is because .blit puts the top left pixel of the square in the place you chose
    while retry_menu_active_highscore:
        screen.fill(white)
        if Arrow_moved == False:
            wheaty = 220
            Arrow_moved = True
        for event in pygame.event.get():
            # did the user press a key?
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                   arrow_index += 1
                elif event.key == K_UP:
                    arrow_index -= 1
                if event.key == K_ESCAPE:
                    running = False
                    start_menu_active = False
                    game_active = False
                    scores_menu_active = False
                    retry_menu_active_highscore = False
            if event.type == pygame.KEYDOWN:
                    if event.key == K_RETURN:
                        if arrow_index == 0:
                            name = text_field
                            if len(name) >= 15:
                                text_field = 'Name too long!'    
                            elif len(name) == 0:
                                text_field = 'Enter something noob'
                            else:
                                Scores[name] = player.score
                                with open('assets/data/Highscores.json', 'w') as in_file:
                                    json.dump(Scores,in_file)
                                text_field = ''
                        elif arrow_index == 1:
                            print('retry')
                            for sprite in all_sprites:
                                sprite.kill()
                            running = True
                            start_menu_active = False
                            game_active = True
                            scores_menu_active = False
                            retry_menu_active = False
                            retry_menu_active_highscore = False
                            player.bossBattle = False
                            player.lives = 3
                            player.score = 0
                            player.hp = 3
                            player.surf = player_surf.copy()
                            player.rect = player.surf.get_rect()  
                        elif arrow_index == 2:
                            print('exit')
                            running = False
                            start_menu_active = False
                            game_active = False
                            scores_menu_active = False
                            retry_menu_active = False
                            retry_menu_active_highscore = False
                    elif event.key == pygame.K_BACKSPACE:
                        text_field = text_field[:-1]
                    else:
                        text_field += event.unicode
                        text_field = text_field[:14]
                # was it the escape key?
            elif event.type == QUIT:
                running = False
                start_menu_active = False
                game_active = False
                retry_menu_active_highscore = False
        txt_surface = font48.render(text_field, True, (0,255,0))
        
        # limit arrow_index
        if arrow_index > 2:
            arrow_index = 2
        if arrow_index < 0:
            arrow_index = 0

        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        surf4_rect.w = width
        surf4_rect.y = 170
        surf4_rect.centerx = screen_width / 2
        # Blit the text.
        # Blit the input_box rect.
        # if wheaty + 5 < Retry_rect_y:
        #     wheaty = Retry_rect_y - 5
        # if wheaty + 5 > exitRect3_y:
        #     wheaty = exitRect3_y - 5
        pygame.draw.rect(screen, (0,255,0), surf4_rect, 2)
        screen.blit(txt_surface, (surf4_rect.x+5, surf4_rect.y+5))
        screen.blit(enterText,enterTextRect)
        screen.blit(highscoreText,highscoreTextRect)
        screen.blit(arrow, (wheatx, [enterTextRect_y, Retry_rect.y, exitRect3_y][arrow_index]))
        screen.blit(Retry, Retry_rect)
        screen.blit(text3, (360,exitRect3_y))
        pygame.display.flip()
        clock.tick(30)
