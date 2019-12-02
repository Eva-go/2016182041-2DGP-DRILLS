import random
from pico2d import *
import game_world
import game_framework


class Ball:
    image = None

    def __init__(self):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x = random.randint(400, 800 - 1)
        self.y = random.randint(200, 600- 1)
        self.ball_hp = 50

    def get_bb(self):
        return self.x - 10, self.y-10,self.x + 10,self.y+10

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        draw_rectangle(*self.get_bb())

    # fill here for def stop


class BigBall:
    MIN_FALL_SPEED = 50  # 50 pps = 1.5 meter per sec
    MAX_FALL_SPEED = 200  # 200 pps = 6 meter per sec
    image = None

    def __init__(self):
        if BigBall.image == None:
            BigBall.image = load_image('ball41x41.png')
        self.x = random.randint(400, 800 - 1)
        self.y = random.randint(200, 600 - 1)
        self.bigball_hp=100

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        draw_rectangle(*self.get_bb())
