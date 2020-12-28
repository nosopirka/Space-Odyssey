import pygame
import random 
import os
import sys


pygame.init()
pygame.display.set_caption('')
size = width, height = 1400, 700
screen = pygame.display.set_mode(size)
player_spr = pygame.sprite.Group() 
all_sprites = pygame.sprite.Group() 
player_bullet_spr = pygame.sprite.Group()
opponents_spr = pygame.sprite.Group()
clock = pygame.time.Clock()
order = 0
opponents_armor = [1, 2, 3]
bullet_force = [1, 2, 3]

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(fullname)
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image 


class Button:
    def __init__(self, surface, color, x, y, w, h, text, text_color):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.text_color = text_color
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height), 0)
        new_text = pygame.font.SysFont("Calibri", self.width // len(self.text)).render(self.text, 1, self.text_color)
        surface.blit(new_text, ((self.x + self.width // 2) - new_text.get_width() // 2,
                                (self.y + self.height // 2) - new_text.get_height() // 2))

    def press(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('space.jpg'), (width, 2312))
    screen.blit(fon, (0, 0))
    start_button = Button(screen, (3, 0, 79), (width - 350) // 2, (height - 100) // 2, 350, 100,
                          "Играть", (255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.press(pygame.mouse.get_pos()):
                    return
        pygame.display.flip()
        clock.tick(50)

def spaceships_screen():
    global order
    spaceships = {
        0: ['spaceship1_2.png', 'bullet1_1.png', 'opponent1.png', 'Characteristics 1:'],
        1: ['spaceship2_2.png', 'bullet2_1.png', 'opponent2.png', 'Characteristics 2:'],
        2: ['spaceship3_2.png', 'bullet3_1.png', 'opponent3.png', 'Characteristics 3:']
    }
    while True:
        fon = pygame.transform.scale(load_image('station.jpg'), (width, height))
        screen.blit(fon, (0, 0))

        left_choise = Button(screen, (3, 0, 79), 365, 600, 145, 75, "<<", (255, 255, 255))
        right_choise = Button(screen, (3, 0, 79), 790, 600, 145, 75, ">>", (255, 255, 255))
        choise = Button(screen, (3, 0, 79), 530, 600, 240, 75, "Выбрать", (255, 255, 255))

        character_text = pygame.font.SysFont("Calibri", 30).render(spaceships[order][3], 1, (255, 255, 255))

        ship_image = pygame.transform.scale(load_image(spaceships[order][0], -1), (305, 300))
        bullet_image = pygame.transform.scale(load_image(spaceships[order][1], -1), (50, 85))

        screen.blit(ship_image, (500, 200))
        screen.blit(bullet_image, (625, 100))
        screen.blit(character_text, (100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if left_choise.press(pygame.mouse.get_pos()):
                    order = (order - 1) % 3
                elif right_choise.press(pygame.mouse.get_pos()):
                    order = (order + 1) % 3
                elif choise.press(pygame.mouse.get_pos()):
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    order = (order - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    order = (order + 1) % 3
        pygame.display.flip()
        clock.tick(50)
       
        
class Player_2d(pygame.sprite.Sprite):
    def __init__(self, spaceship_id, player):
        super().__init__(all_sprites)
        image = load_image("spaceship"+str(spaceship_id)+".png", -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = player[0]-32
        self.rect.y = player[1]-27
        player_spr.add(self)
        
    def update(self, x, y):
        self.rect = self.rect.move(x, y)
     
        
class Player_bullet(pygame.sprite.Sprite):
    def __init__(self, spaceship_id, player):
        super().__init__(all_sprites)
        self.player_bullet_spr = pygame.sprite.Group()
        image = load_image("bullet"+str(spaceship_id)+".png", -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = player[0]-5
        self.rect.y = player[1]-9
        self.player_bullet_spr.add(self)
        
    def update(self, x, y):
        self.rect = self.rect.move(x, y)


class Opp_bullet(pygame.sprite.Sprite):
    def __init__(self, spaceship_id, pos):
        super().__init__(all_sprites)
        self.opp_bullet_spr = pygame.sprite.Group()
        image = load_image("opponent_bullet.png", -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]-5
        self.rect.y = pos[1]-9
        self.opp_bullet_spr.add(self)
        
    def update(self, x, y):
        self.rect = self.rect.move(x, y)
   
        
class Opponents(pygame.sprite.Sprite):
    def __init__(self, opp_id, pos, lvl_opp):
        super().__init__(all_sprites)
        self.opponents_spr = pygame.sprite.Group()
        image = load_image("opponent"+str(lvl_opp)+".png", -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]-32
        self.rect.y = pos[1]-30
        self.opponents_spr.add(self)
        
    def update(self, x, y):
        self.rect = self.rect.move(x, y)
        
        
class Game_2d:
    def __init__(self, width, height, fps, spaceship_id, opp_id, k_k, f_d, opp_ver, bull_sp, opp_bul_ver): 
        global player_spr
        cadr = 1
        mbp = 0
        player = (600, 600)
        player_spr = pygame.sprite.Group() 
        Player_2d(spaceship_id, player)  
        opponents_spr = pygame.sprite.Group()
        fon = pygame.transform.scale(load_image('space.jpg'), (width-200, 2312))
        killed_ships = 0
        opponents = []
        player_bullets = []
        opp_bullets = []
        last_pressed_button = None
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    last_pressed_button = event
                if event.type == pygame.KEYUP:
                    last_pressed_button = None
                if event.type == pygame.MOUSEBUTTONDOWN and abs(event.pos[0] - player[0]) < 32 and abs(event.pos[1] - player[1]) < 30:
                    mbp = 1
                if event.type == pygame.MOUSEBUTTONUP:
                    mbp = 0
                if event.type == pygame.MOUSEMOTION and mbp==1:
                    s = (-player[0] + max(32, min(player[0] + event.rel[0], width-232)), -player[1] + max(32, min(player[1] + event.rel[1], height-32)))
                    player = (max(32, min(player[0] + event.rel[0], width-232)), max(32, min(player[1] + event.rel[1], height-32)))
                    player_spr.update(*s)
                    
            if last_pressed_button != None: 
                event = last_pressed_button
                if event.type == pygame.KEYDOWN and event.key == 1073741906:
                    s = min(10, player[1]-30)
                    player = (player[0], player[1]-s)
                    player_spr.update(0, -s)
                if event.type == pygame.KEYDOWN and event.key == 1073741903:
                    s = min(10, width - 232 - player[0])
                    player = (player[0]+s, player[1])
                    player_spr.update(s, 0)
                if event.type == pygame.KEYDOWN and event.key == 1073741905:
                    s = min(10, height-player[1]-30)
                    player = (player[0], player[1]+s)
                    player_spr.update(0, s)
                if event.type == pygame.KEYDOWN and event.key == 1073741904:
                    s = min(10, player[0]-32)
                    player = (player[0]-s, player[1])   
                    player_spr.update(-s, 0)
                
            screen.fill(pygame.Color('black')) 
            screen.blit(fon, (0, cadr%(2312)))
            screen.blit(fon, (0, cadr%(2312)-2312))             
            if cadr % opp_ver == 0 or opponents == []:
                pos_opp = (random.randrange((width-200)//75)*75+32, -20)
                lvl_opp = random.randrange(opp_id)+1
                opponents.append([Opponents(opp_id, pos_opp, lvl_opp), pos_opp, opponents_armor[lvl_opp-1]])
                
            if cadr % bull_sp == 0:
                player_bullets.append([Player_bullet(spaceship_id, [player[0], player[1] -30]), [player[0], player[1] -35]])
                
            if random.randrange(opp_bul_ver) == 0:
                pos = opponents[random.randrange(len(opponents))][1]
                opp_bullets.append([Opp_bullet(spaceship_id, pos), pos])
            
            pygame.draw.line(screen, (255, 255, 255), (width-200, 0), (width-200, height), 1)
            font = pygame.font.Font(None, 38)
            text = font.render("FPS: "+str(int(clock.get_fps())), True, (100, 255, 100))
            screen.blit(text, (width-199, 10))            
            font = pygame.font.Font(None, 38)
            text = font.render("Цель:", True, (100, 255, 100))
            screen.blit(text, (width-199, 60))            
            font = pygame.font.Font(None, 34)
            text = font.render("Нанести урон", True, (100, 255, 100))
            screen.blit(text, (width-199, 100))                      
            font = pygame.font.Font(None, 34)
            text = font.render(str(k_k), True, (100, 255, 100))
            screen.blit(text, (width-199, 130))            
            player_spr.draw(screen)
            if f_d < 100000:
                text = font.render("Пролететь "+str(f_d), True, (100, 255, 100))
                screen.blit(text, (width-199, 160))                      
                font = pygame.font.Font(None, 34)
            else:
                text = font.render("Пролететь", True, (100, 255, 100))
                screen.blit(text, (width-199, 160))                      
                font = pygame.font.Font(None, 34)
                text = font.render(str(f_d), True, (100, 255, 100))
                screen.blit(text, (width-199, 190))                      
                font = pygame.font.Font(None, 34)
            text = font.render("Нанесён урон", True, (100, 255, 100))
            screen.blit(text, (width-199, 250))                      
            font = pygame.font.Font(None, 34)
            text = font.render(str(killed_ships), True, (100, 255, 100))
            screen.blit(text, (width-199, 280))            
            player_spr.draw(screen)
            if cadr < 100000:
                text = font.render("Пройдено "+str(cadr), True, (100, 255, 100))
                screen.blit(text, (width-199, 310))                      
                font = pygame.font.Font(None, 34)
            else:
                text = font.render("Пройдено", True, (100, 255, 100))
                screen.blit(text, (width-199, 310))                      
                font = pygame.font.Font(None, 34)
                text = font.render(str(cadr), True, (100, 255, 100))
                screen.blit(text, (width-199, 340))                      
                font = pygame.font.Font(None, 34)
            
                
            w = 0
            for opponent in range(len(opponents)):
                opponents[opponent-w][0].opponents_spr.update(0, 1)
                opponents[opponent-w][0].opponents_spr.draw(screen)
                opponents[opponent-w][1] = (opponents[opponent-w][1][0], opponents[opponent-w][1][1]+1)
                if abs(opponents[opponent-w][1][0]- player[0]) < 60 and abs(opponents[opponent-w][1][1]- player[1]) < 60:
                    self.res = 0
                    running = False  
                    
                f = 0
                for j in range(len(player_bullets)):
                    if f == 0 and ((player_bullets[j][1][0] - opponents[opponent-w][1][0])**2 + (player_bullets[j][1][1] - opponents[opponent-w][1][1])**2)**0.5 < 25:
                        killed_ships += min(bullet_force[spaceship_id-1], opponents[opponent-w][2])
                        opponents[opponent-w][2] -= bullet_force[spaceship_id-1]
                        del player_bullets[j]
                        if opponents[opponent-w][2] <= 0:
                            del opponents[opponent-w]
                            w += 1
                        
                        f = 1
                if f == 0 and opponents[opponent-w][1][1] > height+50:
                    del opponents[opponent-w]
                    w += 1                    
            w = 0
            for player_bullet in range(len(player_bullets)):
                player_bullets[player_bullet-w][0].player_bullet_spr.update(0, -5)
                player_bullets[player_bullet-w][0].player_bullet_spr.draw(screen)
                player_bullets[player_bullet-w][1] = (player_bullets[player_bullet-w][1][0], player_bullets[player_bullet-w][1][1]-5)
                if player_bullets[player_bullet-w][1][1] < -50:
                    del player_bullets[player_bullet-w]
                    w += 1
            w = 0
            for opp_bullet in range(len(opp_bullets)):
                opp_bullets[opp_bullet-w][0].opp_bullet_spr.update(0, 5)
                opp_bullets[opp_bullet-w][0].opp_bullet_spr.draw(screen)
                opp_bullets[opp_bullet-w][1] = (opp_bullets[opp_bullet-w][1][0], opp_bullets[opp_bullet-w][1][1]+5) 
                if ((opp_bullets[opp_bullet-w][1][0]-player[0])**2+(opp_bullets[opp_bullet-w][1][1]-player[1])**2)**0.5  < 20:
                    del opp_bullets[opp_bullet-w]
                    w += 1
                    self.res = 0
                    running = False  
                elif opp_bullets[opp_bullet-w][1][1] < -50:
                    del opp_bullets[opp_bullet-w]
                    w += 1
                    
            cadr += 1
            if killed_ships >= k_k and cadr >= f_d:
                self.res = 1
                running = False
            pygame.display.flip()
        
            clock.tick(fps)

lvl = 10
while True:
    start_screen()
    spaceships_screen()
    if Game_2d(1300, 700, 60, order + 1, 3, lvl, 100, 100, 6, 60).res == 1:
        print(lvl//10)
        lvl += 10
pygame.quit()
