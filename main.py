import pygame as pg
import numpy as np

WIN_SIZE_X = 1000
WIN_SIZE_Y = 1000

AVERAGE_VEL = 4
VEL_DEVIATION = 1
ANGLE_DEVIATION = 0
RADIUS_OF_HEARING = 50

DEF_COLOR = (255, 255, 255)

WIN = pg.display.set_mode((WIN_SIZE_X, WIN_SIZE_Y))
pg.display.set_caption("Cluster")
clock = pg.time.Clock()


class Boid:
    SCREAM_RANGE = 50

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
        self.counters[0] += 1
        self.counters[1] += 1

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

    def collide(self):
        global Stations

        for Cur_Station in Stations:
            sign = Cur_Station.signature
            distance_sq = (self.pos[0] - Cur_Station.pos[0]) ** 2 + (self.pos[1] - Cur_Station.pos[1]) ** 2
            if distance_sq <= Cur_Station.SIZE ** 2:
                self.counters[sign] = 0
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
    SIZE = 50

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


def scream_and_hear(win):
    global Boids

    # checking distances between all Boids and if someone near to other updating their counters
    for Cur_Boid in Boids:
        for i in range(0, len(Boids)):
            distance_sq = (Cur_Boid.pos[0] - Boids[i].pos[0]) ** 2 + (Cur_Boid.pos[1] - Boids[i].pos[1]) ** 2

            if distance_sq <= RADIUS_OF_HEARING ** 2:
                something_changes = False

                # checking A
                if Cur_Boid.counters[0] > Boids[i].counters[0] + RADIUS_OF_HEARING:
                    Cur_Boid.counters[0] = Boids[i].counters[0] + RADIUS_OF_HEARING
                    if Cur_Boid.target == 0:
                        something_changes = True

                # checking B
                if Cur_Boid.counters[1] > Boids[i].counters[1] + RADIUS_OF_HEARING:
                    Cur_Boid.counters[1] = Boids[i].counters[1] + RADIUS_OF_HEARING
                    if Cur_Boid.target == 1:
                        something_changes = True

                # changing direction
                if something_changes:
                    if draw_lines:
                        pg.draw.line(win, DEF_COLOR, Cur_Boid.pos, Boids[i].pos)
                    distances = [Cur_Boid.pos[0] - Boids[i].pos[0], Cur_Boid.pos[1] - Boids[i].pos[1]]

                    if distances[0] == 0:
                        angle = 90
                    else:
                        tan = (distances[1]) / (distances[0])
                        angle = np.degrees(np.arctan(tan))

                    # attention OY axis is inverted and all signs at y cords is inverted too
                    if distances[0] < 0 < distances[1]:
                        Cur_Boid.angle = -angle
                    elif distances[0] > 0 > distances[1]:
                        Cur_Boid.angle = 180 - angle
                    elif distances[0] < 0 and distances[1] < 0:
                        Cur_Boid.angle = 360 - angle
                    elif distances[0] > 0 and distances[1] > 0:
                        Cur_Boid.angle = 180 - angle


Stations = [Station(100, 100, 0), Station(600, 600, 1)]

Boids = []
for i in range(0, 300):
    Boids.append(Boid())
draw_lines = False
counter = 0
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        if event.type == pg.MOUSEBUTTONDOWN:
            buttons = pg.mouse.get_pressed(3)
            if buttons[0]:
                if draw_lines:
                    draw_lines = False
                elif not draw_lines:
                    draw_lines = True
            elif buttons[2]:
                Stations[1].pos = pg.mouse.get_pos()

    WIN.fill((0, 0, 0))
    '''
    if counter == 30:
        counter = 0
        scream_and_hear()
    else:
        counter += 1
    '''
    scream_and_hear(WIN)
    for Boid in Boids:
        Boid.move()
        Boid.collide()
        Boid.draw(WIN)

    for Station in Stations:
        Station.draw(WIN)
    pg.display.update()
    clock.tick(60)
