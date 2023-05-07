import pygame
from settings import *


def cords(c):
    return c[0], c[1], c[2], c[3]


characters = {'roy': {'hp': 30,
                      'hit': 30,
                      'str': 30,
                      'skl': 30,
                      'lck': 30,
                      'def': 30,
                      'res': 30,
                      'move': 4},

              'lyn': {'hp': 30,
                      'hit': 30,
                      'str': 30,
                      'skl': 30,
                      'lck': 30,
                      'def': 30,
                      'res': 30,
                      'move': 5},

              'hector': {'hp': 30,
                         'hit': 30,
                         'str': 30,
                         'skl': 30,
                         'lck': 30,
                         'def': 30,
                         'res': 30,
                         'move': 3},

              'eirika': {'hp': 30,
                         'hit': 30,
                         'str': 30,
                         'skl': 30,
                         'lck': 30,
                         'def': 30,
                         'res': 30,
                         'move': 6},

              'eliwood': {'hp': 30,
                          'hit': 30,
                          'str': 30,
                          'skl': 30,
                          'lck': 30,
                          'def': 30,
                          'res': 30,
                          'move': 6},

              'marth': {'hp': 30,
                        'hit': 30,
                        'str': 30,
                        'skl': 30,
                        'lck': 30,
                        'def': 30,
                        'res': 30,
                        'move': 4},

              'ike': {'hp': 30,
                      'hit': 30,
                      'str': 30,
                      'skl': 30,
                      'lck': 30,
                      'def': 30,
                      'res': 30,
                      'move': 4},

              'sorcerer': {'hp': 30,
                           'hit': 30,
                           'str': 30,
                           'skl': 30,
                           'lck': 30,
                           'def': 30,
                           'res': 30,
                           'move': 3}}


class Person:
    def __init__(self, x, y, name):
        print('person')
        self.x = x
        self.y = y
        self.name = name
        self.state = 'stay'
        self.pos = (self.x // TILE, self.y // TILE)
        self.want_move = self.pos
        self.move_to = ''
        self.damage_for_me = 0

        self.hp = characters[self.name]['hp']
        self.max_hp = 50
        self.hit = characters[self.name]['hit']
        self.str = characters[self.name]['str']
        self.skl = characters[self.name]['skl']
        self.lck = characters[self.name]['lck']
        self.def_ = characters[self.name]['def']
        self.res = characters[self.name]['res']
        self.movement = characters[self.name]['move']

        self.dmg = self.str + 20
        self.crt = self.skl + 20

        self.can_fight_with = []
        self.attack_button = None

        # person
        self.stay_images = [pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/person/map_idle.png').
                                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)] + \
                           [pygame.transform.scale(
                               pygame.image.load(f'templates/persons/{name}/person/map_selected.png').
                               subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.move_up_images = [pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/person/map_up.png').
                                                      subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.move_down_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/person/map_down.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.move_left_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/person/map_side.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.move_right_images = [pygame.transform.flip(i, True, False) for i in self.move_left_images]
        self.img = self.stay_images[0]

        # enemy
        self.enemy_stay_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/enemy/map_idle.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.enemy_move_up_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/enemy/map_up.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.enemy_move_down_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/enemy/map_down.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.enemy_move_left_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/enemy/map_side.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.enemy_move_right_images = [
            pygame.transform.flip(i, True, False) for i in self.move_left_images]

    def get_big_pos(self):
        return (self.pos[0] * TILE, self.pos[1] * TILE)

    def move(self, cords):
        if self.pos != self.want_move:
            self.state = 'move_'
            cords.reverse()
            cord = cords[0]
            if self.y < cord[1] * TILE:
                self.y += 8
                self.move_to = 'D'
            elif self.y > cord[1] * TILE:
                self.y -= 8
                self.move_to = 'U'
            elif self.x < cord[0] * TILE:
                self.x += 8
                self.move_to = 'R'
            elif self.x > cord[0] * TILE:
                self.x -= 8
                self.move_to = 'L'
            else:
                self.pos = cord
                cords.reverse()
                cords.remove(cord)
                cords.reverse()
            cords.reverse()
        return cords

    def choice_image(self, tick, choice):
        if self.pos != self.want_move:
            if self.move_to == 'L':
                self.img = self.move_left_images[tick % 40 // 10]
            elif self.move_to == 'R':
                self.img = self.move_right_images[tick % 40 // 10]
            elif self.move_to == 'D':
                self.img = self.move_down_images[tick % 40 // 10]
            elif self.move_to == 'U':
                self.img = self.move_up_images[tick % 40 // 10]
        else:
            self.state = 'stay'
            self.move_to = ''
            if tick % 120 < 40:
                i_ = (tick % 40 // 10) + (4 if choice else 0)
            else:
                i_ = 0

            self.img = self.stay_images[i_]
