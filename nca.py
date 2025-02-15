import pygame as pg
from pygame.constants import QUIT
from time import sleep
import torch
import random


screen_b = screen_h = 1000
scale = 10
custom_activation = False
randomize = True

# rule = torch.tensor([
#     [ 0.0,-0.1, 0.0],
#     [-0.1, 0.1,-0.1],
#     [ 0.0,-0.1, 1.3]
# ])

rule = torch.tensor([
    [ 0.00,-0.20, 0.00],
    [-0.20, 0.05,-0.20],
    [ 0.00,-0.20, 1.00]
])

# rule = torch.tensor([
#     [1.00, 1.25, 0.75],
#     [1.00, 9.00, 1.00],
#     [0.75, 1.25, 1.00]
# ])

# Game of Life rule
# rule = torch.tensor([
#     [1.0, 1.0, 1.0],
#     [1.0, 9.0, 1.0],
#     [1.0, 1.0, 1.0]
# ])

def draw_screen(screen, grid):
    # draw grid
    # print(screen)
    for i in range(screen_b // scale):
        for j in range(screen_h // scale):
            color = 255 * grid[i][j]
            pg.draw.rect(
                    screen, (color, 0, 0), (i * scale, j * scale, scale, scale)
                )

            # if grid[i][j] > 0.5 and grid[i][j] < 0.7:
            #     color = min(255, 255 * (grid[i][j] - 0.5) / 0.2)
            #     color = max(0, color)
            #     pg.draw.rect(
            #         screen, (color, 0, 0), (i * scale, j * scale, scale, scale)
            #     )


def gol_activation(x: float) -> float:
    if x >= 2.33 and x <= 3.66:
        return 1.
    if x >= 10.33 and x <= 12.66:
        return 1.
    return 0.
    

def main():
    pg.init()
    pg.font.init()
    game_font = pg.font.SysFont('Roboto', 20)

    pg.display.set_caption("Neural Cellular Automata")
    screen = pg.display.set_mode([screen_b, screen_h])
    grid = torch.rand((screen_b, screen_h))

    generation = 0
    rnd = round(random.random(), 3)
    while True:
        generation += 1
        screen.fill((0, 0, 0))
          
        grid1 = torch.nn.functional.conv2d(
            grid.view(1, 1, screen_b, screen_h), rule.view(1, 1, 3, 3), padding=1
        )
        
        if custom_activation:
            grid1 = grid1.apply_(gol_activation)
        else:
            grid1 = torch.nn.functional.relu_(grid1)
            # grid1 = torch.nn.functional.leaky_relu_(grid1, 0.1)
            # grid1 = torch.nn.functional.sigmoid(grid1)
            grid1 = torch.clamp(grid1, 0, 1)
        
       
        grid = grid1.view(screen_b, screen_h)
        draw_screen(screen, grid)

        if randomize:
            if generation % 5 == 0:
                rnd = round(random.random(), 3)
                if round((rnd * 10)) % 2 == 0:
                    rnd *= -1
                rule[1][1] = rnd
            textsurface = game_font.render(f'rnd: {rnd}', False, (255, 255, 255))
            screen.blit(textsurface,(0,0))

        pg.display.flip()
        sleep(0.1)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                return


if __name__ == "__main__":
    main()
