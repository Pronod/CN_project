import pygame
import socket
import pickle
from Circle import Circle
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT
)
point_radius = 5
host = 'localhost'
port = 5555
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700


def redraw(screen, player1, player2, points):
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, player1.color, (player1.x, player1.y), player1.radius)
    pygame.draw.circle(screen, player2.color, (player2.x, player2.y), player2.radius)
    for point in points:
        pygame.draw.circle(screen, point.color, (point.x, point.y), point.radius)
    pygame.display.flip()


def print_result(screen, player):
    screen.fill((255, 255, 255))
    myfont = pygame.font.SysFont("monospace", 45)
    label = None
    if player == 1:
        label = myfont.render("The Green wins", 1, (0, 255, 0))
    else:
        label = myfont.render("The Red wins", 1, (255, 0, 0))
    screen.blit(label, ((SCREEN_WIDTH - label.get_width())/2, (SCREEN_HEIGHT - label.get_height())/2))
    pygame.display.flip()



pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Agar.io")
running = True
clock = pygame.time.Clock()
player1 = Circle(20, 20, 20, (0, 255, 0))
player2 = Circle(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20, 20, (255, 0, 0))


points = []
cur_player = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print("Connected")
    s.connect((host, port))
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        flags = [keys[pygame.K_LEFT], keys[pygame.K_UP], keys[pygame.K_RIGHT], keys[pygame.K_DOWN]]

        s.sendall(bytes(flags))

        info = pickle.loads(s.recv(2024))

        win = info[-1]



        player1.set_values(info[0])
        player2.set_values(info[1])

        points = info[2]

        redraw(screen, player1, player2, points)
        if win != 0:
            s.close()
            running = False

running = True
print_result(screen, win)
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

