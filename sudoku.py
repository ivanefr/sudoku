import pygame as pg
import pygame_func as pg_help
from config import *
from button import Button, MiniButton
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

    def reset_bg(self):
        self.screen.fill(BG_COLOR)

    def run(self):
        self.reset_bg()
        self.draw_title()
        field = Field(self.screen, self.state)
        field.generate()
        field.draw()

        buttons = []
        x = LEFT_MARGIN + MARGIN_MINI_BTN_SIZE
        y = TOP_MARGIN + FIELD_HEIGHT + 10
        font1 = pg_help.get_font("timesnewroman", 40)
        font2 = pg_help.get_font("timesnewroman", 20)

        for n in range(1, 10):
            btn = MiniButton(x + (n - 1) * CEIL_SIZE, y, MINI_BTN_WIDTH, MINI_BTN_HEIGHT, str(n),
                             str(field.get_count(n)), FIELD_BG_COLOR, GOOD_FONT_COLOR, WHITE, font1, font2, n)
            buttons.append(btn)
        for btn in buttons:
            btn.draw(self.screen)

        while True:
            pg_help.update()
            typ, *args = pg_help.wait_press_sudoku(buttons)
            if typ == FIELD:
                field.click(*args)
            elif typ == EMPTY:
                field.draw()
            elif typ == NUM:
                number = args[0]
                field.input_number(number)
                buttons[number - 1].change_text2(str(field.get_count(number)))
                buttons[number - 1].draw(self.screen)
            elif typ == BTN:
                n = args[0]
                field.check_num(n)

    def draw_play_window(self):
        self.reset_bg()
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

    def draw_start_window(self):
        self.reset_bg()
        self.draw_title()
        font = pg_help.get_font("calibri", 30)
        button_play = Button(int(WIDTH / 2) - 140,
                             int(HEIGHT / 3),
                             280, 50, "Играть",
                             BUTTON_COLOR, WHITE, font, PLAY)
        button_statistic = Button(int(WIDTH / 2) - 140,
                                  int(HEIGHT / 3) + 60,
                                  280, 50, "Статистика",
                                  BUTTON_COLOR, WHITE, font, STATISTIC)
        button_settings = Button(int(WIDTH / 2) - 140,
                                 int(HEIGHT / 3) + 120,
                                 280, 50, "Настройки",
                                 BUTTON_COLOR, WHITE, font, SETTINGS)
        button_exit = Button(int(WIDTH / 2) - 140,
                             int(HEIGHT / 3) + 180,
                             280, 50, "Выход",
                             BUTTON_COLOR, WHITE, font, EXIT)
        buttons = [button_play, button_statistic, button_exit, button_settings]
        for button in buttons:
            button.draw(self.screen)

        while True:
            pg_help.update()
            btn = pg_help.wait_press_buttons(buttons)
            if btn:
                if btn.id == EXIT:
                    pg_help.exit_game()
                if btn.id == STATISTIC:
                    self.draw_statistic()
                if btn.id == PLAY:
                    self.draw_play_window()
                if btn.id == SETTINGS:
                    self.draw_settings()
                return

    def draw_statistic(self):
        self.draw_start_window()

    def draw_settings(self):
        self.draw_start_window()

    def draw_title(self):
        text, rect = pg_help.get_text_rect("gillsansultra", "Sudoku",
                                           50, FONT_COLOR)
        rect.centerx = WIDTH / 2
        rect.y = 0
        self.screen.blit(text, rect)
