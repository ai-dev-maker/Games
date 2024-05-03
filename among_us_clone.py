import pygame
import sys
import time
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
SCENE_WIDTH = 8565
SCENE_HEIGHT = 4794

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

    def draw(self, display, x, y, message, action=None, font_size=35):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1:
                # pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(100)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))

        print_text(display, message=message, x=x + 10, y=y + 10, font_color=(0, 0, 0), font_size=font_size)

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
        self.width_sprite = width_sprite
        self.height_sprite = height_sprite

    def reset(self):
        screen.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, speed=0):
        GameSprite.__init__(self, player_image, player_x, player_y, player_width, player_height, speed=0)
        self.counter = 0

    def update(self):
        global cam_x
        global cam_y

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if self.rect.y < HEIGHT // 2 - height_sprite and cam_y + self.speed <= 0:
                cam_y += self.speed
            elif self.rect.y > 10:
                if not self.check_collision(0, -self.speed):
                    self.rect.y -= self.speed
            self.animation(kind='right')

        elif keys[pygame.K_s]:
            if self.rect.y > HEIGHT // 2 - height_sprite and cam_y - self.speed >= HEIGHT - SCENE_HEIGHT:
                cam_y -= self.speed
            elif self.rect.y < HEIGHT - 50:
                if not self.check_collision(0, self.speed):
                    self.rect.y += self.speed
            self.animation(kind='left')

        elif keys[pygame.K_a]:
            if self.rect.x < WIDTH // 2 and cam_x + self.speed <= 0:
                cam_x += self.speed
            elif self.rect.x > 0:
                if not self.check_collision(-self.speed, 0):
                    self.rect.x -= self.speed
            self.animation(kind='left')

        elif keys[pygame.K_d]:
            if self.rect.x > WIDTH // 2 and cam_x - self.speed >= WIDTH - SCENE_WIDTH:
                cam_x -= self.speed
            elif self.rect.x < WIDTH - 50:
                if not self.check_collision(self.speed, 0):
                    self.rect.x += self.speed
            self.animation(kind='right')

        else:
            self.animation(kind='stay')

    def animation(self, kind):
        if kind == 'stay':
            self.image = pygame.transform.scale(pygame.image.load("images/sprites/red_sprite.png"), (self.width_sprite, self.height_sprite))

        elif kind == 'right':
            self.counter += 1
            if 0 <= self.counter < 15:
                self.image = pygame.transform.scale(pygame.image.load("images/sprites/red_right0.png"), (self.width_sprite, self.height_sprite))
            elif 15 <= self.counter < 30:
                self.image = pygame.transform.scale(pygame.image.load("images/sprites/red_right1.png"), (self.width_sprite, self.height_sprite))
            elif 30 <= self.counter < 45:
                self.image = pygame.transform.scale(pygame.image.load("images/sprites/red_right2.png"), (self.width_sprite, self.height_sprite))
            elif 45 <= self.counter < 60:
                self.image = pygame.transform.scale(pygame.image.load("images/sprites/red_right3.png"), (self.width_sprite, self.height_sprite))

            if self.counter > 60:
                self.counter = 0

        elif kind == 'left':
            self.counter += 1
            if 0 <= self.counter < 15:
                self.image = pygame.transform.scale(pygame.image.load("images/sprites/red_left0.png"), (self.width_sprite, self.height_sprite))
            elif 15 <= self.counter < 30:
                self.image = pygame.transform.scale(pygame.image.load("images/sprites/red_left1.png"), (self.width_sprite, self.height_sprite))
            elif 30 <= self.counter < 45:
                self.image = pygame.transform.scale(pygame.image.load("images/sprites/red_left2.png"), (self.width_sprite, self.height_sprite))
            elif 45 <= self.counter < 60:
                self.image = pygame.transform.scale(pygame.image.load("images/sprites/red_left1.png"), (self.width_sprite, self.height_sprite))

            if self.counter > 60:
                self.counter = 0

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

    def controls(self):
        pass


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

wall1 = Wall(50, 200, -100, -100, (255, 255, 255))
wall2 = Wall(200, 50, -1725, -136, (255, 255, 255))

GroupWall.add(wall1, wall2)


player = Player('images/sprites/red_sprite.png', WIDTH // 2, HEIGHT // 2 - height_sprite,
                width_sprite, height_sprite, 5)

cam_x = -player.rect.x - WIDTH // 2
cam_y = -player.rect.y - HEIGHT // 2


def game_run():
    map_image = pygame.image.load("images/map/The_Skeld_map.webp")

    scale_factor = 0.5
    scaled_map = pygame.transform.scale(map_image,
                                        (map_image.get_width() * scale_factor, map_image.get_height() * scale_factor))

    keys = pygame.key.get_pressed()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.KEYDOWN:
            #     if keys[pygame.K_TAB]:
            #         open_mini_map()
            # if event.type == pygame.KEYUP:
            #     if keys[pygame.K_TAB]:
            #         showing_mini_map = False

        screen.blit(scaled_map, (cam_x, cam_y))

        player.reset()
        player.update()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def game_menu():
    # pygame.mixer.init()
    # pygame.mixer.music.load('music/among_us_impostor.mp3')
    # pygame.mixer.music.play()

    map_image = pygame.image.load("images/map/main_menu.jpg")
    transform_map = pygame.transform.scale(map_image, (WIDTH, HEIGHT))

    play_btn = Button(105, 45, (100, 0, 0), (150, 0, 0), screen)
    settings_btn = Button(185, 45, (100, 0, 0), (150, 0, 0), screen)
    quit_btn = Button(105, 45, (100, 0, 0), (150, 0, 0), screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(transform_map, (0, 0))

        play_btn.draw(screen, WIDTH // 2 - 370, HEIGHT - 570, "Play", game_run, 30)
        settings_btn.draw(screen, WIDTH // 2 - 370, HEIGHT - 520, "Settings", settings, 30)
        quit_btn.draw(screen, WIDTH // 2 + 270, HEIGHT - 570, "Quit", close, 30)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def settings():
    map_image = pygame.image.load("images/map/main_menu.jpg")
    transform_map = pygame.transform.scale(map_image, (WIDTH, HEIGHT))

    back_btn = Button(115, 45, (100, 0, 0), (150, 0, 0), screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(transform_map, (0, 0))

        back_btn.draw(screen, WIDTH // 2 - 370, HEIGHT - 570, "Back", game_menu, 30)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def open_mini_map():
    map_image = pygame.image.load("images/map/mini_map.png")
    transform_map = pygame.transform.scale(map_image, (WIDTH, HEIGHT))

    running = True
    showing_mini_map = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if showing_mini_map:
            screen.blit(transform_map, (0, 0))

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
    sys.exit()


def close():
    click = pygame.mouse.get_pressed()
    if click[0] == 1:
        sys.exit()


game_menu()
