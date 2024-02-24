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
        if self.rect.x > 650:
            self.direction = 'left'
        elif self.rect.x < 450:
            self.direction = 'right'

        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    direction_y = 'up'

    def update_y(self):
        if self.rect.y > 350:
            self.direction = 'up'
        elif self.rect.y < 450:
            self.direction = 'down'

        if self.direction == 'up':
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed

    arrow_x = 0
    arrow_y = 0
    cadr = 0

    def update_random(self):
        self.cadr += 1

        if self.cadr % 20 == 0:
            self.arrow_x += randint(-self.speed, self.speed)
            self.arrow_y += randint(-self.speed, self.speed)

        self.rect.x = self.arrow_x
        self.rect.y = self.arrow_y

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


mixer.init()
# mixer.music.load("music/jungles.ogg")
# mixer.music.play()

money = mixer.Sound("music/money.ogg")
kick = mixer.Sound("music/kick.ogg")

window_width, window_height = 700, 500
sprite_width, sprite_height = 70, 50
window = display.set_mode((window_width, window_height))
display.set_caption('Maze')

background = transform.scale(image.load('background.jpg'), (window_width, window_height))


game = True
player = Player("sprites/hero.png", 50, 50, 50, 50, 5)
monster = Enemy("sprites/cyborg.png", 550, 300, 50, 50, 5)
gold = GameSprite("sprites/treasure.png", 550, 400, 70, 70, 0)

clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    # Draw Objects
    window.blit(background, (0, 0))
    player.reset()
    monster.reset()
    gold.reset()

    # Manage Sprite
    player.update()

    # Monster Update
    monster.follow_player_update(player.rect)

    clock.tick(60)
    display.update()
