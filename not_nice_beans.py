from beans import Graph, Grid, Bean, MovingBean
import pygame

#initialize pygame and the window
pygame.init()
width, height = 480, 480
screen = pygame.display.set_mode((width, height))
quit = False

#initialize game objects
grid = Grid((10, 10, width - 10, height - 10), (6, 10))
grid.draw_grid_lines = True
moving_beans

while not quit:
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        moving_bean00.Spin()
    if keys[pygame.K_a]:
        moving_bean00.Move([-1, 0])
    if keys[pygame.K_s]:
        moving_bean00.Move([0, +1])
    if keys[pygame.K_d]:
        moving_bean00.Move([+1, 0])

    pygame.time.delay(60) #until more is going on

    #drawing
    screen.fill((50, 50, 50))
    if grid.draw_grid_lines:
        for start, end in grid.grid_lines:
            pygame.draw.line(screen, (0, 0, 0), start, end)
    pivot_bean, spin_bean = moving_bean00.beans
    pygame.draw.circle(screen, pivot_bean.color, grid.ToPixels(pivot_bean.coordinate), 10)
    pygame.draw.circle(screen, spin_bean.color, grid.ToPixels(spin_bean.coordinate), 10)
    pygame.display.flip()

pygame.quit()