from beans import Grid, Bean, MovingBean, SettledBeans
from graph import Graph
import pygame
import sys #logging

#initialize pygame and the window
pygame.init()
width, height = 640, 640
screen = pygame.display.set_mode((width, height))
quit = False

#initialize game objects
grid = Grid((60, 60, width - 60, height - 60), (6, 10))
grid.draw_grid_lines = True
moving_bean00 = MovingBean()
settled_beans = SettledBeans()

while not quit:
    pygame.time.delay(100) #until more is going on this will be used to debounce the keyboard

    #spawn
    if moving_bean00.has_settled:
        pivot_bean, spin_bean = moving_bean00.beans
        settled_beans.Settle(moving_bean00)
        settled_beans.MatchDetect(moving_bean00)
        moving_bean00 = MovingBean()

    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        moving_bean00.Spin()
    elif keys[pygame.K_a]:
        moving_bean00.Move([-1, 0])
    elif keys[pygame.K_s]:
        moving_bean00.Move([0, +1])
    elif keys[pygame.K_d]:
        moving_bean00.Move([+1, 0])

    #land beans
    grid.SettleDetect(moving_bean00)

    #drawing
    screen.fill((50, 50, 50))
    if grid.draw_grid_lines:
        for start, end in grid.grid_lines:
            pygame.draw.line(screen, (0, 0, 0), start, end)
    pivot_bean, spin_bean = moving_bean00.beans
    pygame.draw.circle(screen, pivot_bean.color, grid.ToPixels(pivot_bean.coordinate), 10)
    pygame.draw.circle(screen, spin_bean.color, grid.ToPixels(spin_bean.coordinate), 10)
    for coordinate, color in settled_beans.color_map.items():
        pygame.draw.circle(screen, color, grid.ToPixels(coordinate), 10)
    pygame.display.flip()

with open('settled_beans_graph', 'w') as graph_log:
    graph_log.write(repr(settled_beans))

pygame.quit()