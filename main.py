import pygame
import random  # for generating a bunch of rocks randomly

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 20))
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
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = 2
    
    def update(self):
        # update the rock's horizontal and vertical position
        self.rect.y -= self.speedy
        # delete the item when it is out of the window
        if self.rect.bottom < 0:
           self.kill()     # this automatically removes the bullet from all_sprites
                           # or any group which owns it 

# pygame.sprite.Group():
# A container that is used to manage multiple Sprite objects. 
all_sprites = pygame.sprite.Group()
# A group of rocks that is used to collects all rocks
rocks = pygame.sprite.Group()
# A group of bullets that is used to collect all bullets
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

running = True

while running:
    clock.tick(FPS)
    # (1) get all pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # (2) update game
    # every update function of each item in all_sprites will be called 
    all_sprites.update()
    # After all sprites update their positions, we should update the collision between rocks and bullets
    are_rocks_disappeared = True
    are_bullets_disappeared = True
    hits = pygame.sprite.groupcollide(rocks, bullets, 
                               are_rocks_disappeared, 
                               are_bullets_disappeared)
                               
    # Add enough rocks that its amount is equal to the number of collisions                           
    for hit in hits:
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)

    # (3) display
    screen.fill(BLACK)
    
    # draw all objects in all_sprites container
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()
