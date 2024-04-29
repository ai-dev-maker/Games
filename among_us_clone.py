import pygame
import sys
import time
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Among Us Clone")

clock = pygame.time.Clock()
FPS = 60

sprite_running_right = None
sprite_running_left = None

width_sprite, height_sprite = 40, 50

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

    def update(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.rect.x < 0:
            if not self.check_collision(-self.speed, 0):
                self.rect.x += self.speed
            # self.image = pygame.transform.scale(image.load("images/sprites/red_sprite"), (self.rect.width, self.rect.height))
        elif keys[pygame.K_d] and self.rect.x < screen.get_width() - 50:
            if not self.check_collision(self.speed, 0):
                self.rect.x -= self.speed
            # self.image = pygame.transform.scale(image.load("Pright.png"), (self.rect.width, self.rect.height))

        elif keys[pygame.K_w] and self.rect.y < 0:
            if not self.check_collision(0, -self.speed):
                self.rect.y += self.speed
            # self.image = pygame.transform.scale(image.load("Pup.png"), (self.rect.width, self.rect.height))
        elif keys[pygame.K_s] and self.rect.y < screen.get_height() - 50:
            if not self.check_collision(0, self.speed):
                self.rect.y -= self.speed
            # self.image = pygame.transform.scale(image.load("Pdown.png"), (self.rect.width, self.rect.height))
        if keys[pygame.K_g]:
            print(self.rect.x, self.rect.y)

    def check_collision(self, x_shift, y_shift):
        new_rect = self.rect.move(x_shift, y_shift)
        for wall in GroupWall:
            wall.reset()

            wall_closest_x = min(max(new_rect.x, wall.rect.x), wall.rect.x + wall.rect.width)
            wall_closest_y = min(max(new_rect.y, wall.rect.y), wall.rect.y + wall.rect.height)

            distance = math.sqrt((new_rect.x - wall_closest_x) ** 2 + (new_rect.y - wall_closest_y) ** 2)

            if distance <= float(0):
                print('000')
                return True

            if distance <= self.speed:
                print('111')
                return True

            if new_rect.colliderect(wall.rect):
                print('222')
                return True

        return False


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


GroupWall = pygame.sprite.Group()

wall1 = Wall(50, 200, -1625, -136, (255, 255, 255))
wall2 = Wall(200, 50, -1725, -136, (255, 255, 255))

GroupWall.add(wall1, wall2)


def game_run():
    map_image = pygame.image.load("images/map/The_Skeld_map.webp")

    scale_factor = 0.5
    scaled_map = pygame.transform.scale(map_image, (map_image.get_width() * scale_factor, map_image.get_height() * scale_factor))
    player = Player('images/sprites/red_sprite.png', -1925, -100, width_sprite, height_sprite, 5)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(scaled_map, (player.rect.x, player.rect.y))

        player.reset()
        player.update()

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

        play_btn.draw(screen, WIDTH // 2 + 240, HEIGHT - 550, "Play", game_run, 30)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


game_run()
