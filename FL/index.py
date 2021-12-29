from os import spawnle, spawnve
import pygame
import random
import sys

from pygame.constants import K_SPACE
from pygame.transform import rotate

# tạo hàm cho game


def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 650))

    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True


def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3, 1)
    return new_bird


pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
# tạo biến cho game
gravity = 0.25  # trọng lực
bird_movement = 0  # di chuyeern chim
game_active = True

# chen background
bg = pygame.image.load('FileGame\\assets\\background-night.png').convert()
bg = pygame.transform.scale2x(bg)
# chen sàn
floor = pygame.image.load('FileGame\\assets\\floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# tạo chim
# bird_down = pygame.transform.scale2x(pygame.image.load('FileGame\\assets\\yellowbird-downflap.png')).convert_alpha
# bird_mid = pygame.transform.scale2x(pygame.image.load('FileGame\\assets\\yellowbird-midflap.png')).convert_alpha
# bird_up = pygame.transform.scale2x(pygame.image.load('FileGame\\assets\\yellowbird-upflap.png')).convert_alpha
# bird_list = [bird_down, bird_mid, bird_up] #0 1 2
# bird_index = 0
# bird = bird_list[bird_index]
bird = pygame.image.load(
    'FileGame\\assets\\yellowbird-midflap.png').convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 384))
# tạo ống
pipe_surface = pygame.image.load('FileGame\\assets\\pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -7
            if event.key == K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

    screen.blit(bg, (0, 0))

    if game_active:
        # chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

    # sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
