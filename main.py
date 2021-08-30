import pygame

pygame.init()
screen = pygame.display.set_mode((500, 600))

running = True

while running:
    # (1) get all pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # (2) update game

    # (3) display


pygame.quit()
