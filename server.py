import socket
import pygame
import pickle
from random import randint
from Circle import Circle

host = 'localhost'
port = 5555
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
running = True
point_radius = 5
pygame.init()

print("server is running")


def add_point():
    x = randint(point_radius, SCREEN_WIDTH - point_radius)
    y = randint(point_radius, SCREEN_HEIGHT - point_radius)
    color = (randint(0, 255), randint(0, 255), randint(0,255))
    point = Circle(x, y, point_radius, color)
    return point


def check_collision_points(circle, points):
    for point in points:
        if circle.collision(point):
            circle.inc_radius()
            points.remove(point)


def win_check():
    if player1.collision(player2):
        if player1.radius >= player2.radius:
            return 1
        else:
            return 2
    return 0


def add_points(num, points):
    for i in range(num):
        points.append(add_point())

ADDPOINT = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPOINT, 1000)

points = []
win = 0
player1 = Circle(20, 20, 20, (0, 255, 0))
player2 = Circle(SCREEN_WIDTH-20, SCREEN_HEIGHT-20, 20, (255, 0, 0))
point = add_point()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(2)
    conn1, addr1 = s.accept()
    conn2, addr2 = s.accept()
    with conn1:
        with conn2:
            print("connection is established")
            while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == ADDPOINT:
                            point = add_point()
                            points.append(point)
                    try:
                        keys_1 = tuple(conn1.recv(1024))
                        keys_2 = tuple(conn2.recv(1024))

                        if len(keys_1) < 4 or len(keys_2) < 4:
                            running = False

                        player1.keys_proceed(keys_1)
                        player2.keys_proceed(keys_2)

                        win = win_check()

                        check_collision_points(player1, points)
                        check_collision_points(player2, points)

                        conn1.sendall(pickle.dumps([player1.get_info(), player2.get_info(), points, win]))
                        conn2.sendall(pickle.dumps([player1.get_info(), player2.get_info(), points, win]))
                    except:
                        print("connection is over")
                        break
