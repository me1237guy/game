import pygame
import random  # for generating a bunch of rocks randomly
import os
from pygame import draw

from pygame.transform import rotate      # get path for widnows/linux
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

# load images
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
# rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
# load 7 rock images that will be randomly selected later
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    use_anti_arial = True
    # draw text on a new Surface
    text_surface = font.render(text, use_anti_arial, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,20))
        # self.image.fill((0,255,0))
        self.image = pygame.transform.scale(player_img, (50, 38)) 
        # set the transparent colorkey  
        self.image.set_colorkey(BLACK)   
        # get the rectangle of the image and then we can set its position
        self.rect = self.image.get_rect()
        self.radius = 15
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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
        # self.image = pygame.Surface((30, 20))
        # self.image.fill(RED)
        # image_orig is a copy of rock_img, and it will be used for rotation later  
        self.image_orig = random.choice(rock_imgs)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()     
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85/2)
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 5)
        self.rotate_total = 0
        self.rotate_deg = random.randrange(-10, 10)

    def update(self):
        self.rotate()
        # update the rock's horizontal and vertical position
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # reset the item that is out of the boundary
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(0, WIDTH-self.rect.width)
            self.rect.y = random.randrange(-40, -10)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)
            self.rotate_total = 0
            self.rotate_deg = random.randrange(-10, 10)

    def rotate(self):
        self.rotate_total += self.rotate_deg
        self.rotate_total = self.rotate_total % 360
        # (1) get the center of the current surrounded rectangle
        self.center_old = self.rect.center
        # rotate a lossless image which is a copy of rock_img
        self.image = pygame.transform.rotate(self.image_orig, self.rotate_total)
        # (2) because the image rotated, its center of the surrounded rectangle has changed also
        self.rect = self.image.get_rect()
        # (3) modify the latest center of the surrounded rectangle with the previous value, ie. center_old
        self.rect.center = self.center_old

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        # self.image.fill(YELLOW)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
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
score = 0

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
        score += hit.radius
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)  

    # Check if the player is colliding with any of rocks
    is_player_disappeared = False
    hits = pygame.sprite.spritecollide(player, rocks, 
                                      is_player_disappeared,
                                      pygame.sprite.collide_circle)    
    # if hits:
        # running = False

    # (3) display
    # screen.fill(BLACK)
    screen.blit(background_img, (0,0))

    # draw all objects in all_sprites container
    all_sprites.draw(screen)
    draw_text(screen, str(score), 50, WIDTH/2, 10)
    pygame.display.update()

pygame.quit()
