import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Among Us Clone")

map_image = pygame.image.load("The_Skeld.webp")

scale_factor = 3
scaled_map = pygame.transform.scale(map_image, (map_image.get_width() * scale_factor, map_image.get_height() * scale_factor))

clock = pygame.time.Clock()
FPS = 60


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, speed=0):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (player_width, player_height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        screen.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self, player_image, map_x, map_y, player_width, player_height, speed=0):
        super().__init__(player_image, map_x, map_y, player_width, player_height, speed)
        self.map_x = map_x
        self.map_y = map_y

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.map_x += self.speed
        elif keys[pygame.K_d]:
            self.map_x -= self.speed
        if keys[pygame.K_w]:
            self.map_y += self.speed
        elif keys[pygame.K_s]:
            self.map_y -= self.speed

        self.rect.x = (WIDTH // 2)
        self.rect.y = (HEIGHT // 2)


class Animation(pygame.sprite.Sprite):
    def __init__(self, name_dir_anim, pos_x, pos_y, count_sprite):
        super().__init__()
        self.animation_set = [transform.scale(image.load(f"{name_dir_anim}/{i}.png"), (50, 50)) for i in range(1, count_sprite)]
        self.i = 0
        self.x = pos_x
        self.y = pos_y

    def update(self):
        window.blit(self.animation_set[self.i], (self.x-50, self.y))
        self.i += 1
        if self.i > len(self.animation_set) - 1:
            self.kill()


def game_run():
    player = Player('sprite.png', -1430, -190, 50, 50, 5)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(scaled_map, (player.map_x, player.map_y))

        player.reset()
        player.update()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


game_run()
