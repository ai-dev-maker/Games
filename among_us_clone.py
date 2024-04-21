import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Among Us Clone")

clock = pygame.time.Clock()
FPS = 60

sprite_running_right = None
sprite_running_left = None

width_sprite, height_sprite = 65, 65


class Button:
    def __init__(self, width, height, inactive_color, active_color, display):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.display = display

    def draw(self, window, x, y, message, action=None, font_size=35):
        mouse_ = mouse.get_pos()
        click = mouse.get_pressed()
        if x < mouse_[0] < x + self.width and y < mouse_[1] < y + self.height:
            draw.rect(window, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1:
                time.delay(3)
                if action is not None:
                    action()
        else:
            draw.rect(window, self.inactive_color, (x, y, self.width, self.height))

        print_text(window, message=message, x=x+10, y=y+10, font_color=(0, 0, 0), font_size=font_size)

    def is_clicked(self, mouse_pos):
        button_rect = pygame.Rect(0, 0, self.width, self.height)
        return button_rect.collidepoint(mouse_pos)


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
        global sprite_running_right, sprite_running_left
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.map_x += self.speed
            sprite_running_left = True
        elif keys[pygame.K_d]:
            self.map_x -= self.speed
            sprite_running_right = True
        if keys[pygame.K_w]:
            self.map_y += self.speed
            sprite_running_left = True
        elif keys[pygame.K_s]:
            self.map_y -= self.speed
            sprite_running_right = True
        elif keys[pygame.K_g]:
            print(self.map_x, self.map_y)

        self.rect.x = (WIDTH // 2)
        self.rect.y = (HEIGHT // 2)


class Animation(pygame.sprite.Sprite):
    def __init__(self, name_dir_anim, pos_x, pos_y, count_sprite):
        super().__init__()
        self.animation_set = [pygame.transform.scale(pygame.image.load(f"{name_dir_anim}/{i}.png"), (width_sprite, height_sprite)) for i in range(1, count_sprite)]
        self.i = 0
        self.x = pos_x
        self.y = pos_y

    def update(self):
        screen.blit(self.animation_set[self.i], (self.x, self.y))
        self.i += 1
        if self.i > len(self.animation_set) - 1:
            self.kill()


class Wall(pygame.sprite.Sprite):
    def __init__(self, wall_width, wall_height, wall_x, wall_y, color):
        super().__init__()
        self.image = pygame.Surface((wall_width, wall_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def reset(self):
        screen.blit(self.image, self.rect)


def game_run():
    map_image = pygame.image.load("images/map/The_Skeld_map.webp")

    scale_factor = 0.5
    scaled_map = pygame.transform.scale(map_image, (map_image.get_width() * scale_factor, map_image.get_height() * scale_factor))
    player = Player('images/sprites/sprite.png', -1825, -136, width_sprite, height_sprite, 5)

    wall1 = Wall(20, 200, -1825, -136, (100, 0, 0))

    walls = [wall1]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(scaled_map, (player.map_x, player.map_y))

        player.reset()
        player.update()

        for wall in walls:
            wall.reset()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def game_menu():
    map_image = pygame.image.load("images/map/menu.webp")
    transform_map = pygame.transform.scale(map_image, (WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(transform_map, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


game_menu()
