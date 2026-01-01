import pygame
from os.path import join 
from random import randint, uniform

#constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
LASER_SPEED = 800
CD = 1000

#classes
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png'))
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT //1.5))
        self.direction = pygame.Vector2()
        self.speed = 500
        self.can_shoot = True
        self.shoot_time = 0
        self.mask = pygame.mask.from_surface(self.image)
        

    def recharge(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_time >= CD:
            self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])  
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        if self.direction:
            self.direction = self.direction.normalize()
        self.rect.center += dt * self.direction * self.speed
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites,laser_group), self.rect.midtop, laser_surf)
            laser_sound.play()
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
        self.recharge()
        
class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, dt):
        self.rect.y -= LASER_SPEED * dt
        if self.rect.bottom <= 0:
            self.kill()
            
        
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image  = surf
        self.rect = self.image.get_frect(center = (randint(0,WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.original_image = surf
        self.image = self.original_image
        self.rect = self.image.get_frect(center = (randint(0,WINDOW_WIDTH), randint(-200, -100)))
        self.speed = randint(500,900)
        self.direction = pygame.Vector2((uniform(-0.5, 0.5), 1))
        self.rotation = 0
        self.rotation_speed = randint(-200, 200) 
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, dt):
        self.rect.center += self.speed * dt * self.direction         
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
        self.rotation += self.rotation_speed  * dt
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center )
        
class Explosion(pygame.sprite.Sprite):
    def __init__(self, groups, pos, frames):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        if self.frame_index >= len(frames):
            self.kill()
           


def collisions():
    if pygame.sprite.spritecollide(player, meteor_group, True, pygame.sprite.collide_mask):
        return False
    for laser in laser_group:
        if pygame.sprite.spritecollide(laser, meteor_group, True, pygame.sprite.collide_mask):
            laser.kill()
            Explosion(all_sprites, laser.rect.center, frames)
            explosion_sound.play() 
    
    return True
    
def display_time():
    current_time = pygame.time.get_ticks() / 1000

    text_surf = font.render(f'{current_time:.1f}', True, "#fcfcfc")
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 100))
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, 'white', text_rect.inflate(20,20).move(0,-5), 5,10)

#init
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('gwiezdna strzelanka')
clock = pygame.time.Clock()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 35)
running = True

#importy
frames = [pygame.image.load(join('images', 'explosion',  f'{i}.png')).convert_alpha() for i in range(21)]
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()

laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laser_sound.set_volume(0.01)
game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music.set_volume(0.01)
game_music.play(-1)
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosion_sound.set_volume(0.01)
damage_sound = pygame.mixer.Sound(join('audio', 'damage.ogg'))
damage_sound.set_volume(0.01)
#sprites
all_sprites = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

#custom events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 600)

#main loop
while running:
    dt = clock.tick() / 1000
    screen.fill("#070a3f")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor((all_sprites, meteor_group), meteor_surf)

    display_time()
    all_sprites.update(dt)
    all_sprites.draw(screen)
    
    running = collisions()
    

    pygame.display.update()

pygame.quit()

