import pygame
import random  # for generating a bunch of rocks randomly
import os

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WIDTH = 500
HEIGHT = 600
pygame.init()
# initialize the mixer module
pygame.mixer.init() 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("This is my first pygame.") 
clock = pygame.time.Clock()

# load images
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
player_img_mini = pygame.transform.scale(player_img, (25, 19))
player_img_mini.set_colorkey(BLACK)

# load 7 rock images that will be randomly selected later
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
# use a dictionary
expl_anim = {}        # initial expl_anim  
expl_anim['lg'] = []  # lg for large image
expl_anim['sm'] = []  # sm for small image
expl_anim['player']=[] # player represnts the player's explosion
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30,30)))
    
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
# load sounds
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
die_sound   = pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
# load music
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.2)

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    use_anti_arial = True
    # draw text on a new Surface
    text_surface = font.render(text, use_anti_arial, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, health, x, y):
    if health<0:
        health = 0
    BAR_LENGTH = 130
    BAR_HEIGHT = 14
    health_bar_length = (health/100)*BAR_LENGTH
    outside_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    filled_rect  = pygame.Rect(x, y, health_bar_length, BAR_HEIGHT)
    pygame.draw.rect(surf, YELLOW, outside_rect, 3)
    # warning hints
    health_warning_thresh = 40
    color = YELLOW
    if health > health_warning_thresh:
        pygame.Surface.fill(surf, GREEN, filled_rect)
    else:
        pygame.Surface.fill(surf, RED, filled_rect)
        color = RED
    offsetX = 20
    offsetY = -5
    # draw health value
    draw_text(surf, str(health), font_size, x + BAR_LENGTH + offsetX, y + offsetY,  color)
   
def draw_lives(surf, lives_left, img, x, y):   
    for i in range(lives_left):
        # first, get the img's surrounded rectangle
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        # ready to draw img on surf
        surf.blit(img, img_rect)

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
        # add a speed property
        self.speedx = 8
        # add a health property
        self.health = 100
        # add a death count
        self.death_count = 0
        # add a maximum death count
        self.death_count_max = 5
        self.is_hidden = False
        self.hidden_time = 0

    def update(self):
        # to show up again when it was hidden
        if self.is_hidden and pygame.time.get_ticks()-self.hidden_time > 1000:
            self.is_hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 50
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
        if not(self.is_hidden):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
    
    def hide(self):
        self.is_hidden = True
        self.hidden_time = pygame.time.get_ticks()
        # put the player outside the window
        self.rect.center = (WIDTH/2, HEIGHT+500)


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image_orig = pygame.Surface((30, 20))
        # self.image_orig.fill(BLUE)
        # image_orig is a copy of rock_img, and it will be used for rotation later  
        self.image_orig = random.choice(rock_imgs)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()     
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85/2)
        self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 5)
        self.rotate_total = 0
        self.rotate_deg = random.randrange(-10, 10)
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

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
        # self.image = pygame.Surface((10, 10))
        # self.image.fill(YELLOW)
        self.radius = 20
        self.image = bullet_img    
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        
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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        # center of object that is going to explore
        # size of explosion
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        # size can be either "sm" or "lg", and zero means the first image
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        # record the index of which to play
        self.frameIndex = 0
        self.last_update = pygame.time.get_ticks()
        self.time_to_update = 50  # 50 (ms)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.time_to_update:
            self.last_update = now
            self.frameIndex += 1
            if self.frameIndex == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frameIndex]
                # get the central position of the old rectangle
                center = self.rect.center
                # get the new rectangle after updating self.image
                self.rect = self.image.get_rect() 
                # put it back to the previos central position
                self.rect.center = center
    
   
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
    new_rock()

score = 0
pygame.mixer.music.play()
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
                               are_bullets_disappeared, 
                               pygame.sprite.collide_circle)

    # Add enough rocks that its amount is equal to the number of collisions                           
    for hit in hits:
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, "lg")
        all_sprites.add(expl)
        score += hit.radius
        new_rock()  

    # Check if the player is colliding with any of rocks
    is_rock_disappeared = True
    hits = pygame.sprite.spritecollide(player, rocks, 
                                      is_rock_disappeared,
                                      pygame.sprite.collide_circle) 
    health_gain = 1
    for hit in hits:
        new_rock()
        player.health -= int(hit.radius/health_gain)
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <=0:
            if player.death_count < player.death_count_max:
                expl_player = Explosion(player.rect.center,'player')
                all_sprites.add(expl_player)
                die_sound.play()
                player.death_count+=1
                player.health = 100
                player.hide()  
            # else:      

    # 1. player's death count has arrived its maximum value
    # 2. wait to stop running game until the player finished its last explosion
    if player.death_count == player.death_count_max and not(expl_player.alive()):
        running = False   
    # if hits:
    #     # running = False

    # (3) display
    # screen.fill(BLACK)
    screen.blit(background_img, (0,0))

    # draw all objects in all_sprites container
    all_sprites.draw(screen)
    draw_text(screen, str(score), 50, WIDTH/2, 10, WHITE)
    font_size = 20
    draw_health(screen, player.health, 10, 20)
    draw_lives(screen, player.death_count_max-player.death_count, player_img_mini, WIDTH-160, 15)
    pygame.display.update()

pygame.quit()
