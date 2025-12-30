import pygame
from os.path import join
from random import randint, uniform

#stałe
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
PLAYER_SPEED = 500
PLAYER_CD = 800 
LASER_SPEED = 1000

#klasy
class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/1.5))
        self.direction = pygame.math.Vector2()
        self.can_shoot = True 
        self.shoot_time = 0
    def recharge(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= PLAYER_CD:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) 
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) 
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * PLAYER_SPEED * dt
        keys_just = pygame.key.get_just_pressed()
        if keys_just[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (allsprites, laser_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
        self.recharge()

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    
    def update(self, dt):
        self.rect.y -= LASER_SPEED * dt            
        if self.rect.bottom < 0:
            self.kill()

class Star(pygame.sprite.Sprite):
    def __init__(self, group, surf):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
    
class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups,  image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(-200, -100)))
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = uniform(400, 500)

    def update(self, dt):
        self.rect.center += self.speed * dt * self.direction           
        if self.rect.top >= WINDOW_HEIGHT:
            self.kill()

def collisions():
    global running
    for laser in laser_sprites:
        collisions = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collisions:
            laser.kill()
    player_col = pygame.sprite.spritecollide(player, meteor_sprites, False)
    if player_col:
        running = False
#init
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Gwiezdna jadka')
running = True
clock = pygame.time.Clock()

#importy
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()

#sprites
allsprites = pygame.sprite.Group()
for _ in range(20):
    Star(allsprites, star_surf)
player = Player(allsprites)
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

#custom event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

#main loop
while running:
    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
        if event.type == meteor_event:
            Meteor((allsprites, meteor_sprites), meteor_surf)


    screen.fill('grey')

    allsprites.update(dt)
    allsprites.draw(screen)
    
    collisions( )

    pygame.display.update()

pygame.display.quit()