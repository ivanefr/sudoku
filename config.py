import pygame as pg

WIDTH = 800
HEIGHT = 800
SIZE = WIDTH, HEIGHT

FIELD_WIDTH = WIDTH / 1.5
FIELD_HEIGHT = FIELD_WIDTH
CEIL_SIZE = FIELD_HEIGHT / 9
MINI_BTN_WIDTH = CEIL_SIZE / 1.2
MINI_BTN_HEIGHT = MINI_BTN_WIDTH * 2
MARGIN_MINI_BTN_SIZE = (CEIL_SIZE - MINI_BTN_WIDTH) / 2

LEFT_MARGIN = (WIDTH - FIELD_WIDTH) / 2
TOP_MARGIN = 100

GREEN = 0, 255, 0
BLUE = 0, 0, 255
BLACK = 0, 0, 0
WHITE = 255, 255, 255
YELLOW = 255, 255, 0
RED = 255, 0, 0
PURPLE = 146, 110, 174

BG_COLOR = 18, 18, 18
FONT_COLOR = WHITE
BUTTON_COLOR = WHITE
FIELD_BORDER_COLOR = BLACK
FIELD_BG_COLOR = 33, 36, 51
CLICKED_CEIL_COLOR = 53, 77, 115
CHECK_CEIL_COLOR = 17, 20, 27
GOOD_FONT_COLOR = 121, 160, 255
BAD_FONT_COLOR = RED

EASY = 100
NORMAL = 200
HARD = 300
EXTREME = 400
FIELD = 500
EMPTY = 600
NUM = 700
PLAY = 800
STATISTIC = 900
SETTINGS = 1000
EXIT = 1100
BTN = 1200
ARROW = 1300
MENU = 1400

UP = pg.K_UP
DOWN = pg.K_DOWN
LEFT = pg.K_LEFT
RIGHT = pg.K_RIGHT

K_NUMS = (pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9)
K_ARROWS = (UP, DOWN, RIGHT, LEFT)