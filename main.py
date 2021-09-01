import pygame
import random  # for generating a bunch of rocks randomly

FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
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
        # add a speed propery
        self.speedx = 8
        
    def update(self):
        # get the state of all keyboard buttons
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        # set player's boundary
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0   

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 10)
    
    def update(self):
        # update the rock's horizontal and vertical position
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # reset the item that is out of the boundary
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(0, WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)
        
       

# pygame.sprite.Group():
# A container class to hold and manage multiple Sprite objects. 
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    r = Rock()
    all_sprites.add(r)

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
