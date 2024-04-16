import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Among Us Clone")

map_image = pygame.image.load("The_Skeld.webp")

scale_factor = 3

clock = pygame.time.Clock()
FPS = 60


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, speed=0):
        super().__init__()
        self.image = pygame.transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        screen.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed=0):
        super().__init__(player_image, player_x, player_y, player_width, player_height, player_speed)
        last_direction = None

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= player_speed
            last_direction = 'left'
        elif keys[pygame.K_d]:
            self.rect.x += player_speed
            last_direction = 'right'

        if keys[pygame.K_w]:
            self.rect.y -= player_speed
            last_direction = 'up'
        elif keys[pygame.K_s]:
            self.rect.y += player_speed
            last_direction = 'down'


scaled_map = pygame.transform.scale(map_image, (map_image.get_width() * scale_factor, map_image.get_height() * scale_factor))

player = Player('sprite.png', WIDTH / 2 - 50, HEIGHT / 2 - 50, 50, 50, 5)


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    map_x = WIDTH // 2
    map_y = HEIGHT // 2

    screen.blit(scaled_map, (-map_x, -map_y))

    player.reset()

    player_center_x = WIDTH // 2
    player_center_y = HEIGHT // 2

    pygame.display.flip()

pygame.quit()
sys.exit()
