types = {'infinite': ['lord'],
         'cavalry': ['knight_lord', 'cavalier', 'troubadour', 'valkyrie',
                     'nomad', 'nomadic_trooper'],
         'armored': ['great_lord', 'knight', 'general'],
         'swords': ['mercenary', 'hero', 'myrmidon', 'sword_master', 'blade_lord'],
         'flying': ['pegasus_knight', 'falco_knight', 'wyvern_rider', 'wyvern_lord'],
         'dragons': ['wyvern_rider', 'wyvern_lord', 'fire_dragon'],
         'nergal': ['druid']}

classes_bonus = {'great_lord': {'hp': 4,
                                'str': 2,
                                'skl': 3,
                                'speed': 2,
                                'lck': 0,
                                'def': 2,
                                'res': 5,
                                'con': 2,
                                'move': 1},

                 'blade_lord': {'hp': 3,
                                'str': 3,
                                'skl': 2,
                                'speed': 0,
                                'lck': 0,
                                'def': 3,
                                'res': 5,
                                'con': 1,
                                'move': 1},

                 'knight_lord': {'hp': 4,
                                 'str': 2,
                                 'skl': 0,
                                 'speed': 1,
                                 'lck': 0,
                                 'def': 1,
                                 'res': 3,
                                 'con': 2,
                                 'move': 2},

                 'sniper': {'hp': 4,
                            'str': 3,
                            'skl': 1,
                            'speed': 1,
                            'lck': 0,
                            'def': 2,
                            'res': 2,
                            'con': 0,
                            'move': 0},

                 'druid': {'hp': 2,
                           'str': 4,
                           'skl': 2,
                           'speed': 3,
                           'lck': 0,
                           'def': 2,
                           'res': 2,
                           'con': 1,
                           'move': 1},

                 'sage': {'hp': 3,
                          'str': 3,
                          'skl': 3,
                          'speed': 3,
                          'lck': 0,
                          'def': 1,
                          'res': 2,
                          'con': 1,
                          'move': 1}
                 }
