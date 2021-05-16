from collections import Counter
import pygame as pg
from pygame.constants import QUIT
import pygame.mouse as mouse
import random as rnd
import math
import sys
from time import sleep

def nn(pos):
    for dx, dy in [(-1, -1), (0, -1), (1, -1),
                   (-1,  0),          (1,  0),
                   (-1,  1), (0,  1), (1,  1)]:
        yield pos[0] + dx, pos[1] + dy

def next_gen(field):
    n = Counter([pos for cell in field for pos in nn(cell)])
    return {pos for pos, count in n.items() if count == 3 or (count == 2 and pos in field)}

def get_dim(field, length):
    xs, ys = zip(*field)
    minx, miny, maxx, maxy = min(xs), min(ys), max(xs), max(ys)
    mina, maxa = min(minx, miny), max(maxx, maxy)
    a = maxa - mina + 1
    return length/a, -mina

def new_color(r, g, b, gen):
    amplitude = 25
    offset = 255 - amplitude - 1
    r = offset + int(math.sin(gen/17) * amplitude)
    g = offset + int(math.cos(gen/17) * amplitude)
    b = offset + int(math.sin(gen/41) * amplitude)
    return (r, g, b)

def zoom(x, y, ox, oy, a, scale):
    if a*scale <= 1:
        return ox, oy, 1

    mousex = ox - x/a
    mousey = oy - y/a

    a*=scale
    ox = mousex + x/a
    oy = mousey + y/a

    return int(ox), int(oy), a
    

pg.init()
pg.font.init()
game_font = pg.font.SysFont('Roboto', 20)

field = {(rnd.randrange(250), rnd.randrange(250)) for i in range(10000)}
screen_b = screen_h = 1000
scroll = 20
a, o = get_dim(field, screen_b)
pg.display.set_caption("Conway's Game of Life")
screen = pg.display.set_mode([screen_b, screen_h])

gen = 0
color = (255,255,255)
left_pressed = False
right_pressed = False
paused = False
a, ox, oy = 4, 0, 0
inc_x = 0
inc_y = 0

while True:
    screen.fill((0,0,0))
    color = new_color(*color, gen)

    mx, my = mouse.get_pos()
    ox, oy = ox + inc_x, oy + inc_y

    if right_pressed: # translate 
        move_x, move_y = mouse.get_rel()
        if abs(move_x)<100 and abs(move_y)<100:
            ox, oy = ox + int(move_x/a), oy + int(move_y/a)

    if left_pressed: # add new points
        field.add((math.floor(mx/a-ox), math.floor(my/a-oy)))


    textsurface = game_font.render(f'Generation: {gen} / alive: {len(field)}', False, (255, 255, 255))
    screen.blit(textsurface,(0,0))

    for event in pg.event.get():
        left, middle, right = mouse.get_pressed(3)

        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONUP:
            left_pressed = False
            right_pressed = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if left:
                left_pressed = True
            if middle: # delete a single point
                coordinates = (math.floor(mx/a-ox), math.floor(my/a-oy))
                if field.issuperset({coordinates}): field.remove(coordinates)
            if right:
                right_pressed = True
        elif event.type == pg.MOUSEWHEEL:
            if event.y > 0:              
                ox, oy, a = zoom(mx, my, ox, oy, a, 1.1)
            if event.y < 0:
                ox, oy, a = zoom(mx, my, ox, oy, a, 0.9)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                ox, oy, a = 0, 0, 4
            elif event.key == pg.K_q or event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == pg.K_UP or event.key == pg.K_w:
                inc_y = scroll/a
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                inc_x = scroll/a
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                inc_y = -scroll/a
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                inc_x = -scroll/a
            elif event.key == pg.K_PAGEUP:
                ox, oy, a = zoom(mx, my, ox, oy, a, 1.1)
            elif event.key == pg.K_PAGEDOWN:
                ox, oy, a = zoom(mx, my, ox, oy, a, 0.9)
            elif event.key == pg.K_e or event.key == pg.K_n:
                field = next_gen(field) # make a step
            elif event.key == pg.K_p or event.key == pg.K_SPACE:
                paused = not paused
            else:
                pass

        elif event.type == pg.KEYUP:
            inc_x = 0
            inc_y = 0

    if not paused:
        field = next_gen(field)
        gen += 1
    else:
        sleep(0.005)


    for x,y in field:
        if (x+ox)*a > screen_b or (y+oy)*a > screen_h:
            next
    
        pg.draw.rect(screen, color, ((x+ox)*a, (y+oy)*a, a, a))
    pg.display.flip()

