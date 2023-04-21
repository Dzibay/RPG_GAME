import socket
import pygame

server_ip = 'localhost'

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind((server_ip, 10000))
main_socket.setblocking(0)
main_socket.listen(5)

pygame.init()
clock = pygame.time.Clock()

FPS = 60
TILE = 80
tick = 0


class Person:
    def __init__(self, x, y, name):
        self.name = name
        self.pos = (x, y)

    def get_big_pos(self):
        return (self.pos[0] * TILE, self.pos[1] * TILE)


class Player:
    def __init__(self, conn, addr):
        self.addr = addr
        self.conn = conn
        self.errors = 0
        self.persons = [Person(1, 0, 'eliwood(lord)'),
                        Person(10, 5, 'eliwood(lord)')]


players = []
run = True
while run:
    tick += 1
    clock.tick(FPS)

    if tick == 200:
        tick = 0
        # проверим, есть ли желающие войти в игру
        try:
            new_socket, addr = main_socket.accept()
            print(f'Подключился игрок, игроков на сервере: {len(players)}')
            new_socket.setblocking(0)

            new_player = Player(new_socket, addr)
            players.append(new_player)
        except:
            pass

    for player in players:
        try:
            data = player.conn.recv(1024)
            data = data.decode()

            player.errors = 0
        except:
            player.errors += 1
            if player.errors > 200:
                player.conn.close()
                players.remove(player)
                print(f'Отключился игрок, игроков на сервере: {len(players)}')

    for player in players:
        try:
            sms = '<'
            for person in player.persons:
                sms += f'{person.name} {person.pos[0]} {person.pos[1]},'
            for player_2 in players:
                if player_2 != player:
                    for person in player_2.persons:
                        sms += f'{person.name} {person.pos[0]} {person.pos[1]},'
            sms += '>'
            player.conn.send(sms.encode())
        except:
            pass