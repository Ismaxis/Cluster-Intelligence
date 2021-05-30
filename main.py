import pygame as pg
import numpy as np

WIN_SIZE_X = 1000
WIN_SIZE_Y = 1000
AVERAGE_VEL = 5
VEL_DEVIATION = 2
ANGLE_DEVIATION = 3
DEF_COLOR = (255, 255, 255)
WIN = pg.display.set_mode((WIN_SIZE_X, WIN_SIZE_Y))
pg.display.set_caption("Cluster")
clock = pg.time.Clock()


class Boid:
    SCREAM_RANGE = 50

    def __init__(self):
        # randomise pos of Boid
        self.pos = [None, None]
        self.pos[0] = np.random.randint(1, WIN_SIZE_X)
        self.pos[1] = np.random.randint(1, WIN_SIZE_Y)

        # randomise Boid vel and direction
        self.vel = np.random.randint(AVERAGE_VEL - VEL_DEVIATION, AVERAGE_VEL + VEL_DEVIATION + 1)
        self.angle = np.random.randint(0, 360)

        # randomise Boid counters
        self.counter_A = np.random.randint(0, 500)
        self.counter_B = np.random.randint(0, 500)

    def draw(self, win):
        pg.draw.line(win, DEF_COLOR, self.pos, self.pos, 1)

    def move(self):
        self.angle += np.random.randint(-ANGLE_DEVIATION, ANGLE_DEVIATION + 1)

        sin = np.sin(np.radians(self.angle))
        cos = np.cos(np.radians(self.angle))

        vel_x = self.vel * cos
        vel_y = self.vel * sin

        self.pos[0] += vel_x
        self.pos[1] += vel_y

        if self.pos[0] >= WIN_SIZE_X:
            self.angle = 180 - self.angle
        elif self.pos[0] <= 0:
            self.angle = 180 - self.angle
        elif self.pos[1] >= WIN_SIZE_Y:
            self.angle = 360 - self.angle
        elif self.pos[1] <= 0:
            self.angle = 360 - self.angle


Boids = []
for i in range(0, 300):
    Boids.append(Boid())

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    WIN.fill((0, 0, 0))
    for Boid in Boids:
        Boid.move()
        Boid.draw(WIN)

    pg.display.update()
    clock.tick(60)
