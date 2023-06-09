from settings import *
import pygame
from random import randint
from data.weapon import weapon_img, weapon_arrow
from person import lords
from data.magic import magic
from damage.triangle import triangle
from damage.damage import calculate_damage


class Fight:
    def __init__(self, person, enemy, fight_images, not_my_fight=False):
        self.fight_img = fight_images
        self.img = None
        self.person = person
        self.enemy = enemy
        self.tick = 0

        self.person_dmg = calculate_damage(triangle, person, enemy)
        self.enemy_dmg = calculate_damage(triangle, enemy, person)
        if self.person_dmg < 0:
            self.person_dmg = 0
        if self.enemy_dmg < 0:
            self.enemy_dmg = 0

        self.person_hit = person.hit - enemy.avoid
        self.enemy_hit = enemy.hit - person.avoid
        if triangle(person.weapon.name, enemy.weapon.name) is None:
            pass
        elif triangle(person.weapon.name, enemy.weapon.name):
            self.person_hit += 15
            self.enemy_hit -= 15
        else:
            self.person_hit -= 15
            self.enemy_hit += 15

        self.moves = [True if randint(0, 100) <= self.person.crt else False,
                      True if randint(0, 100) <= (100 - self.person_hit) else False,
                      True if randint(0, 100) <= self.enemy.crt else False,
                      True if randint(0, 100) <= (100 - self.enemy_hit) else False]
        # self.moves = [False, True, False, True]

        self.person_count_attack = 1
        self.enemy_count_attack = 1 if not self.enemy.support else 0
        if self.enemy_count_attack == 0:
            self.without_enemy_attack = True
        else:
            self.without_enemy_attack = False

        self.distance_fight = False
        range_persons = abs(person.pos[0] - enemy.pos[0]) + abs(person.pos[1] - enemy.pos[1])
        if person.attack_speed - enemy.attack_speed >= 4:
            self.person_count_attack = 2
        elif enemy.attack_speed - person.attack_speed >= 4:
            self.enemy_count_attack = 2
        if range_persons not in enemy.weapon.range:
            self.enemy_count_attack = 0

        if person.weapon.name in ['brave_sword', 'brave_axe', 'brave_lance', 'brave_bow']:
            self.person_count_attack = self.person_count_attack * 2
        if enemy.weapon.name in ['brave_sword', 'brave_axe', 'brave_lance', 'brave_bow']:
            self.enemy_count_attack = self.enemy_count_attack * 2

        if range_persons > 1:
            self.distance_fight = True

        self.need_moves = [0, 0]
        self.attack_tick = 0
        self.cadr = 0
        self.dodge_tick = 0

        # weapon
        self.person_weapon_img = weapon_img[person.weapon.name]
        self.enemy_weapon_img = weapon_img[enemy.weapon.name]

        self.person_img_id = 0
        self.enemy_img_id = 0
        self.person_weapon_arrow = weapon_arrow['up' if triangle(person.weapon.name, enemy.weapon.name) else 'down']
        self.enemy_weapon_arrow = weapon_arrow['up' if triangle(enemy.weapon.name, person.weapon.name) else 'down']

        # magic
        self.magic_tick = 0
        self.magic_img_id = -1
        self.person_magic_cords = (1, 1)
        self.person_magic_cords_sms = (1, 1)
        self.enemy_magic_cords = (1, 1)
        self.enemy_magic_cords_sms = (1, 1)
        self.person_magic_effect = []
        self.enemy_magic_effect = []
        self.person_magic_effect_time = 0
        self.enemy_magic_effect_time = 0

        if person.weapon.class_ == 'magic':
            self.person_magic_cords = (magic[person.weapon.name]['x'], magic[person.weapon.name]['y'])
            self.person_magic_cords_sms = (magic[person.weapon.name]['x1'], magic[person.weapon.name]['y'])

            self.person_magic_effect = self.fight_img.magic_effects[person.weapon.name]['person']
            self.person_magic_effect_time = len(self.person_magic_effect) * 2
            self.person_magic_delay = magic[person.weapon.name]['delay']

        if enemy.weapon.class_ == 'magic':
            self.enemy_magic_cords = (magic[enemy.weapon.name]['x1'], magic[enemy.weapon.name]['y'])
            self.enemy_magic_cords_sms = (magic[enemy.weapon.name]['x'], magic[enemy.weapon.name]['y'])

            self.enemy_magic_effect = self.fight_img.magic_effects[enemy.weapon.name]['enemy']
            self.enemy_magic_effect_time = len(self.enemy_magic_effect) * 2
            self.enemy_magic_delay = magic[enemy.weapon.name]['delay']

        if not_my_fight:
            self.all_magic_effects = self.enemy_magic_effect + self.person_magic_effect
        else:
            self.all_magic_effects = self.person_magic_effect + self.enemy_magic_effect

        if self.distance_fight:
            if self.person_magic_cords != (0, 0):
                self.person_magic_cords = (self.person_magic_cords[0] + 200, self.person_magic_cords[1])
                self.person_magic_cords_sms = (self.person_magic_cords_sms[0] - 200, self.person_magic_cords_sms[1])
            if self.enemy_magic_cords != (0, 0):
                self.enemy_magic_cords = (self.enemy_magic_cords[0] - 200, self.enemy_magic_cords[1])
                self.enemy_magic_cords_sms = (self.enemy_magic_cords_sms[0] + 200, self.enemy_magic_cords_sms[1])

        # base
        self.fight_bg = pygame.image.load('templates/fight/bg.png').subsurface(2, 2, 240, 160)
        if self.distance_fight:
            self.fight_characters = pygame.image.load('templates/fight/distance_baze.png')
        else:
            self.fight_characters = pygame.image.load('templates/fight/baze.png')
        self.fight_bg = pygame.transform.scale(self.fight_bg, (1200, 800))
        self.fight_characters = pygame.transform.scale(self.fight_characters, (1200, 800))
        self.numbers = [pygame.transform.scale(
            pygame.image.load('templates/numbers/numbers.png').subsurface(i * 8, 0, 8, 8), (40, 40)) for i in range(10)]
        self.hp = [pygame.transform.scale(
            pygame.image.load('templates/fight/hp.png').subsurface(i * 2, 0, 2, 7), (10, 35)) for i in range(2)]

        # miss
        self.miss_tick = 0
        self.miss_img = [pygame.image.load(f'templates/miss/{i}.png') for i in range(0, 12)]
        for i in range(len(self.miss_img)):
            self.miss_img[i] = pygame.transform.scale(self.miss_img[i], (100, 100))
        self.miss_data = [-1, (0, 0)]

        # persons
        person_weapon_class = person.weapon.class_
        self.person_cant_crt = False
        if self.distance_fight:
            if range_persons in person.weapon.range:
                if person_weapon_class == 'axe' and 'distance_axe' in self.fight_img.images[person.name + '/' + person.class_]:
                    person_weapon_class = 'distance_axe'
                elif person_weapon_class == 'lance' and 'distance_lance' in self.fight_img.images[person.name + '/' + person.class_]:
                    person_weapon_class = 'distance_lance'
                    self.moves[0] = False
                    self.person_cant_crt = True
        enemy_weapon_class = enemy.weapon.class_
        self.enemy_cant_crt = False
        if self.distance_fight:
            if range_persons in enemy.weapon.range:
                if enemy_weapon_class == 'axe' and 'distance_axe' in self.fight_img.images[enemy.name + '/' + enemy.class_]:
                    enemy_weapon_class = 'distance_axe'
                elif enemy_weapon_class == 'lance' and 'distance_lance' in self.fight_img.images[enemy.name + '/' + enemy.class_]:
                    enemy_weapon_class = 'distance_lance'
                    self.moves[2] = False
                    self.enemy_cant_crt = True

        # files
        self.person_attack_img = self.fight_img.images[person.name + '/' + person.class_][person_weapon_class]['person']
        if person.name in lords:
            t_ = 'T1' if self.person.lvl < 10 else 'T2'
            self.person_index = self.fight_img.read(open(f'templates/persons/lords/{self.person.name}/battle/{t_}/'
                                                         f'{person_weapon_class}/Index.txt'), person_weapon_class)
            self.person_script, self.person_times = self.fight_img.read(open(f'templates/persons/lords/{self.person.name}/battle/{t_}/'
                                                                        f'{person_weapon_class}/Script.txt'), '', True)
        else:
            try:
                self.person_index = self.fight_img.read(open(f'templates/persons/other/{self.person.class_}/{person.name}/battle/'
                                                             f'{person_weapon_class}/Index.txt'), person_weapon_class)
                self.person_script, self.person_times = self.fight_img.read(open(f'templates/persons/other/{self.person.class_}/{person.name}/battle/'
                                                                                 f'{person_weapon_class}/Script.txt'), '', True)
            except:
                self.person_index = self.fight_img.read(open(f'templates/persons/other/{self.person.class_}/{person.gender}/battle/'
                                                             f'{person_weapon_class}/Index.txt'), person_weapon_class)
                self.person_script, self.person_times = self.fight_img.read(open(f'templates/persons/other/{self.person.class_}/{person.gender}/battle/'
                                                                            f'{person_weapon_class}/Script.txt'), '', True)
        self.person_stay_img = self.person_attack_img[0]

        self.enemy_attack_img = self.fight_img.images[enemy.name + '/' + enemy.class_][enemy_weapon_class]['enemy']
        if enemy.name in lords:
            t_ = 'T1' if self.enemy.lvl < 10 else 'T2'
            self.enemy_index = self.fight_img.read(open(f'templates/persons/lords/{self.enemy.name}/battle/{t_}/'
                                                        f'{enemy_weapon_class}/Index.txt'), enemy_weapon_class)
            self.enemy_script, self.enemy_times = self.fight_img.read(open(f'templates/persons/lords/{self.enemy.name}/battle/{t_}/'
                                                                      f'{enemy_weapon_class}/Script.txt'), '', True)
        else:
            try:
                self.enemy_index = self.fight_img.read(open(f'templates/persons/other/{self.enemy.class_}/{enemy.name}/battle/'
                                                            f'{enemy_weapon_class}/Index.txt'), enemy_weapon_class)
                self.enemy_script, self.enemy_times = self.fight_img.read(open(f'templates/persons/other/{self.enemy.class_}/{enemy.name}/battle/'
                                                                          f'{enemy_weapon_class}/Script.txt'), '', True)
            except:
                self.enemy_index = self.fight_img.read(open(f'templates/persons/other/{self.enemy.class_}/{enemy.gender}/battle/'
                                                            f'{enemy_weapon_class}/Index.txt'), enemy_weapon_class)
                self.enemy_script, self.enemy_times = self.fight_img.read(open(f'templates/persons/other/{self.enemy.class_}/{enemy.gender}/battle/'
                                                                               f'{enemy_weapon_class}/Script.txt'), '', True)
        self.enemy_stay_img = self.enemy_attack_img[0]

        self.img = self.person_stay_img
        self.img_ = self.enemy_stay_img

        self.person_dmg_time = self.person_times['critical' if self.moves[0] else 'attack']
        self.enemy_dmg_time = self.enemy_times['critical' if self.moves[2] else 'attack']

        self.person_x, self.person_y = self.person_index[0][0][4] + 100, self.person_index[0][0][5] + 200
        self.enemy_x, self.enemy_y = self.enemy_index[0][0][4] + 100 + 300, self.enemy_index[0][0][5] + 200

        # attack time
        self.person_attack_time = sum([i[1] for i in self.person_script['critical' if self.moves[0] else 'attack']])
        self.enemy_attack_time = sum([i[1] for i in self.enemy_script['critical' if self.moves[2] else 'attack']])

        # time
        self.start_enemy_attack = 50 + self.person_attack_time + 100

        self.person_dmg_tick = 50 + self.person_dmg_time
        self.enemy_dmg_tick = self.start_enemy_attack + self.enemy_dmg_time

        if self.person.weapon.class_ == 'magic':
            self.end = self.start_enemy_attack + max(self.enemy_magic_effect_time, self.enemy_attack_time) + 50
        else:
            self.end = self.start_enemy_attack + self.enemy_attack_time + 50

        self.cadr = 0
        self.cadr_tick = 0
        self.script_navigator = 0

        self.dead_tick = 0
        self.death_opacity = [0, 20, 20, 20, 20, 44, 44, 44, 44, 64,
                              64, 64, 64, 84, 84, 84, 108, 108, 108, 108,
                              128, 128, 128, 128, 148, 148, 148, 148, 172, 172,
                              172, 192, 192, 192, 192, 212, 212, 212, 212, 236,
                              236, 236, 236, 255, 255, 255, 0, 0, 0, 0,
                              0, 0, 255, 0, 0, 0, 0, 0, 0, 255,
                              0, 0, 0, 0, 0, 0, 255, 0, 0, 0,
                              0, 0, 0, 255, 0, 0, 0, 0, 0, 0,
                              255, 0, 0, 0, 0, 0, 0]
        self.person_dead = False
        self.enemy_dead = False

        # fonts
        self.f1 = pygame.font.Font(None, 30)
        self.f2 = pygame.font.Font(None, 50)
        self.f3 = pygame.font.Font(None, 70)

    def attack(self, script, person=True):
        self.cadr_tick += 1
        if self.cadr_tick == script[self.script_navigator][1]:
            self.cadr = script[self.script_navigator][0]
            self.cadr_tick = 0
            self.script_navigator += 1
            if self.script_navigator == len(script):
                self.script_navigator = 0
                self.cadr = 0
                self.cadr_tick = 0
        return self.person_attack_img[self.cadr] if person else self.enemy_attack_img[self.cadr]

    def miss(self):
        self.miss_tick += 1
        if self.miss_tick < 22:
            img = self.miss_img[self.miss_tick % 22 // 2]
            self.miss_data[0] = self.miss_tick % 22 // 2
        else:
            img = self.miss_img[11]
            self.miss_data[0] = 11

        if self.miss_tick > 40:
            self.miss_tick = 0
        return img

    def draw_persons(self, screen, first_enemy):
        if first_enemy:
            for i in range(len(self.img)):
                if self.tick < self.start_enemy_attack:
                    c_ = (1550 - self.person_index[self.cadr][i][2] * 5 - self.person_index[self.cadr][i][4] * 5 -
                          (200 if self.distance_fight else 0), self.person_index[self.cadr][i][5] * 5 + 250)
                else:
                    c_ = (1550 - self.person_index[0][i][2] * 5 - self.person_index[0][i][4] * 5 -
                          (200 if self.distance_fight else 0), self.person_index[0][i][5] * 5 + 250)
                screen.blit(self.img[i], c_)

            for i in range(len(self.img_)):
                if self.tick > self.start_enemy_attack:
                    c_ = (self.enemy_index[self.cadr][i][4] * 5 + (580 if self.distance_fight else 380),
                          self.enemy_index[self.cadr][i][5] * 5 + 250)
                else:
                    c_ = (self.enemy_index[0][i][4] * 5 + (580 if self.distance_fight else 380),
                          self.enemy_index[0][i][5] * 5 + 250)
                screen.blit(self.img_[i], c_)
        else:
            for i in range(len(self.img_)):
                if self.tick > self.start_enemy_attack:
                    c_ = (self.enemy_index[self.cadr][i][4] * 5 + (580 if self.distance_fight else 380),
                          self.enemy_index[self.cadr][i][5] * 5 + 250)
                else:
                    c_ = (self.enemy_index[0][i][4] * 5 + (580 if self.distance_fight else 380),
                          self.enemy_index[0][i][5] * 5 + 250)
                screen.blit(self.img_[i], c_)

            for i in range(len(self.img)):
                if self.tick < self.start_enemy_attack:
                    c_ = (1550 - self.person_index[self.cadr][i][2] * 5 - self.person_index[self.cadr][i][4] * 5 -
                          (200 if self.distance_fight else 0), self.person_index[self.cadr][i][5] * 5 + 250)
                else:
                    c_ = (1550 - self.person_index[0][i][2] * 5 - self.person_index[0][i][4] * 5 -
                          (200 if self.distance_fight else 0), self.person_index[0][i][5] * 5 + 250)
                screen.blit(self.img[i], c_)

    def render_base_for_fight(self, screen):
        x_, y_ = 360, 240

        # bg
        screen.fill(BLACK)
        screen.blit(self.fight_bg, (x_, y_))
        screen.blit(self.fight_characters, (x_, y_))

        # characters person
        text_name = self.f3.render(self.person.name, True, WHITE)
        screen.blit(text_name, (50 + x_, 50 + y_))

        if self.person.support:
            hit, dmg, crt = '', '', ''
        else:
            hit = str(self.person_hit) if self.person_hit > 0 else f'0{self.person_hit}'
            dmg = str(self.person_dmg) if self.person_dmg > 9 else f'0{self.person_dmg}'
            crt = str(self.person.crt) if self.person.crt > 9 else f'0{self.person.crt}'
        for i in range(len(hit)):
            if len(hit) < 3:
                screen.blit(self.numbers[int(hit[i])], (120 + i * 40 + x_, 560 + y_))
            else:
                screen.blit(self.numbers[int(hit[i])], (80 + i * 40 + x_, 560 + y_))
        for i in range(len(dmg)):
            screen.blit(self.numbers[int(dmg[i])], (120 + i * 40 + x_, 600 + y_))
        for i in range(len(crt)):
            screen.blit(self.numbers[int(crt[i])], (120 + i * 40 + x_, 640 + y_))

        # characters enemy
        text_name = self.f3.render(self.enemy.name, True, WHITE)
        screen.blit(text_name, (1000 + x_, 50 + y_))

        if self.without_enemy_attack or self.person.support:
            hit, dmg, crt = '', '', ''
        else:
            hit = str(self.enemy_hit) if self.enemy_hit > 0 else f'0{self.enemy_hit}'
            dmg = str(self.enemy_dmg) if self.enemy_dmg > 9 else f'0{self.enemy_dmg}'
            crt = str(self.enemy.crt) if self.enemy.crt > 9 else f'0{self.enemy.crt}'
        for i in range(len(hit)):
            if len(hit) < 3:
                screen.blit(self.numbers[int(hit[i])], (1115 + i * 40 + x_, 560 + y_))
            else:
                screen.blit(self.numbers[int(hit[i])], (1075 + i * 40 + x_, 560 + y_))
        for i in range(len(dmg)):
            screen.blit(self.numbers[int(dmg[i])], (1115 + i * 40 + x_, 600 + y_))
        for i in range(len(crt)):
            screen.blit(self.numbers[int(crt[i])], (1115 + i * 40 + x_, 640 + y_))

        # hp
        text_hp = str(self.person.hp) if self.person.hp > 0 else '0'
        for i in range(len(text_hp)):
            screen.blit(self.numbers[int(text_hp[i])], (20 + i * 40 + x_, 725 + y_))

        for i in range(2 if self.person.max_hp > 45 else 1):
            if self.person.max_hp > 45:
                for j in range(0, 45):
                    screen.blit(self.hp[0 if j + i * 45 < self.person.hp else 1],
                                (110 + j * 10 + x_, 705 + y_ if i == 0 else 745 + y_))
            else:
                for j in range(0, self.person.max_hp):
                    screen.blit(self.hp[0 if j < self.person.hp else 1],
                                (110 + j * 10 + x_, 726 + y_))

        text_hp = str(self.enemy.hp) if self.enemy.hp > 0 else '0'
        for i in range(len(text_hp)):
            screen.blit(self.numbers[int(text_hp[i])], (630 + i * 40 + x_, 725 + y_))
        for i in range(2 if self.enemy.max_hp > 45 else 1):
            if self.enemy.max_hp > 45:
                for j in range(0, 45):
                    screen.blit(self.hp[0 if j + i * 45 < self.enemy.hp else 1],
                                (720 + j * 10 + x_, 705 + y_ if i == 0 else 745 + y_))
            else:
                for j in range(0, self.enemy.max_hp):
                    screen.blit(self.hp[0 if j < self.enemy.hp else 1],
                                (720 + j * 10 + x_, 726 + y_))

        # weapon
        screen.blit(self.person_weapon_img, (220 + x_, 608 + y_))
        screen.blit(self.enemy_weapon_img, (620 + x_, 608 + y_))
        screen.blit(self.person_weapon_arrow[self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (272 + x_, 635 + y_))
        screen.blit(self.enemy_weapon_arrow[self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (672 + x_, 635 + y_))
        text1 = self.f2.render(self.person.weapon.name, True, BLACK)
        text2 = self.f2.render(self.enemy.weapon.name, True, BLACK)
        screen.blit(text1, (310 + x_, 625 + y_))
        screen.blit(text2, (710 + x_, 625 + y_))

        return x_, y_

    def render_fight(self, screen):
        self.tick += 1

        # deal damage
        for person in [self.person] + [self.enemy]:
            if person.damage_for_me > 0:
                person.hp -= 1
                person.damage_for_me -= 1

        if self.person.hp <= 0 and not self.person_dead:
            if self.dead_tick < len(self.death_opacity) - 1:
                for i in self.img:
                    i.set_alpha(self.death_opacity[self.dead_tick])
            self.dead_tick += 1
            if self.dead_tick == len(self.death_opacity):
                self.person_dead = True
                self.dead_tick = 0

        if self.enemy.hp <= 0 and not self.enemy_dead:
            if self.dead_tick < len(self.death_opacity) - 1:
                for i in self.img_:
                    i.set_alpha(self.death_opacity[self.dead_tick])
            self.dead_tick += 1
            if self.dead_tick == len(self.death_opacity):
                self.enemy_dead = True
                self.dead_tick = 0

        if self.tick <= 50:
            pass
        else:
            # person
            if self.tick <= 50 + self.person_attack_time and not any([self.enemy_dead, self.person_dead]):
                self.img = self.attack(self.person_script['critical' if self.moves[0] else 'attack'])
            else:
                self.img = self.person_stay_img
            # enemy
            if (self.tick >= self.start_enemy_attack) and \
                    (self.tick <= self.start_enemy_attack + self.enemy_attack_time) and not any([self.enemy_dead, self.person_dead]):
                self.img_ = self.attack(self.enemy_script['critical' if self.moves[2] else 'attack'], False)
            else:
                self.img_ = self.enemy_stay_img

            # damage
            if not self.moves[1]:
                if self.tick == self.person_dmg_tick + 5:
                    k_ = 3 if self.moves[0] else 1
                    self.enemy.damage_for_me = self.person_dmg * k_

            if not self.moves[3]:
                if self.tick == self.enemy_dmg_tick + 5:
                    k_ = 3 if self.moves[2] else 1
                    self.person.damage_for_me = self.enemy_dmg * k_

        # magic effect
        magic_img = None
        if self.person.weapon.name in self.fight_img.magic_effects:
            if (self.tick > 55 + self.person_magic_delay) and \
                    (self.tick <= 55 + self.person_magic_delay + self.person_magic_effect_time):
                self.magic_tick += 1
                magic_img = self.person_magic_effect[
                    self.magic_tick % self.person_magic_effect_time // 2]
                if self.tick == 55 + self.person_magic_delay + self.person_magic_effect_time:
                    self.magic_tick = 0
                    magic_img = None

        if self.enemy.weapon.name in self.fight_img.magic_effects:
            if (self.tick > self.start_enemy_attack + self.enemy_magic_delay) and \
                    (self.tick <= self.start_enemy_attack + self.enemy_magic_delay +
                     self.enemy_magic_effect_time):
                self.magic_tick += 1
                magic_img = self.enemy_magic_effect[
                    self.magic_tick % self.enemy_magic_effect_time // 2]
                if self.tick == self.start_enemy_attack + self.enemy_magic_delay + \
                        self.enemy_magic_effect_time:
                    self.magic_tick = 0
                    magic_img = None

        if self.tick < self.start_enemy_attack:
            cords_ = self.person_magic_cords_sms
        else:
            cords_ = self.enemy_magic_cords_sms

        # fight base
        x_, y_ = self.render_base_for_fight(screen)

        # persons
        self.draw_persons(screen, self.tick > self.start_enemy_attack)

        self.person_img_id = self.person_attack_img.index(self.img)
        self.enemy_img_id = self.enemy_attack_img.index(self.img_)

        # miss
        self.miss_data[0] = -1
        if self.moves[1]:
            if (self.tick > self.person_dmg_tick) and (
                    self.tick <= self.person_dmg_tick + 40):
                screen.blit(self.miss(), (1450, 550))
                self.miss_data[1] = (450, 600)
        if self.moves[3]:
            if (self.tick > self.enemy_dmg_tick) and (
                    self.tick <= self.enemy_dmg_tick + 40):
                screen.blit(self.miss(), (450, 600))
                self.miss_data[1] = (1450, 550)

        # magic
        if magic_img is not None:
            screen.blit(magic_img, (self.person_magic_cords[0] + x_, self.person_magic_cords[1] + y_)
            if self.tick < self.start_enemy_attack
            else (self.enemy_magic_cords[0] + x_, self.enemy_magic_cords[1] + y_))
            self.magic_img_id = self.all_magic_effects.index(magic_img)
        else:
            self.magic_img_id = -1

        # end
        if self.tick == 10 + self.person_attack_time:
            self.person_count_attack -= 1
        elif self.tick == self.start_enemy_attack + self.enemy_attack_time:
            self.enemy_count_attack -= 1

        if self.person_dead or self.enemy_dead:
            self.dead_tick -= 1
            if self.dead_tick == -50:
                return None
        elif self.tick == self.start_enemy_attack:
            if self.enemy_count_attack == 0 and self.person_count_attack == 0:
                return None
            elif self.enemy_count_attack == 0 and self.person_count_attack > 0:
                self.tick = 2
                self.cadr = 0
                self.script_navigator = 0
                self.cadr_tick = 0
                self.moves = [True if randint(0, 100) <= self.person.crt and not self.person_cant_crt else False,
                              True if randint(0, 100) <= (100 - self.person_hit) else False,
                              True if randint(0, 100) <= self.enemy.crt and not self.enemy_cant_crt else False,
                              True if randint(0, 100) <= (100 - self.enemy_hit) else False]

                # time
                self.person_dmg_time = self.person_times['critical' if self.moves[0] else 'attack']
                self.enemy_dmg_time = self.enemy_times['critical' if self.moves[2] else 'attack']
                self.person_attack_time = sum(
                    [i[1] for i in self.person_script['critical' if self.moves[0] else 'attack']])
                self.enemy_attack_time = sum(
                    [i[1] for i in self.enemy_script['critical' if self.moves[2] else 'attack']])
                self.start_enemy_attack = 50 + self.person_attack_time + 100

                self.person_dmg_tick = 50 + self.person_dmg_time
                self.enemy_dmg_tick = self.start_enemy_attack + self.enemy_dmg_time

                if self.person.weapon.class_ == 'magic':
                    self.end = self.start_enemy_attack + max(self.enemy_magic_effect_time, self.enemy_attack_time) + 50
                else:
                    self.end = self.start_enemy_attack + self.enemy_attack_time + 50
        else:
            if self.tick > self.end:
                if self.person_count_attack == 0 and self.enemy_count_attack == 0:
                    return None
                elif self.person_count_attack > 0:
                    self.tick = 2
                    self.cadr = 0
                    self.script_navigator = 0
                    self.cadr_tick = 0
                    self.moves = [True if randint(0, 100) <= self.person.crt and not self.person_cant_crt else False,
                                  True if randint(0, 100) <= (100 - self.person_hit) else False,
                                  True if randint(0, 100) <= self.enemy.crt and not self.enemy_cant_crt else False,
                                  True if randint(0, 100) <= (100 - self.enemy_hit) else False]

                    # time
                    self.person_dmg_time = self.person_times['critical' if self.moves[0] else 'attack']
                    self.enemy_dmg_time = self.enemy_times['critical' if self.moves[2] else 'attack']
                    self.person_attack_time = sum(
                        [i[1] for i in self.person_script['critical' if self.moves[0] else 'attack']])
                    self.enemy_attack_time = sum(
                        [i[1] for i in self.enemy_script['critical' if self.moves[2] else 'attack']])
                    self.start_enemy_attack = 50 + self.person_attack_time + 100

                    self.person_dmg_tick = 50 + self.person_dmg_time
                    self.enemy_dmg_tick = self.start_enemy_attack + self.enemy_dmg_time

                    if self.person.weapon.class_ == 'magic':
                        self.end = self.start_enemy_attack + max(self.enemy_magic_effect_time,
                                                                 self.enemy_attack_time) + 50
                    else:
                        self.end = self.start_enemy_attack + self.enemy_attack_time + 50

                elif self.enemy_count_attack > 0:
                    self.tick = self.start_enemy_attack
                    self.cadr = 0
                    self.script_navigator = 0
                    self.cadr_tick = 0
                    self.moves = [True if randint(0, 100) <= self.person.crt and not self.person_cant_crt else False,
                                  True if randint(0, 100) <= (100 - self.person_hit) else False,
                                  True if randint(0, 100) <= self.enemy.crt and not self.enemy_cant_crt else False,
                                  True if randint(0, 100) <= (100 - self.enemy_hit) else False]

                    # time
                    self.person_dmg_time = self.person_times['critical' if self.moves[0] else 'attack']
                    self.enemy_dmg_time = self.enemy_times['critical' if self.moves[2] else 'attack']
                    self.person_attack_time = sum(
                        [i[1] for i in self.person_script['critical' if self.moves[0] else 'attack']])
                    self.enemy_attack_time = sum(
                        [i[1] for i in self.enemy_script['critical' if self.moves[2] else 'attack']])
                    self.start_enemy_attack = 50 + self.person_attack_time + 100

                    self.person_dmg_tick = 50 + self.person_dmg_time
                    self.enemy_dmg_tick = self.start_enemy_attack + self.enemy_dmg_time

                    if self.person.weapon.class_ == 'magic':
                        self.end = self.start_enemy_attack + max(self.enemy_magic_effect_time,
                                                                 self.enemy_attack_time) + 50
                    else:
                        self.end = self.start_enemy_attack + self.enemy_attack_time + 50
        return cords_

    def render_not_my_fight(self, screen, effects_data):
        self.tick += 1
        magic_data, miss_data, opacity = effects_data
        opacity = opacity[0]

        # fight base
        x_, y_ = self.render_base_for_fight(screen)

        # person
        for i in range(len(self.person_attack_img[self.person_img_id])):
            img = self.person_attack_img[self.person_img_id][i]
            if (self.person.hp <= 0) and (opacity > 0):
                img.set_alpha(self.death_opacity[opacity])
            c_ = (1550 - self.person_index[self.person_img_id][i][2] * 5 - self.person_index[self.person_img_id][i][4] * 5 -
                  (200 if self.distance_fight else 0), self.person_index[self.person_img_id][i][5] * 5 + 250)
            screen.blit(img, c_)

        # enemy
        for i in range(len(self.enemy_attack_img[self.enemy_img_id])):
            img = self.enemy_attack_img[self.enemy_img_id][i]
            if (self.enemy.hp <= 0) and (opacity > 0):
                img.set_alpha(self.death_opacity[opacity])
            c_ = (self.enemy_index[self.enemy_img_id][i][4] * 5 + (580 if self.distance_fight else 380),
                  self.enemy_index[self.enemy_img_id][i][5] * 5 + 250)
            screen.blit(img, c_)

        # magic
        id_, x__, y__ = magic_data[0], magic_data[1], magic_data[2]
        if id_ >= 0:
            screen.blit(self.all_magic_effects[id_], (x__ + x_, y__ + y_))

        # miss
        id_, x__, y__ = miss_data[0], miss_data[1], miss_data[2]
        if id_ >= 0:
            screen.blit(self.miss_img[id_], (x__, y__))


class Support(Fight):
    def __init__(self, person, target, fight_images):
        super().__init__(person, target, fight_images)
        self.person = person
        self.target = target

        self.person_heal = 10 + self.person.mag
        self.person_heal_tick = 50 + 25  # ~
        self.end = 50 + self.person_attack_time + 50

    def render_support(self, screen):
        self.tick += 1

        # healing
        if self.target.heal_to_me > 0 and self.tick % 2 == 0:
            if self.target.hp < self.target.max_hp:
                self.target.hp += 1
            self.target.heal_to_me -= 1

        if self.tick <= 50:
            pass
        else:
            # person
            if self.tick <= 50 + self.person_attack_time:
                self.img = self.attack(self.person_script['attack'])
            else:
                self.img = self.person_stay_img

            # heal
            if self.person.weapon.name == 'heal':
                if self.tick == self.person_heal_tick + 5:
                    self.enemy.heal_to_me = self.person_heal

        # magic effect
        # magic_img = None
        # if self.person.weapon.name in self.fight_img.magic_effects:
        #     if (self.tick > 55 + self.person_magic_delay) and \
        #             (self.tick <= 55 + self.person_magic_delay + self.person_magic_effect_time):
        #         self.magic_tick += 1
        #         magic_img = self.person_magic_effect[
        #             self.magic_tick % self.person_magic_effect_time // 2]
        #         if self.tick == 55 + self.person_magic_delay + self.person_magic_effect_time:
        #             self.magic_tick = 0
        #             magic_img = None
        #
        # if self.enemy.weapon.name in self.fight_img.magic_effects:
        #     if (self.tick > self.start_enemy_attack + self.enemy_magic_delay) and \
        #             (self.tick <= self.start_enemy_attack + self.enemy_magic_delay +
        #              self.enemy_magic_effect_time):
        #         self.magic_tick += 1
        #         magic_img = self.enemy_magic_effect[
        #             self.magic_tick % self.enemy_magic_effect_time // 2]
        #         if self.tick == self.start_enemy_attack + self.enemy_magic_delay + \
        #                 self.enemy_magic_effect_time:
        #             self.magic_tick = 0
        #             magic_img = None
        #
        # if self.tick < self.start_enemy_attack:
        #     cords_ = self.person_magic_cords_sms
        # else:
        #     cords_ = self.enemy_magic_cords_sms

        # fight base
        x_, y_ = self.render_base_for_fight(screen)

        # persons
        self.draw_persons(screen, False)

        self.person_img_id = self.person_attack_img.index(self.img)
        self.enemy_img_id = self.enemy_attack_img.index(self.img_)

        # magic
        # if magic_img is not None:
        #     screen.blit(magic_img, (self.person_magic_cords[0] + x_, self.person_magic_cords[1] + y_)
        #     if self.tick < self.start_enemy_attack
        #     else (self.enemy_magic_cords[0] + x_, self.enemy_magic_cords[1] + y_))
        #     self.magic_img_id = self.all_magic_effects.index(magic_img)
        # else:
        #     self.magic_img_id = -1

        # end
        if self.tick >= self.end:
            return None
        return x_, y_