from pygame import *
from random import *
from time import time as timer


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

        if keys[K_w] and self.rect.y > 500:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < window_height - self.rect.height:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < window_width - self.rect.width:
            self.rect.x += self.speed

        # pos = mouse.get_pos()
        # self.rect.x = pos[0]
        # self.rect.y = pos[1]


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > window_height + 100:
            self.rect.y = -100
            self.rect.x = randint(10, window_width - 50)
            self.speed = randint(2, 4)


window_width, window_height = 900, 700
sprite_width, sprite_height = 70, 50
window = display.set_mode((window_width, window_height))
display.set_caption('Shooter')

background = transform.scale(image.load('images/galaxy.jpg'), (window_width, window_height))

font.init()
font2 = font.Font(None, 50)
win = font2.render("You win", True, (0, 200, 0))
lose = font2.render("You lose", True, (200, 0, 0))
game = True


player = Player("images/rocket.png", window_width / 2 - 70, window_height - 100, 70, 90, 6)

monsters = sprite.Group()
monsters_png = ["images/ufo.png", "images/asteroid.png"]
for i in range(5):
    monster = Enemy(choice(monsters_png), randint(0, window_width), -100, 50, 50, randint(1, 2))
    monsters.add(monster)


clock = time.Clock()

run = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if run:
        window.blit(background, (0, 0))

        player.update()
        player.reset()

        monsters.update()
        monsters.draw(window)

    display.update()
    clock.tick(60)

