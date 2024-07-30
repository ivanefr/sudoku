import time
import sys
from config import *
import os
import pygame as pg


def exit_game():
    pg.quit()
    sys.exit()


def check_exit():
    for event in pg.event.get():
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                exit_game()
        pg.event.post(event)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit_game()
        pg.event.post(event)


def gaussian_blur(surface, radius):
    scaled_surface = pg.transform.smoothscale(surface, (surface.get_width() // radius, surface.get_height() // radius))
    scaled_surface = pg.transform.smoothscale(scaled_surface, (surface.get_width(), surface.get_height()))
    return scaled_surface


def update():
    pg.display.update()
    check_exit()


def wait_press_buttons(button_arr):
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in button_arr:
                x, y = pg.mouse.get_pos()
                if button.is_clicked(x, y):
                    return button
    return None


def wait_press_buttons_keyboard(buttons, keys):
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            for k in keys:
                if event.key == k:
                    return k
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in buttons:
                x, y = pg.mouse.get_pos()
                if button.is_clicked(x, y):
                    return button
    return None


def wait_press_sudoku(mini_buttons):
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            if LEFT_MARGIN <= x <= LEFT_MARGIN + FIELD_WIDTH and TOP_MARGIN < y < TOP_MARGIN + FIELD_HEIGHT:
                return FIELD, int((x - LEFT_MARGIN) // CEIL_SIZE), int((y - TOP_MARGIN) // CEIL_SIZE)
            else:
                for btn in mini_buttons:
                    if btn.is_clicked(x, y):
                        if btn.id == PAUSE:
                            return PAUSE, None
                        return BTN, btn.id
                return EMPTY, 0, 0
        elif event.type == pg.KEYDOWN and event.key in K_NUMS:
            return NUM, K_NUMS.index(event.key) + 1
        elif event.type == pg.KEYDOWN and event.key in K_ARROWS:
            return ARROW, event.key
        elif event.type == pg.KEYDOWN and event.key == SPACE:
            return SPACE, None
    return None, 0, 0


def get_font(name, size, italic=False, bold=False):
    return pg.font.SysFont(name, size, italic, bold)


def get_text_rect(name, text, size, color):
    f = get_font(name, size)
    t = f.render(text, True, color)
    return t, t.get_rect()


def reset_bg(screen):
    screen.fill(BG_COLOR)


def draw_title(screen):
    text, rect = get_text_rect("gillsansultra", "Sudoku",
                               50, FONT_COLOR)
    rect.centerx = WIDTH / 2
    rect.y = 0
    screen.blit(text, rect)


def get_level_text(level):
    if level == EASY:
        return "Лёгкий"
    if level == NORMAL:
        return "Нормальный"
    if level == HARD:
        return "Сложный"
    if level == EXTREME:
        return "Экстремальный"


def get_level_color(level):
    if level == EASY:
        return GREEN
    if level == NORMAL:
        return YELLOW
    if level == HARD:
        return RED
    return PURPLE


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pg.image.load(fullname)
    image = image.convert_alpha()
    return image


def get_string_time(t):
    mil = int(t % 1 * 100)
    mil = str(mil).zfill(2)
    t = time.strftime(f"%H:%M:%S.{mil}", time.gmtime(t))
    return t
