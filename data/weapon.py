import pygame

weapon = {'iron_sword': {'mt': 5, 'wt': 5, 'hit': 90, 'crt': 0, 'range': [1], 'class': 'sword'},
          'steel_sword': {'mt': 8, 'wt': 10, 'hit': 75, 'crt': 0, 'range': [1], 'class': 'sword'},
          'silver_sword': {'mt': 13, 'wt': 8, 'hit': 80, 'crt': 0, 'range': [1], 'class': 'sword'},
          'killing_edge': {'mt': 9, 'wt': 7, 'hit': 75, 'crt': 30, 'range': [1], 'class': 'sword'},
          'armor_slayer': {'mt': 8, 'wt': 11, 'hit': 80, 'crt': 0, 'range': [1], 'class': 'sword'},
          'long_sword': {'mt': 6, 'wt': 11, 'hit': 85, 'crt': 0, 'range': [1], 'class': 'sword'},
          'lance_reaver': {'mt': 9, 'wt': 9, 'hit': 75, 'crt': 5, 'range': [1], 'class': 'sword'},
          'brave_sword': {'mt': 9, 'wt': 12, 'hit': 75, 'crt': 5, 'range': [1], 'class': 'sword'},
          'wo_dao': {'mt': 8, 'wt': 5, 'hit': 75, 'crt': 35, 'range': [1], 'class': 'sword'},
          'durandal': {'mt': 17, 'wt': 16, 'hit': 90, 'crt': 0, 'range': [1], 'class': 'sword'},
          'sol_katti': {'mt': 12, 'wt': 14, 'hit': 95, 'crt': 25, 'range': [1], 'class': 'sword'},

          'iron_axe': {'mt': 8, 'wt': 10, 'hit': 75, 'crt': 0, 'range': [1], 'class': 'axe'},
          'hand_axe': {'mt': 7, 'wt': 12, 'hit': 60, 'crt': 0, 'range': [1, 2], 'class': 'axe'},
          'steel_axe': {'mt': 11, 'wt': 15, 'hit': 65, 'crt': 0, 'range': [1], 'class': 'axe'},
          'silver_axe': {'mt': 15, 'wt': 12, 'hit': 70, 'crt': 0, 'range': [1], 'class': 'axe'},
          'tomahawk': {'mt': 13, 'wt': 14, 'hit': 65, 'crt': 0, 'range': [1, 2], 'class': 'axe'},
          'killer_axe': {'mt': 11, 'wt': 11, 'hit': 65, 'crt': 30, 'range': [1], 'class': 'axe'},
          'hammer': {'mt': 15, 'wt': 10, 'hit': 55, 'crt': 0, 'range': [1], 'class': 'axe'},
          'halberd': {'mt': 15, 'wt': 10, 'hit': 60, 'crt': 0, 'range': [1], 'class': 'axe'},
          'sword_reaver': {'mt': 11, 'wt': 13, 'hit': 65, 'crt': 5, 'range': [1], 'class': 'axe'},
          'brave_axe': {'mt': 10, 'wt': 16, 'hit': 65, 'crt': 0, 'range': [1], 'class': 'axe'},
          'wolf_beil': {'mt': 10, 'wt': 10, 'hit': 75, 'crt': 5, 'range': [1], 'class': 'axe'},
          'armads': {'mt': 18, 'wt': 18, 'hit': 75, 'crt': 0, 'range': [1], 'class': 'axe'},

          'iron_lance': {'mt': 7, 'wt': 8, 'hit': 80, 'crt': 0, 'range': [1], 'class': 'lance'},
          'steel_lance': {'mt': 10, 'wt': 13, 'hit': 70, 'crt': 0, 'range': [1], 'class': 'lance'},
          'silver_lance': {'mt': 14, 'wt': 10, 'hit': 75, 'crt': 0, 'range': [1], 'class': 'lance'},
          'javelin': {'mt': 6, 'wt': 11, 'hit': 65, 'crt': 0, 'range': [1, 2], 'class': 'lance'},
          'short_spear': {'mt': 9, 'wt': 12, 'hit': 60, 'crt': 0, 'range': [1], 'class': 'lance'},
          'killer_lance': {'mt': 10, 'wt': 9, 'hit': 70, 'crt': 30, 'range': [1], 'class': 'lance'},
          'heavy_spear': {'mt': 9, 'wt': 14, 'hit': 70, 'crt': 0, 'range': [1], 'class': 'lance'},
          'horse_slayer': {'mt': 7, 'wt': 13, 'hit': 70, 'crt': 0, 'range': [1], 'class': 'lance'},
          'axe_reaver': {'mt': 10, 'wt': 11, 'hit': 70, 'crt': 5, 'range': [1], 'class': 'lance'},
          'brave_lance': {'mt': 10, 'wt': 14, 'hit': 70, 'crt': 0, 'range': [1], 'class': 'lance'},

          'iron_bow': {'mt': 6, 'wt': 5, 'hit': 80, 'crt': 0, 'range': [2], 'class': 'bow'},
          'steel_bow': {'mt': 9, 'wt': 9, 'hit': 70, 'crt': 0, 'range': [2], 'class': 'bow'},
          'silver_bow': {'mt': 13, 'wt': 6, 'hit': 75, 'crt': 0, 'range': [2], 'class': 'bow'},
          'killer_bow': {'mt': 9, 'wt': 7, 'hit': 75, 'crt': 30, 'range': [2], 'class': 'bow'},
          'brave_bow': {'mt': 10, 'wt': 12, 'hit': 70, 'crt': 0, 'range': [2], 'class': 'bow'},
          'long_bow': {'mt': 5, 'wt': 10, 'hit': 65, 'crt': 0, 'range': [2, 3], 'class': 'bow'},
          'short_bow': {'mt': 5, 'wt': 3, 'hit': 85, 'crt': 10, 'range': [2], 'class': 'bow'},
          'rien_fleche': {'mt': 20, 'wt': 7, 'hit': 80, 'crt': 0, 'range': [2], 'class': 'bow'},

          'fire': {'mt': 5, 'wt': 4, 'hit': 95, 'crt': 0, 'range': [1, 2], 'class': 'magic', 'subclass': 'anima'},
          'elfire': {'mt': 10, 'wt': 10, 'hit': 85, 'crt': 0, 'range': [1, 2], 'class': 'magic', 'subclass': 'anima'},
          'fimbulvetr': {'mt': 13, 'wt': 12, 'hit': 80, 'crt': 0, 'range': [1, 2], 'class': 'magic',
                         'subclass': 'anima'},
          'excalibur': {'mt': 18, 'wt': 13, 'hit': 90, 'crt': 10, 'range': [1, 2], 'class': 'magic',
                        'subclass': 'anima'},

          'miracle': {'mt': 4, 'wt': 6, 'hit': 95, 'crt': 5, 'range': [1, 2], 'class': 'magic', 'subclass': 'light'},
          'divine': {'mt': 8, 'wt': 12, 'hit': 85, 'crt': 10, 'range': [1, 2], 'class': 'magic', 'subclass': 'light'},
          'lightning': {'mt': 12, 'wt': 15, 'hit': 85, 'crt': 15, 'range': [1, 2], 'class': 'magic',
                        'subclass': 'light'},

          'flux': {'mt': 7, 'wt': 8, 'hit': 80, 'crt': 0, 'range': [1, 2], 'class': 'magic', 'subclass': 'dark'},
          'ereshkigal': {'mt': 20, 'wt': 12, 'hit': 95, 'crt': 0, 'range': [1, 2], 'class': 'magic',
                         'subclass': 'dark'},

          'heal': {'mt': 0, 'wt': 2, 'hit': 100, 'crt': 0, 'range': [1], 'class': 'staff'},

          'refresh': {'mt': 0, 'wt': 0, 'hit': 100, 'crt': 0, 'range': [1], 'class': 'dance'},
          }

