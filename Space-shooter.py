
import pygame
from os.path import join
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images','player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH /2, WINDOW_HEIGHT/1.5))
        self.direction = pygame.math.Vector2()
        self.speed = 500

        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown = 400

    def laser_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_time >= self.cooldown:
            self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * dt * self.speed
        recent_keys = pygame.key.get_just_pressed()
        if int(recent_keys[pygame.K_SPACE]) and self.can_shoot:
            print('fire laser') 
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0,1200), random.randint(0,720))) 
    
#setup
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Gwiezdna Jadka')
running = True
clock = pygame.time.Clock()


#surface
surf = pygame.Surface((100,150))
surf.fill('white')

#
all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


meteor = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor.get_frect(center = (WINDOW_WIDTH /2, WINDOW_HEIGHT/2))

laser = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

# custom events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)



while running:
    dt = clock.tick() /1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False        
        #if event.type == meteor_event:
          #  print("chuj")


    screen.fill("gray")
    #akcje
    all_sprites.update(dt)
      
    all_sprites.draw(screen)
    
    pygame.display.update()

pygame.quit()