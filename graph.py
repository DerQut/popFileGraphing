import math

import numpy
import pygame

import window
import assets


class GraphingSurface(window.Surface):

    def __init__(self, window, x_cord, y_cord, x_size, y_size, bg_colour, line_colour, line_width, axis_colour, highlight_colour):
        super().__init__(window, x_cord, y_cord, x_size, y_size, bg_colour)

        self.line_colour = line_colour
        self.axis_colour = axis_colour
        self.highlight_colour = highlight_colour
        self.highlight_colour_2 = (highlight_colour[0]*0.5, highlight_colour[1]*0.5, highlight_colour[2]*0.5)

        self.line_width = line_width

        self.points = []
        self.highlights = []

        self.last_function = ""

        self.x_unit = 75
        self.y_unit = 75

        self.x_delimiter = 1
        self.y_delimiter = 1

        self.x_uses_floats = False

        self.zero_point = (0.5*self.x_size, 0.5*self.y_size)

    def draw(self):

        self.pg_surface.fill(self.colour)

        self.draw_axis()

        for element in self.elements:
            if element.is_visible:
                element.draw()

        for highlight in self.highlights:
            pygame.draw.circle(self.pg_surface, self.highlight_colour_2, highlight, 7)
            if highlight[0] != self.zero_point[0]:
                pygame.draw.line(self.pg_surface, self.highlight_colour_2, highlight, (highlight[0], self.zero_point[1]), 1)
            if highlight[1] != self.zero_point[1]:
                pygame.draw.line(self.pg_surface, self.highlight_colour_2, highlight, (self.zero_point[0], highlight[1]), 1)

        if len(self.points) > 1:
            pygame.draw.lines(self.pg_surface, self.line_colour, False, self.points, self.line_width)

        for highlight in self.highlights:
            pygame.draw.circle(self.pg_surface, self.highlight_colour, highlight, 3)

            self.pg_surface.blit((assets.SF_Pro_Light_16.render("x=" + ("{:.1f}".format((highlight[0]-self.zero_point[0]) / self.x_unit)) + ", y="+"{:.1f}".format(((self.zero_point[1]-highlight[1]) / self.y_unit)), True, self.highlight_colour)), (highlight[0]+7, highlight[1]+10*(numpy.sign(highlight[1]-self.zero_point[1])-1)))

        self.window.screen.blit(self.pg_surface, (self.x_cord, self.y_cord))

    def clear(self):
        self.highlights = []
        self.points = []
        self.zero_point = (0.5*self.x_size, 0.5*self.y_size)
        self.last_function = ""

        self.x_unit = 75
        self.y_unit = 75

        self.x_delimiter = 1
        self.y_delimiter = 1

        self.x_uses_floats = False

    def draw_axis(self):
        # y
        pygame.draw.line(self.pg_surface, self.axis_colour, (0, self.zero_point[1]), (self.x_size, self.zero_point[1]))

        y_cord = 0
        i = 0
        while y_cord <= self.y_size - self.zero_point[1]:
            pygame.draw.line(self.pg_surface, self.axis_colour, (self.zero_point[0], self.zero_point[1]+y_cord), (self.zero_point[0]+5, self.zero_point[1]+y_cord), 1)
            pygame.draw.line(self.pg_surface, self.axis_colour, (self.zero_point[0], self.zero_point[1]-y_cord), (self.zero_point[0]+5, self.zero_point[1]-y_cord), 1)

            if i:
                self.pg_surface.blit(assets.SF_Pro_Light_16.render(str(self.y_delimiter*i), True, self.axis_colour), (self.zero_point[0]+7, self.zero_point[1]-y_cord-10))
                self.pg_surface.blit(assets.SF_Pro_Light_16.render(str(self.y_delimiter*-i), True, self.axis_colour), (self.zero_point[0]+7, self.zero_point[1]+y_cord-10))

            y_cord = y_cord + self.y_delimiter * self.y_unit
            i = i + 1

        # x
        pygame.draw.line(self.pg_surface, self.axis_colour, (self.zero_point[0], 0), (self.zero_point[0], self.y_size))

        x_cord = 0
        i = 0
        while x_cord <= self.x_size - self.zero_point[0]:
            pygame.draw.line(self.pg_surface, self.axis_colour, (self.zero_point[0]+x_cord, self.zero_point[1]), (self.zero_point[0]+x_cord, self.zero_point[1]+5), 1)
            pygame.draw.line(self.pg_surface, self.axis_colour, (self.zero_point[0]-x_cord, self.zero_point[1]), (self.zero_point[0]-x_cord, self.zero_point[1]+5), 1)

            if i:
                if self.x_uses_floats:
                    self.pg_surface.blit(assets.SF_Pro_Light_16.render("{:.2f}".format(float(self.x_delimiter*i)), True, self.axis_colour), (self.zero_point[0]+x_cord-12, self.zero_point[1]+10))
                    self.pg_surface.blit(assets.SF_Pro_Light_16.render("{:.2f}".format(float(self.x_delimiter*-i)), True, self.axis_colour), (self.zero_point[0]-x_cord-12, self.zero_point[1]+10))
                else:
                    self.pg_surface.blit(assets.SF_Pro_Light_16.render(str(self.x_delimiter*i), True, self.axis_colour), (self.zero_point[0]+x_cord-5, self.zero_point[1]+10))
                    self.pg_surface.blit(assets.SF_Pro_Light_16.render(str(self.x_delimiter*-i), True, self.axis_colour), (self.zero_point[0]-x_cord-5, self.zero_point[1]+10))

            x_cord = x_cord + self.x_delimiter*self.x_unit
            i = i + 1

    def draw_sine(self, angles, uses_radians):

        self.clear()

        self.last_function = "sin"

        self.y_unit = 100
        self.x_unit = 50

        self.x_delimiter = math.pi/2
        self.x_uses_floats = True
        self.y_delimiter = 1

        conversion_multiplier = 1
        if not uses_radians:
            conversion_multiplier = math.pi/180
            self.x_delimiter = 90
            self.x_uses_floats = False

        self.x_unit = self.x_unit * conversion_multiplier
        print(math.sin(math.radians(190)))

        i = -0.6 * self.x_size
        while i*self.x_unit <= 0.5 * self.x_size:
            self.points.append((self.zero_point[0]+i*self.x_unit, self.zero_point[1] - self.y_unit*math.sin(i*conversion_multiplier)))
            i = i + 0.01

        self.highlights.append((self.zero_point[0]+angles*self.x_unit, self.zero_point[1] - self.y_unit*math.sin(angles*conversion_multiplier)))

    def draw_cosine(self, angles, uses_radians):

        self.clear()

        self.last_function = "cos"

        self.x_unit = 50
        self.y_unit = 100

        self.x_delimiter = math.pi/2

        self.x_uses_floats = uses_radians

        conversion_multiplier = 1
        if not uses_radians:
            conversion_multiplier = math.pi / 180
            self.x_delimiter = 90

        self.x_unit = self.x_unit * conversion_multiplier

        i = -0.6 * self.x_size
        while i * self.x_unit <= 0.5 * self.x_size:
            self.points.append((self.zero_point[0] + i * self.x_unit,
                                self.zero_point[1] - self.y_unit * math.cos(i * conversion_multiplier)))
            i = i + 0.01

        self.highlights.append((self.zero_point[0] + angles * self.x_unit,
                                self.zero_point[1] - self.y_unit * math.cos(angles * conversion_multiplier)))

    def draw_tangent(self, angles, uses_radians):

        self.clear()

        self.last_function = "tan"

        self.x_unit = 50
        self.y_unit = 50

        self.x_uses_floats = uses_radians

        self.y_delimiter = 1

        conversion_multiplier = math.pi / 180
        self.x_delimiter = 90

        self.x_unit = self.x_unit * conversion_multiplier

        i = -0.6 * self.x_size
        while i * self.x_unit <= 0.5 * self.x_size:
            self.points.append((self.zero_point[0] + i * self.x_unit, self.zero_point[1] - self.y_unit * math.tan(i * conversion_multiplier)))
            i = i + 0.01

        if uses_radians:
            self.x_delimiter = math.pi/2
            self.x_unit = self.x_unit * 180/math.pi
            self.x_uses_floats = True
            conversion_multiplier = 1

        self.highlights.append((self.zero_point[0] + angles*self.x_unit, self.zero_point[1] - self.y_unit * math.tan(angles * conversion_multiplier)))

    def draw_sinh(self, angles, uses_radians):

        self.clear()

        self.last_function = "sinh"

        self.x_unit = 33
        self.y_unit = 40

        self.x_delimiter = math.pi/2

        self.x_uses_floats = uses_radians
        conversion_multiplier = 1

        if not uses_radians:
            self.x_delimiter = 90
            conversion_multiplier = math.pi / 180

        self.x_unit = self.x_unit * conversion_multiplier

        i = -0.6 * self.x_size
        while i * self.x_unit <= 0.5 * self.x_size:
            self.points.append((self.zero_point[0] + i * self.x_unit, self.zero_point[1] - self.y_unit * math.sinh(i * conversion_multiplier)))
            i = i + 0.01

        self.highlights.append((self.zero_point[0] + angles * self.x_unit, self.zero_point[1] - self.y_unit * math.sinh(angles * conversion_multiplier)))

    def draw_cosh(self, angles, uses_radians):

        self.clear()

        self.x_unit = 33
        self.y_unit = 40

        self.y_delimiter = 1

        self.x_delimiter = math.pi/2

        self.last_function = "cosh"

        self.x_uses_floats = uses_radians

        conversion_multiplier = 1
        if not uses_radians:
            self.x_delimiter = 90
            conversion_multiplier = math.pi / 180

        self.x_unit = self.x_unit * conversion_multiplier

        i = -0.6 * self.x_size
        while i * self.x_unit <= 0.5 * self.x_size:
            self.points.append((self.zero_point[0] + i * self.x_unit, self.zero_point[1] - self.y_unit * math.cosh(i * conversion_multiplier)))
            i = i + 0.01

        self.highlights.append((self.zero_point[0] + angles * self.x_unit, self.zero_point[1] - self.y_unit * math.cosh(angles * conversion_multiplier)))

    def draw_tanh(self, angles, uses_radians):

        self.clear()

        self.x_unit = 33
        self.y_unit = 40

        self.x_uses_floats = uses_radians

        self.x_delimiter = math.pi/2
        self.y_delimiter = 1

        self.last_function = "tanh"

        conversion_multiplier = 1
        if not uses_radians:
            self.x_delimiter = 90
            conversion_multiplier = math.pi / 180

        self.x_unit = self.x_unit * conversion_multiplier

        i = -self.x_size
        while i * self.x_unit <= 0.5 * self.x_size:
            self.points.append((self.zero_point[0] + i * self.x_unit, self.zero_point[1] - self.y_unit * math.tanh(i * conversion_multiplier)))
            i = i + 0.01

        self.highlights.append((self.zero_point[0] + angles * self.x_unit, self.zero_point[1] - self.y_unit * math.tanh(angles * conversion_multiplier)))

    def draw_quadratic(self, a, b, c, solutions):

        self.clear()

        self.x_unit = 50
        self.y_unit = 50

        self.x_delimiter = 1
        self.y_delimiter = 1

        i = -0.6 * self.x_size
        while i*self.x_unit < 0.5 * self.x_size:

            self.points.append((self.zero_point[0] + i*self.x_unit, self.zero_point[1]-self.y_unit*(a*i**2 + b*i + c)))
            i = i + 0.001

        for solution in solutions:
            if solution != "NULL":
                self.highlights.append((self.zero_point[0] + solution*self.x_unit, self.zero_point[1]))

    def draw_y_to_x(self, x, y):

        self.clear()

        self.last_function = f"{y}_to_x"

        self.y_delimiter = abs(int(y ** x))
        self.y_unit = abs(int(33 / (y ** x)))

        if abs(int(y ** x)) > 1:
            self.x_unit = abs(int(66/x))
            self.x_delimiter = abs(int(x))
        else:
            self.x_unit = 66
            self.x_delimiter = 1
            self.y_delimiter = abs(int(y))
            self.y_unit = abs(int(33/y))

        print(self.y_delimiter)

        self.x_uses_floats = False

        i = -0.6 * self.x_size
        while i * self.x_unit < 0.5 * self.x_size:
            self.points.append((self.zero_point[0] + i * self.x_unit, self.zero_point[1] - self.y_unit * (y**i)))
            i = i + (abs(x)+0.5)/1000

        self.highlights.append((self.zero_point[0] + x * self.x_unit, self.zero_point[1] - y**x * self.y_unit))

    def draw_x_to_y(self, x, y):

        if y < 1:
            return 1

        self.clear()

        self.last_function = f"x_to_{y}"

        if abs(x) > 0:
            self.x_unit = 33/x
            self.y_unit = 33/x**y

            self.x_delimiter = x
            self.y_delimiter = x**y*2

        else:
            self.x_unit = 33
            self.y_unit = 33
            self.x_delimiter = 1
            self.y_delimiter = 1

        self.x_uses_floats = False

        i = -10 * self.x_size
        while i * self.x_unit < 0.5 * self.x_size:
            self.points.append((self.zero_point[0] + i * self.x_unit, self.zero_point[1] - self.y_unit * (i**y)))
            i = i + (abs(x)+1)/10

        self.highlights.append((self.zero_point[0] + x * self.x_unit, self.zero_point[1] - x**y * self.y_unit))

    def draw_root(self, x, root):

        if x < 0 and not root % 2:
            return 1

        self.clear()

        self.last_function = f"{root} root of x"

        if abs(x) >= 1:
            self.x_unit = 33 / abs(x)
            self.x_delimiter = int(abs(x))
            self.y_unit = 33 / math.pow(abs(x), 1/root)
            self.y_delimiter = int(math.pow(abs(x), 1/root))
        else:
            self.x_unit = 33
            self.x_delimiter = 1
            self.y_unit = 33
            self.y_delimiter = 1

        self.x_uses_floats = False

        i = 0
        if root % 2:
            i = -0.6 * self.x_size

        while i * self.x_unit < 0.5 * self.x_size:
            self.points.append((self.zero_point[0] + i * self.x_unit, self.zero_point[1] - self.y_unit * numpy.sign(i)*(pow(abs(i), 1/root))))
            i = i + x/10000

        self.highlights.append((self.zero_point[0] + x * self.x_unit, self.zero_point[1] - self.y_unit * numpy.sign(i)*pow(abs(x), 1/root)))

    def draw_log(self, x, base):

        if x <= 0:
            return 1

        self.clear()

        if abs(x) >= 1:
            self.x_unit = 66/x
            self.x_delimiter = int(x)
        else:
            self.x_unit = 66
            self.x_delimiter = 1

        if math.log(x, base) > 1:
            self.y_delimiter = int(math.log(x, base))
            self.y_unit = 66/math.log(x, base)
        else:
            self.y_unit = 66
            self.y_delimiter = 1

        i = (abs(x))/1000000000000
        while i * self.x_unit < 0.5 * self.x_size:
            print(i)
            self.points.append((self.zero_point[0] + i * self.x_unit, self.zero_point[1] - self.y_unit * math.log(i, base)))
            i = i + (abs(x)+1)/1000

        self.highlights.append((self.zero_point[0] + x * self.x_unit, self.zero_point[1] - self.y_unit * math.log(x, base)))
