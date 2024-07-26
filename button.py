import pygame
import pygame_func as pg_help


class Button:
    def __init__(self, x, y, width, height, text, color_button, color_font, font, _id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color_button = color_button
        self.color_font = color_font
        self.size = (width, height)
        self.font = font
        self.id = _id

    def draw(self, screen):
        pygame.draw.rect(screen,
                         self.color_button,
                         (self.x, self.y, *self.size), 1)
        text = self.font.render(self.text, True, self.color_font)
        rect = text.get_rect()
        rect.center = (int(self.x + self.width / 2), int(self.y + self.height / 2))
        screen.blit(text, rect)

    def is_clicked(self, mouse_x, mouse_y):
        return self.x < mouse_x < self.x + self.width \
            and self.y < mouse_y < self.y + self.height

    def __str__(self):
        return self.text


class MiniButton(Button):
    def __init__(self, x, y, width, height, text1, text2, color_button, color_font1, color_font2, font1, font2, _id):
        super().__init__(x, y, width, height, text1, color_button, color_font1, font1, _id)
        self.text1 = text1
        self.text2 = text2
        self.color_font1 = color_font1
        self.color_font2 = color_font2
        self.font1 = font1
        self.font2 = font2

    def change_text2(self, text):
        self.text2 = text

    def draw(self, screen):
        pygame.draw.rect(screen,
                         self.color_button,
                         (self.x, self.y, *self.size), border_radius=10)
        text1 = self.font1.render(self.text1, True, self.color_font1)
        rect1 = text1.get_rect()
        rect1.centerx = int(self.x + self.width / 2)
        rect1.centery = int(self.y + self.height / 2) - 20

        text2 = self.font2.render(self.text2, True, self.color_font2)
        rect2 = text2.get_rect()
        rect2.centerx = int(self.x + self.width / 2)
        rect2.centery = int(self.y + self.height / 2) + 20

        screen.blit(text1, rect1)
        screen.blit(text2, rect2)