from pygame import *  
from time import time as timer 
import sys  
import math  

mixer.init()

WIDTH, HEIGHT = 800, 600 
SCENE_WIDTH = 8565  
SCENE_HEIGHT = 4794 

SCREEN_SIZE = (WIDTH, HEIGHT)

screen = display.set_mode(SCREEN_SIZE)
display.set_caption("Among Us")
display.set_icon(image.load('images/icon_among_us.png'))

clock = time.Clock()
FPS = 60

width_sprite, height_sprite = 40, 50


button_sound = mixer.Sound('music/button.mp3')
running_sound = mixer.Sound('music/running.wav')
round_start_sound = mixer.Sound('music/round-start.mp3')
win_sound = mixer.Sound('music/win.mp3')
lose_sound = mixer.Sound('music/lose.mp3')
impostor_catch = mixer.Sound('music/impostor_kill.mp3')


class Button:
    def __init__(self, width, height, inactive_color, active_color, window):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.window = window

    def draw(self, window, x, y, message, action=None, font_size=35):
        mouse_ = mouse.get_pos()
        click = mouse.get_pressed()
        if x < mouse_[0] < x + self.width and y < mouse_[1] < y + self.height:
            draw.rect(window, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1:
                button_sound.set_volume(0.3)
                button_sound.play()
                time.delay(100)
                if action is not None:
                    action()
        else:
            draw.rect(window, self.inactive_color, (x, y, self.width, self.height))

        print_text(window, message=message, x=x + 10, y=y + 10, font_color=(220, 220, 220), font_size=font_size)
        
    def is_clicked(self, mouse_pos):
        button_rect = Rect(0, 0, self.width, self.height)
        return button_rect.collidepoint(mouse_pos)


def print_text(window, message, x, y, font_color, font_type="font/game_font.ttf", font_size=35):
    font.init()
    font_type = font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    window.blit(text, (x, y))


"""Головний клас"""


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, speed=0):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width_sprite = width_sprite
        self.height_sprite = height_sprite
        self.counter = 0

    def animation(self, kind):
        if kind == 'stay_right':
            self.image = transform.scale(image.load("images/sprites/red_sprite.png"),
                                         (self.width_sprite, self.height_sprite))

        elif kind == 'right':
            self.counter += 1
            if 0 <= self.counter < 20:
                self.image = transform.scale(image.load("images/sprites/red_right0.png"),
                                             (self.width_sprite, self.height_sprite))
            elif 20 <= self.counter < 25:
                self.image = transform.scale(image.load("images/sprites/red_right1.png"),
                                             (self.width_sprite, self.height_sprite))
            elif 25 <= self.counter < 45:
                self.image = transform.scale(image.load("images/sprites/red_right2.png"),
                                             (self.width_sprite, self.height_sprite))
            elif 45 <= self.counter < 60:
                self.image = transform.scale(image.load("images/sprites/red_right3.png"),
                                             (self.width_sprite, self.height_sprite))

            if self.counter > 60:
                self.counter = 0

        if kind == 'stay_left':
            self.image = transform.scale(image.load("images/sprites/stay_left.png"),
                                         (self.width_sprite, self.height_sprite))
        elif kind == 'left':
            self.counter += 1
            if 0 <= self.counter < 20:
                self.image = transform.scale(image.load("images/sprites/red_left0.png"),
                                             (self.width_sprite, self.height_sprite))
            elif 20 <= self.counter < 25:
                self.image = transform.scale(image.load("images/sprites/red_left1.png"),
                                             (self.width_sprite, self.height_sprite))
            elif 25 <= self.counter < 45:
                self.image = transform.scale(image.load("images/sprites/red_left2.png"),
                                             (self.width_sprite, self.height_sprite))
            elif 45 <= self.counter < 60:
                self.image = transform.scale(image.load("images/sprites/red_left1.png"),
                                             (self.width_sprite, self.height_sprite))

            if self.counter > 60:
                self.counter = 0

        elif kind == 'dead':
            self.image = transform.scale(image.load("images/sprites/dead2.png"),
                                         (self.width_sprite, self.height_sprite))
    def reset(self):
        screen.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, speed=0):
        super().__init__(player_image, player_x, player_y, player_width, player_height, 5)
        self.counter = 0
        self.is_moving = False

    def update(self):
        global cam_x
        global cam_y

        keys = key.get_pressed()

        if keys[K_w]:
            self.is_moving = True
            if self.rect.y < HEIGHT // 2 - height_sprite and cam_y + self.speed <= 0:
                cam_y += self.speed
            elif self.rect.y > 10:
                if not self.check_collision(0, -self.speed):
                    self.rect.y -= self.speed
            self.animation(kind='right')

        elif keys[K_s]:
            self.is_moving = True
            if self.rect.y > HEIGHT // 2 - height_sprite and cam_y - self.speed >= HEIGHT - SCENE_HEIGHT:
                cam_y -= self.speed
            elif self.rect.y < HEIGHT - 50:
                if not self.check_collision(0, self.speed):
                    self.rect.y += self.speed
            self.animation(kind='left')

        elif keys[K_a]:
            self.is_moving = True
            if self.rect.x < WIDTH // 2 and cam_x + self.speed <= 0:
                cam_x += self.speed
            elif self.rect.x > 0:
                if not self.check_collision(-self.speed, 0):
                    self.rect.x -= self.speed
            self.animation(kind='left')

        elif keys[K_d]:
            self.is_moving = True
            if self.rect.x > WIDTH // 2 and cam_x - self.speed >= WIDTH - SCENE_WIDTH:
                cam_x -= self.speed
            elif self.rect.x < WIDTH - 50:
                if not self.check_collision(self.speed, 0):
                    self.rect.x += self.speed
            self.animation(kind='right')

        else:
            self.animation(kind='stay_right')
            self.is_moving = False

        if self.is_moving:
            if running_sound.get_num_channels() == 0:
                running_sound.set_volume(0.05)
                running_sound.play()
        else:
            running_sound.stop()

    def check_collision(self, x_shift, y_shift):
        new_rect = self.rect.move(x_shift, y_shift)
        for wall in GroupWall:
            # wall.reset()

            wall_closest_x = min(max(new_rect.x, wall.rect.x), wall.rect.x + wall.rect.width)
            wall_closest_y = min(max(new_rect.y, wall.rect.y), wall.rect.y + wall.rect.height)

            distance = math.sqrt((new_rect.x - wall_closest_x) ** 2 + (new_rect.y - wall_closest_y) ** 2)

            if distance <= float(0):
                return True

            if distance <= self.speed:
                return True

            if new_rect.colliderect(wall.rect):
                return True

        return False


