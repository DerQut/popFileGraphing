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

        self.box = pygame.rect.Rect(150, 80, self.x_size-175, self.y_size-180)

        self.x_pixel_size = self.box.width
        self.y_pixel_size = self.box.height

        self.x_pixel_delimiter = self.x_pixel_size / ((self.x_max - self.x_min) / self.x_delimiter)
        self.y_pixel_delimiter = self.y_pixel_size / ((self.y_max - self.y_min) / self.y_delimiter)

        self.global_max = (0, 0)
        self.global_max_rescaled = (0, 0)

        self.rescaled_points = []

        self.shows_fwhm = False
        self.fwhm = 0

    def draw(self):

        self.pg_surface.fill(self.colour)

        if self.shows_fwhm and len(self.points) > 2:
            self.draw_fwhm()

        self.draw_points()

        self.draw_axis()

        for element in self.elements:
            if element.is_visible:
                element.draw()

        self.window.screen.blit(self.pg_surface, (self.x_cord, self.y_cord))

    def set_scale(self, x_min, x_max, y_min, y_max):

        if x_min >= x_max or y_min >= y_max:
            return 1

        self.x_min = x_min
        self.x_max = x_max
        self.x_delimiter = (self.x_max - self.x_min) / 10

        self.y_min = y_min
        self.y_max = y_max
        self.y_delimiter = (self.y_max - self.y_min) / 10

        self.x_pixel_size = self.box.width
        self.y_pixel_size = self.box.height

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

        self.x_pixel_size = self.box.width
        self.y_pixel_size = self.box.height

        self.x_pixel_delimiter = self.x_pixel_size / ((self.x_max - self.x_min) / self.x_delimiter)
        self.y_pixel_delimiter = self.y_pixel_size / ((self.y_max - self.y_min) / self.y_delimiter)

        self.global_max = (0, 0)
        self.global_max_rescaled = (0, 0)

    def draw_axis(self):

        pygame.draw.lines(self.pg_surface, self.axis_colour, True, (self.box.topleft, self.box.topright, self.box.bottomright, self.box.bottomleft))

        i = self.x_min
        x = 0
        while x <= self.x_pixel_size:
            pygame.draw.line(self.pg_surface, self.axis_colour, (self.box.left+x, self.box.bottom), (self.box.left+x, self.box.bottom+10), 1)
            if int(i) == i:
                self.pg_surface.blit(assets.SF_Pro_Light_16.render(str(int(i)), True, self.axis_colour), (self.box.left+x-4*len(str(int(i))), self.box.bottom+10))
            else:
                self.pg_surface.blit(assets.SF_Pro_Light_16.render("{:.1f}".format(i), True, self.axis_colour), (self.box.left+x-4*(len("{:.1f}".format(i))-1), self.box.bottom + 10))
            x = x + self.x_pixel_delimiter
            i = i + self.x_delimiter

        i = self.y_min
        y = self.y_pixel_size
        while y >= 0:
            pygame.draw.line(self.pg_surface, self.axis_colour, (self.box.left, self.box.top+y), (self.box.left-10, self.box.top+y), 1)
            if int(i) == i:
                self.pg_surface.blit(assets.SF_Pro_Light_16.render(str(int(i)), True, self.axis_colour), (self.box.left-16-8*len("{:.1f}".format(i)), self.box.top+y-8))
            else:
                self.pg_surface.blit(assets.SF_Pro_Light_16.render("{:.1f}".format(i), True, self.axis_colour), (self.box.left-16-8*len("{:.1f}".format(i)), self.box.top+y-8))
            y = y - self.y_pixel_delimiter
            i = i + self.y_delimiter

    def draw_points(self):

        self.rescaled_points = []

        for point in self.points:

            rescaled_point_x = self.box.left + ((point[0] - self.x_min) * self.x_pixel_delimiter / self.x_delimiter)
            rescaled_point_y = self.box.bottom - ((point[1] - self.y_min) * self.y_pixel_delimiter / self.y_delimiter)

            self.rescaled_points.append((rescaled_point_x, rescaled_point_y))

            if point == self.global_max:
                self.global_max_rescaled = (rescaled_point_x, rescaled_point_y)

        if self.shows_points:
            for point in self.rescaled_points:
                pygame.draw.circle(self.pg_surface, self.highlight_colour_2, point, 7)

        if len(self.rescaled_points) >= 2:
            pygame.draw.lines(self.pg_surface, self.line_colour, False, self.rescaled_points, self.line_width)

        if self.shows_points:
            for point in self.rescaled_points:
                pygame.draw.circle(self.pg_surface, self.highlight_colour, point, 3)
                if point == self.global_max_rescaled:
                    pygame.draw.line(self.pg_surface, self.highlight_colour, point, (point[0], self.box.bottom), 1)
                    pygame.draw.line(self.pg_surface, self.highlight_colour, point, (self.box.left, point[1]), 1)

    def draw_fwhm(self):

        i = 0
        j = 0

        x1 = 0
        x2 = 0

        max_index = 0

        found = False
        while i < len(self.rescaled_points):
            if self.rescaled_points[i] == self.global_max_rescaled:
                found = True
                max_index = i

                j = i
                while j > 1:
                    if self.points[j][1] <= self.points[j-1][1]:
                        break
                    j = j - 1

            if found:
                if self.points[i][1] <= self.points[i+1][1]:
                    break
            i = i + 1

        y = max(self.points[i][1], self.points[j][1]) + (abs(self.global_max[1] - max(self.points[i][1], self.points[j][1]))/2)
        y_rescaled = self.box.bottom - ((y - self.y_min) * self.y_pixel_delimiter / self.y_delimiter)

        a = max_index
        while a < len(self.points):
            if self.points[a][1] > y > self.points[a+1][1]:
                y_ratio = (y - self.points[a][1])/(self.points[a+1][1] - self.points[a][1])
                x1 = self.points[a][0] + abs(y_ratio*(self.points[a+1][0] - self.points[a][0]))
                break
            a = a + 1

        a = max_index
        while a > 0:
            if self.points[a][1] > y > self.points[a-1][1]:
                y_ratio = (y - self.points[a-1][1])/(self.points[a][1] - self.points[a-1][1])
                x2 = self.points[a][0] - abs(y_ratio*(self.points[a-1][0] - self.points[a][0]))
                break
            a = a - 1

        x1_rescaled = self.box.left + ((x1 - self.x_min) * self.x_pixel_delimiter / self.x_delimiter)
        x2_rescaled = self.box.left + ((x2 - self.x_min) * self.x_pixel_delimiter / self.x_delimiter)

        self.fwhm = abs(x2 - x1)

        pygame.draw.line(self.pg_surface, self.highlight_colour, (x1_rescaled, y_rescaled), (x2_rescaled, y_rescaled), 3)
