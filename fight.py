from settings import *
import pygame
from random import randint

img_cords_melee_attack = [(7, 89, 43, 43), (52, 89, 43, 43), (97, 89, 43, 43), (140, 89, 43, 43), (181, 89, 43, 43),
                          (226, 89, 78, 43), (309, 89, 65, 43), (377, 89, 62, 43), (443, 89, 63, 43), (14, 152, 57, 43),
                          (74, 152, 52, 43), (127, 152, 44, 43), (174, 152, 36, 43), (219, 152, 38, 43),
                          (274, 152, 42, 43), (328, 152, 37, 43), (369, 152, 35, 50), (407, 152, 33, 50),
                          (439, 152, 49, 43), (30, 200, 32, 50), (66, 200, 44, 50), (112, 200, 46, 50),
                          (160, 200, 47, 50), (211, 200, 48, 50), (262, 200, 48, 50), (312, 200, 47, 50),
                          (358, 200, 38, 50), (402, 200, 39, 50), (444, 200, 42, 50)]
img_cords_critical_attack = [()]


class Fight:
    def __init__(self, person_crt=0, enemy_crt=0):
        self.moves = [True if randint(0, 100) <= person_crt else False,
                      False,
                      True if randint(0, 100) <= enemy_crt else False,
                      True if randint(0, 100) <= 30 else False]
        self.tick = 0
        self.dodge_tick = 0
        self.miss_tick = 0
        self.person_x, self.person_y = 150, 200
        self.enemy_x, self.enemy_y = 650, 200
        self.person_img_id = 0
        self.enemy_img_id = 0
        self.speed = 2
        self.fight_bg = pygame.image.load('templates/fight_bg/bg.png').subsurface((2, 2, 240, 160))
        self.fight_bg = pygame.transform.scale(self.fight_bg, (WIDTH, HEIGHT))
        self.miss_img = [pygame.image.load(f'templates/persons_fight/miss/{i}.png') for i in range(0, 12)]
        for i in range(len(self.miss_img)):
            self.miss_img[i] = pygame.transform.scale(self.miss_img[i], (100, 100))

        # person
        self.person_melee_attack_img = [
            pygame.image.load(f'templates/persons_fight/eliwood(lord)/person/melee_attack/{i}.png') for i in range(0, 29)]
        for i in range(len(self.person_melee_attack_img)):
            self.person_melee_attack_img[i] = pygame.transform.scale(self.person_melee_attack_img[i], (400, 400))
            self.person_melee_attack_img[i] = pygame.transform.flip(self.person_melee_attack_img[i], True, False)
        self.person_critical_attack_img = [
            pygame.image.load(f'templates/persons_fight/eliwood(lord)/person/critical_attack/{i}.png') for i in range(0, 69)]
        for i in range(len(self.person_critical_attack_img)):
            self.person_critical_attack_img[i] = pygame.transform.scale(self.person_critical_attack_img[i], (400, 400))
            self.person_critical_attack_img[i] = pygame.transform.flip(self.person_critical_attack_img[i], True, False)
        self.person_dodge_img = [
            pygame.image.load(f'templates/persons_fight/eliwood(lord)/person/dodge/{i}.png') for i in range(0, 5)]
        for i in range(len(self.person_dodge_img)):
            self.person_dodge_img[i] = pygame.transform.scale(self.person_dodge_img[i], (400, 400))
            self.person_dodge_img[i] = pygame.transform.flip(self.person_dodge_img[i], True, False)
        self.person_stay_img = self.person_melee_attack_img[0]
        self.all_person_img = self.person_melee_attack_img + self.person_critical_attack_img + self.person_dodge_img

        # enemy
        self.enemy_melee_attack_img = [
            pygame.image.load(f'templates/persons_fight/eliwood(lord)/enemy/melee_attack/{i}.png')
            for i in range(0, 29)]
        for i in range(len(self.enemy_melee_attack_img)):
            self.enemy_melee_attack_img[i] = pygame.transform.scale(self.enemy_melee_attack_img[i], (400, 400))
        self.enemy_critical_attack_img = []
        for i in self.person_critical_attack_img:
            self.enemy_critical_attack_img.append(pygame.transform.flip(i, True, False))
        self.enemy_dodge_img = []
        for i in self.person_dodge_img:
            self.enemy_dodge_img.append(pygame.transform.flip(i, True, False))
        self.enemy_stay_img = self.enemy_melee_attack_img[0]
        self.all_enemy_img = self.enemy_melee_attack_img + self.enemy_critical_attack_img + self.enemy_dodge_img

    def mellee_person_attack(self):
        self.tick += 1
        img = self.person_melee_attack_img[self.tick % 145 // 5]

        if self.tick < 25:
            pass
        elif self.tick < 50:
            self.person_x += 14
        elif self.tick < 95:
            pass
        elif self.tick < 145:
            self.person_x -= 7

        if self.tick == 145:
            self.tick = 0

        return img

    def critical_person_attack(self):
        self.tick += 1
        img = self.person_critical_attack_img[self.tick % 345 // 5]

        if self.tick < 185:
            pass
        elif self.tick < 210:
            self.person_x += 14
        elif self.tick < 220:
            pass
        elif self.tick < 270:
            self.person_x -= 7

        if self.tick == 345:
            self.tick = 0

        return img

    def dodge_person(self):
        self.dodge_tick += 1
        img = self.person_dodge_img[self.dodge_tick % 40 // 10]
        if self.dodge_tick == 40:
            self.dodge_tick = 0
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
        img = self.enemy_melee_attack_img[self.tick % 145 // 5]

        if self.tick < 25:
            pass
        elif self.tick < 50:
            self.enemy_x -= 14
        elif self.tick < 95:
            pass
        elif self.tick < 145:
            self.enemy_x += 7

        if self.tick == 145:
            self.tick = 0

        return img

    def critical_enemy_attack(self):
        self.tick += 1
        img = self.enemy_critical_attack_img[self.tick % 345 // 5]

        if self.tick < 185:
            pass
        elif self.tick < 210:
            self.enemy_x -= 14
        elif self.tick < 220:
            pass
        elif self.tick < 270:
            self.enemy_x += 7

        if self.tick == 345:
            self.tick = 0

        return img
