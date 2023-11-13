import math

import parser
import ui_elements
import window
import assets
import graph
import macos_ui

import pygame
from pygame.locals import *


def maxx(value):
    x = math.ceil(value)

    i = 0
    while x > 10:
        x = math.ceil(x/10)
        i = i + 1

    return x * 10**i


def minn(value):
    x = math.floor(value)

    i = 0
    while x > 10:
        x = math.floor(x/10)
        i = i + 1

    return x * 10 ** i


def loop_action():
    graphing_layer.draw()
    graph_title_field.push_text_right()
    x_label_field.push_text_right()
    y_label_field.push_text_right()

    x_range_min_field.push_text_right()
    x_range_max_field.push_text_right()
    y_range_min_field.push_text_right()
    y_range_max_field.push_text_right()

    x_axis_label.label.change_text(x_label_field.label.text)
    x_axis_label.center_text()

    y_axis_label.change_text(y_label_field.label.text)
    y_axis_label.rotate(90)
    y_axis_label.y_cord = graphing_layer.box.top + (graphing_layer.box.bottom - y_axis_label.height)/2

    graph_title_label.label.change_text(graph_title_field.label.text)
    graph_title_label.center_text()

    global_max_plate.label.change_text("Max: (" + "{:.1f}".format(graphing_layer.global_max[0]) + ", " + "{:.1f}".format(graphing_layer.global_max[1]) + ")")
    global_max_plate.center_text()

    fwhm_plate.label.change_text("FWHM: " + "{:.3f}".format(graphing_layer.fwhm))
    fwhm_plate.center_text()

    x_max = float(x_range_max_field.label.text)
    x_min = float(x_range_min_field.label.text)
    y_max = float(y_range_max_field.label.text)
    y_min = float(y_range_min_field.label.text)

    graphing_layer.set_scale(x_min, x_max, y_min, y_max)


def button_handler(event_key, needs_shifting, is_shifting):
    if event_key == pygame.K_F1:
        get_points()

    elif event_key == pygame.K_ESCAPE and is_shifting:
        graphing_layer.clear()
        x_label_field.label.change_text("x")
        y_label_field.label.change_text("y")
        graph_title_field.label.change_text("Title")
        x_range_min_field.label.change_text("0")
        x_range_max_field.label.change_text("100")
        y_range_min_field.label.change_text("0")
        y_range_max_field.label.change_text("100")
        x_range_min_field.has_comma = False
        x_range_max_field.has_comma = False
        y_range_min_field.has_comma = False
        y_range_max_field.has_comma = False

    elif event_key == pygame.K_F2:
        graphing_layer.shows_points = not graphing_layer.shows_points
        global_max_plate.is_visible = not global_max_plate.is_visible
        global_max_plate.label.is_visible = not global_max_plate.label.is_visible

    elif event_key == pygame.K_F3:
        graphing_layer.shows_fwhm = not graphing_layer.shows_fwhm
        fwhm_plate.is_visible = not fwhm_plate.is_visible
        fwhm_plate.label.is_visible = not fwhm_plate.label.is_visible


def get_points():

    filename = parser.get_file()
    if not filename:
        return 1

    real_name = parser.get_name(filename)

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
            graphing_layer.global_max = point

        graphing_layer.points.append(point)

    file.close()

    x_min = math.floor(x_min)
    x_max = math.ceil(x_max)
    y_min = minn(y_min)
    y_max = maxx(y_max)

    graph_title_field.label.change_text(real_name)

    if y_min:
        if y_max / y_min >= 1000:
            y_min = 0

    x_range_max_field.label.change_text(str(x_max))
    x_range_min_field.label.change_text(str(x_min))
    y_range_max_field.label.change_text(str(y_max))
    y_range_min_field.label.change_text(str(y_min))

    graphing_layer.set_scale(x_min, x_max, y_min, y_max)


program_window = window.Window(1280, 720, DOUBLEBUF, assets.bg_colour, "The Graphing Engine")


input_layer = window.Surface(program_window, 0, 0, 360, 720, assets.bg_colour_inactive)

graph_title_txt = ui_elements.Text(input_layer, 15, 50, assets.SF_Pro_Medium_20, "Graph title:", assets.text_colour)
x_label_txt = ui_elements.Text(input_layer, 15, 100, assets.SF_Pro_Medium_20, "x label:", assets.text_colour)
y_label_txt = ui_elements.Text(input_layer, 15, 150, assets.SF_Pro_Medium_20, "y label:", assets.text_colour)

