from pico2d import *
import random


# Game object class here
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = 0
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = random.randint(0, 7)
        self.x += 2

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


class Ball:
    def __init__(self):
        self.x, self.y = random.randint(10, 700), 599
        self.draws = random.randint(1, 3)
        if self.draws % 2 == 0:
            self.image = load_image('ball21x21.png')
        else:
            self.image = load_image('ball41x41.png')

    def update(self):
        if self.y > 60:
            self.y -= random.randint(10, 20)

    def draw(self):
        self.image.draw(self.x, self.y)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False



# initialization code 초기화
# rand = bool

open_canvas()
grass = Grass()
team = [Boy() for i in range(11)]
balls = [Ball() for j in range(20)]

running = True
# game main loop code 루프
while running:
    handle_events()
    for boy in team:
        boy.update()
    for ball in balls:
        ball.update()
    clear_canvas()
    grass.draw()
    for boy in team:
        boy.draw()
    for ball in balls:
        ball.draw()

    delay(0.05)
    update_canvas()

# finalization code 종료
close_canvas()
