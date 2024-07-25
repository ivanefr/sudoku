import pygame as pg
import sys


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

def get_font(name, size, italic=False, bold=False):
    return pg.font.SysFont(name, size, italic, bold)


def get_text_rect(name, text, size, color):
    f = get_font(name, size)
    t = f.render(text, True, color)
    return t, t.get_rect()
