import pygame as pg
import numpy as np
from scream_and_hear_function import scream_and_hear
pg.font.init()

WIN_SIZE_X = 1000
WIN_SIZE_Y = 1000
STAT_FONT = pg.font.SysFont("comics", 50)

AMOUNT_OF_BOIDS = 300
AVERAGE_VEL = 2
VEL_DEVIATION = 0.5
ANGLE_DEVIATION = 2
RADIUS_OF_HEARING = 50
side_of_square = RADIUS_OF_HEARING/2

GLOBAL_SUPPLIES_CARIED = 0

DEF_COLOR = (255, 255, 255)

WIN = pg.display.set_mode((WIN_SIZE_X, WIN_SIZE_Y))
pg.display.set_caption("Cluster")
clock = pg.time.Clock()


class Boid:
    SCREAM_RANGE = 50
    SUPPLY_TAKEN = False

    def __init__(self):
        global Stations

        # randomise pos of Boid
        self.pos = [None, None]
        self.pos[0] = np.random.randint(1, WIN_SIZE_X)
        self.pos[1] = np.random.randint(1, WIN_SIZE_Y)
        for Cur_Station in Stations:
            if (self.pos[0] - Cur_Station.pos[0]) ** 2 + (self.pos[1] - Cur_Station.pos[1]) ** 2 <= Cur_Station.SIZE**2:
                self.pos[0] += Cur_Station.SIZE
                self.pos[1] -= Cur_Station.SIZE

        # randomise Boid vel and direction
        self.vel = np.random.randint(AVERAGE_VEL - VEL_DEVIATION, AVERAGE_VEL + VEL_DEVIATION + 1)
        self.angle = np.random.randint(0, 360)

        # randomise Boid counters
        self.counters = [1000, 1000]

        # randomise Boid target
        self.target = np.random.randint(0, 2)

    def draw(self, win):
        if self.target == 0:
            color = (255, 100, 100)
        elif self.target == 1:
            color = (100, 100, 255)
        else:
            color = DEF_COLOR
        pg.draw.line(win, color, self.pos, self.pos, 2)

    def move(self):
        self.counters[0] += AVERAGE_VEL
        self.counters[1] += AVERAGE_VEL

        self.angle += np.random.randint(-ANGLE_DEVIATION, ANGLE_DEVIATION + 1)

        sin = np.sin(np.radians(self.angle))
        cos = np.cos(np.radians(self.angle))

        vel_x = self.vel * cos
        vel_y = self.vel * sin

        self.pos[0] += vel_x
        self.pos[1] -= vel_y

        if self.pos[0] >= WIN_SIZE_X:
            self.angle = 180 - self.angle
        elif self.pos[0] <= 0:
            self.angle = 180 - self.angle
        elif self.pos[1] >= WIN_SIZE_Y:
            self.angle = 360 - self.angle
        elif self.pos[1] <= 0:
            self.angle = 360 - self.angle

        if self.pos[0] >= WIN_SIZE_X:
            self.pos[0] = WIN_SIZE_X - 1
        if self.pos[1] >= WIN_SIZE_Y:
            self.pos[1] = WIN_SIZE_Y - 1

    def collide(self):
        global Stations, GLOBAL_SUPPLIES_CARIED

        for Cur_Station in Stations:
            sign = Cur_Station.signature
            distance_sq = (self.pos[0] - Cur_Station.pos[0]) ** 2 + (self.pos[1] - Cur_Station.pos[1]) ** 2
            if distance_sq <= Cur_Station.SIZE ** 2:
                self.counters[sign] = 0
                if not self.SUPPLY_TAKEN:
                    self.SUPPLY_TAKEN = True
                elif self.SUPPLY_TAKEN and self.target == sign:
                    GLOBAL_SUPPLIES_CARIED += 1
                    self.SUPPLY_TAKEN = False

                if self.angle >= 180:
                    self.angle -= 180
                else:
                    self.angle += 180

                if self.target == sign:
                    if self.target == 0:
                        self.target = 1
                    elif self.target == 1:
                        self.target = 0


class Station:
    SIZE = 25

    def __init__(self, x, y, signature):
        self.pos = (x, y)
        self.signature = signature
        if signature == 0:
            self.color = (255, 0, 0)
        elif signature == 1:
            self.color = (0, 0, 255)
        else:
            self.color = DEF_COLOR

    def draw(self, win):
        pg.draw.circle(win, self.color, self.pos, self.SIZE)


class BoidGroup:
    def __init__(self):
        self.Items = []


def matrix_drawing(size_x, size_y):
    global WIN, WIN_SIZE_X, WIN_SIZE_Y, side_of_square, Squares

    for i in range(0, size_x):
        for j in range(0, size_y):
            len1 = len(Squares[i, j].Items)

            if len1 > 0:
                label = STAT_FONT.render(f'{len1}', True, DEF_COLOR)
                WIN.blit(label, (i * side_of_square, j * side_of_square))

            pg.draw.line(WIN, DEF_COLOR, (i * side_of_square, 0), (i * side_of_square, WIN_SIZE_X))
            pg.draw.line(WIN, DEF_COLOR, (0, i * side_of_square), (WIN_SIZE_Y, i * side_of_square))


Stations = [Station(100, 100, 0), Station(900, 900, 1)]

Boids = []
for i in range(0, AMOUNT_OF_BOIDS):
    Boids.append(Boid())

grid_size_x = int(WIN_SIZE_X // side_of_square)
grid_size_y = int(WIN_SIZE_Y // side_of_square)

# contains groups of Boids by squares
Squares = np.zeros((grid_size_x, grid_size_y), dtype=BoidGroup)

for i in range(0, grid_size_x):
    for j in range(0, grid_size_y):
        Squares[i, j] = BoidGroup()

draw_lines = False
draw_matrix = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        if event.type == pg.MOUSEBUTTONDOWN:
            buttons = pg.mouse.get_pressed(3)
            if buttons[2]:
                if draw_lines:
                    draw_lines = False
                elif not draw_lines:
                    draw_lines = True

            if buttons[1]:
                if draw_matrix:
                    draw_matrix = False
                elif not draw_matrix:
                    draw_matrix = True

            elif buttons[0]:
                Stations[1].pos = pg.mouse.get_pos()

    for i in range(0, grid_size_x):
        for j in range(0, grid_size_y):
            Squares[i, j].Items.clear()

    for B in Boids:
        sq_x = int(B.pos[0] // side_of_square)
        sq_y = int(B.pos[1] // side_of_square)

        Squares[sq_x, sq_y].Items.append(B)

    WIN.fill((0, 0, 0))

    label = STAT_FONT.render("SUPPLIES CARIED: " + str(GLOBAL_SUPPLIES_CARIED), True, DEF_COLOR)
    WIN.blit(label, (WIN_SIZE_X - label.get_width() - 15, 10))

    scream_and_hear(WIN, draw_lines, Squares, (grid_size_x, grid_size_y), RADIUS_OF_HEARING)

    for Boid in Boids:
        Boid.move()
        Boid.collide()
        Boid.draw(WIN)

    for Station in Stations:
        Station.draw(WIN)

    # draw matrix with side = side_of_square
    if draw_matrix:
        matrix_drawing(grid_size_x, grid_size_y)

    pg.display.update()
    clock.tick(100)
