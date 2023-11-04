import math
import time

import parser
import ui_elements
import window
import assets
import graph

import pygame
from pygame.locals import *


def minimalise(value):
    x = math.floor(value)

    i=0
    while x > 10:
        x = int(x/10)
        i=i+1

    return x * 10**i


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
    if not filename:
        return 1

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
    y_max = minimalise(y_max*1.1)

    if y_min:
        if y_max/y_min >= 500:
            y_min = 0

    if x_min:
        if x_max/x_min >= 500:
            x_min = 0

    graphing_layer.set_scale(x_min, x_max, y_min, y_max)


program_window = window.Window(1280, 720, DOUBLEBUF, assets.button_colour_dark, "The Graphing Engine")


input_layer = window.Surface(program_window, 0, 0, 360, 720, assets.bg_colour)

graph_title_txt = ui_elements.Text(input_layer, 50, 50, assets.SF_Pro_Medium_20, "Graph title:", assets.text_colour)
x_label_txt = ui_elements.Text(input_layer, 50, 100, assets.SF_Pro_Medium_20, "x label:", assets.text_colour)
y_label_txt = ui_elements.Text(input_layer, 50, 150, assets.SF_Pro_Medium_20, "y label:", assets.text_colour)

button_open = ui_elements.LabelledButton(input_layer, 15, 655, 150, 50, assets.blue, pygame.K_F1, assets.dark_blue, "Open", assets.text_colour, assets.SF_Pro_Medium_20, False)
button_clear = ui_elements.LabelledButton(input_layer, 195, 655, 150, 50, assets.button_colour_light, pygame.K_ESCAPE, assets.button_colour_dark, "Clear", assets.text_colour, assets.SF_Pro_Medium_20, False)


graphing_layer = graph.GraphingSurface(program_window, 360, 0, 920, 720, assets.bg_colour, assets.text_colour, 2, assets.button_colour_light, assets.blue)