class Wall(sprite.Sprite):
    def __init__(self, wall_width, wall_height, wall_x, wall_y, back_color):
        super().__init__()
        self.image = Surface((wall_width, wall_height))
        self.image.fill(back_color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

        self.local_x = wall_x
        self.local_y = wall_y

    def update(self):
        self.rect.x = (self.local_x + cam_x)
        self.rect.y = (self.local_y + cam_y)
        screen.blit(self.image, self.rect)

    def reset(self):
        screen.blit(self.image, self.rect)


class Crewmate(GameSprite):
    def __init__(self, bot_image, bot_x, bot_y, bot_width, bot_height, speed=0):
        super().__init__(bot_image, bot_x, bot_y, bot_width, bot_height, 5)
        self.counter = 0

    def update(self, player_rect):
        different_x = player_rect.x - self.rect.x
        different_y = player_rect.y - self.rect.y

        if abs(different_x) > abs(different_y):
            if different_x > 0:
                self.rect.x += self.speed - 3
                self.animation(kind="right")
            else:
                self.rect.x -= self.speed - 3
                self.animation(kind="left")
        else:
            if different_y > 0:
                self.rect.y += self.speed - 3
            else:
                self.rect.y -= self.speed - 3


class Impostor(GameSprite):
    def __init__(self, impostor_image, impostor_x, impostor_y, impostor_width, impostor_height, speed=0):
        super().__init__(impostor_image, impostor_x, impostor_y, impostor_width, impostor_height, 2)
        self.local_x = impostor_x
        self.local_y = impostor_y
        
    def update(self, player_rect):
        different_x = player_rect.x - self.rect.x
        different_y = player_rect.y - self.rect.y

        if abs(different_x) > abs(different_y):
            if different_x > 0:
                if not self.check_collision(-self.speed, 0):
                    self.rect.x += self.speed
                    self.animation(kind="right")
                if self.check_collision(-self.speed, 0):
                    self.rect.y -= self.speed
            else:
                if not self.check_collision(self.speed, 0):
                    self.rect.x -= self.speed
                    self.animation(kind="left")
                if self.check_collision(0, -self.speed):
                    self.rect.y -= self.speed
        else:
            if different_y > 0:
                if not self.check_collision(0, -self.speed):
                    self.rect.y += self.speed
            else:
                if not self.check_collision(0, self.speed):
                    self.rect.y -= self.speed

        # self.rect.x = (self.local_x + cam_x + 1700)
        # self.rect.y = (self.local_y + cam_y + 380)

        screen.blit(self.image, self.rect)

    def check_collision(self, x_shift, y_shift):
        """Створюю 'хітбокс'"""
        new_rect = self.rect.move(x_shift, y_shift)
        for wall in GroupWall:
            # wall.reset()

            wall_closest_x = min(max(new_rect.x, wall.rect.x), wall.rect.x + wall.rect.width)
            wall_closest_y = min(max(new_rect.y, wall.rect.y), wall.rect.y + wall.rect.height)

            distance = math.sqrt((new_rect.x - wall_closest_x) ** 2 + (new_rect.y - wall_closest_y) ** 2)

            if distance <= float(0):
                return True

            if distance <= self.speed:
                return True

            if new_rect.colliderect(wall.rect):
                return True

        return False
    
    def reset(self):
        self.rect.x = (self.local_x + cam_x + 1700)
        self.rect.y = (self.local_y + cam_y + 380)
        screen.blit(self.image, self.rect)


GroupWall = sprite.Group()

wall1 = Wall(770, 13, 1157, 480, (255, 0, 255))
wall2 = Wall(13, 192, 1153, 585, (255, 0, 255))
wall3 = Wall(447, 13, 1153, 585, (255, 0, 255))
wall4 = Wall(13, 132, 1598, 585, (255, 0, 255))
wall5 = Wall(132, 13, 1478, 705, (255, 0, 255))
wall6 = Wall(13, 423, 1477, 635, (255, 0, 255))
wall7 = Wall(13, 240, 1868, 640, (255, 0, 255))
wall8 = Wall(13, 215, 1922, 588, (255, 0, 255))
wall9 = Wall(13, 295, 1922, 198, (255, 0, 255))
wall10 = Wall(195, 13, 1740, 586, (255, 0, 255))
wall11 = Wall(13, 132, 1730, 586, (255, 0, 255))
wall12 = Wall(150, 13, 1730, 705, (255, 0, 255))
wall13 = Wall(13, 878, 2024, 1020, (255, 0, 255))
wall14 = Wall(510, 173, 1524, 1147, (255, 0, 255))
wall15 = Wall(220, 13, 2150, 1023, (255, 0, 255))
wall16 = Wall(220, 13, 2488, 1023, (255, 0, 255))
wall17 = Wall(13, 210, 2492, 1023, (255, 0, 255))
wall18 = Wall(13, 350, 2353, 1023, (255, 0, 255))
wall19 = Wall(200, 13, 2160, 1360, (255, 0, 255))
wall20 = Wall(700, 13, 1330, 1988, (255, 0, 255))
wall21 = Wall(13, 260, 1324, 1738, (255, 0, 255))
wall22 = Wall(180, 13, 1154, 1738, (255, 0, 255))
wall23 = Wall(300, 13, 1154, 1628, (255, 0, 255))
wall24 = Wall(13, 160, 1154, 1738, (255, 0, 255))
wall25 = Wall(320, 13, 838, 1883, (255, 0, 255))
wall26 = Wall(13, 220, 1154, 1408, (255, 0, 255))
wall27 = Wall(150, 305, 1034, 1168, (255, 0, 255))
wall28 = Wall(150, 305, 764, 1168, (255, 0, 255))
wall29 = Wall(150, 305, 1034, 768, (255, 0, 255))
wall30 = Wall(150, 305, 764, 768, (255, 0, 255))
wall31 = Wall(118, 13, 1463, 1880, (255, 0, 255))
wall32 = Wall(337, 13, 1688, 1880, (255, 0, 255))
wall33 = Wall(13, 268, 1463, 1630, (255, 0, 255))
wall34 = Wall(13, 588, 1563, 1310, (255, 0, 255))
wall35 = Wall(13, 145, 1692, 1740, (255, 0, 255))
wall36 = Wall(145, 13, 1692, 1740, (255, 0, 255))
wall37 = Wall(13, 185, 1910, 1475, (255, 0, 255))
wall38 = Wall(50, 185, 2050, 1415, (255, 0, 255))
wall39 = Wall(50, 120, 2100, 1385, (255, 0, 255))
wall40 = Wall(70, 120, 2150, 1355, (255, 0, 255))
wall41 = Wall(210, 70, 2150, 1355, (255, 0, 255))
wall42 = Wall(250, 340, 2220, 1600, (255, 0, 255))
wall43 = Wall(13, 320, 2575, 1365, (255, 0, 255))
wall44 = Wall(80, 13, 2495, 1425, (255, 0, 255))
wall45 = Wall(13, 120, 2495, 1315, (255, 0, 255))
wall46 = Wall(170, 13, 2495, 1315, (255, 0, 255))
wall47 = Wall(670, 13, 2495, 1215, (255, 0, 255))
wall48 = Wall(400, 13, 2650, 1560, (255, 0, 255))
wall49 = Wall(13, 260, 2660, 1320, (255, 0, 255))
wall50 = Wall(13, 260, 3120, 1230, (255, 0, 255))
wall51 = Wall(200, 100, 2800, 1350, (255, 0, 255))
wall52 = Wall(640, 13, 2590, 1675, (255, 0, 255))
wall53 = Wall(310, 150, 2580, 1785, (255, 0, 255))
wall54 = Wall(13, 420, 2580, 1785, (255, 0, 255))
wall55 = Wall(940, 13, 2180, 2195, (255, 0, 255))
wall56 = Wall(13, 30, 2020, 1995, (255, 0, 255))
wall57 = Wall(185, 140, 2320, 480, (255, 0, 255))
wall58 = Wall(230, 180, 2075, 230, (255, 0, 255))
wall59 = Wall(230, 180, 2515, 215, (255, 0, 255))
wall60 = Wall(230, 150, 2515, 720, (255, 0, 255))
wall61 = Wall(230, 150, 2055, 720, (255, 0, 255))
wall62 = Wall(360, 220, 724, 1538, (255, 0, 255))
wall63 = Wall(13, 450, 724, 1408, (255, 0, 255))
wall64 = Wall(150, 100, 724, 1838, (255, 0, 255))
wall65 = Wall(140, 170, 624, 1288, (255, 0, 255))
wall66 = Wall(140, 170, 624, 763, (255, 0, 255))
wall67 = Wall(13, 400, 719, 370, (255, 0, 255))
wall68 = Wall(210, 13, 428, 763, (255, 0, 255))
wall69 = Wall(13, 660, 428, 763, (255, 0, 255))
wall70 = Wall(200, 13, 428, 1403, (255, 0, 0))
wall71 = Wall(100, 260, 428, 920, (255, 0, 255))
wall72 = Wall(360, 220, 724, 450, (255, 0, 255))
wall73 = Wall(70, 13, 719, 380, (255, 0, 255))
wall74 = Wall(370, 13, 789, 360, (255, 0, 255))
wall75 = Wall(13, 130, 1159, 360, (255, 0, 255))
wall76 = Wall(260, 13, 1174, 1283, (255, 0, 255))
wall77 = Wall(13, 410, 1419, 873, (255, 0, 255))
wall78 = Wall(100, 130, 1349, 1030, (255, 0, 255))
wall79 = Wall(50, 13, 1369, 873, (255, 0, 255))
wall80 = Wall(50, 13, 1184, 873, (255, 0, 255))
wall81 = Wall(180, 13, 1219, 843, (255, 0, 255))
wall82 = Wall(50, 140, 1479, 1050, (255, 0, 255))
wall83 = Wall(20, 225, 1979, 855, (255, 0, 255))
wall84 = Wall(20, 220, 1929, 810, (255, 0, 255))
wall85 = Wall(20, 140, 1871, 840, (255, 0, 255))
wall86 = Wall(20, 50, 2039, 920, (255, 0, 255))
wall87 = Wall(20, 50, 2109, 990, (255, 0, 255))
wall88 = Wall(20, 140, 1979, 1400, (255, 0, 255))
wall89 = Wall(20, 140, 1939, 1430, (255, 0, 255))
wall90 = Wall(20, 70, 1889, 1670, (255, 0, 255))
wall91 = Wall(20, 70, 1859, 1710, (255, 0, 255))
wall92 = Wall(230, 110, 1570, 1450, (255, 0, 255))
wall93 = Wall(20, 50, 2070, 960, (255, 0, 255))
wall94 = Wall(20, 50, 2070, 30, (255, 0, 255))
wall95 = Wall(20, 50, 2020, 90, (255, 0, 255))
wall96 = Wall(20, 50, 1970, 150, (255, 0, 255))
wall97 = Wall(600, 13, 2100, 50, (255, 0, 255))
wall98 = Wall(20, 70, 2700, 30, (255, 0, 255))
wall99 = Wall(20, 50, 2750, 90, (255, 0, 255))
wall100 = Wall(20, 50, 2800, 150, (255, 0, 255))
wall101 = Wall(20, 50, 2850, 210, (255, 0, 255))
wall102 = Wall(20, 50, 2900, 270, (255, 0, 255))
wall103 = Wall(13, 200, 2940, 288, (255, 0, 255))
wall104 = Wall(13, 340, 2940, 588, (255, 0, 255))
wall105 = Wall(410, 20, 2870, 858, (255, 0, 0))
wall106 = Wall(130, 20, 2830, 898, (255, 0, 255))
wall107 = Wall(130, 20, 2790, 938, (255, 0, 255))
wall108 = Wall(130, 20, 2740, 978, (255, 0, 255))
wall109 = Wall(500, 13, 2720, 1038, (255, 0, 255))
wall110 = Wall(13, 65, 3190, 1000, (255, 0, 255))
wall111 = Wall(50, 20, 2900, 828, (255, 0, 255))
wall112 = Wall(308, 13, 3190, 988, (255, 0, 255))
wall113 = Wall(260, 13, 3635, 988, (255, 0, 255))
wall114 = Wall(260, 13, 3635, 1108, (255, 0, 255))
wall115 = Wall(13, 160, 3635, 1108, (255, 0, 0))
wall116 = Wall(13, 190, 3635, 808, (255, 0, 255))
wall117 = Wall(210, 13, 3425, 858, (255, 0, 255))
wall118 = Wall(13, 320, 3405, 558, (255, 0, 255))
wall119 = Wall(13, 280, 3285, 598, (255, 0, 255))
wall120 = Wall(340, 13, 2945, 588, (255, 0, 255))
wall121 = Wall(250, 13, 2945, 478, (255, 0, 255))
wall122 = Wall(13, 100, 3185, 378, (255, 0, 255))
wall123 = Wall(50, 13, 3185, 378, (255, 0, 255))
wall124 = Wall(13, 100, 3235, 278, (255, 0, 255))
wall125 = Wall(120, 13, 3235, 268, (255, 0, 255))
wall126 = Wall(40, 30, 3385, 298, (255, 0, 255))
wall127 = Wall(40, 30, 3425, 338, (255, 0, 255))
wall128 = Wall(40, 30, 3465, 378, (255, 0, 255))
wall129 = Wall(40, 60, 3505, 418, (255, 0, 255))
wall130 = Wall(70, 13, 3435, 468, (255, 0, 255))
wall131 = Wall(13, 80, 3425, 468, (255, 0, 255))
wall132 = Wall(13, 175, 3490, 1000, (255, 0, 255))
wall133 = Wall(205, 13, 3285, 1162, (255, 0, 255))
wall134 = Wall(13, 455, 3275, 1162, (255, 0, 255))
wall135 = Wall(235, 13, 3405, 1262, (255, 0, 255))
wall136 = Wall(13, 400, 3405, 1262, (255, 0, 255))
wall137 = Wall(13, 100, 3405, 1812, (255, 0, 255))
wall138 = Wall(13, 200, 3435, 1632, (255, 0, 255))
wall139 = Wall(50, 50, 3345, 1922, (255, 0, 255))
wall140 = Wall(250, 13, 3105, 1962, (255, 0, 255))
wall141 = Wall(13, 180, 3135, 1782, (255, 0, 255))
wall142 = Wall(170, 13, 3035, 1782, (255, 0, 255))
wall143 = Wall(170, 13, 3125, 1882, (255, 0, 255))
wall144 = Wall(13, 30, 3280, 1852, (255, 0, 255))
wall145 = Wall(50, 50, 3200, 1802, (255, 0, 255))
wall146 = Wall(50, 50, 3220, 1612, (255, 0, 255))
wall147 = Wall(50, 50, 3060, 1532, (255, 0, 255))
wall148 = Wall(50, 60, 3090, 1512, (255, 0, 255))
wall149 = Wall(13, 140, 3023, 1782, (255, 0, 255))
wall150 = Wall(60, 13, 3023, 1922, (255, 0, 255))
wall151 = Wall(13, 280, 3083, 1922, (255, 0, 255))
wall152 = Wall(40, 180, 3043, 2032, (255, 0, 255))
wall153 = Wall(50, 180, 2623, 2032, (255, 0, 255))
wall154 = Wall(200, 70, 2763, 2132, (255, 0, 255))
wall155 = Wall(50, 50, 2023, 2052, (255, 0, 255))
wall156 = Wall(60, 50, 2043, 2082, (255, 0, 255))
wall157 = Wall(70, 50, 2063, 2112, (255, 0, 255))
wall158 = Wall(80, 50, 2083, 2142, (255, 0, 255))
wall159 = Wall(13, 140, 3890, 1108, (255, 0, 255))
wall160 = Wall(13, 180, 3890, 808, (255, 0, 255))
wall161 = Wall(180, 13, 3890, 1226, (255, 0, 255))
wall162 = Wall(180, 13, 3890, 808, (255, 0, 255))
wall163 = Wall(13, 430, 4070, 813, (255, 0, 255))


GroupWall.add(wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9, wall10, wall11, wall12, wall13,
              wall14, wall15, wall16, wall17, wall18, wall19, wall20, wall21, wall22, wall23, wall24, wall25,
              wall26, wall27, wall28, wall29, wall30, wall31, wall32, wall33, wall34, wall35, wall36, wall37,
              wall38, wall39, wall40, wall41, wall42, wall43, wall44, wall45, wall46, wall47, wall48, wall49,
              wall50, wall51, wall52, wall53, wall54, wall55, wall56, wall57, wall58, wall59, wall60, wall61,
              wall62, wall63, wall64, wall65, wall66, wall67, wall68, wall69, wall70, wall71, wall72, wall73,
              wall74, wall75, wall76, wall77, wall78, wall79, wall80, wall81, wall82, wall83, wall84, wall85,
              wall86, wall87, wall88, wall89, wall90, wall91, wall92, wall93, wall94, wall95, wall96, wall97,
              wall98, wall99, wall100, wall101, wall102, wall103, wall104, wall105, wall106, wall107, wall108,
              wall109, wall110, wall111, wall112, wall113, wall114, wall115, wall116, wall117, wall118, wall119,
              wall120, wall121, wall122, wall123, wall124, wall125, wall126, wall127, wall128, wall129, wall130,
              wall131, wall132, wall133, wall134, wall135, wall136, wall137, wall138, wall139, wall140, wall141,
              wall142, wall143, wall144, wall145, wall146, wall147, wall148, wall149, wall150, wall151, wall152,
              wall153, wall154, wall155, wall156, wall157, wall158, wall159, wall160, wall161, wall162, wall163)

GroupCrewmate = sprite.Group()

# crewmate1 = Crewmate("images/sprites/red_sprite.png", 1000, 100, width_sprite, height_sprite, 3)
# crewmate2 = Crewmate("images/sprites/red_sprite.png", 900, 100, width_sprite, height_sprite, 3)
# crewmate3 = Crewmate("images/sprites/red_sprite.png", 800, 100, width_sprite, height_sprite, 3)
#
# GroupCrewmate.add(crewmate1, crewmate2, crewmate3)

player = Player('images/sprites/red_sprite.png', WIDTH // 2, HEIGHT // 2 - height_sprite,
                width_sprite, height_sprite, 5)

cam_x = -player.rect.x - WIDTH // 2 - 1050
cam_y = -player.rect.y - HEIGHT // 2 + 350

impostor = Impostor("images/sprites/red_sprite.png", 700, 300, width_sprite, height_sprite, 4)


def game_run():
    start_time = time.get_ticks()
    game_duration = 15
    font_ = font.Font("font/game_font.ttf", 20)

    map_image = image.load("images/map/The_Skeld_map.webp")
    scale_factor = 0.5
    scaled_map = transform.scale(map_image,
                                 (map_image.get_width() * scale_factor, map_image.get_height() * scale_factor))

    dark_surface = Surface((1000, 600), SRCALPHA)
    dark_color = (0, 0, 0)
    max_alpha = 255
    current_alpha = 0

    increasing_alpha = True

    alpha_change_speed = 1

    running = True
    game_timer = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        if game_timer:
            elapsed_time = time.get_ticks() - start_time
            elapsed_seconds = elapsed_time // 1000

            GroupWall.update()

            screen.blit(scaled_map, (cam_x, cam_y))

            player.reset()
            player.update()

            if elapsed_seconds <= 10:
                impostor.reset()
                timer_text = font_.render(str(int(10 - elapsed_seconds)), True, (0, 0, 0))
                screen.blit(timer_text, (WIDTH // 2, 500))
            elif elapsed_seconds >= 10:
                impostor.update(player.rect)
                timer_text = font_.render("Time: " + str(int(game_duration - elapsed_seconds)), True, (255, 255, 255))
                screen.blit(timer_text, (10, 10))

            collide = sprite.collide_rect(player, impostor)
            if collide:
                if impostor_catch.get_num_channels() == 0:
                    impostor_catch.set_volume(0.05)
                    impostor_catch.play()
                player.speed = 0
                player.animation(kind='dead')
                impostor.speed = 0
                time.delay(20)
                if running_sound.get_num_channels() == 0:
                    lose_sound.set_volume(0.05)
                    lose_sound.play()
                if increasing_alpha:
                    current_alpha += alpha_change_speed
                    if current_alpha >= max_alpha:
                        increasing_alpha = False

                dark_surface.fill((dark_color[0], dark_color[1], dark_color[2], current_alpha))
                screen.blit(dark_surface, (0, 0))
                if not increasing_alpha:
                    game_menu()
                    running = False
                    game_timer = False
            else:
                if elapsed_seconds >= game_duration:
                    player.speed = 0
                    impostor.speed = 0
                    player.animation(kind='stay_right')
                    impostor.animation(kind='stay_right')
                    if running_sound.get_num_channels() == 0:
                        win_sound.set_volume(0.05)
                        win_sound.play()
                    if increasing_alpha:
                        current_alpha += alpha_change_speed
                        if current_alpha >= max_alpha:
                            increasing_alpha = False

                    dark_surface.fill((dark_color[0], dark_color[1], dark_color[2], current_alpha))
                    screen.blit(dark_surface, (0, 0))

                    if not increasing_alpha:
                        game_menu()
                        running = False
                        game_timer = False

            display.update()
            clock.tick(FPS)

    quit()
    sys.exit()
    

def game_menu():
    map_image = image.load("images/map/among-us-menu.jpg")
    transform_map = transform.scale(map_image, (WIDTH, HEIGHT))

    play_btn = Button(150, 56, (0, 0, 0), (50, 0, 10), screen)
    settings_btn = Button(265, 56, (0, 0, 0), (50, 0, 10), screen)
    quit_btn = Button(135, 56, (0, 0, 0), (50, 0, 10), screen)

    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        screen.blit(transform_map, (0, 0))

        play_btn.draw(screen, WIDTH // 2 - 75, HEIGHT - 385, "Play", lobby, 45)
        settings_btn.draw(screen, WIDTH // 2 - 132.5, HEIGHT - 330, "Settings", settings, 45)
        quit_btn.draw(screen, WIDTH // 2 - 67.5, HEIGHT - 275, "Quit", close, 45)

        display.update()
        clock.tick(FPS)

    quit()
    sys.exit()


def settings():
    map_image = image.load("images/map/main_menu.jpg")
    transform_map = transform.scale(map_image, (WIDTH, HEIGHT))

    back_btn = Button(115, 45, (0, 0, 0), (50, 0, 0), screen)
    how_to_play_btn = Button(290, 50, (0, 0, 0), (50, 0, 10), screen)
    features_btn = Button(225, 50, (0, 0, 0), (50, 0, 10), screen)

    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        screen.blit(transform_map, (0, 0))

        back_btn.draw(screen, WIDTH // 2 - 370, HEIGHT - 570, "Back", game_menu, 30)
        how_to_play_btn.draw(screen, WIDTH // 2 - 145, HEIGHT - 455, "How To Play", how_to_play, 35)
        features_btn.draw(screen, WIDTH // 2 - 112.5, HEIGHT - 405, "Features", describe, 35)

        display.update()
        clock.tick(FPS)

    quit()
    sys.exit()


def how_to_play():
    map_image = image.load("images/map/how_to_play.jpg")
    transform_map = transform.scale(map_image, (WIDTH, HEIGHT))

    back_btn = Button(115, 45, (0, 0, 0), (50, 0, 0), screen)

    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        screen.blit(transform_map, (0, 0))

        back_btn.draw(screen, WIDTH // 2 - 370, HEIGHT - 570, "Back", settings, 30)

        print_text(screen, """Мета:""", WIDTH // 2 - 300, HEIGHT - 500, (255, 255, 255), font_size=25)
        print_text(screen, """Протриматися певний час від перевертня,""",
                   WIDTH // 2 - 280, HEIGHT - 470, (255, 255, 255), font_size=15)
        print_text(screen, """щоб він не наздогнав головного героя""",
                   WIDTH // 2 - 280, HEIGHT - 450, (255, 255, 255), font_size=15)
        print_text(screen, """Управління:""", WIDTH // 2 - 300, HEIGHT - 420, (255, 255, 255), font_size=25)
        print_text(screen, """w - уверх""", WIDTH // 2 - 280, HEIGHT - 380, (255, 255, 255), font_size=15)
        print_text(screen, """s - униз""", WIDTH // 2 - 280, HEIGHT - 360, (255, 255, 255), font_size=15)
        print_text(screen, """d - вправо""", WIDTH // 2 - 280, HEIGHT - 340, (255, 255, 255), font_size=15)
        print_text(screen, """a - вліво""", WIDTH // 2 - 280, HEIGHT - 320, (255, 255, 255), font_size=15)

        display.update()
        clock.tick(FPS)

    quit()
    sys.exit()


def describe():
    map_image = image.load("images/map/how_to_play.jpg")
    transform_map = transform.scale(map_image, (WIDTH, HEIGHT))

    back_btn = Button(115, 45, (0, 0, 0), (50, 0, 0), screen)
    wall = Wall(800, 200, WIDTH // 2 - 400, HEIGHT - 420, (0, 0, 0))

    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        screen.blit(transform_map, (0, 0))

        back_btn.draw(screen, WIDTH // 2 - 370, HEIGHT - 570, "Back", settings, 30)

        wall.reset()

        print_text(screen, """Мій бот - ворог, має не ідеальний, але не поганий ШІ""", WIDTH // 2 - 380,
                   HEIGHT - 420, (255, 255, 255), font_size=15)
        print_text(screen, """Іноді можна пройти через стіну, іноді - ні""", WIDTH // 2 - 380,
                   HEIGHT - 380, (255, 255, 255), font_size=15)
        print_text(screen, """Бот передвигається швидше, коли головний герой біжить""", WIDTH // 2 - 380,
                   HEIGHT - 340, (255, 255, 255), font_size=15)

        display.update()
        clock.tick(FPS)

    quit()
    sys.exit()


def lobby():
    map_image = image.load("images/among_us.jpg")
    transform_map = transform.scale(map_image, (1000, 600))

    dark_surface = Surface((1000, 600), SRCALPHA)
    dark_color = (0, 0, 0)
    max_alpha = 250
    current_alpha = 0

    increasing_alpha = True

    alpha_change_speed = 1.2

    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        if increasing_alpha:
            current_alpha += alpha_change_speed
            if current_alpha >= max_alpha:
                increasing_alpha = False
                game_run()
                running = False

        dark_surface.fill((dark_color[0], dark_color[1], dark_color[2], current_alpha))

        screen.blit(transform_map, (-100, 0))
        screen.blit(dark_surface, (0, 0))

        if round_start_sound.get_num_channels() == 0:
            round_start_sound.set_volume(0.2)
            round_start_sound.play()
            time.delay(100)

        display.update()
        clock.tick(FPS)

    quit()
    sys.exit()


def close():
    click = mouse.get_pressed()
    if click[0] == 1:
        sys.exit()


game_menu() 
