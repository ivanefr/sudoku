import pygame as pg
import pygame_func as pg_help
from config import *
from button import Button


class Sudoku:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Sudoku")
        self.screen = pg.display.set_mode(SIZE)
        self.state = None

    def start(self):
        self.draw_start_window()
        self.run()

    def run(self):
        ...

    def draw_start_window(self):
        self.draw_title()

        font = pg_help.get_font("calibri", 30)
        button_lvl_1 = Button(int(WIDTH / 2) - 140,
                              int(HEIGHT / 3),
                              280, 50, "Лёгкий",
                              BUTTON_COLOR, GREEN, font, EASY_BTN)
        button_lvl_2 = Button(int(WIDTH / 2) - 140,
                              int(HEIGHT / 3) + 60,
                              280, 50, "Нормальный",
                              BUTTON_COLOR, YELLOW, font, NORMAL_BTN)
        button_lvl_3 = Button(int(WIDTH / 2) - 140,
                              int(HEIGHT / 3) + 120,
                              280, 50, "Сложный",
                              BUTTON_COLOR, RED, font, HARD_BTN)
        button_lvl_4 = Button(int(WIDTH / 2) - 140,
                              int(HEIGHT / 3) + 200,
                              280, 50, "Экстремальный",
                              BUTTON_COLOR, PURPLE, font, EXTREME_BTN)

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
