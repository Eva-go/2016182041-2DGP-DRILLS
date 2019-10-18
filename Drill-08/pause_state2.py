from pico2d import *
import game_framework
import main_state

count = 0.0


image = None


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_state()


def enter():
    global image
    image = load_image('pause.png')


def exit():
    global image
    del (image)


def update():
    pass


def draw():
    global count

    clear_canvas()
    main_state.grass.draw()
    main_state.boy.draw()
    image.draw(400, 300, 200, 200)
    draw()
    update_canvas()


def pause(): pass


def resume(): pass
