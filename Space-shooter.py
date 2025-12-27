#main
import pygame
from os.path import join
import random
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

#importing an image
player_surf = pygame.image.load(join('images','player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH /2, WINDOW_HEIGHT/1.5))
player_direction = pygame.math.Vector2(0,0)
player_speed = 500


star = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_pos = [((random.randint(0,1200), random.randint(0,720))) for _ in range(20)]

meteor = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor.get_frect(center = (WINDOW_WIDTH /2, WINDOW_HEIGHT/2))

laser = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))



while running:
    dt = clock.tick() /1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False        
   
    screen.fill("grey")
    #akcje
       
    keys = pygame.key.get_pressed()

    player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    player_direction = player_direction.normalize() if player_direction else player_direction
    player_rect.center += player_direction * dt * player_speed

    recent_keys = pygame.key.get_just_pressed()
    print('fire laser') if int(recent_keys[pygame.K_SPACE]) else None

    for pos in star_pos:
        screen.blit(star, pos)
    
    screen.blit(laser, laser_rect)    
    screen.blit(meteor, meteor_rect)
    
    screen.blit(player_surf, player_rect)
    
    
    pygame.display.update()

pygame.quit()