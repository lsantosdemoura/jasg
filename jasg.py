import random

import pygame
from pygame.locals import *

SCREEN_SIZE = (1200, 800)
PIXEL_SIZE = 20
PIXEL_WIDTH = 20
PIXEL_HEIGHT = 20


UP = K_UP
RIGHT = K_RIGHT
DOWN = K_DOWN
LEFT = K_LEFT


def get_random_location():
    x_axis = random.randint(0, 1190)
    y_axis = random.randint(0, 790)
    return (x_axis // PIXEL_SIZE * PIXEL_SIZE, y_axis // PIXEL_SIZE * PIXEL_SIZE)


def collision(position1, position2):
    return (position1[0] == position2[0]) and (position1[1] == position2[1])


def move_snake_tail(snake_location):
    for i in range(len(snake_location) - 1, 0, -1):
        snake_location[i] = (snake_location[i - 1][0], snake_location[i - 1][1])
    return snake_location


def move_snake(direction, snake_location):
    snake_location = move_snake_tail(snake_location)

    if direction == UP:
        snake_location[0] = (snake_location[0][0], snake_location[0][1] - PIXEL_SIZE)
    if direction == DOWN:
        snake_location[0] = (snake_location[0][0], snake_location[0][1] + PIXEL_SIZE)
    if direction == RIGHT:
        snake_location[0] = (snake_location[0][0] + PIXEL_SIZE, snake_location[0][1])
    if direction == LEFT:
        snake_location[0] = (snake_location[0][0] - PIXEL_SIZE, snake_location[0][1])

    return snake_location


def get_direction(key, current_direction):
    if key == K_UP and current_direction != DOWN:
        return UP
    if key == K_DOWN and current_direction != UP:
        return DOWN
    if key == K_LEFT and current_direction != RIGHT:
        return LEFT
    if key == K_RIGHT and current_direction != LEFT:
        return RIGHT
    return current_direction


def blit_snake(snake_location, screen):
    for i, pos in enumerate(snake_location):
        if i % 2 == 0:
            screen.blit(YELLOW_SNAKE_SKIN, pos)
        else:
            screen.blit(BLUE_SNAKE_SKIN, pos)


def game_over(snake_location):
    snake_head = snake_location[0]
    if (
        snake_head[0] == 1200
        or snake_head[1] == 800
        or snake_head[0] < 0
        or snake_head[1] < 0
    ):
        return True
    for i in range(1, len(snake_location) - 1):
        if collision(snake_head, snake_location[i]):
            return True
    return False

def quit_game():
    pygame.quit()
    quit()


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Jasg")


snake_location = [(200, 200), (220, 200), (240, 200)]
YELLOW_SNAKE_SKIN = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
BLUE_SNAKE_SKIN = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
YELLOW_SNAKE_SKIN.fill((255, 220, 83))
BLUE_SNAKE_SKIN.fill((62, 123, 172))


fruit_location = get_random_location()
fruit = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
fruit.fill((255, 0, 0))

direction = LEFT

clock = pygame.time.Clock()

while True:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()

    # check if fruit had been eaten
    if collision(snake_location[0], fruit_location):
        fruit_location = get_random_location()
        snake_location.append((0, 0))

    if game_over(snake_location):
        quit_game()

    if event.type == KEYDOWN:
        direction = get_direction(event.key, direction)

    snake_location = move_snake(direction, snake_location)

    screen.fill((0, 0, 0))
    screen.blit(fruit, fruit_location)
    blit_snake(snake_location=snake_location, screen=screen)

    pygame.display.update()
