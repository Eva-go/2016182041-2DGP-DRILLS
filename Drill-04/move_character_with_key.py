from pico2d import *


def handle_events():
    global running
    global dir

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir += 1
            elif event.key == SDLK_LEFT:
                dir -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1


open_canvas()
grass = load_image('grass.png')
character = load_image('animation_sheet.png')

dir_move = 0

running = True
x = 800 // 2
frame = 0
dir = 0
while running:
    clear_canvas()
    grass.draw(400, 30)
    if dir_move == 0:
        character.clip_draw(frame * 100, 300 * 1, 100, 100, x, 90)
    if dir == 1:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, 90)
        dir_move = 1
    elif dir == 0 and dir_move == 1:
        character.clip_draw(frame * 100, 300 * 1, 100, 100, x, 90)
    elif dir == -1:
        character.clip_draw(frame * 100, 0, 100, 100, x, 90)
        dir_move = -1
    elif dir == 0 and dir_move == -1:
        character.clip_draw(frame * 100, 200 * 1, 100, 100, x, 90)
    if x >= 800:
        x = 800
    elif x <= 0:
        x = 0
    update_canvas()
    x += dir
    handle_events()
    frame = (frame + 1) % 8
    # delay(0.01)

close_canvas()
