
import random
from pico2d import *
import game_world
import game_framework
import main_state
class Ball:
    image = None

    def __init__(self):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y =random.randint(0, 1837 - 1), random.randint(0, 1109 - 1)
        #random.randint(0, 1837 - 1), random.randint(0, 1109 - 1)
        self.ball=1
        self.cx,self.cy = 0,0
        self.bg=0
    def get_bb(self):
        # fill here
        return self.x-10,self.y-10,self.x+10,self.y+10

    def draw(self):
        ball_left, ball_bottom  = main_state.background.get_window_in_ball_left_bottom()
        cx, cy = self.x - ball_left, self.y - ball_bottom

        Ball.image.draw(cx, cy)

    def update(self):
        pass
    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2
        self.y = self.bg.h / 2
