import pygame as pg
import numpy as np


def check_dist_and_updating_counters(cur_boid, boids, draw_lines, win, radius_of_hearing):

    for k in range(0, len(boids)):
        distance_sq = (cur_boid.pos[0] - boids[k].pos[0]) ** 2 + (cur_boid.pos[1] - boids[k].pos[1]) ** 2

        if distance_sq <= radius_of_hearing ** 2:
            something_changes = False

            # checking A
            if cur_boid.counters[0] > boids[k].counters[0] + radius_of_hearing:
                cur_boid.counters[0] = boids[k].counters[0] + radius_of_hearing
                if cur_boid.target == 0:
                    something_changes = True

            # checking B
            if cur_boid.counters[1] > boids[k].counters[1] + radius_of_hearing:
                cur_boid.counters[1] = boids[k].counters[1] + radius_of_hearing
                if cur_boid.target == 1:
                    something_changes = True

            if something_changes:
                if draw_lines:
                    pg.draw.line(win, (255, 255, 255), cur_boid.pos, boids[k].pos)
                distances = [cur_boid.pos[0] - boids[k].pos[0], cur_boid.pos[1] - boids[k].pos[1]]

                if distances[0] == 0:
                    angle = 90
                else:
                    tan = (distances[1]) / (distances[0])
                    angle = np.degrees(np.arctan(tan))

                # attention OY axis is inverted and all signs at y cords is inverted too
                if distances[0] < 0 < distances[1]:
                    cur_boid.angle = -angle
                elif distances[0] > 0 > distances[1]:
                    cur_boid.angle = 180 - angle
                elif distances[0] < 0 and distances[1] < 0:
                    cur_boid.angle = 360 - angle
                elif distances[0] > 0 and distances[1] > 0:
                    cur_boid.angle = 180 - angle


def scream_and_hear(win, draw_lines, squares, grid, radius_of_hearing):

    # goes throw all Squares
    for i in range(0, grid[0]):
        for j in range(0, grid[1]):
            for Cur_Boid in squares[i, j].Items:

                # first compare with its square boids
                boids = squares[i, j].Items
                check_dist_and_updating_counters(Cur_Boid, boids, draw_lines, win, radius_of_hearing)

                # cleaning 
                boids.clear()

                # second compare with boids from neighbour squares
                true_counter = 0
                if i + 1 < grid[0]:
                    for boid in squares[i + 1, j].Items:
                        boids.append(boid)
                    true_counter += 1
                if j + 1 < grid[1]:
                    for boid in squares[i, j + 1].Items:
                        boids.append(boid)
                    true_counter += 1
                if true_counter >= 2:
                    for boid in squares[i + 1, j + 1].Items:
                        boids.append(boid)

                check_dist_and_updating_counters(Cur_Boid, boids, draw_lines, win, radius_of_hearing)
