import os.path
import pygame_func as pg_help
from config import *
from button import ButtonImage


def get_time_file(level):
    if level == EASY:
        return "data/easy_time.txt"
    if level == HARD:
        return "data/hard_time.txt"
    if level == NORMAL:
        return "data/normal_time.txt"
    else:
        return "data/extreme_time.txt"


def get_games_file(level):
    if level == EASY:
        return "data/easy_games.txt"
    if level == HARD:
        return "data/hard_games.txt"
    if level == NORMAL:
        return "data/normal_games.txt"
    else:
        return "data/extreme_games.txt"


def get_games(level):
    filename = get_games_file(level)
    if not os.path.exists(filename):
        return 0
    with open(filename) as f:
        return int(f.read())


def get_average_time(level):
    filename = get_time_file(level)
    if not os.path.exists(filename):
        return 0
    with open(filename) as f:
        return float(f.read())


def update_games(level):
    filename = get_games_file(level)
    count = get_games(level)
    with open(filename, 'w') as f:
        f.write(str(count + 1))


def update_time(level, time):
    filename = get_time_file(level)
    average_time = get_average_time(level)
    with open(filename, 'w') as f:
        average_time = (average_time * (get_games(level) - 1) + time) / get_games(level)
        average_time = round(average_time, 2)
        f.write(str(average_time))


def get_full_time():
    filename = "data/full_time.txt"
    if not os.path.exists(filename):
        return 0.0
    with open(filename) as f:
        return float(f.read())


def update_full_time(time):
    full_time = get_full_time()
    filename = "data/full_time.txt"
    with open(filename, 'w') as f:
        f.write(str(full_time + time))


def get_full_games():
    c = 0
    for level in (EASY, NORMAL, HARD, EXTREME):
        c += get_games(level)
    return c


def get_record_filename(level):
    filename = None
    if level == EASY:
        filename = "data/record_easy.txt"
    elif level == NORMAL:
        filename = "data/record_normal.txt"
    elif level == HARD:
        filename = "data/record_hard.txt"
    else:
        filename = "data/record_extreme.txt"
    return filename


def get_level_record(level):
    filename = get_record_filename(level)
    if not os.path.exists(filename):
        return None
    with open(filename) as f:
        record = float(f.read())
    return record


def draw(screen):
    pg_help.reset_bg(screen)
    pg_help.draw_title(screen)

    font = pg_help.get_font("calibri", 30)
    levels = (EASY, NORMAL, HARD, EXTREME)
    width = WIDTH / 4 - 20
    for i in range(4):
        pg.draw.rect(screen, WHITE, (10 + i * (WIDTH / 4), 100, WIDTH / 4 - 20, 400), 1)

        text, rect = pg_help.get_text_rect("calibri", pg_help.get_level_text(levels[i]),
                                           27, pg_help.get_level_color(levels[i]))
        rect.y = 120
        rect.centerx = 10 + width / 2 + i * (WIDTH / 4)
        screen.blit(text, rect)

        text, rect = pg_help.get_text_rect("calibri", "Всего игр:", 20, FONT_COLOR)
        rect.y = 180
        rect.centerx = 10 + width / 2 + i * (WIDTH / 4)
        screen.blit(text, rect)

        text, rect = pg_help.get_text_rect("calibri", str(get_games(levels[i])), 50, FONT_COLOR)
        rect.y = 220
        rect.centerx = 10 + width / 2 + i * (WIDTH / 4)
        screen.blit(text, rect)

        text, rect = pg_help.get_text_rect("calibri", "среднее время", 20, FONT_COLOR)
        rect.y = 300
        rect.centerx = 10 + width / 2 + i * (WIDTH / 4)
        screen.blit(text, rect)

        text, rect = pg_help.get_text_rect("calibri", "прохождения:", 20, FONT_COLOR)
        rect.y = 320
        rect.centerx = 10 + width / 2 + i * (WIDTH / 4)
        screen.blit(text, rect)

        text, rect = pg_help.get_text_rect("calibri", pg_help.get_string_time(get_average_time(levels[i])),
                                           25, FONT_COLOR)
        rect.y = 350
        rect.centerx = 10 + width / 2 + i * (WIDTH / 4)
        screen.blit(text, rect)

        text, rect = pg_help.get_text_rect("calibri", "Рекорд:", 20, FONT_COLOR)
        rect.y = 400
        rect.centerx = 10 + width / 2 + i * (WIDTH / 4)
        screen.blit(text, rect)

        text, rect = pg_help.get_text_rect("calibri", pg_help.get_string_time(get_level_record(levels[i])),
                                           25, FONT_COLOR)
        rect.y = 430
        rect.centerx = 10 + width / 2 + i * (WIDTH / 4)
        screen.blit(text, rect)

    pg.draw.rect(screen, WHITE, (10, 510, 780, 280), 1)

    text, rect = pg_help.get_text_rect("calibri", "Общее время прохождений:", 30, FONT_COLOR)
    rect.y = 530
    rect.centerx = WIDTH / 2
    screen.blit(text, rect)

    text, rect = pg_help.get_text_rect("calibri", pg_help.get_string_time(get_full_time()), 50, FONT_COLOR)
    rect.y = 570
    rect.centerx = WIDTH / 2
    screen.blit(text, rect)

    text, rect = pg_help.get_text_rect("calibri", "Всего игр:", 30, FONT_COLOR)
    rect.y = 635
    rect.centerx = WIDTH / 2
    screen.blit(text, rect)

    text, rect = pg_help.get_text_rect("calibri", str(get_full_games()), 50, FONT_COLOR)
    rect.y = 670
    rect.centerx = WIDTH / 2
    screen.blit(text, rect)

    button_back = ButtonImage(10, 10, 60, 60, "back.png", BUTTON_COLOR, BACK)
    buttons = [button_back]
    buttons[0].draw(screen)
    btn = None

    while True:
        pg_help.update()
        btn = pg_help.wait_press_buttons_keyboard(buttons, [LEFT])
        if btn is not None:
            return BACK


def update(level, time):
    update_games(level)
    update_time(level, time)
    update_full_time(time)
