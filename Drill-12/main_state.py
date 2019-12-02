import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from ground import Ground
from zombie import Zombie
from ball import Ball, BigBall

name = "MainState"

boy = None
zombie = None
balls=[]
bigballs = []
bigball_count=0
ball_count=0

def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def get_boy():
    return boy


def get_ball():
    return balls

def get_bigball():
    return bigballs


def enter():
    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global zombie
    zombie = Zombie()
    game_world.add_object(zombie, 1)

    ground = Ground()
    game_world.add_object(ground, 0)

    global balls
    balls = [Ball() for i in range(5)]
    game_world.add_objects(balls, 1)

    global bigballs
    bigballs = [BigBall() for i in range(5)]
    game_world.add_objects(bigballs, 1)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        #elif game_over == True:
         #   game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    global boy, zombie,bigball_count,ball_count

    for game_object in game_world.all_objects():
        game_object.update()


    for ball in balls:
        if bigball_count==5:
            if collide(zombie, ball):
                balls.remove(ball)
                game_world.remove_object(ball)
                zombie.zombie_hp += ball.ball_hp
                ball_count+=1

    for bigball in bigballs:
        if collide(zombie, bigball):
            bigballs.remove(bigball)
            game_world.remove_object(bigball)
            zombie.zombie_hp += bigball.bigball_hp
            bigball_count+=1

    if zombie.zombie_hp >750:
        if collide(zombie, boy):
            # boy.remove(boy)
            game_world.remove_object(boy)

    elif zombie.zombie_hp < 750:
        if collide(boy, zombie):
            # zombie.remove(zombie)
            game_world.remove_object(zombie)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


