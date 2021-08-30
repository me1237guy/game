import pygame

FPS = 60
WHITE = (255, 255, 255)
WIDTH = 500
HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("This is my first pygame.") 
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,20))
        self.image.fill((0,255,0))
        # get the rectangle of the image and then we can set its position
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT - 50
        
    def update(self):
        self.rect.x += 2

# pygame.sprite.Group():
# A container class to hold and manage multiple Sprite objects. 
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True

while running:
    clock.tick(FPS)
    # (1) get all pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # (2) update game
    # every update function of each item in all_sprites will be called 
    all_sprites.update()

    # (3) display
    screen.fill(WHITE)
    
    # draw all objects in all_sprites container
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()
