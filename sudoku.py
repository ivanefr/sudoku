import random
import time
import pygame as pg
import pygame_func as pg_help
from config import *
from button import Button, MiniButton
from field import Field
from firework import create_particles
import os


class Sudoku:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Sudoku")
        self.screen = pg.display.set_mode(SIZE)
        self.state = None
        self.start_time = None
        self.mistakes = None
        self.time = None
        self.is_record = None

    def start_init(self):
        self.time = None
        self.mistakes = 0
        self.state = EASY
        self.is_record = None

    def start(self):
        # self.draw_end_window()
        self.start_init()
        self.draw_start_window()
        self.run()

    def reset_bg(self):
        self.screen.fill(BG_COLOR)

    def draw_timer(self):
        t = self.get_timer()
        text, rect = pg_help.get_text_rect("timesnewroman", t, 30, FONT_COLOR)
        rect.x = WIDTH - rect.width - 3
        rect.y = 0

        self.screen.fill(BG_COLOR, (rect.x, rect.y, rect.width, rect.height))
        self.screen.blit(text, rect)

    def draw_run_window(self, field):
        self.reset_bg()
        self.draw_title()
        self.draw_level()
        self.draw_timer()
        self.draw_mistakes()

        field.draw()
        buttons = {}
        x = LEFT_MARGIN + MARGIN_MINI_BTN_SIZE
        y = TOP_MARGIN + FIELD_HEIGHT + 10
        font1 = pg_help.get_font("timesnewroman", 40)
        font2 = pg_help.get_font("timesnewroman", 20)

        for n in range(1, 10):
            if field.get_count(n):
                btn = MiniButton(x + (n - 1) * CEIL_SIZE, y, MINI_BTN_WIDTH, MINI_BTN_HEIGHT, str(n),
                                 str(field.get_count(n)), FIELD_BG_COLOR, GOOD_FONT_COLOR, WHITE, font1, font2, n)
                buttons.update({n: btn})
        for btn in buttons.values():
            btn.draw(self.screen)
        return buttons

    def run(self):
        self.start_time = time.time()

        field = Field(self.screen, self.state)
        field.generate()
        buttons = self.draw_run_window(field)

        while True:
            pg_help.update()
            typ, *args = pg_help.wait_press_sudoku(buttons.values())
            if typ == FIELD:
                field.click(*args)
            elif typ == EMPTY:
                field.draw()
            elif typ == NUM:
                number = args[0]
                if number not in buttons:
                    continue
                field.input_number(number)
                c = field.get_count(number)
                if not c:
                    field.remove_bad(number)
                    if number in buttons:
                        buttons[number].fill(self.screen, BG_COLOR)
                        del buttons[number]
                else:
                    buttons[number].change_text2(str(c))
                    buttons[number].draw(self.screen)
                self.mistakes = field.bad
            elif typ == BTN:
                n = args[0]
                field.check_num(n)
            elif typ == ARROW:
                arrow = args[0]
                field.input_arrow(arrow)
            elif typ == SPACE:
                status = self.draw_pause_window()
                if status == MENU:
                    return self.start()
                if status == SETTINGS:
                    self.draw_settings()
                buttons = self.draw_run_window(field)
            if field.is_over():
                break
            self.draw_mistakes()
            self.draw_timer()
        self.draw_end_window()

    def draw_pause_window(self):
        pause = pg_help.gaussian_blur(self.screen, 50)
        self.screen.blit(pause, (0, 0))

        # self.reset_bg()
        self.draw_title()
        self.draw_timer()
        t0 = time.time()
        font = pg_help.get_font("calibri", 30)
        button_continue = Button(int(WIDTH / 2) - 140,
                                 int(HEIGHT / 3) + 70,
                                 280, 50, "Продолжить",
                                 BUTTON_COLOR, WHITE, font, CONTINUE)
        button_menu = Button(int(WIDTH / 2) - 140,
                             int(HEIGHT / 3) + 130,
                             280, 50, "Меню",
                             BUTTON_COLOR, WHITE, font, MENU)
        button_settings = Button(int(WIDTH / 2) - 140,
                                 int(HEIGHT / 3) + 190,
                                 280, 50, "Настройки",
                                 BUTTON_COLOR, WHITE, font, SETTINGS)
        buttons = [button_continue, button_menu, button_settings]
        key_arr = [SPACE]
        for btn in buttons:
            btn.draw(self.screen)

        while True:
            response = pg_help.wait_press_buttons_keyboard(buttons, key_arr)
            if response is not None:
                diff = time.time() - t0
                self.start_time += diff
                if isinstance(response, Button):
                    return response.id
                return response
            pg_help.update()

    def draw_mistakes(self):
        text, rect = pg_help.get_text_rect("timesnewroman", f"Ошибки: {self.mistakes}",
                                           30, FONT_COLOR)
        rect.x = LEFT_MARGIN + FIELD_WIDTH - 150
        rect.y = TOP_MARGIN - 33
        self.screen.fill(BG_COLOR, (rect.x, rect.y, rect.width, rect.height - 2))
        self.screen.blit(text, rect)

    def render_end_window(self):
        self.reset_bg()
        self.draw_title()

        text = f"Вы прошли уровень сложности"
        text, rect = pg_help.get_text_rect("timesnewroman", text, 40, FONT_COLOR)
        rect.centerx = WIDTH / 2
        rect.y = 200
        self.screen.blit(text, rect)

        text = pg_help.get_level_text(self.state)
        color = pg_help.get_level_color(self.state)
        text, rect = pg_help.get_text_rect("timesnewroman", text, 40, color)
        rect.centerx = WIDTH / 2
        rect.y = 250
        self.screen.blit(text, rect)
        if self.time is None:
            self.time = self.get_timer()
        text, rect = pg_help.get_text_rect("timesnewroman", f"Ваше время: {self.time}",
                                           35, FONT_COLOR)
        rect.centerx = WIDTH / 2
        rect.y = 350
        self.screen.blit(text, rect)

        font = pg_help.get_font("calibri", 30)
        button_menu = Button(int(WIDTH / 2) - 140,
                             int(HEIGHT / 3) + 180,
                             280, 50, "Меню",
                             BUTTON_COLOR, WHITE, font, MENU)
        button_exit = Button(int(WIDTH / 2) - 140,
                             int(HEIGHT / 3) + 240,
                             280, 50, "Выход",
                             BUTTON_COLOR, WHITE, font, EXIT)
        buttons = [button_menu, button_exit]
        for btn in buttons:
            btn.draw(self.screen)
        if self.new_record():
            text, rect = pg_help.get_text_rect("timesnewroman", "НОВЫЙ РЕКОРД!", 50, color)
            rect.centerx = WIDTH / 2
            rect.y = 100
            self.screen.blit(text, rect)
        return buttons

    def rewrite_record(self):
        t = time.time() - self.start_time
        t = int(t)
        filename = pg_help.get_record_filename(self.state)
        with open(filename, 'w') as f:
            f.write(str(t))

    def new_record(self):
        if self.is_record is not None:
            return self.is_record
        t = time.time() - self.start_time
        t = int(t)
        filename = pg_help.get_record_filename(self.state)
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(str(10 ** 9))
        with open(filename) as f:
            record = float(f.read())
        if t < record:
            self.is_record = True
            return True
        self.is_record = False
        return False

    def draw_end_window(self):

        buttons_arr = self.render_end_window()

        btn = pg_help.wait_press_buttons(buttons_arr)

        all_sprites = None
        last_zv = None
        count_zv = None

        record = self.new_record()
        if record:
            self.rewrite_record()
            all_sprites = pg.sprite.Group()
            last_zv = 0
            count_zv = 0
        while btn is None:
            if record:
                if time.time() - last_zv > 0.25 and count_zv < 10:
                    from firework import create_particles
                    create_particles((random.randint(100, WIDTH - 100),
                                      random.randint(100, HEIGHT - 100)),
                                     all_sprites, WIDTH, HEIGHT)
                    last_zv = time.time()
                    count_zv += 1
                all_sprites.update()
                buttons_arr = self.render_end_window()
                all_sprites.draw(self.screen)
            pg_help.update()
            btn = pg_help.wait_press_buttons(buttons_arr)
        if btn.id == MENU:
            self.start()
        elif btn.id == EXIT:
            pg_help.exit_game()

    def get_timer(self):
        t = int(time.time() - self.start_time)
        t = time.strftime("%H:%M:%S", time.gmtime(t))
        return t

    def draw_level(self):
        level = self.state
        color = pg_help.get_level_color(level)
        name = pg_help.get_level_text(level)
        text, rect = pg_help.get_text_rect("timesnewroman", name, 30, color)
        rect.x = LEFT_MARGIN
        rect.y = TOP_MARGIN - 33

        self.screen.blit(text, rect)

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
