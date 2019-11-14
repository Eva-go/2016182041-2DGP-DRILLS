from pico2d import *
import game_framework


class Brick:
    def __init__(self):
        self.image = load_image('brick180x40.png')
        self.x = 400
        self.y = 250
        self.brick_speed = 100
    def get_bb(self):
        return self.x - 100, self.y - 20, self.x + 100, self.y + 20

    def update(self):
        self.x -= self.brick_speed * game_framework.frame_time
        if self.x > 1600 - 50:
            self.brick_speed *= -1
        elif self.x < 100 - 50:
            self.brick_speed *= -1

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 90, self.y - 20, self.x + 90, self.y + 20
