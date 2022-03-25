import pygame
import pygame.constants
from random import choice
from vars import pygame_btns, pygame_btns_reversed


def color():
    return choice(COLORS), choice(COLORS), choice(COLORS)


def render_text():
    font = pygame.font.SysFont('cera pro', 80)
    text = font.render(msg, True, (255, 255, 255))
    text_under = font.render(msg[:count], True, pygame.color.Color('yellow'))
    screen.blit(text, TEXT_POS)
    screen.blit(text_under, TEXT_POS)
    pygame.display.update()


SIZE = 800, 600
TEXT_POS = 240, 240
FPS = 30
COLORS = [i for i in range(255)]
BLACK = 0, 0, 0

count = 0
msg = 'DETEST ME'

pygame.init()
clock = pygame.time.Clock()
game_icon = pygame.image.load('icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption('Need for nicotine')
screen = pygame.display.set_mode(SIZE)
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            # print(pygame.mouse.get_pos())
            pass
        if event.type == pygame.KEYDOWN:
            need_button = pygame.key.key_code(msg[count])
            keys = pygame.key.get_pressed()
            if keys[need_button]:
                count += 1
    screen.fill(BLACK)
    render_text()
    pygame.display.flip()
