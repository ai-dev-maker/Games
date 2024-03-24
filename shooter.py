from pygame import *
from random import *
from time import time as timer
import sys


window_width, window_height = 900, 700
sprite_width, sprite_height = 70, 50
window = display.set_mode((window_width, window_height))
display.set_caption('Shooter')

mixer.init()

FPS = 60
clock = time.Clock()


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


class Gun(GameSprite):
    def __init__(self, gun_image, bullet_image, player, size_x, size_y, fire_speed):
        super().__init__(gun_image, player.rect.x, player.rect.y, size_x, size_y, fire_speed)
        self.player = player
        self.bullet_image = bullet_image

    def update(self, shift_x=0, shift_y=0):
        self.rect.x = self.player.rect.x + shift_x
        self.rect.y = self.player.rect.y + shift_y
        self.reset()

    def fire(self):
        bullet = Bullet("images/bullet.png", self.rect.centerx-6, self.rect.y, 10, 14, 10)
        Bullets.add(bullet)


class Animation(sprite.Sprite):
    def __init__(self, name_dir_anim, pos_x, pos_y, count_sprite):
        super().__init__()
        self.animation_set = [transform.scale(image.load(f"{name_dir_anim}/{i}.png"), (50, 50)) for i in range(1, count_sprite)]
        self.i = 0
        self.x = pos_x
        self.y = pos_y

    def update(self):
        window.blit(self.animation_set[self.i], (self.x, self.y))
        self.i += 1
        if self.i > len(self.animation_set) - 1:
            self.kill()


class Boss(GameSprite):
    def __init__(self, boss_image, boss_x, boss_y, size_x, size_y, live=100, fire_speed=10):
        super().__init__(boss_image, boss_x, boss_y, size_x, size_y, 0)
        self.live = live
        self.fire_speed = fire_speed
        self.boss_bullets = sprite.Group()
        self.last_time = 0
        self.boss_is_dead = False

    def update(self):
        if self.boss_is_dead:
            return

        if self.live < 0:
            self.rect.x = -1000
            self.boss_is_dead = True

        print_text(window, "Boss: " + str(self.live), 20, 100, (0, 255, 0), None, 30)

        now_time = timer()
        if now_time - self.last_time > 1:
            bossBullet = Bullet("images/bullet.png", randint(self.rect.x, self.rect.right), self.rect.top + 150, 25, 35, -self.fire_speed)
            self.boss_bullets.add(bossBullet)
            self.last_time = timer()

        self.boss_bullets.update()
        self.boss_bullets.draw(window)
        self.reset()


def print_text(window, message, x, y, font_color, font_type=None, font_size=35):
    font_type = font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    window.blit(text, (x, y))


def game_menu():
    font.init()
    menu_bg = image.load("images/city_menu.png")
    menu_bg = transform.scale(menu_bg, (window.get_width(), window.get_height()))

    play_btn = Button(230, 60, (255, 152, 255), (255, 104, 255), window)
    quit_btn = Button(110, 60, (255, 152, 255), (255, 104, 255), window)

    show = True
    while show:
        for e in event.get():
            if e.type == QUIT:
                show = False

        window.blit(menu_bg, (0, 0))

        play_btn.draw(window, (window_width / 2) - 90, (window_height / 2) - 50, "Play Game", game_run, 57)
        quit_btn.draw(window, (window_width / 2) - 30, (window_height / 2) + 50, "Quit", close_window, 57)

        display.update()
        clock.tick(FPS)


def game_run():
    global Bullets
    global lost

    background = transform.scale(image.load('images/galaxy.jpg'), (window_width, window_height))

    font.init()
    font2 = font.Font(None, 50)
    font3 = font.SysFont('Georgia', 20)
    win = font2.render("You win", True, (0, 200, 0))
    lose = font2.render("You lose", True, (200, 0, 0))
    game = True

    player = Player("images/rocket.png", window_width / 2 - 70, window_height - 100, 70, 90, 6)
    gun1 = Gun("images/rocket.png", "images/bullet.png", player, 50, 70, 6)
    gun2 = Gun("images/rocket.png", "images/bullet.png", player, 50, 70, 6)

    boss = Boss('images/ufo.png', window_width / 2 - 150, 0, 150, 150, 100, 10)

    monsters = sprite.Group()
    monsters_png = ["images/ufo.png", "images/asteroid.png"]
    for i in range(10):
        monster = Enemy(choice(monsters_png), randint(0, window_width), -100, 50, 50, randint(1, 2))
        monsters.add(monster)

    Bullets = sprite.Group()

    anim_hit = sprite.Group()

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
                # gun1.fire()
                # gun2.fire()

        if run:
            window.blit(background, (0, 0))

            player.update()
            player.reset()

            gun1.update(-30, -15)
            gun2.update(50, -15)

            monsters.update()
            monsters.draw(window)

            Bullets.update()
            Bullets.draw(window)

            anim_hit.update()

            score_text = font3.render("Score: " + str(score), True, (255, 255, 255))
            window.blit(score_text, (20, 20))
            lost_text = font3.render("Lost: " + str(lost), True, (255, 255, 255))
            window.blit(lost_text, (20, 45))
            live_text = font3.render("Live: " + str(live), True, (150, 0, 0))
            window.blit(live_text, (20, 70))

            if score > 1:
                boss.update()
                col = sprite.spritecollide(boss, Bullets, True)
                for c in col:
                    x, y = c.rect.x - 10, c.rect.y - 10
                    hit = Animation('images/anim11', x, y, 19)
                    anim_hit.add(hit)
                    boss.live -= 1
                    score += 1

            collide = sprite.groupcollide(Bullets, monsters, True, True)
            for c in collide:
                score += 1
                monster = Enemy(choice(monsters_png), randint(0, window_width), -100, 50, 50, randint(1, 2))
                monsters.add(monster)

                x, y = c.rect.x-10, c.rect.y-10
                hit = Animation('images/anim11', x, y, 19)
                anim_hit.add(hit)

            collide_2 = sprite.spritecollide(player, monsters, True)
            for i in collide_2:
                if live > 1:
                    live -= 1
                    monster = Enemy(choice(monsters_png), randint(0, window_width), -100, 50, 50, randint(1, 2))
                    monsters.add(monster)
                else:
                    run = False

        display.update()
        clock.tick(FPS)


def close_window():
    click = mouse.get_pressed()
    if click[0] == 1:
        sys.exit()


game_menu()