weapon_can_be_used = {'rapier': ['eliwood', 'knight_lord'],
                      'mani_katti': ['lyn', 'blade_lord'],
                      'wo_dao': ['lyn', 'blade_lord', 'myrmidon', 'sword_master'],
                      'durandal': ['eliwood', 'knight_lord'],
                      'armads': ['hector', 'great_lord'],
                      'sol_katti': ['lyn', 'blade_lord'],
                      'wolf_beil': ['hector', 'great_lord'],
                      }

weapon_have_triangle_bonus = ['lance_reaver', 'axe_reaver', 'sword_reaver', 'sword_slayer']

weapon_effective = {'infinite': [],
                    'cavalry': ['mani_katti', 'rapier', 'wolf_beil',
                                'long_sword', 'horse_slayer', 'halberd'],
                    'armored': ['mani_katti', 'rapier', 'wolf_beil',
                                'armor_slayer', 'heavy_spear', 'hammer'],
                    'swords': ['sword_slayer'],
                    'flying': ['iron_bow', 'steel_bow', 'silver_bow', 'killer_bow',
                               'brave_bow', 'long_bow', 'short_bow', 'rien_fleche'],
                    'dragons': ['wyrm_slayer', 'dragon_axe', 'durandal', 'armads',
                                'forblaze', 'sol_katti', 'aureola'],
                    'nergal': ['aureola'],
                    }

