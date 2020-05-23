import math
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 100/math.sqrt(radius)

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.y -= self.speed
        if pressed_keys[K_DOWN]:
            self.y += self.speed
        if pressed_keys[K_LEFT]:
            self.x -= self.speed
        if pressed_keys[K_RIGHT]:
            self.x += self.speed

        if self.x - self.radius < 0:
            self.x = self.radius
        if self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
        if self.y - self.radius<= 0:
            self.y = self.radius
        if self.y + self.radius >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius

    def collision(self, circle):
        x = self.x - circle.x
        y = self.y - circle.y
        if math.sqrt(x**2 + y**2) <= self.radius + circle.radius:
            return True
        return False

    def get_info(self):
        return [self.x, self.y, self.radius]

    def set_values(self, info):
        self.x = info[0]
        self.y = info[1]
        self.radius = info[2]
        self.speed = int(100/math.sqrt(self.radius))

    def keys_proceed(self, keys_tulpe):
        if keys_tulpe[1]:
            self.y -= self.speed
        if keys_tulpe[3]:
            self.y += self.speed
        if keys_tulpe[0]:
            self.x -= self.speed
        if keys_tulpe[2]:
            self.x += self.speed

        if self.x - self.radius < 0:
            self.x = self.radius
        if self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
        if self.y - self.radius<= 0:
            self.y = self.radius
        if self.y + self.radius >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius

    def inc_radius(self):
        self.radius += 1
        self.speed = 100/math.sqrt(self.radius)