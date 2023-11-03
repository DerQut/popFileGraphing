import math
import time

import parser
import window
import assets
import graph

import pygame
from pygame.locals import *


def round(x):
    return int(math.ceil(x/10**(len(str(abs(int(x)))))-1)) * 10**(len(str(abs(int(x))))-1)


def loop_action():
    graphing_layer.draw()


def button_handler(event_key, needs_shifting, is_shifting):
    if event_key == pygame.K_F1:
        get_points()
    elif event_key == pygame.K_ESCAPE:
        graphing_layer.clear()
    elif event_key == pygame.K_s:
        graphing_layer.shows_points = not graphing_layer.shows_points


def get_points():

    filename = parser.get_file()

    graphing_layer.clear()

    file = open(filename, "r")

    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0

    is_first = True

    for line in file:

        point = (float(line.split()[0]), float(line.split()[1]))

        if is_first:
            x_min = point[0]
            y_min = point[1]

        is_first = False

        if point[0] < x_min:
            x_min = point[0]

        if point[0] > x_max:
            x_max = point[0]

        if point[1] < y_min:
            y_min = point[1]

        if point[1] > y_max:
            y_max = point[1]

        graphing_layer.points.append(point)

    file.close()

    print("done")

    x_min = math.floor(x_min)
    x_max = math.ceil(x_max)
    y_min = math.floor(y_min)
    y_max = math.ceil(y_max)

    graphing_layer.set_scale(x_min, x_max, y_min, y_max)


program_window = window.Window(1280, 720, DOUBLEBUF, assets.bg_colour, "The Graphing Engine")

input_layer = window.Surface(program_window, 0, 0, 360, 720, (0, 0, 0))

graphing_layer = graph.GraphingSurface(program_window, 360, 0, 920, 720, assets.bg_colour,
                                       assets.text_colour, 1, assets.button_colour_light, assets.orange)
