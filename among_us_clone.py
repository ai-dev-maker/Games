import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)

WHITE = (255, 255, 255)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Among Us Clone")

map_image = pygame.image.load("The_Skeld.webp")

player_x, player_y = WIDTH // 2, HEIGHT // 2

player_speed = 3

scale_factor = 3

last_direction = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
        last_direction = 'left'
    elif keys[pygame.K_d]:
        player_x += player_speed
        last_direction = 'right'

    if keys[pygame.K_w]:
        player_y -= player_speed
        last_direction = 'up'
    elif keys[pygame.K_s]:
        player_y += player_speed
        last_direction = 'down'

    screen.fill(WHITE)

    map_x = player_x - WIDTH // 2
    map_y = player_y - HEIGHT // 2

    scaled_map = pygame.transform.scale(map_image, (map_image.get_width() * scale_factor, map_image.get_height() * scale_factor))
    screen.blit(scaled_map, (-map_x, -map_y))
    pygame.draw.circle(screen, (255, 0, 0), (WIDTH // 2, HEIGHT // 2), 10)

    pygame.display.flip()

pygame.quit()
sys.exit()