graph_title_field = macos_ui.RoundedTextField(input_layer, 150, 50, 195, 25, assets.text_colour, "Title", (0, 0, 0), assets.SF_Pro_Light_16, 18, assets.blue, [32, 700])
x_label_field = macos_ui.RoundedTextField(input_layer, 150, 100, 195, 25, assets.text_colour, "x", (0, 0, 0), assets.SF_Pro_Light_16, 18, assets.blue, [32, 700])
y_label_field = macos_ui.RoundedTextField(input_layer, 150, 150, 195, 25, assets.text_colour, "y", (0, 0, 0), assets.SF_Pro_Light_16, 18, assets.blue, [32, 700])

x_range_min_txt = ui_elements.Text(input_layer, 15, 200, assets.SF_Pro_Medium_20, "x range (min):", assets.text_colour)
x_range_max_txt = ui_elements.Text(input_layer, 15, 250, assets.SF_Pro_Medium_20, "x range (max):", assets.text_colour)
y_range_min_txt = ui_elements.Text(input_layer, 15, 300, assets.SF_Pro_Medium_20, "y range (min):", assets.text_colour)
y_range_max_txt = ui_elements.Text(input_layer, 15, 350, assets.SF_Pro_Medium_20, "y range (max):", assets.text_colour)

x_range_min_field = macos_ui.RoundedTextField(input_layer, 150, 200, 195, 25, assets.text_colour, "0", (0, 0, 0), assets.SF_Pro_Light_16, 18, assets.blue, [48, 57], [pygame.K_PERIOD], is_numerical=True)
x_range_max_field = macos_ui.RoundedTextField(input_layer, 150, 250, 195, 25, assets.text_colour, "100", (0, 0, 0), assets.SF_Pro_Light_16, 18, assets.blue, [48, 57], [pygame.K_PERIOD], is_numerical=True)
y_range_min_field = macos_ui.RoundedTextField(input_layer, 150, 300, 195, 25, assets.text_colour, "0", (0, 0, 0), assets.SF_Pro_Light_16, 18, assets.blue, [48, 57], [pygame.K_PERIOD], is_numerical=True)
y_range_max_field = macos_ui.RoundedTextField(input_layer, 150, 350, 195, 25, assets.text_colour, "100", (0, 0, 0), assets.SF_Pro_Light_16, 18, assets.blue, [48, 57], [pygame.K_PERIOD], is_numerical=True)

button_open = macos_ui.RoundedLabelledButton(input_layer, 15, 655, 150, 50, assets.blue, pygame.K_F1, assets.dark_blue, "Open", assets.text_colour, assets.SF_Pro_Medium_20, assets.dark_blue)
button_clear = macos_ui.RoundedLabelledButton(input_layer, 195, 655, 150, 50, assets.button_colour_light, pygame.K_ESCAPE, assets.button_colour_dark, "Clear", assets.text_colour, assets.SF_Pro_Medium_20, assets.button_colour_dark, needs_shift=True)


graphing_layer = graph.GraphingSurface(program_window, 362, 0, 920, 720, assets.bg_colour, assets.text_colour, 2, assets.button_colour_light, assets.blue)

border = ui_elements.Rect(graphing_layer, 0, 0, 1, 720, assets.bg_border)

graph_title_label = ui_elements.LabelledButton(graphing_layer, graphing_layer.box.left, graphing_layer.box.top-35, graphing_layer.box.right-graphing_layer.box.left, 20, graphing_layer.colour, 0, graphing_layer.colour, graph_title_field.label.text, assets.text_colour, assets.SF_Pro_Medium_24, 0.5)
x_axis_label = ui_elements.LabelledButton(graphing_layer, graphing_layer.box.left, graphing_layer.box.bottom+35, graphing_layer.box.right-graphing_layer.box.left, 20, graphing_layer.colour, 0, graphing_layer.colour, x_label_field.label.text, assets.text_colour, assets.SF_Pro_Medium_24, 0.5)
y_axis_label = ui_elements.Text(graphing_layer, graphing_layer.box.left-135, graphing_layer.box.top, assets.SF_Pro_Medium_24, y_label_field.label.text, assets.text_colour)

global_max_plate = macos_ui.RoundedLabelledButton(graphing_layer, graphing_layer.box.right-210, graphing_layer.box.top+11, 200, 50, assets.bg_colour_inactive, 0, assets.bg_colour_inactive, "Max: (" + "{:.1f}".format(graphing_layer.global_max[0]) + ", " + "{:.1f}".format(graphing_layer.global_max[1]) + ")", assets.text_colour, assets.SF_Pro_Medium_18, assets.bg_border, False, 2, 7, False)

fwhm_plate = macos_ui.RoundedLabelledButton(graphing_layer, graphing_layer.box.right-210, graphing_layer.box.top+72, 200, 50, assets.bg_colour_inactive, 0, assets.bg_colour_inactive, "FWHM: " + "{:.3f}".format(graphing_layer.fwhm), assets.text_colour, assets.SF_Pro_Medium_18, assets.bg_border, False, 2, 7, False)