img_ = pygame.image.load('templates/weapon/weapon.png')
weapon_img = {
    'iron_sword': pygame.transform.scale(img_.subsurface((17, 0, 16, 16)), (72, 72)),
    'steel_sword': pygame.transform.scale(img_.subsurface((34, 0, 16, 16)), (72, 72)),
    'silver_sword': pygame.transform.scale(img_.subsurface((51, 0, 16, 16)), (72, 72)),
    'killing_edge': pygame.transform.scale(img_.subsurface((68, 0, 16, 16)), (72, 72)),
    'armor_slayer': pygame.transform.scale(img_.subsurface((85, 0, 16, 16)), (72, 72)),
    'long_sword': pygame.transform.scale(img_.subsurface((102, 0, 16, 16)), (72, 72)),
    'lance_reaver': pygame.transform.scale(img_.subsurface((119, 0, 16, 16)), (72, 72)),
    'brave_sword': pygame.transform.scale(img_.subsurface((0, 17, 16, 16)), (72, 72)),
    'wo_dao': pygame.transform.scale(img_.subsurface((34, 17, 16, 16)), (72, 72)),
    'durandal': pygame.transform.scale(img_.subsurface((51, 17, 16, 16)), (72, 72)),
    'sol_katti': pygame.transform.scale(img_.subsurface((68, 17, 16, 16)), (72, 72)),

    'iron_axe': pygame.transform.scale(img_.subsurface((119, 51, 16, 16)), (72, 72)),
    'steel_axe': pygame.transform.scale(img_.subsurface((0, 68, 16, 16)), (72, 72)),
    'silver_axe': pygame.transform.scale(img_.subsurface((17, 68, 16, 16)), (72, 72)),
    'hand_axe': pygame.transform.scale(img_.subsurface((34, 68, 16, 16)), (72, 72)),
    'tomahawk': pygame.transform.scale(img_.subsurface((51, 68, 16, 16)), (72, 72)),
    'killer_axe': pygame.transform.scale(img_.subsurface((68, 68, 16, 16)), (72, 72)),
    'hammer': pygame.transform.scale(img_.subsurface((85, 68, 16, 16)), (72, 72)),
    'halberd': pygame.transform.scale(img_.subsurface((102, 68, 16, 16)), (72, 72)),
    'sword_reaver': pygame.transform.scale(img_.subsurface((119, 68, 16, 16)), (72, 72)),
    'brave_axe': pygame.transform.scale(img_.subsurface((0, 85, 16, 16)), (72, 72)),
    'wolf_beil': pygame.transform.scale(img_.subsurface((17, 85, 16, 16)), (72, 72)),
    'armads': pygame.transform.scale(img_.subsurface((34, 85, 16, 16)), (72, 72)),

    'iron_lance': pygame.transform.scale(img_.subsurface((34, 34, 16, 16)), (72, 72)),
    'steel_lance': pygame.transform.scale(img_.subsurface((51, 34, 16, 16)), (72, 72)),
    'silver_lance': pygame.transform.scale(img_.subsurface((68, 34, 16, 16)), (72, 72)),
    'javelin': pygame.transform.scale(img_.subsurface((85, 34, 16, 16)), (72, 72)),
    'short_spear': pygame.transform.scale(img_.subsurface((102, 34, 16, 16)), (72, 72)),
    'killer_lance': pygame.transform.scale(img_.subsurface((119, 34, 16, 16)), (72, 72)),
    'heavy_spear': pygame.transform.scale(img_.subsurface((0, 51, 16, 16)), (72, 72)),
    'horse_slayer': pygame.transform.scale(img_.subsurface((17, 51, 16, 16)), (72, 72)),
    'axe_reaver': pygame.transform.scale(img_.subsurface((34, 51, 16, 16)), (72, 72)),
    'brave_lance': pygame.transform.scale(img_.subsurface((51, 51, 16, 16)), (72, 72)),

    'iron_bow': pygame.transform.scale(img_.subsurface((51, 85, 16, 16)), (72, 72)),
    'steel_bow': pygame.transform.scale(img_.subsurface((68, 85, 16, 16)), (72, 72)),
    'silver_bow': pygame.transform.scale(img_.subsurface((85, 85, 16, 16)), (72, 72)),
    'killer_bow': pygame.transform.scale(img_.subsurface((102, 85, 16, 16)), (72, 72)),
    'brave_bow': pygame.transform.scale(img_.subsurface((119, 85, 16, 16)), (72, 72)),
    'long_bow': pygame.transform.scale(img_.subsurface((0, 102, 16, 16)), (72, 72)),
    'short_bow': pygame.transform.scale(img_.subsurface((17, 102, 16, 16)), (72, 72)),
    'rien_fleche': pygame.transform.scale(img_.subsurface((34, 102, 16, 16)), (72, 72)),

    'flux': pygame.transform.scale(img_.subsurface((51, 119, 16, 16)), (72, 72)),
    'fire': pygame.transform.scale(img_.subsurface((51, 102, 16, 16)), (72, 72)),
    'elfire': pygame.transform.scale(img_.subsurface((68, 102, 16, 16)), (72, 72)),
    'fimbulvetr': pygame.transform.scale(img_.subsurface((85, 102, 16, 16)), (72, 72)),
    'excalibur': pygame.transform.scale(img_.subsurface((102, 102, 16, 16)), (72, 72)),
    'miracle': pygame.transform.scale(img_.subsurface((119, 102, 16, 16)), (72, 72)),
    'divine': pygame.transform.scale(img_.subsurface((0, 119, 16, 16)), (72, 72)),
    'lightning': pygame.transform.scale(img_.subsurface((17, 119, 16, 16)), (72, 72)),
    'ereshkigal': pygame.transform.scale(img_.subsurface((102, 119, 16, 16)), (72, 72)),

    'heal': pygame.transform.scale(img_.subsurface((119, 119, 16, 16)), (72, 72)),

    'refresh': pygame.transform.scale(pygame.image.load('templates/weapon/dance.png'), (72, 72))
}

weapon_arrow = {'up': [pygame.transform.scale(pygame.image.load('templates/fight/up_arrow.png').
                                              subsurface(x * 7, 0, 7, 10), (32, 45)) for x in range(3)],
                'down': [pygame.transform.scale(pygame.image.load('templates/fight/down_arrow.png').
                                                subsurface(x * 7, 0, 7, 10), (32, 45)) for x in range(3)]}
