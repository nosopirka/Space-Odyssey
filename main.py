import pygame
import random 
import os
import sys
import math
import sqlite3

con = sqlite3.connect("data/records.sqlite")
cur = con.cursor()
pygame.init()
pygame.display.set_caption('')
size = width, height = 1300, 700
screen = pygame.display.set_mode(size)
player_spr = pygame.sprite.Group() 
all_sprites = pygame.sprite.Group() 
player_bullet_spr = pygame.sprite.Group()
opponents_spr = pygame.sprite.Group()
clock = pygame.time.Clock()
order = 0
opponents_armor = [1, 2, 3]
bullet_force = [1, 2, 3]
gaming = True
gaming2 = True
nickname = ''


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
    def __init__(self, surface, color, x, y, w, h, text, text_color, text_size=0):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.text_color = text_color
        if text_size == 0:
            self.size = self.width // len(self.text)
        else:
            self.size = text_size

        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height), 0)
        new_text = pygame.font.SysFont("Calibri", self.size).render(self.text, 1, self.text_color)
        surface.blit(new_text, ((self.x + self.width // 2) - new_text.get_width() // 2,
                                (self.y + self.height // 2) - new_text.get_height() // 2))

    def press(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False


class InputText:
    def __init__(self, color, x, y, w, h, text_size=80, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.size = text_size
        self.txt_surface = pygame.font.SysFont("Calibri", self.size).render(self.text, True, self.color)
        self.active = False

    def text_event(self, event):
        global nickname
        pygame.draw.rect(screen, (3, 0, 79), self.rect, 0)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+20))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                if self.text[-1:] != '_':
                    self.text += '_'
            else:
                self.active = False
                if self.text != '':
                    self.text = self.text[:-1]
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if len(self.text) != 0 and self.text != '_':
                        nickname = self.text[:-1]
                        return 0
                        self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-2] + '_'
                else:
                    if len(self.text) < 20:
                        self.text = self.text[:-1] + event.unicode + '_'
        self.txt_surface = pygame.font.SysFont("Calibri", self.size).render(self.text, True, self.color)


def terminate():
    pygame.quit()
    sys.exit()


def nick_screen():
    fon = pygame.transform.scale(load_image('space.jpg'), (width, 2312))
    screen.blit(fon, (0, 0))
    name_text = pygame.font.SysFont("Calibri", 50).render(('Введите имя:'), 1, (255, 255, 255))
    screen.blit(name_text, (300, 225))
    nick = InputText((255, 255, 255), 300, 300, 700, 100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif nick.text_event(event) == 0:
                return
        pygame.display.flip()
        clock.tick(10)


def chooseD_screen():
    global gaming
    fon = pygame.transform.scale(load_image('space.jpg'), (width, 2312))
    screen.blit(fon, (0, 0))
    d2_button = Button(screen, (3, 0, 79), (width - 700) // 4, (height - 200) // 2, 350, 200, "2D", (255, 255, 255))
    d3_button = Button(screen, (3, 0, 79), width - (width - 700) // 4 - 350, (height - 200) // 2, 350, 200,
                          "3D", (255, 255, 255))
    pre_button = Button(screen, (3, 0, 79), 25, height - 75, 175, 50, "Назад", (255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if d2_button.press(pygame.mouse.get_pos()):
                    gaming = True
                    return 2
                elif d3_button.press(pygame.mouse.get_pos()):
                    gaming = True
                    return 3
                elif pre_button.press(pygame.mouse.get_pos()):
                    gaming = False
                    return
        pygame.display.flip()
        clock.tick(50)


def records_screen():
    fon = pygame.transform.scale(load_image('space.jpg'), (width, 2312))
    screen.blit(fon, (0, 0))
    pre_button = Button(screen, (3, 0, 79), 25, height - 75, 175, 50, "Назад", (255, 255, 255))
    result = cur.execute("""SELECT * FROM rec
    ORDER BY lvl""").fetchall()
    x = (width - 350) // 2
    y = 100
    for elem in result:
        result_text = pygame.font.SysFont("Calibri", 30).render(elem[0] + ': уровень ' + str(elem[1]), 1, (255, 255, 255))
        screen.blit(result_text, (x, y))
        y += 50
        if y > 600:
            break
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pre_button.press(pygame.mouse.get_pos()):
                    return
        pygame.display.flip()
        clock.tick(50)


def rules_screen():
    fon = pygame.transform.scale(load_image('space.jpg'), (width, 2312))
    screen.blit(fon, (0, 0))
    pre_button = Button(screen, (3, 0, 79), 25, height - 75, 175, 50, "Назад", (255, 255, 255))
    f = open('data/rules.txt', encoding="utf8")
    x = 50
    y = 50
    for line in f:
        s = ''
        for elem in line.rstrip("\n"):
            s += elem
        rules_text = pygame.font.SysFont("Calibri", 30).render(s, 1, (255, 255, 255))
        screen.blit(rules_text, (x, y))
        y += 40
    f.close()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pre_button.press(pygame.mouse.get_pos()):
                    return
        pygame.display.flip()
        clock.tick(50)


def start_screen():
    result = cur.execute("""SELECT nick FROM rec""").fetchall()
    if (nickname,) not in result:
        cur.execute("""INSERT INTO rec(nick, lvl) VALUES('""" + nickname + """', 1)""").fetchall()
    fon = pygame.transform.scale(load_image('space.jpg'), (width, 2312))
    screen.blit(fon, (0, 0))
    start_button = Button(screen, (3, 0, 79), (width - 350) // 2, 260, 350, 100, "Начать", (255, 255, 255), 50)
    records_button = Button(screen, (3, 0, 79), (width - 350) // 2, 370, 350, 100, "Рекорды", (255, 255, 255), 50)
    rules_button = Button(screen, (3, 0, 79), (width - 350) // 2, 480, 350, 100, "Об игре", (255, 255, 255), 50)
    exit_button = Button(screen, (3, 0, 79), (width - 350) // 2, 590, 350, 100, "Выход", (255, 255, 255), 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.press(pygame.mouse.get_pos()):
                    return
                elif records_button.press(pygame.mouse.get_pos()):
                    records_screen()
                    screen.blit(fon, (0, 0))
                    start_button = Button(screen, (3, 0, 79), (width - 350) // 2, 260, 350, 100, "Начать",
                                          (255, 255, 255), 50)
                    records_button = Button(screen, (3, 0, 79), (width - 350) // 2, 370, 350, 100, "Рекорды",
                                            (255, 255, 255), 50)
                    rules_button = Button(screen, (3, 0, 79), (width - 350) // 2, 480, 350, 100, "Об игре",
                                          (255, 255, 255), 50)
                    exit_button = Button(screen, (3, 0, 79), (width - 350) // 2, 590, 350, 100, "Выход",
                                         (255, 255, 255), 50)
                elif rules_button.press(pygame.mouse.get_pos()):
                    rules_screen()
                    screen.blit(fon, (0, 0))
                    start_button = Button(screen, (3, 0, 79), (width - 350) // 2, 260, 350, 100, "Начать",
                                          (255, 255, 255), 50)
                    records_button = Button(screen, (3, 0, 79), (width - 350) // 2, 370, 350, 100, "Рекорды",
                                            (255, 255, 255), 50)
                    rules_button = Button(screen, (3, 0, 79), (width - 350) // 2, 480, 350, 100, "Об игре",
                                          (255, 255, 255), 50)
                    exit_button = Button(screen, (3, 0, 79), (width - 350) // 2, 590, 350, 100, "Выход",
                                         (255, 255, 255), 50)
                elif exit_button.press(pygame.mouse.get_pos()):
                    terminate()
        pygame.display.flip()
        clock.tick(50)


def spaceships_screen():
    global order, gaming2
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
        choise = Button(screen, (3, 0, 79), 530, 600, 240, 75, "Выбрать", (255, 255, 255), 50)
        pre_button = Button(screen, (3, 0, 79), 25, height - 75, 175, 50, "Назад", (255, 255, 255))

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
                    gaming2 = True
                    return
                elif pre_button.press(pygame.mouse.get_pos()):
                    gaming2 = False
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    order = (order - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    order = (order + 1) % 3
        pygame.display.flip()
        clock.tick(50)


def menu_screen():
    global gaming, gaming2
    fon = pygame.transform.scale(load_image('space.jpg'), (width, 2312))
    screen.blit(fon, (0, 0))
    continue_button = Button(screen, (3, 0, 79), (width - 350) // 2, 300, 350, 100, "Продолжить", (255, 255, 255), 50)
    pre_button = Button(screen, (3, 0, 79), (width - 350) // 2, 450, 350, 100, "Выход", (255, 255, 255), 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.press(pygame.mouse.get_pos()):
                    return True
                elif pre_button.press(pygame.mouse.get_pos()):
                    gaming = False
                    gaming2 = False
                    return False
        pygame.display.flip()
        clock.tick(50)



def levelpass_screen(passed, lvl):
    global gaming, gaming2

    fon = pygame.transform.scale(load_image('space.jpg'), (width, 2312))
    screen.blit(fon, (0, 0))

    if passed:
        text = f'Уровень {lvl} пройден!'
        text_continue = 'Продолжить'
        character_text = pygame.font.SysFont("Calibri", 80).render(text, 1, (255, 255, 255))
        screen.blit(character_text, (325, 100))
    else:
        text = f'Уровень {lvl} не пройден!'
        text_continue = 'Заново'
        character_text = pygame.font.SysFont("Calibri", 80).render(text, 1, (255, 255, 255))
        screen.blit(character_text, (275, 100))

    continue_button = Button(screen, (3, 0, 79), (width - 350) // 2, 280, 350, 100, text_continue, (255, 255, 255), 50)
    pre_button = Button(screen, (3, 0, 79), (width - 350) // 2, 420, 350, 100, "Меню", (255, 255, 255), 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.press(pygame.mouse.get_pos()):
                    gaming = True
                    gaming2 = True
                    return
                elif pre_button.press(pygame.mouse.get_pos()):
                    gaming = False
                    gaming2 = False
                    return
        pygame.display.flip()
        clock.tick(50)


class Player_2d(pygame.sprite.Sprite):
    def __init__(self, spaceship_id, player):
        super().__init__(all_sprites)
        image = load_image("spaceship" + str(spaceship_id) + ".png", -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = player[0] - 32
        self.rect.y = player[1] - 27
        player_spr.add(self)

    def update(self, x, y):
        self.rect = self.rect.move(x, y)


class Player_bullet(pygame.sprite.Sprite):
    def __init__(self, spaceship_id, player):
        super().__init__(all_sprites)
        self.player_bullet_spr = pygame.sprite.Group()
        image = load_image("bullet" + str(spaceship_id) + ".png", -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = player[0] - 5
        self.rect.y = player[1] - 9
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
        self.rect.x = pos[0] - 5
        self.rect.y = pos[1] - 9
        self.opp_bullet_spr.add(self)

    def update(self, x, y):
        self.rect = self.rect.move(x, y)


class Opponents(pygame.sprite.Sprite):
    def __init__(self, opp_id, pos, lvl_opp):
        super().__init__(all_sprites)
        self.opponents_spr = pygame.sprite.Group()
        image = load_image("opponent" + str(lvl_opp) + ".png", -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] - 32
        self.rect.y = pos[1] - 30
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
        fon = pygame.transform.scale(load_image('space.jpg'), (width - 200, 2312))
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
                    if event.key == pygame.K_ESCAPE:
                        last_pressed_button = None
                        pygame.mouse.set_visible(True)
                        if not menu_screen():
                            self.res = -1
                            fps = 0
                            running = False
                        else:
                            break
                if event.type == pygame.KEYUP:
                    last_pressed_button = None
                if event.type == pygame.MOUSEBUTTONDOWN and abs(event.pos[0] - player[0]) < 32 and abs(
                        event.pos[1] - player[1]) < 30:
                    mbp = 1 - mbp
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mbp = 0
                if mbp == 1:
                    pygame.mouse.set_visible(False)
                else:
                    pygame.mouse.set_visible(True)

                if event.type == pygame.MOUSEMOTION and mbp == 1 and last_pressed_button == None:
                    s = (-player[0] + max(32, min(player[0] + event.rel[0], width - 232)),
                         -player[1] + max(32, min(player[1] + event.rel[1], height - 32)))
                    player = (max(32, min(player[0] + event.rel[0], width - 232)),
                              max(32, min(player[1] + event.rel[1], height - 32)))
                    player_spr.update(*s)

            if not running:
                break

            if last_pressed_button != None and mbp == 0:
                event = last_pressed_button
                if event.type == pygame.KEYDOWN and event.key == 1073741906:
                    s = min(10, player[1] - 30)
                    player = (player[0], player[1] - s)
                    player_spr.update(0, -s)
                if event.type == pygame.KEYDOWN and event.key == 1073741903:
                    s = min(10, width - 232 - player[0])
                    player = (player[0] + s, player[1])
                    player_spr.update(s, 0)
                if event.type == pygame.KEYDOWN and event.key == 1073741905:
                    s = min(10, height - player[1] - 30)
                    player = (player[0], player[1] + s)
                    player_spr.update(0, s)
                if event.type == pygame.KEYDOWN and event.key == 1073741904:
                    s = min(10, player[0] - 32)
                    player = (player[0] - s, player[1])
                    player_spr.update(-s, 0)

            screen.fill(pygame.Color('black'))
            screen.blit(fon, (0, cadr % (2312)))
            screen.blit(fon, (0, cadr % (2312) - 2312))
            if cadr % opp_ver == 0 or opponents == []:
                pos_opp = (random.randrange((width - 200) // 75) * 75 + 32, -20)
                lvl_opp = random.randrange(opp_id) + 1
                opponents.append([Opponents(opp_id, pos_opp, lvl_opp), pos_opp, opponents_armor[lvl_opp - 1]])
            if cadr % bull_sp == 0:
                player_bullets.append(
                    [Player_bullet(spaceship_id, [player[0], player[1] - 30]), [player[0], player[1] - 35]])

            if random.randrange(opp_bul_ver) == 0:
                pos = opponents[random.randrange(len(opponents))][1]
                opp_bullets.append([Opp_bullet(spaceship_id, (pos[0], pos[1] + 20)), (pos[0], pos[1] + 20)])

            pygame.draw.line(screen, (255, 255, 255), (width - 200, 0), (width - 200, height), 1)
            font = pygame.font.Font(None, 38)
            text = font.render("FPS: " + str(int(clock.get_fps())), True, (100, 255, 100))
            screen.blit(text, (width - 199, 10))
            font = pygame.font.Font(None, 38)
            text = font.render("Цель:", True, (100, 255, 100))
            screen.blit(text, (width - 199, 60))
            font = pygame.font.Font(None, 34)
            text = font.render("Нанести урон", True, (100, 255, 100))
            screen.blit(text, (width - 199, 100))
            font = pygame.font.Font(None, 34)
            text = font.render(str(k_k), True, (100, 255, 100))
            screen.blit(text, (width - 199, 130))
            player_spr.draw(screen)
            if f_d < 100000:
                text = font.render("Пролететь " + str(f_d), True, (100, 255, 100))
                screen.blit(text, (width - 199, 160))
                font = pygame.font.Font(None, 34)
            else:
                text = font.render("Пролететь", True, (100, 255, 100))
                screen.blit(text, (width - 199, 160))
                font = pygame.font.Font(None, 34)
                text = font.render(str(f_d), True, (100, 255, 100))
                screen.blit(text, (width - 199, 190))
                font = pygame.font.Font(None, 34)
            text = font.render("Нанесён урон", True, (100, 255, 100))
            screen.blit(text, (width - 199, 250))
            font = pygame.font.Font(None, 34)
            text = font.render(str(killed_ships), True, (100, 255, 100))
            screen.blit(text, (width - 199, 280))
            player_spr.draw(screen)
            if cadr < 100000:
                text = font.render("Пройдено " + str(cadr), True, (100, 255, 100))
                screen.blit(text, (width - 199, 310))
                font = pygame.font.Font(None, 34)
            else:
                text = font.render("Пройдено", True, (100, 255, 100))
                screen.blit(text, (width - 199, 310))
                font = pygame.font.Font(None, 34)
                text = font.render(str(cadr), True, (100, 255, 100))
                screen.blit(text, (width - 199, 340))
                font = pygame.font.Font(None, 34)

            w = 0
            for opponent in range(len(opponents)):
                opponents[opponent - w][0].opponents_spr.update(0, 1)
                opponents[opponent - w][0].opponents_spr.draw(screen)
                opponents[opponent - w][1] = (opponents[opponent - w][1][0], opponents[opponent - w][1][1] + 1)
                if abs(opponents[opponent - w][1][0] - player[0]) < 60 and abs(
                        opponents[opponent - w][1][1] - player[1]) < 60:
                    self.res = 0
                    pygame.mouse.set_visible(True)
                    running = False

                f = 0
                for j in range(len(player_bullets)):
                    if f == 0 and ((player_bullets[j][1][0] - opponents[opponent - w][1][0]) ** 2 + (
                            player_bullets[j][1][1] - opponents[opponent - w][1][1]) ** 2) ** 0.5 < 25:
                        killed_ships += min(bullet_force[spaceship_id - 1], opponents[opponent - w][2])
                        opponents[opponent - w][2] -= bullet_force[spaceship_id - 1]
                        del player_bullets[j]
                        if opponents[opponent - w][2] <= 0:
                            del opponents[opponent - w]
                            w += 1

                        f = 1
                if f == 0 and opponents[opponent - w][1][1] > height + 50:
                    del opponents[opponent - w]
                    w += 1
            w = 0
            for player_bullet in range(len(player_bullets)):
                player_bullets[player_bullet - w][0].player_bullet_spr.update(0, -5)
                player_bullets[player_bullet - w][0].player_bullet_spr.draw(screen)
                player_bullets[player_bullet - w][1] = (
                player_bullets[player_bullet - w][1][0], player_bullets[player_bullet - w][1][1] - 5)
                if player_bullets[player_bullet - w][1][1] < -50:
                    del player_bullets[player_bullet - w]
                    w += 1
            w = 0
            for opp_bullet in range(len(opp_bullets)):
                opp_bullets[opp_bullet - w][0].opp_bullet_spr.update(0, 5)
                opp_bullets[opp_bullet - w][0].opp_bullet_spr.draw(screen)
                opp_bullets[opp_bullet - w][1] = (
                opp_bullets[opp_bullet - w][1][0], opp_bullets[opp_bullet - w][1][1] + 5)
                if ((opp_bullets[opp_bullet - w][1][0] - player[0]) ** 2 + (
                        opp_bullets[opp_bullet - w][1][1] - player[1]) ** 2) ** 0.5 < 20:
                    del opp_bullets[opp_bullet - w]
                    w += 1
                    pygame.mouse.set_visible(True)
                    self.res = 0

                    running = False
                elif opp_bullets[opp_bullet - w][1][1] < -50:
                    del opp_bullets[opp_bullet - w]
                    w += 1

            cadr += 1
            if killed_ships >= k_k and cadr >= f_d:
                self.res = 1
                pygame.mouse.set_visible(True)
                running = False
            pygame.display.flip()

            clock.tick(fps)


def angle_trunc(a):
    while a < 0.0:
        a += math.pi * 2
    return a


def getAngleBetweenPoints(x_orig, y_orig, x_landmark, y_landmark):
    deltaY = y_landmark - y_orig
    deltaX = x_landmark - x_orig
    return angle_trunc(math.atan2(deltaY, deltaX))


def angle(cam, cam_a, i):
    s = ((cam[0] - i[0]) ** 2 + (cam[1] - i[1]) ** 2 + (cam[2] - i[2]) ** 2) ** 0.5  # расстояние
    # рисование каждой точки в поле зрения
    if s < 2000:
        gs = ((cam[0] - i[0]) ** 2 + (cam[1] - i[1]) ** 2) ** 0.5  # расстояние по горизонтальной плоскости
        if (cam[0], cam[1]) != (i[0], i[1]):
            xs = cam_a[0] - (360 - math.degrees(getAngleBetweenPoints(cam[0], cam[1], i[0], i[1])))
            if xs > 0:
                xs1 = -(360 - xs)
            else:
                xs1 = 360 + xs
                if abs(xs1) < abs(xs):
                    xs = xs1
        else:
            xs = 0
        ys = math.degrees(getAngleBetweenPoints(0, cam[2], gs, i[2])) - cam_a[1]
        if ys > 0:
            ys1 = -(360 - ys)
        else:
            ys1 = 360 + ys
        if abs(ys1) < abs(ys):
            ys = ys1
        return (xs, ys)
    return None


class Game_3d:
    def __init__(self, width, height, fps, spaceship_id, opp_id, k_k, f_d, opp_ver, bull_sp, opp_bul_ver):
        opponents = []
        opp = [[[-5, 0, 0], [5, 0, 1]],
               [[-5, 0, 0], [5, 0, -1]],
               [[-5, 0, 0], [5, 1, 0]],
               [[-5, 0, 0], [5, -1, 0]],
               [[4, 0, 0], [5, 0, 1]],
               [[4, 0, 0], [5, 0, -1]],
               [[4, 0, 0], [5, 1, 0]],
               [[4, 0, 0], [5, -1, 0]],
               [[5, 1, 0], [5, 0, 1]],
               [[5, 0, 1], [5, -1, 0]],
               [[5, 0, -1], [5, 1, 0]],
               [[5, -1, 0], [5, 0, -1]],  
               [[1, 0.3, -0.3], [1, 4.5, -1.9]],
               [[4, 0.45, -0.45], [2, 4.5, -1.9]],
               [[1, -0.3, -0.3], [1, -4.5, -1.9]],
               [[4, -0.45, -0.45], [2, -4.5, -1.9]],
               [[1, 0.3, 0.3], [1, 4.5, 1.9]],
               [[4, 0.45, 0.45], [2, 4.5, 1.9]],
               [[1, -0.3, 0.3], [1, -4.5, 1.9]],
               [[4, -0.45, 0.45], [2, -4.5, 1.9]],
               
               [[-1, 4.8, -2.2], [-1, 4.8, -1.9]],
               [[-1, 4.5, -1.9], [-1, 4.8, -1.9]],
               [[-1, 4.5, -2.2], [-1, 4.8, -2.2]],
               [[-1, 4.5, -2.2], [-1, 4.5, -1.9]],
               [[3, 4.8, -2.2], [3, 4.8, -1.9]],
               [[3, 4.5, -1.9], [3, 4.8, -1.9]],
               [[3, 4.5, -2.2], [3, 4.8, -2.2]],
               [[3, 4.5, -2.2], [3, 4.5, -1.9]],
               [[3, 4.8, -2.2], [-1, 4.8, -2.2]],
               [[-1, 4.5, -1.9], [3, 4.5, -1.9]],
               [[3, 4.8, -1.9], [-1, 4.8, -1.9]],
               [[3, 4.5, -2.2], [-1, 4.5, -2.2]],

               [[-1, -4.8, -2.2], [-1, -4.8, -1.9]],
               [[-1, -4.5, -1.9], [-1, -4.8, -1.9]],
               [[-1, -4.5, -2.2], [-1, -4.8, -2.2]],
               [[-1, -4.5, -2.2], [-1, -4.5, -1.9]],
               [[3, -4.8, -2.2], [3, -4.8, -1.9]],
               [[3, -4.5, -1.9], [3, -4.8, -1.9]],
               [[3, -4.5, -2.2], [3, -4.8, -2.2]],
               [[3, -4.5, -2.2], [3, -4.5, -1.9]],
               [[3, -4.8, -2.2], [-1, -4.8, -2.2]],
               [[-1, -4.5, -1.9], [3, -4.5, -1.9]],
               [[3, -4.8, -1.9], [-1, -4.8, -1.9]],
               [[3, -4.5, -2.2], [-1, -4.5, -2.2]],               

               [[-1, 4.8, 2.2], [-1, 4.8, 1.9]],
               [[-1, 4.5, 1.9], [-1, 4.8, 1.9]],
               [[-1, 4.5, 2.2], [-1, 4.8, 2.2]],
               [[-1, 4.5, 2.2], [-1, 4.5, 1.9]],
               [[3, 4.8, 2.2], [3, 4.8, 1.9]],
               [[3, 4.5, 1.9], [3, 4.8, 1.9]],
               [[3, 4.5, 2.2], [3, 4.8, 2.2]],
               [[3, 4.5, 2.2], [3, 4.5, 1.9]],
               [[3, 4.8, 2.2], [-1, 4.8, 2.2]],
               [[-1, 4.5, 1.9], [3, 4.5, 1.9]],
               [[3, 4.8, 1.9], [-1, 4.8, 1.9]],
               [[3, 4.5, 2.2], [-1, 4.5, 2.2]],

               [[-1, -4.8, 2.2], [-1, -4.8, 1.9]],
               [[-1, -4.5, 1.9], [-1, -4.8, 1.9]],
               [[-1, -4.5, 2.2], [-1, -4.8, 2.2]],
               [[-1, -4.5, 2.2], [-1, -4.5, 1.9]],
               [[3, -4.8, 2.2], [3, -4.8, 1.9]],
               [[3, -4.5, 1.9], [3, -4.8, 1.9]],
               [[3, -4.5, 2.2], [3, -4.8, 2.2]],
               [[3, -4.5, 2.2], [3, -4.5, 1.9]],
               [[3, -4.8, 2.2], [-1, -4.8, 2.2]],
               [[-1, -4.5, 1.9], [3, -4.5, 1.9]],
               [[3, -4.8, 1.9], [-1, -4.8, 1.9]],
               [[3, -4.5, 2.2], [-1, -4.5, 2.2]],                
               ]
        player_bullets = []
        opp_bullets = []   
        self.res = 0
        # данные наблюдателя - позиция и угол
        cam = (0, 0, 0)
        cam_a = (0, 0)
        cadr = 1
        pv = 0
        killed_ships = 0
        xc = 550
        yc = 350
        running = True
        k = 0
        clock = pygame.time.Clock()
        mbd = 0
        vcm = 0.1
        # угол обзора в градусах
        vax = 90
        vc = xc / vax * 2
        
        while running:
             # перемещение
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == 112:
                        pv = 1 - pv
                    elif event.key == pygame.K_ESCAPE:
                        last_pressed_button = None
                        pygame.mouse.set_visible(True)
                        if not menu_screen():
                            self.res = -1
                            fps = 0
                            running = False
                        else:
                            break                    
                    elif event.key == pygame.K_LEFT:
                        k = -1
                    elif event.key == pygame.K_RIGHT:
                        k = 1
                    elif event.key == pygame.K_UP:
                        k = 3
                    elif event.key == pygame.K_DOWN:
                        k = -3
                    elif event.key == 97:
                        k = 4
                    elif event.key == 100:
                        k = -4
                    elif event.key == 119:
                        k = 5 
                    elif event.key == 115:
                        k = -5
                elif event.type == pygame.KEYUP:
                    k = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mbd = 1- mbd
                elif mbd == 1 and event.type == pygame.MOUSEMOTION:
                    cam_a = (min(45, max(-45, cam_a[0] + event.rel[0]*vcm)), min(45, max(-45, cam_a[1] - event.rel[1]*vcm)))
        
            screen.fill(pygame.Color('black'))
            cam = (cam[0]+1, cam[1], cam[2])
            
            if random.randrange(opp_ver) == 0 or opponents == []:
                opponents.append([cam[0] + 1000, random.randrange(101)-50, random.randrange(101)-50])
            if cadr % bull_sp == 0:
                if pv == 1:
                    cam = [cam[0]+20, cam[1], cam[2]-3]
                    player_bullets.append([cam[0]-2, cam[1]+4.7, cam[2] + 2, cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]-2, cam[1]-4.7, cam[2] +2, cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]-2, cam[1]+4.7, cam[2]- 2, cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]-2, cam[1]-4.7, cam[2] - 2, cam_a[0], cam_a[1]])
                else:
                    player_bullets.append([cam[0]-2, cam[1]+4.7, cam[2] -1, cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]-2, cam[1]-4.7, cam[2]-1, cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]-2, cam[1]+4.7, cam[2]-5, cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]-2, cam[1]-4.7, cam[2] -5, cam_a[0], cam_a[1]])                    
                if pv == 1:
                    cam = [cam[0]-20, cam[1], cam[2]+3]
            if random.randrange(opp_bul_ver) == 0:
                pos = opponents[random.randrange(len(opponents))]
                opp_bullets.append((pos[0]-6, pos[1]-4.75, pos[2]-2))
                opp_bullets.append((pos[0]-6, pos[1]-4.75, pos[2]+2))
                opp_bullets.append((pos[0]-6, pos[1]+4.75, pos[2]-2))
                opp_bullets.append((pos[0]-6, pos[1]+4.75, pos[2]+2))
            if k == 1:
                cam = (cam[0], max(-50, cam[1] - 1), cam[2])
            elif k == -1:
                cam = (cam[0], min(50, cam[1] + 1), cam[2])
            elif k == 3:
                cam = (cam[0], cam[1], min(50, cam[2]+1))
            elif k == -3:
                cam = (cam[0], cam[1], max(-50, cam[2]-1))
            elif k == 4:
                cam_a = (max(-45, cam_a[0] - 1), cam_a[1])
            elif k == -4:
                cam_a = (min(45, cam_a[0] + 1), cam_a[1])
            elif k == -5:
                cam_a = (cam_a[0], max(-45, cam_a[1] - 1))
            elif k == 5:
                cam_a = (cam_a[0], min(45, cam_a[1] + 1))
            if pv == 1:
                cam = [cam[0]-15, cam[1], cam[2]+3]            
            for wall in [[[cam[0] + 1000, 60, 60], [cam[0] + 1000, -60, 60], [cam[0],-100, 200], [cam[0],100, 200]],
                        [[cam[0] + 1000, 60, 60], [cam[0] + 1000, 60, -60], [cam[0],100, -200], [cam[0],100, 200]],
                        [[cam[0] + 1000, -60, -60], [cam[0] + 1000, 60, -60], [cam[0],100, -200], [cam[0],-100, -200]],
                        [[cam[0] + 1000, -60, -60], [cam[0] + 1000, -60, 60], [cam[0],-100, 200], [cam[0],-100, -200]]]:
                poly = []
                for i in wall:
                    if len(i) == 3:
                        xs, ys = angle(cam, cam_a, i)
                        poly.append((int(xc - xs * vc), int(yc - ys * vc)))                        
                    else:
                        poly.append(i)
                
                pygame.draw.line(screen, (155, 155, 155), poly[1], poly[0], 1)
                pygame.draw.line(screen, (155, 155, 155), poly[1], poly[2], 1)
                pygame.draw.line(screen, (155, 155, 155), poly[0], poly[3], 1)
        
            for i in opponents:
                s = ((cam[0] - i[0])**2 + (cam[1] - i[1])**2 + (cam[2] - i[2])**2)**0.5                
                for p in opp:
                    r = angle(cam, cam_a, (i[0]+p[0][0], i[1]+p[0][1], i[2]+p[0][2]))
                    r1 = angle(cam, cam_a, (i[0]+p[1][0], i[1]+p[1][1], i[2]+p[1][2]))
                    pygame.draw.line(screen, (255, 255, 0), (int(xc - r[0] * vc), int(yc - r[1] * vc)), (int(xc - r1[0] * vc), int(yc - r1[1] * vc)), 1)
            if pv == 1: 
                i = [cam[0]+15, cam[1], cam[2]-3]       
                for p in opp:
                    r = angle(cam, cam_a, (i[0]-p[0][0], i[1]+p[0][1], i[2]+p[0][2]))
                    r1 = angle(cam, cam_a, (i[0]-p[1][0], i[1]+p[1][1], i[2]+p[1][2]))
                    pygame.draw.line(screen, (255, 255, 0), (int(xc - r[0] * vc), int(yc - r[1] * vc)), (int(xc - r1[0] * vc), int(yc - r1[1] * vc)), 1) 
            
                cam = [cam[0]+15, cam[1], cam[2]-3]
            
            w = 0
            for opponent in range(len(opponents)):
                if abs(opponents[opponent-w][0]- cam[0]) < 5 and abs(opponents[opponent-w][1]- cam[1]) < 5 and abs(opponents[opponent-w][2]- cam[2]) < 5 :
                    self.res = 0
                    running = False  
                    
                f = 0
                for j in range(len(player_bullets)):
                    if f == 0 and ((player_bullets[j][0] - opponents[opponent-w][0])**2 + (player_bullets[j][1] - opponents[opponent-w][1])**2+(player_bullets[j][2] - opponents[opponent-w][2])**2)**0.5 < 10:
                        killed_ships += 1
                        del player_bullets[j]
                        del opponents[opponent-w]
                        w += 1
                        f = 1
                
                if f == 0 and opponents[opponent-w][0] < cam[0] - 00:
                    del opponents[opponent-w]
                    w += 1                    
            w = 0
            for player_bullet in range(len(player_bullets)):
                xs, ys = angle(cam, cam_a, player_bullets[player_bullet-w])
                s = ((cam[0] -  player_bullets[player_bullet-w][0])**2 + (cam[1] -  player_bullets[player_bullet-w][1])**2 + (cam[2] -  player_bullets[player_bullet-w][2])**2)**0.5   
                if s < 300:
                    pygame.draw.circle(screen, (0,255,0), (int(xc - xs * vc), int(yc - ys * vc)), 10/s**0.4) 
                else:
                    screen.fill((0,255,0), (int(xc - xs * vc), int(yc - ys * vc), 1, 1))                    
                player_bullets[player_bullet-w] = (player_bullets[player_bullet-w][0]+5*math.cos(math.radians(player_bullets[player_bullet-w][3]*0.82)), 
                                                   player_bullets[player_bullet-w][1]-5*math.sin(math.radians(player_bullets[player_bullet-w][3]*0.82)), player_bullets[player_bullet-w][2]+5*math.sin(math.radians(player_bullets[player_bullet-w][4]*0.82)), player_bullets[player_bullet-w][3], player_bullets[player_bullet-w][4])
                if player_bullets[player_bullet-w][0] > cam[0] + 1100 or player_bullets[player_bullet-w][1] < -60 or player_bullets[player_bullet-w][1] > 60 or player_bullets[player_bullet-w][2]< -60 or player_bullets[player_bullet-w][2]> 60:
                    del player_bullets[player_bullet-w]
                    w += 1 
                    
            w = 0
            for opp_bullet in range(len(opp_bullets)):
                xs, ys = angle(cam, cam_a, opp_bullets[opp_bullet-w])
                s = ((cam[0] - opp_bullets[opp_bullet-w][0])**2 + (cam[1] - opp_bullets[opp_bullet-w][1])**2 + (cam[2] - opp_bullets[opp_bullet-w][2])**2)**0.5   
                if s < 600:
                    pygame.draw.circle(screen, (255, 0, 0), (int(xc - xs * vc), int(yc - ys * vc)), 20/s**0.4) 
                else:
                    screen.fill((255, 0, 0), (int(xc - xs * vc), int(yc - ys * vc), 1, 1))             
                    
                opp_bullets[opp_bullet-w] = (opp_bullets[opp_bullet-w][0]-1, opp_bullets[opp_bullet-w][1], opp_bullets[opp_bullet-w][2]) 
                if ((opp_bullets[opp_bullet-w][0]-cam[0])**2+(opp_bullets[opp_bullet-w][1]-cam[1])**2+(opp_bullets[opp_bullet-w][2]-cam[2])**2)**0.5 < 3:
                    del opp_bullets[opp_bullet-w]
                    w += 1
                    self.res = 0
                    
                    running = False  
                elif opp_bullets[opp_bullet-w][0] < cam[0] - 50:
                    del opp_bullets[opp_bullet-w]
                    w += 1
                    
            pygame.draw.rect(screen, (0,0,0), [1100, 0, 200, 700])   
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
            cadr += 1 
            if killed_ships >= k_k and cadr >= f_d:
                self.res = 1
                running = False            
            pygame.draw.circle(screen, (255, 0, 0), (int(xc), int(yc)), 3)
            pygame.display.flip()
            clock.tick(fps)
    
    
    
lvl = 10
nick_screen()
while True:
    start_screen()
    gaming = True
    while gaming:
        res = chooseD_screen()
        gaming2 = True
        if res == 3:
            while gaming2:
                spaceships_screen()
                res_game = Game_3d(1300, 700, 60, order + 1, 3, lvl, 100, 200, 6, 60).res
                if res_game == 1:
                    levelpass_screen(True, lvl // 10)
                    lvl += 10
                elif res_game == 0:
                    levelpass_screen(False, lvl // 10)
                    result = cur.execute("""SELECT lvl FROM rec
                                            WHERE nick == '""" + nickname + """'""").fetchall()
                    if lvl // 10 > result[0][0]:
                        cur.execute("""UPDATE rec
                        SET lvl = """ + str(lvl // 10) + """ 
                        WHERE nick == '""" + nickname + """'""").fetchall()
                        con.commit()
                    lvl = 10
        elif res == 2:
            while gaming2:
                spaceships_screen()
                if gaming2:
                    res_game = Game_2d(1300, 700, 60, order + 1, 3, lvl, 100, 100, 6, 60).res
                    if res_game == 1:
                        levelpass_screen(True, lvl // 10)
                        lvl += 10
                    elif res_game == 0:
                        levelpass_screen(False, lvl // 10)
                        result = cur.execute("""SELECT lvl FROM rec
                        WHERE nick == '""" + nickname + """'""").fetchall()
                        if lvl // 10 > result[0][0]:
                            cur.execute("""UPDATE rec
                            SET lvl = """ + str(lvl // 10) + """ 
                            WHERE nick == '""" + nickname + """'""").fetchall()
                            con.commit()
                        lvl = 10
pygame.quit()
con.close()
