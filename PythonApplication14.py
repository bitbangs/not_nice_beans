from beans import Grid, Bean, MovingBean
import pygame

#initialize pygame and the window
pygame.init()
width, height = 640, 640
screen = pygame.display.set_mode((width, height))
quit = False

#initialize game objects
grid = Grid((60, 60, width - 60, height - 60), (6, 10))
grid.draw_grid_lines = True
moving_bean00 = MovingBean()

while not quit:
    #spawn
    if moving_bean00.has_settled:
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
    #grid.MatchDetect()

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