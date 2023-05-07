from settings import *
import pygame
from random import randint

sizes = {'roy': [{'width': 124,
                  'height': 102,
                  'w': 11,
                  'h': 8,
                  'frames': 82,
                  'x': 205,
                  'y': 70,
                  'x1': 420,
                  'size': (550, 450),
                  'dmg_time': 100},

                 {'width': 142,
                  'height': 102,
                  'w': 12,
                  'h': 8,
                  'frames': 96,
                  'x': 130,
                  'y': 70,
                  'x1': 410,
                  'size': (650, 450),
                  'dmg_time': 140}],

         'lyn': [{'width': 118,
                  'height': 119,
                  'w': 7,
                  'h': 6,
                  'frames': 37,
                  'x': 280,
                  'y': 55,
                  'x1': 390,
                  'size': (530, 530),
                  'dmg_time': 40},

                 {'width': 220,
                  'height': 144,
                  'w': 9,
                  'h': 13,
                  'frames': 115,
                  'x': 60,
                  'y': 90,
                  'x1': 160,
                  'size': (970, 650),
                  'dmg_time': 110}],

         'hector': [{'width': 117,
                     'height': 99,
                     'w': 7,
                     'h': 6,
                     'frames': 33,
                     'x': 230,
                     'y': 110,
                     'x1': 455,
                     'size': (530, 450),
                     'dmg_time': 60},

                    {'width': 118,
                     'height': 99,
                     'w': 7,
                     'h': 6,
                     'frames': 32,
                     'x': 230,
                     'y': 110,
                     'x1': 435,
                     'size': (530, 450),
                     'dmg_time': 60}],

         'eirika': [{'width': 114,
                     'height': 67,
                     'w': 6,
                     'h': 5,
                     'frames': 28,
                     'x': 240,
                     'y': 220,
                     'x1': 450,
                     'size': (515, 300),
                     'dmg_time': 35},

                    {'width': 116,
                     'height': 70,
                     'w': 6,
                     'h': 6,
                     'frames': 32,
                     'x': 240,
                     'y': 225,
                     'x1': 450,
                     'size': (515, 300),
                     'dmg_time': 45}],

         'eliwood': [{'width': 144,
                      'height': 106,
                      'w': 7,
                      'h': 6,
                      'frames': 40,
                      'x': 220,
                      'y': 50,
                      'x1': 330,
                      'size': (650, 480),
                      'dmg_time': 60},

                     {'width': 205,
                      'height': 126,
                      'w': 8,
                      'h': 8,
                      'frames': 59,
                      'x': 95,
                      'y': 50,
                      'x1': 180,
                      'size': (920, 570),
                      'dmg_time': 120}],

         'marth': [{'width': 96,
                    'height': 67,
                    'w': 8,
                    'h': 4,
                    'frames': 29,
                    'x': 325,
                    'y': 270,
                    'x1': 440,
                    'size': (430, 300),
                    'dmg_time': 30},

                   {'width': 114,
                    'height': 101,
                    'w': 9,
                    'h': 8,
                    'frames': 70,
                    'x': 250,
                    'y': 80,
                    'x1': 435,
                    'size': (515, 450),
                    'dmg_time': 115}],

         'ike': [{'width': 96,
                  'height': 70,
                  'w': 5,
                  'h': 5,
                  'frames': 23,
                  'x': 320,
                  'y': 220,
                  'x1': 450,
                  'size': (430, 315),
                  'dmg_time': 45},

                 {'width': 150,
                  'height': 125,
                  'w': 7,
                  'h': 7,
                  'frames': 44,
                  'x': 300,
                  'y': -25,
                  'x1': 240,
                  'size': (675, 560),
                  'dmg_time': 60}],

         'sorcerer': [{'width': 68,
                       'height': 51,
                       'w': 8,
                       'h': 2,
                       'frames': 16,
                       'x': 240,
                       'y': 300,
                       'x1': 665,
                       'size': (300, 225),
                       'dmg_time': 40},

                      {'width': 80,
                       'height': 111,
                       'w': 8,
                       'h': 8,
                       'frames': 61,
                       'x': 220,
                       'y': 60,
                       'x1': 620,
                       'size': (360, 500),
                       'dmg_time': 160}],
         }


class Fight_images:
    def __init__(self):
        self.images = {}
        self.magic_effects = {'sorcerer': {'norm': [pygame.transform.scale(
            pygame.image.load(f'templates/persons/sorcerer/normal_effect.png').
            subsurface(x * 65, y * 99, 65, 99), (290, 450)) for y in range(0, 7) for x in range(0, 5)][:35],

                                           'crt': [pygame.transform.flip(pygame.transform.scale(
                                               pygame.image.load(f'templates/persons/sorcerer/critical_effect.png').
                                               subsurface(x * 240, y * 128, 240, 128), (WIDTH, HEIGHT)), True, False)
                                               for y in range(0, 10) for x in range(0, 6)][:56]}}
        self.all_magic_img = self.magic_effects['sorcerer']['norm'] + self.magic_effects['sorcerer']['crt']

    def uppload_images(self, names):
        for name in set(names):
            self.images[name] = {'person': {'norm': [], 'crt': []}, 'enemy': {'norm': [], 'crt': []}}
            # enemy
            enemy_melee_attack_img = [pygame.image.load(f'templates/persons/{name}/normal_attack.png').
                                      subsurface(sizes[name][0]['width'] * x, sizes[name][0]['height'] * y,
                                                 sizes[name][0]['width'], sizes[name][0]['height'])
                                      for y in range(0, sizes[name][0]['h'])
                                      for x in range(0, sizes[name][0]['w'])][:sizes[name][0]['frames']]
            for i in range(len(enemy_melee_attack_img)):
                enemy_melee_attack_img[i] = pygame.transform.scale(enemy_melee_attack_img[i], sizes[name][0]['size'])

            enemy_critical_attack_img = [pygame.image.load(f'templates/persons/{name}/critical_attack.png').
                                         subsurface(sizes[name][1]['width'] * x, sizes[name][1]['height'] * y,
                                                    sizes[name][1]['width'], sizes[name][1]['height'])
                                         for y in range(0, sizes[name][1]['h'])
                                         for x in range(0, sizes[name][1]['w'])][:sizes[name][1]['frames']]
            for i in range(len(enemy_critical_attack_img)):
                enemy_critical_attack_img[i] = pygame.transform.scale(enemy_critical_attack_img[i],
                                                                      sizes[name][1]['size'])

            # person
            person_melee_attack_img = [pygame.transform.flip(img, True, False) for img in enemy_melee_attack_img]
            person_critical_attack_img = [pygame.transform.flip(img, True, False) for img in enemy_critical_attack_img]

            self.images[name]['person']['norm'] = person_melee_attack_img
            self.images[name]['person']['crt'] = person_critical_attack_img
            self.images[name]['enemy']['norm'] = enemy_melee_attack_img
            self.images[name]['enemy']['crt'] = enemy_critical_attack_img


