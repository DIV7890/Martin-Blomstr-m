import pygame
clicked = False
pygame.init()
window = pygame.display.set_mode((250, 250))
rect = pygame.Rect(*window.get_rect().center, 0, 0).inflate(100, 100)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = True

    point = pygame.mouse.get_pos()
    collide = rect.collidepoint(point)
    if collide and clicked:
        color = (255, 0, 0)

    else :
        color = (255, 255, 255)
        clicked = False

    window.fill(0)
    pygame.draw.rect(window, color, rect)
    pygame.display.flip()

pygame.quit()
exit()