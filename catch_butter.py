import pygame, os, sys, random
from pygame import math

pygame.init()
WINDOW_SIZE = (800, 800)
display = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Catch The Butter!")

# Butter Details
butter_size = math.Vector2(50, 50)
butter_objects = []
BUTTER_FALLING_SPEED = 1

# Bread Details
bread_size = math.Vector2(50, 100)
bread_pos = math.Vector2(0, 700)
BREAD_MOVEMENT_SPEED = 50

# Spawn Details
spawns = []
for i in range(int(WINDOW_SIZE[0]/50)): # Adds all spawn locations to spawns list
    spawns.append(math.Vector2(i * 50, -50))

player_score = 0
lives = 3

delta_time = 0
previous_timeframe = 0


while True:

    # Calculating Delta Time or Time Between Frames
    current_time = pygame.time.get_ticks()
    delta_time = (current_time - previous_timeframe)/1000
    previous_timeframe = current_time


    # Background Filling
    display.fill((0, 0, 0))


    # Processing Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            if event.key == pygame.K_a:
                bread_pos.x -= BREAD_MOVEMENT_SPEED
            elif event.key == pygame.K_d:
                bread_pos.x += BREAD_MOVEMENT_SPEED
   

    # Spawning Butter Objects
    if len(butter_objects) > 0: # if list of butter objects is not empty
        if butter_objects[-1][1] >= 10:
            spawn = random.choice(spawns) 
            butter_objects.append(pygame.Rect(spawn, butter_size))
        elif butter_objects[0][1] >= 800:
            lives -= 1
            butter_objects.remove(butter_objects[0])
            print("Lives: ", lives)
    elif len(butter_objects) == 0: # if list of butter_objects is empty
        spawn = random.choice(spawns) # Spawn the first block of butter 
        butter_objects.append(pygame.Rect(spawn, butter_size))


    # Rendering Butter Objects
    for butter in butter_objects:
        butter_rect = pygame.Rect(math.Vector2(butter[0], butter[1] + BUTTER_FALLING_SPEED), math.Vector2(butter[2], butter[3]))
        pygame.draw.rect(display, (255, 200, 10), butter_rect)
        butter_objects[butter_objects.index(butter)] = butter_rect
    

    # Rendering Bread Player
    bread_rect = pygame.draw.rect(display, (255, 200, 10), pygame.Rect(bread_pos, bread_size))
   

    # Checking Bread and Butter Collisions
    for collider in butter_objects:
        if pygame.Rect.colliderect(bread_rect, collider):
            player_score += 1 
            butter_objects.remove(collider)
            print("Score: ", player_score)


    # Checking Bread Lives
    if lives <= 0:
        print("YOU LOSE")
        pygame.quit()
        sys.exit()


    # Update 
    clock.tick(60)
    pygame.display.update()
