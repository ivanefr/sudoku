import pygame


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
