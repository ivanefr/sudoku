import pygame as pg
import pygame_func as pg_help
from config import *
from button import Button
from field import Field


class Sudoku:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Sudoku")
        self.screen = pg.display.set_mode(SIZE)
        self.state = None

    def start(self):
        self.draw_start_window()
        self.run()

    def reset(self):
        self.screen.fill(BLACK)

    def run(self):
        self.reset()
        self.draw_title()
        field = Field(self.state)
        field.generate()
        field.draw(self.screen)
        for i in field.task:
            print(' '.join(map(str, i)))
        print()
        for i in field.table:
            print(' '.join(map(str, i)))

        while True:
            pg_help.update()

    def draw_start_window(self):
        self.draw_title()

        font = pg_help.get_font("calibri", 30)
        button_lvl_1 = Button(int(WIDTH / 2) - 140,
                              int(HEIGHT / 3),
                              280, 50, "Лёгкий",
                              BUTTON_COLOR, GREEN, font, EASY)
        button_lvl_2 = Button(int(WIDTH / 2) - 140,
                              int(HEIGHT / 3) + 60,
                              280, 50, "Нормальный",
                              BUTTON_COLOR, YELLOW, font, NORMAL)
        button_lvl_3 = Button(int(WIDTH / 2) - 140,
                              int(HEIGHT / 3) + 120,
                              280, 50, "Сложный",
                              BUTTON_COLOR, RED, font, HARD)
        button_lvl_4 = Button(int(WIDTH / 2) - 140,
                              int(HEIGHT / 3) + 200,
                              280, 50, "Экстремальный",
                              BUTTON_COLOR, PURPLE, font, EXTREME)

        buttons = [button_lvl_1, button_lvl_2, button_lvl_3, button_lvl_4]
        for button in buttons:
            button.draw(self.screen)

        while True:
            pg_help.update()
            btn = pg_help.wait_press_buttons(buttons)
            if btn:
                self.state = btn.id
                return

    def draw_title(self):
        text, rect = pg_help.get_text_rect("gillsansultra", "Sudoku",
                                           50, FONT_COLOR)
        rect.centerx = WIDTH / 2
        rect.y = 0
        self.screen.blit(text, rect)
