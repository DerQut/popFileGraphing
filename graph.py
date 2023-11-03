import math

import numpy
import pygame

import window
import assets


class GraphingSurface(window.Surface):

    def __init__(self, window, x_cord, y_cord, x_size, y_size, bg_colour, line_colour, line_width, axis_colour,
                 highlight_colour):
        super().__init__(window, x_cord, y_cord, x_size, y_size, bg_colour)

        self.line_colour = line_colour
        self.axis_colour = axis_colour
        self.highlight_colour = highlight_colour
        self.highlight_colour_2 = (highlight_colour[0]*0.5, highlight_colour[1]*0.5, highlight_colour[2]*0.5)

        self.line_width = line_width

        self.shows_points = False

        self.points = []

        self.x_min = 0
        self.x_max = 100
        self.x_delimiter = (self.x_max - self.x_min) / 10

        self.y_min = 0
        self.y_max = 100
        self.y_delimiter = (self.y_max - self.y_min) / 10

        self.box_points = [(100, 50), (self.x_size-25, 50), (self.x_size-25, self.y_size-50), (100, self.y_size-50)]

        self.x_pixel_size = self.box_points[1][0] - self.box_points[0][0]
        self.y_pixel_size = self.box_points[2][1] - self.box_points[0][1]

        self.x_pixel_delimiter = self.x_pixel_size / ((self.x_max - self.x_min) / self.x_delimiter)
        self.y_pixel_delimiter = self.y_pixel_size / ((self.y_max - self.y_min) / self.y_delimiter)

    def draw(self):

        self.pg_surface.fill(self.colour)

        self.draw_points()

        self.draw_axis()

        for element in self.elements:
            if element.is_visible:
                element.draw()

        self.window.screen.blit(self.pg_surface, (self.x_cord, self.y_cord))

    def set_scale(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.x_delimiter = (self.x_max - self.x_min) / 10

        self.y_min = y_min
        self.y_max = y_max
        self.y_delimiter = (self.y_max - self.y_min) / 10

        print(self.y_delimiter)
        print(self.y_min)
        print(self.y_max)

        self.x_pixel_size = self.box_points[1][0] - self.box_points[0][0]
        self.y_pixel_size = self.box_points[2][1] - self.box_points[0][1]

        self.x_pixel_delimiter = self.x_pixel_size / ((self.x_max - self.x_min) / self.x_delimiter)
        self.y_pixel_delimiter = self.y_pixel_size / ((self.y_max - self.y_min) / self.y_delimiter)

    def clear(self):

        self.points = []

        self.x_min = 0
        self.x_max = 100
        self.x_delimiter = (self.x_max - self.x_min) / 10

        self.y_min = 0
        self.y_max = 100
        self.y_delimiter = (self.y_max - self.y_min) / 10

        self.box_points = [(100, 50), (self.x_size - 25, 50), (self.x_size - 25, self.y_size - 50),
                           (100, self.y_size - 50)]

        self.x_pixel_size = self.box_points[1][0] - self.box_points[0][0]
        self.y_pixel_size = self.box_points[2][1] - self.box_points[0][1]

        self.x_pixel_delimiter = self.x_pixel_size / ((self.x_max - self.x_min) / self.x_delimiter)
        self.y_pixel_delimiter = self.y_pixel_size / ((self.y_max - self.y_min) / self.y_delimiter)

    def draw_axis(self):

        pygame.draw.lines(self.pg_surface, self.axis_colour, True, self.box_points, 1)

        i = self.x_min
        x = 0
        while x <= self.x_pixel_size:
            pygame.draw.line(self.pg_surface, self.axis_colour, (self.box_points[3][0]+x, self.box_points[3][1]),
                             (self.box_points[3][0]+x, self.box_points[3][1]+10), 1)
            self.pg_surface.blit(assets.SF_Pro_Light_16.render("{:.1f}".format(i), True, self.axis_colour),
                                 (self.box_points[3][0]+x-8, self.box_points[3][1]+10))
            x = x + self.x_pixel_delimiter
            i = i + self.x_delimiter

        i = self.y_min
        y = self.y_pixel_size
        while y >= 0:
            pygame.draw.line(self.pg_surface, self.axis_colour, (self.box_points[0][0], self.box_points[0][1]+y), (self.box_points[0][0]-10, self.box_points[0][1]+y), 1)
            self.pg_surface.blit(assets.SF_Pro_Light_16.render("{:.1f}".format(i), True, self.axis_colour), (self.box_points[0][0]-60, self.box_points[0][1]+y-8))
            y = y - self.y_pixel_delimiter
            i = i + self.y_delimiter

    def draw_points(self):

        rescaled_points = []

        for point in self.points:

            if point[0] > self.x_max or point[0] < self.x_min:
                continue

            if point[1] > self.y_max or point[1] < self.y_min:
                continue

            rescaled_point_x = self.box_points[3][0] + ((point[0] - self.x_min) * self.x_pixel_delimiter / self.x_delimiter)
            rescaled_point_y = self.box_points[3][1] - ((point[1] - self.y_min) * self.y_pixel_delimiter / self.y_delimiter)

            rescaled_points.append((rescaled_point_x, rescaled_point_y))

        if self.shows_points:
            for point in rescaled_points:
                pygame.draw.circle(self.pg_surface, self.highlight_colour_2, point, 7)

        if len(rescaled_points) >= 2:
            pygame.draw.lines(self.pg_surface, self.line_colour, False, rescaled_points, 1)

        if self.shows_points:
            for point in rescaled_points:
                pygame.draw.circle(self.pg_surface, self.highlight_colour, point, 3)
