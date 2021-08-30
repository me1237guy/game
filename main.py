import pygame

FPS = 60
WHITE = (255, 255, 255)
WIDTH = 500
HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("This is my first pygame.") 
clock = pygame.time.Clock()

running = True

while running:
    clock.tick(FPS)
    # (1) get all pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # (2) update game

    # (3) display
    screen.fill(WHITE)
    pygame.display.update()

pygame.quit()
