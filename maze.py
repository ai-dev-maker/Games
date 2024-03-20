from pygame import *
from random import *

# ---------------- Class ---------------- #


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, speed=0):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def manage_sprite(self):
        keys = key.get_pressed()

        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 450:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 650:
            self.rect.x += self.speed

    def reset(self):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < window_height - self.rect.height:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < window_width - self.rect.width:
            self.rect.x += self.speed


class Enemy(GameSprite):
    direction = 'right'

    def update_x(self):
        if self.rect.x > window_width - 720:
            self.direction = 'left'
        elif self.rect.x < window_width - 890:
            self.direction = 'right'

        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def follow_player_update(self, player_rect):
        different_x = player_rect.x - self.rect.x
        different_y = player_rect.y - self.rect.y

        if abs(different_x) > abs(different_y):
            if different_x > 0:
                self.rect.x += self.speed - 3
            else:
                self.rect.x -= self.speed - 3
        else:
            if different_y > 0:
                self.rect.y += self.speed - 3
            else:
                self.rect.y -= self.speed - 3


class Wall(sprite.Sprite):
    def __init__(self, wall_width, wall_height, wall_x, wall_y, color):
        super().__init__()
        self.image = Surface((wall_width, wall_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


mixer.init()
# mixer.music.load("music/jungles.ogg")
# mixer.music.play()

money = mixer.Sound("music/money.ogg")
kick = mixer.Sound("music/kick.ogg")

window_width, window_height = 900, 700
sprite_width, sprite_height = 70, 50
window = display.set_mode((window_width, window_height))
display.set_caption('Maze')

background = transform.scale(image.load('background.jpg'), (window_width, window_height))


game = True
player = Player("sprites/hero.png", 30, 30, 50, 50, 5)
monster1 = Enemy("sprites/cyborg.png", 50, 560, 50, 50, 5)
gold = GameSprite("sprites/treasure.png", 800, 600, 70, 70, 0)

color_wall = (120, 255, 120)
wall1 = Wall(8, 420, 120, 0, color_wall)
wall2 = Wall(8, 410, 230, 200, color_wall)
wall3 = Wall(280, 8, 230, 70, color_wall)
wall4 = Wall(8, 300, 340, 70, color_wall)
wall5 = Wall(8, 300, 450, 300, color_wall)
wall6 = Wall(300, 8, 350, 600, color_wall)
wall7 = Wall(500, 8, 450, 180, color_wall)
wall8 = Wall(8, 50, 450, 75, color_wall)
wall9 = Wall(45, 8, 300, 200, color_wall)
wall10 = Wall(8, 300, 550, 180, color_wall)
wall11 = Wall(8, 300, 650, 400, color_wall)
wall12 = Wall(8, 300, 750, 180, color_wall)

objects = [wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9, wall10, wall11, wall12]

font.init()
font2 = font.Font(None, 50)
win = font2.render("You win", True, (0, 200, 0))
lose = font2.render("You lose", True, (200, 0, 0))


clock = time.Clock()

run = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if run:
        window.blit(background, (0, 0))
        player.reset()
        monster1.reset()
        gold.reset()

        # Manage Sprite
        player.update()

        # Monster Update
        monster1.update_x()

        # Draw walls
        for object in objects:
            object.reset()
            if sprite.collide_rect(player, object):
                window.blit(lose, (window_width-350, window_height-350))
                run = False

        if sprite.collide_rect(player, gold):
            window.blit(win, (window_width-350, window_height-350))
            run = False

        clock.tick(60)
        display.update()
