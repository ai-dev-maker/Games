import pygame
import sys
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Among Us Clone")

clock = pygame.time.Clock()
FPS = 60

sprite_running_right = None
sprite_running_left = None

width_sprite, height_sprite = 50, 60

run_right = [pygame.image.load("images/sprites/red_right0.png"), pygame.image.load("images/sprites/red_right1.png"),
             pygame.image.load("images/sprites/red_right2.png"), pygame.image.load("images/sprites/red_right3.png")]


class Button:
    def __init__(self, width, height, inactive_color, active_color, display):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.display = display

    def draw(self, display,  x, y, message, action=None, font_size=35):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1:
                # pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(3)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))

        print_text(display, message=message, x=x+10, y=y+10, font_color=(0, 0, 0), font_size=font_size)

    def is_clicked(self, mouse_pos):
        button_rect = pygame.Rect(0, 0, self.width, self.height)
        return button_rect.collidepoint(mouse_pos)


def print_text(window, message, x, y, font_color, font_type="font/game_font.ttf", font_size=35):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    window.blit(text, (x, y))


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
        self.left = False
        self.right = False
        self.stand = True
        self.anim_count = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.map_x += self.speed
            self.left = True
            self.right = False
            self.stand = False
        elif keys[pygame.K_d]:
            self.map_x -= self.speed
            self.right = True
            self.left = False
            self.stand = False
        if keys[pygame.K_w]:
            self.map_y += self.speed
            self.right = False
            self.left = False
            self.stand = True
        elif keys[pygame.K_s]:
            self.map_y -= self.speed
            self.right = False
            self.left = False
            self.stand = True
        else:
            self.right = False
            self.left = False
            self.stand = True
            self.anim_count = 0

        self.rect.x = (WIDTH // 2)
        self.rect.y = (HEIGHT // 2)

    def reset(self):
        if self.anim_count + 1 >= FPS:
            self.anim_count = 0

        if self.stand:
            screen.blit(self.image, self.rect)
        if self.right:
            screen.blit(run_right[self.anim_count // 4], self.rect)
        if self.left:
            pass

        self.anim_count += 1


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
    player = Player('images/sprites/red_sprite.png', -1825, -136, width_sprite, height_sprite, 5)

    wall1 = Wall(20, 200, -1825, -136, (200, 0, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(scaled_map, (player.map_x, player.map_y))

        player.reset()
        player.update()

        wall1.reset()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def game_menu():
    map_image = pygame.image.load("images/map/menu.webp")
    transform_map = pygame.transform.scale(map_image, (WIDTH, HEIGHT))

    play_btn = Button(105, 45, (100, 0, 0), (150, 0, 0), screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(transform_map, (0, 0))

        play_btn.draw(screen, WIDTH // 2 - 50, HEIGHT // 2 - 25, "Play", game_run, 30)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


game_menu()