class Fight:
    def __init__(self, person_name, enemy_name, fight_images, person_crt=0, enemy_crt=0):
        self.moves = [True,
                      False,
                      False,
                      False]
        self.need_moves = [0, 0]
        self.tick = 0
        self.dodge_tick = 0
        self.miss_tick = 0
        self.magic_tick = 0
        self.magic_img_id = -1
        self.enemy_dead = 0

        self.person_x, self.person_y = sizes[person_name][int(self.moves[0])]['x'], \
                                       sizes[person_name][int(self.moves[0])]['y']
        self.enemy_x, self.enemy_y = sizes[enemy_name][int(self.moves[2])]['x1'], \
                                     sizes[enemy_name][int(self.moves[2])]['y']
        self.person_dmg_tick = sizes[enemy_name][int(self.moves[2])]['dmg_time']
        self.enemy_dmg_tick = sizes[person_name][int(self.moves[0])]['dmg_time']
        self.person_img_id = 0
        self.enemy_img_id = 0

        self.fight_bg = pygame.image.load('templates/fight/bg.png').subsurface(1, 1, 240, 160)
        self.fight_bg = pygame.transform.scale(self.fight_bg, (WIDTH, HEIGHT))
        self.fight_characters = pygame.image.load('templates/fight/baze.png')
        self.fight_characters = pygame.transform.scale(self.fight_characters, (WIDTH, HEIGHT))
        self.numbers = [pygame.transform.scale(
            pygame.image.load('templates/fight/numbers.png').subsurface(i * 8, 0, 8, 8), (40, 40)) for i in range(10)]
        self.hp = [pygame.transform.scale(
            pygame.image.load('templates/fight/hp.png').subsurface(i * 2, 0, 2, 7), (10, 35)) for i in range(2)]

        self.miss_img = [pygame.image.load(f'templates/miss/{i}.png') for i in range(0, 12)]
        for i in range(len(self.miss_img)):
            self.miss_img[i] = pygame.transform.scale(self.miss_img[i], (100, 100))

        self.person_melee_attack_img = fight_images.images[person_name]['person']['norm']
        self.person_critical_attack_img = fight_images.images[person_name]['person']['crt']
        self.all_person_img = self.person_melee_attack_img + self.person_critical_attack_img
        self.enemy_melee_attack_img = fight_images.images[enemy_name]['enemy']['norm']
        self.enemy_critical_attack_img = fight_images.images[enemy_name]['enemy']['crt']
        self.all_enemy_img = self.enemy_melee_attack_img + self.enemy_critical_attack_img

        self.person_stay_img = self.person_critical_attack_img[0] if self.moves[0] else self.person_melee_attack_img[0]
        self.enemy_stay_img = self.enemy_critical_attack_img[0] if self.moves[2] else self.enemy_melee_attack_img[0]

        self.person_melee_attack_time = len(self.person_melee_attack_img) * 3
        self.person_critical_attack_time = len(self.person_critical_attack_img) * 3
        self.enemy_melee_attack_time = len(self.enemy_melee_attack_img) * 3
        self.enemy_critical_attack_time = len(self.enemy_critical_attack_img) * 3

    def mellee_person_attack(self):
        self.tick += 1
        img = self.person_melee_attack_img[self.tick % self.person_melee_attack_time // 3]

        if self.tick == self.person_melee_attack_time:
            self.tick = 0

        return img

    def critical_person_attack(self):
        self.tick += 1
        img = self.person_critical_attack_img[self.tick % self.person_critical_attack_time // 3]

        if self.tick == self.person_critical_attack_time:
            self.tick = 0

        return img

    def miss(self):
        self.miss_tick += 1
        if self.miss_tick < 66:
            img = self.miss_img[self.miss_tick % 66 // 6]
        else:
            img = self.miss_img[11]

        if self.miss_tick > 120:
            self.miss_tick = 0
        return img

    def mellee_enemy_attack(self):
        self.tick += 1
        img = self.enemy_melee_attack_img[self.tick % self.enemy_melee_attack_time // 3]

        if self.tick == self.enemy_melee_attack_time:
            self.tick = 0

        return img

    def critical_enemy_attack(self):
        self.tick += 1
        img = self.enemy_critical_attack_img[self.tick % self.enemy_critical_attack_time // 3]

        if self.tick == self.enemy_critical_attack_time:
            self.tick = 0

        return img
