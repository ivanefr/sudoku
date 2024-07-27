from config import *
import pygame as pg
import random
import solver
import pygame_func as pg_help
import copy


class Field:
    def __init__(self, screen, level, n=3):
        self.n = n
        self.table = [[((i * n + i // n + j) % (n * n) + 1) for j in range(n * n)] for i in range(n * n)]
        self.task = [[((i * n + i // n + j) % (n * n) + 1) for j in range(n * n)] for i in range(n * n)]
        self.level = level
        self.diff = self.get_difficult()
        self.screen = screen
        self.clicked = None
        self.good_cells = set()
        self.bad_cells = set()
        self.count_digits = [0] + [9] * 9

    def transposing(self):
        self.table = list(map(lambda x: list(x), zip(*self.table)))

    def get_difficult(self):
        if self.level == EASY:
            return 40
        if self.level == NORMAL:
            return 35
        if self.level == HARD:
            return 30
        else:
            return 0

    def swap_rows_small(self):
        area = random.randrange(0, self.n, 1)
        line1 = random.randrange(0, self.n, 1)
        n1 = area * self.n + line1

        line2 = random.randrange(0, self.n, 1)
        while line1 == line2:
            line2 = random.randrange(0, self.n, 1)

        n2 = area * self.n + line2

        self.table[n1], self.table[n2] = self.table[n2], self.table[n1]

    def swap_columns_small(self):
        self.transposing()
        self.swap_rows_small()
        self.transposing()

    def swap_rows_area(self):
        area1 = random.randrange(0, self.n, 1)

        area2 = random.randrange(0, self.n, 1)
        while area1 == area2:
            area2 = random.randrange(0, self.n, 1)

        for i in range(0, self.n):
            n1, n2 = area1 * self.n + i, area2 * self.n + i
            self.table[n1], self.table[n2] = self.table[n2], self.table[n1]

    def swap_columns_area(self):
        self.transposing()
        self.swap_rows_area()
        self.transposing()

    def shuffle(self, amt=10):
        mix_func = [self.transposing,
                    self.swap_rows_small,
                    self.swap_columns_small,
                    self.swap_rows_area,
                    self.swap_columns_area]
        for i in range(1, amt):
            random.choice(mix_func)()
        self.task = copy.deepcopy(self.table)

    def generate(self):
        self.shuffle(30)

        used = [[False for _ in range(self.n * self.n)] for _ in range(self.n * self.n)]
        c = 0
        difficult = self.n ** 4
        while c < self.n ** 4 and difficult > self.diff:
            i = random.randrange(0, self.n * self.n, 1)
            j = random.randrange(0, self.n * self.n, 1)
            if used[i][j]:
                continue
            c += 1
            used[i][j] = True

            self.task[i][j] = 0
            self.count_digits[self.table[i][j]] -= 1
            difficult -= 1

            temp = []
            for copy_i in range(0, self.n * self.n):
                temp.append(self.task[copy_i][:])

            ii = 0
            for _ in solver.solve_sudoku((self.n, self.n), temp):
                ii += 1

            if ii != 1:
                self.task[i][j] = self.table[i][j]
                difficult += 1
                self.count_digits[self.table[i][j]] += 1

    def draw(self):
        pg.draw.rect(self.screen, FIELD_BG_COLOR,
                     (LEFT_MARGIN, TOP_MARGIN, FIELD_WIDTH, FIELD_HEIGHT))
        pg.draw.rect(self.screen, FIELD_BORDER_COLOR,
                     (LEFT_MARGIN, TOP_MARGIN, FIELD_WIDTH, FIELD_HEIGHT), 1)
        for i in range(self.n ** 2 + 1):
            w = 1
            if i in (0, 3, 6, 9):
                w = 3
            pg.draw.line(self.screen, FIELD_BORDER_COLOR,
                         (LEFT_MARGIN, TOP_MARGIN + i * CEIL_SIZE),
                         (LEFT_MARGIN + FIELD_WIDTH, TOP_MARGIN + i * CEIL_SIZE), w)
            pg.draw.line(self.screen, FIELD_BORDER_COLOR,
                         (LEFT_MARGIN + i * CEIL_SIZE, TOP_MARGIN),
                         (LEFT_MARGIN + i * CEIL_SIZE, TOP_MARGIN + FIELD_HEIGHT), w)
        for i in range(self.n ** 2):
            for j in range(self.n ** 2):
                self.draw_ceil(i, j)
        self.clicked = None

    def draw_ceil(self, i, j):
        if not self.task[i][j] and (i, j) not in self.bad_cells and (i, j) not in self.good_cells:
            return
        if (i, j) in self.good_cells:
            return self.draw_good_ceil(i, j)
        if (i, j) in self.bad_cells:
            # print(self.bad_cells)
            # print(self.good_cells)
            # print(i, j, self.task[i][j])
            # print(self.clicked)
            # print('-----------------')
            return self.draw_bad_ceil(i, j)
        self.draw_default_ceil(i, j, WHITE)

    def draw_good_ceil(self, i, j):
        self.draw_default_ceil(i, j, GOOD_FONT_COLOR)

    def draw_default_ceil(self, i, j, color):
        text, rect = pg_help.get_text_rect("timesnewroman", str(self.task[i][j]), int(CEIL_SIZE), color)
        rect.centerx = LEFT_MARGIN + (j + 0.5) * CEIL_SIZE
        rect.centery = TOP_MARGIN + (i + 0.5) * CEIL_SIZE
        self.screen.blit(text, rect)

    def draw_bad_ceil(self, i, j):
        self.draw_default_ceil(i, j, BAD_FONT_COLOR)

    def draw_click_ceil(self, i, j):
        pg.draw.rect(self.screen, CLICKED_CEIL_COLOR,
                     (LEFT_MARGIN + i * CEIL_SIZE + 1, TOP_MARGIN + j * CEIL_SIZE + 1,
                      CEIL_SIZE - 1, CEIL_SIZE - 1))
        self.draw_ceil(j, i)

    def draw_check_ceil(self, i, j):
        pg.draw.rect(self.screen, CHECK_CEIL_COLOR,
                     (LEFT_MARGIN + i * CEIL_SIZE + 1, TOP_MARGIN + j * CEIL_SIZE + 1,
                      CEIL_SIZE - 1, CEIL_SIZE - 1))
        self.draw_ceil(j, i)

    def draw_click_row(self, row):
        for i in range(self.n ** 2):
            self.draw_check_ceil(row, i)

    def draw_click_column(self, column):
        for i in range(self.n ** 2):
            self.draw_check_ceil(i, column)

    def draw_click_cube(self, i, j):
        for i in range(i // 3 * 3, i // 3 * 3 + 3):
            for j in range(j // 3 * 3, j // 3 * 3 + 3):
                self.draw_check_ceil(i, j)

    def click(self, x, y):
        self.draw()
        self.draw_click_row(x)
        self.draw_click_column(y)
        self.draw_click_cube(x, y)
        self.draw_click_ceil(x, y)
        if self.task[y][x]:
            for i in range(self.n ** 2):
                for j in range(self.n ** 2):
                    if self.task[j][i] == self.task[y][x]:
                        self.draw_click_ceil(i, j)
        self.clicked = (x, y)

    def input_number(self, num):
        if self.clicked is not None:
            y, x = self.clicked
            if (x, y) in self.bad_cells and self.task[x][y] == num:
                self.task[x][y] = 0
                self.bad_cells.remove((x, y))
                self.draw_check_ceil(y, x)
            else:
                if ((x, y) in self.good_cells or
                        self.task[x][y] and (x, y) not in self.bad_cells and (x, y) not in self.good_cells):
                    return
                self.task[x][y] = num
                self.draw_check_ceil(y, x)
                if self.table[x][y] == num:
                    self.count_digits[self.task[x][y]] += 1
                    self.good_cells.add((x, y))
                    if (x, y) in self.bad_cells:
                        self.bad_cells.remove((x, y))
                    self.draw_good_ceil(x, y)
                else:
                    self.bad_cells.add((x, y))
                    self.draw_bad_ceil(x, y)
            self.click(y, x)
            self.clicked = (y, x)

    def get_count(self, n):
        return 9 - self.count_digits[n]

    def check_num(self, num):
        for i in range(self.n ** 2):
            for j in range(self.n ** 2):
                if self.task[i][j] == num:
                    self.click(j, i)
                    return

    def is_over(self):
        s = 0
        for i in range(1, 10):
            s += self.get_count(i)
        return s == 0
