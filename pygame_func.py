import pygame as pg
import sys
from config import *


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


def wait_press_sudoku(mini_buttons):
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            if LEFT_MARGIN <= x <= LEFT_MARGIN + FIELD_WIDTH and TOP_MARGIN < y < TOP_MARGIN + FIELD_HEIGHT:
                return FIELD, int((x - LEFT_MARGIN) // CEIL_SIZE), int((y - TOP_MARGIN) // CEIL_SIZE)
            else:
                for btn in mini_buttons:
                    if btn.is_clicked(x, y):
                        return BTN, btn.id
                return EMPTY, 0, 0
        elif event.type == pg.KEYDOWN and event.key in K_NUMS:
            return NUM, K_NUMS.index(event.key) + 1
    return None, 0, 0


def get_font(name, size, italic=False, bold=False):
    return pg.font.SysFont(name, size, italic, bold)


def get_text_rect(name, text, size, color):
    f = get_font(name, size)
    t = f.render(text, True, color)
    return t, t.get_rect()
