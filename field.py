from config import *
import pygame as pg
import random
import solver
import pygame_func as pg_help
import copy


class Field:
    def __init__(self, level, n=3):
        self.n = n
        self.table = [[((i * n + i // n + j) % (n * n) + 1) for j in range(n * n)] for i in range(n * n)]
        self.task = [[((i * n + i // n + j) % (n * n) + 1) for j in range(n * n)] for i in range(n * n)]
        self.level = level
        self.diff = self.get_difficult()

    def transposing(self):
        self.table = list(map(list, zip(*self.table)))

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

    def swap_colums_small(self):
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

    def swap_colums_area(self):
        self.transposing()
        self.swap_rows_area()
        self.transposing()

    def shuffle(self, amt=10):
        mix_func = [self.transposing,
                    self.swap_rows_small,
                    self.swap_colums_small,
                    self.swap_rows_area,
                    self.swap_colums_area]
        for i in range(1, amt):
            random.choice(mix_func)()
        self.task = copy.deepcopy(self.table)

    def generate(self):
        self.shuffle(15)

        used = [[False for j in range(self.n * self.n)] for i in range(self.n * self.n)]
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

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, FIELD_COLOR,
                     (WIDTH / 6, 100, FIELD_WIDTH, FIELD_HEIGHT), 1)
        for i in range(self.n ** 2):
            w = 1
            if i == 3 or i == 6:
                w = 4
            pg.draw.line(screen, FIELD_COLOR,
                         (WIDTH / 6, 100 + i * CEIL_SIZE),
                         (WIDTH / 6 * 5, 100 + i * CEIL_SIZE), w)
            pg.draw.line(screen, FIELD_COLOR,
                         (WIDTH / 6 + i * CEIL_SIZE, 100),
                         (WIDTH / 6 + i * CEIL_SIZE, 100 + FIELD_HEIGHT), w)
        for i in range(self.n ** 2):
            for j in range(self.n ** 2):
                self.draw_ceil(screen, i, j)

    def draw_ceil(self, screen, i, j):
        if not self.task[i][j]:
            return
        text, rect = pg_help.get_text_rect("timesnewroman", str(self.task[i][j]), 50, WHITE)
        rect.centerx = WIDTH / 6 + (j + 0.5) * CEIL_SIZE
        rect.centery = 100 + (i + 0.5) * CEIL_SIZE
        screen.blit(text, rect)
