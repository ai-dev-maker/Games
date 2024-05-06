class Impostor(GameSprite):
    def __init__(self, impostor_image, impostor_x, impostor_y, impostor_width, impostor_height, speed=0):
        super().__init__(impostor_image, impostor_x, impostor_y, impostor_width, impostor_height, 5)
        self.counter = 0

    def update(self, bot_sprites):
        for bot in bot_sprites:
            # Рассчитываем расстояние между центрами спрайтов
            different_x = bot.rect.centerx - self.rect.centerx
            different_y = bot.rect.centery - self.rect.centery

            if abs(different_x) > abs(different_y):
                if different_x > 0:
                    self.rect.x += self.speed - 2
                    self.animation(kind="right")
                else:
                    self.rect.x -= self.speed - 2
                    self.animation(kind="left")
            else:
                if different_y > 0:
                    self.rect.y += self.speed - 2
                else:
                    self.rect.y -= self.speed - 2
                bot.speed = 0
                bot.animation(kind='dead')
