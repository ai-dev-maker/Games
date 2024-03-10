from pygame import *
from random import *
from time import time as timer

mixer.init()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, speed=0):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

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

    def fire(self):
        bullet = Bullet("images/bullet.png", self.rect.centerx-6, self.rect.y, 10, 14, 10)
        Bullets.add(bullet)
        # f = mixer.Sound("music/fire.ogg")
        # f.play()


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed

        if self.rect.y > window_height + 100:
            self.rect.y = -100
            self.rect.x = randint(10, window_width - 50)
            self.speed = randint(2, 4)
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < -50:
            self.kill()


window_width, window_height = 900, 700
sprite_width, sprite_height = 70, 50
window = display.set_mode((window_width, window_height))
display.set_caption('Shooter')

background = transform.scale(image.load('images/galaxy.jpg'), (window_width, window_height))

font.init()
font2 = font.Font(None, 50)
font3 = font.SysFont('Georgia', 20)
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

Bullets = sprite.Group()

score = 0
lost = 0
live = 10

run = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            player.fire()

    if run:
        window.blit(background, (0, 0))

        player.update()
        player.reset()

        monsters.update()
        monsters.draw(window)

        Bullets.update()
        Bullets.draw(window)

        score_text = font3.render("Score: " + str(score), True, (255, 255, 255))
        window.blit(score_text, (20, 20))
        lost_text = font3.render("Lost: " + str(lost), True, (255, 255, 255))
        window.blit(lost_text, (20, 45))
        live_text = font3.render("Live: " + str(live), True, (150, 0, 0))
        window.blit(live_text, (20, 70))

        collide = sprite.groupcollide(Bullets, monsters, True, True)
        for i in collide:
            score += 1
            monster = Enemy(choice(monsters_png), randint(0, window_width), -100, 50, 50, randint(1, 2))
            monsters.add(monster)

        collide_2 = sprite.spritecollide(player, monsters, True)
        for i in collide_2:
            if live > 1:
                live -= 1
                monster = Enemy(choice(monsters_png), randint(0, window_width), -100, 50, 50, randint(1, 2))
                monsters.add(monster)
            else:
                run = False

    display.update()
    clock.tick(60)

