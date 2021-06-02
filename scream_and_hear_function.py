import pygame as pg
import numpy as np


def updating_counters_and_dir(main_boid, nei_boid, draw_lines, win, radius_of_hearing):
    distance_sq = (main_boid.pos[0] - nei_boid.pos[0]) ** 2 + (main_boid.pos[1] - nei_boid.pos[1]) ** 2

    if distance_sq <= radius_of_hearing ** 2:
        something_changes = False

        # checking A
        if main_boid.counters[0] > nei_boid.counters[0] + radius_of_hearing:
            main_boid.counters[0] = nei_boid.counters[0] + radius_of_hearing
            if main_boid.target == 0:
                something_changes = True

        # checking B
        if main_boid.counters[1] > nei_boid.counters[1] + radius_of_hearing:
            main_boid.counters[1] = nei_boid.counters[1] + radius_of_hearing
            if main_boid.target == 1:
                something_changes = True

        if something_changes:
            if draw_lines:
                pg.draw.line(win, (255, 255, 255), main_boid.pos, nei_boid.pos)
            distances = [main_boid.pos[0] - nei_boid.pos[0], main_boid.pos[1] - nei_boid.pos[1]]

            if distances[0] == 0:
                angle = 90
            else:
                tan = (distances[1]) / (distances[0])
                angle = np.degrees(np.arctan(tan))

            # attention OY axis is inverted and all signs at y cords is inverted too
            if distances[0] < 0 < distances[1]:
                main_boid.angle = -angle
            elif distances[0] > 0 > distances[1]:
                main_boid.angle = 180 - angle
            elif distances[0] < 0 and distances[1] < 0:
                main_boid.angle = 360 - angle
            elif distances[0] > 0 and distances[1] > 0:
                main_boid.angle = 180 - angle


def check_dist_and_updating_counters(cur_boid, boids, draw_lines, win, radius_of_hearing):
    for k in range(0, len(boids)):
        updating_counters_and_dir(cur_boid, boids[k], draw_lines, win, radius_of_hearing)
        updating_counters_and_dir(boids[k], cur_boid, draw_lines, win, radius_of_hearing)


def scream_and_hear(win, draw_lines, squares, grid_size, radius_of_hearing):

    # goes throw all Squares
    for i in range(0, grid_size[0]):
        for j in range(0, grid_size[1]):
            for Cur_Boid in squares[i, j].Items:

                # first compare with its square boids
                check_dist_and_updating_counters(Cur_Boid, squares[i, j].Items, draw_lines, win, radius_of_hearing)

                # second compare with boids from neighbour squares
                if i + 1 < grid_size[0]:
                    check_dist_and_updating_counters(Cur_Boid, squares[i + 1, j].Items, draw_lines, win, radius_of_hearing)
                if j + 1 < grid_size[1]:
                    check_dist_and_updating_counters(Cur_Boid, squares[i, j + 1].Items, draw_lines, win, radius_of_hearing)
                if i + 1 < grid_size[0] and j + 1 < grid_size[1]:
                    check_dist_and_updating_counters(Cur_Boid, squares[i + 1, j + 1].Items, draw_lines, win, radius_of_hearing)
                if i - 1 >= 0 and j + 1 < grid_size[1]:
                    check_dist_and_updating_counters(Cur_Boid, squares[i - 1, j + 1].Items, draw_lines, win, radius_of_hearing)
                if i + 1 < grid_size[0] and j - 1 >= 0:
                    check_dist_and_updating_counters(Cur_Boid, squares[i + 1, j - 1].Items, draw_lines, win, radius_of_hearing)
