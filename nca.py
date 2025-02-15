import pygame as pg
from pygame.constants import QUIT
from time import sleep
import torch


screen_b = screen_h = 1500
scale = 10

rule = torch.tensor([
    [0.0, 0.1, 0.0], 
    [0.1, 0.0, 0.4], 
    [0.0, 0.4, 0.0]
])

def draw_screen(screen, grid):
    # draw grid
    # print(screen)
    pass
    for i in range(screen_b//scale):
        for j in range(screen_h//scale):
            if grid[i][j] > 0.5:
                pg.draw.rect(screen, (255*grid[i][j], 0, 0), (i*scale, j*scale, scale, scale))

def main():
    pg.init()
    pg.font.init()
    # game_font = pg.font.SysFont('Roboto', 20)
    
    
    pg.display.set_caption("Neural Cellular Automata")
    screen = pg.display.set_mode([screen_b, screen_h])
    grid =torch.rand((screen_b, screen_h))
    
         
    while True:
        screen.fill((0, 0, 0))
        
        #grid =torch.rand((screen_b//scale, screen_h//scale))
        grid1 = torch.nn.functional.conv2d(grid.view(1, 1, screen_b, screen_h), rule.view(1, 1, 3, 3), padding=1)
        # grid1 = torch.nn.functional.relu_(grid1)
        grid1 = torch.nn.functional.leaky_relu_(grid1, 0.1)
        grid1 = torch.clamp(grid1, 0, 1)
        grid = grid1.view(screen_b, screen_h)
        draw_screen(screen, grid)
        
        pg.display.flip()
        sleep(.01)
        
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                return
    

if __name__ == "__main__":
    main()
