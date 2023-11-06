import pygame

import program


class Surface:

    def __init__(self, window, x_cord, y_cord, x_size, y_size, colour):

        self.window = window

        self.elements = []

        self.x_cord = x_cord
        self.y_cord = y_cord

        self.x_size = x_size
        self.y_size = y_size

        self.colour = colour

        self.pg_surface = pygame.surface.Surface((self.x_size, self.y_size))

        self.window.surfaces.append(self)

    def draw(self):

        self.pg_surface.fill(self.colour)

        for element in self.elements:
            if element.is_visible:
                element.draw()

        self.window.screen.blit(self.pg_surface, (self.x_cord, self.y_cord))


class Window:

    def __init__(self, x_size, y_size, flags, bg_colour, name):

        self.x_size = x_size
        self.y_size = y_size

        self.surfaces = []

        self.screen = pygame.display.set_mode((self.x_size, self.y_size), flags)
        pygame.display.set_caption(name)

        self.bg_colour = bg_colour

        self.running = True
        self.is_clicking = False
        self.is_shifting = False

    def get_events(self):

        events = pygame.event.get()

        mouse_pos = pygame.mouse.get_pos()
        self.is_clicking = False

        for event in events:
            if event.type == pygame.WINDOWCLOSE:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_down_handler(mouse_pos, event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_up_handler(event)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LSHIFT:
                    self.is_shifting = True

                program.button_handler(event.key, 0.5, self.is_shifting)

                for surface in self.surfaces:
                    for element in surface.elements:
                        if element.type == "Button" or element.type == "LabelledButton":
                            if element.unicode_id == event.key and (self.is_shifting == element.needs_shift or element.needs_shift == 0.5):
                                element.colour = element.secondary_colour
                        elif element.type == "TextField":
                            if element.is_highlighted:
                                element.write(event.key, self.is_shifting)

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_LSHIFT:
                    self.is_shifting = False
                    program.button_handler(event.key, 0.5, self.is_shifting)

                for surface in self.surfaces:
                    for element in surface.elements:
                        if element.type == "Button" or element.type == "LabelledButton":
                            if element.unicode_id == event.key:
                                element.colour = element.main_colour

    def run(self):

        self.screen.fill(self.bg_colour)

        for surface in self.surfaces:
            surface.draw()

        self.get_events()

        program.loop_action()

        pygame.display.flip()

    def mouse_button_down_handler(self, mouse_pos, event):
        if event.button == 1:
            self.is_clicking = True

            for surface in self.surfaces:
                for element in surface.elements:

                    if element.type == "Button" or element.type == "LabelledButton" or element.type == "TextField":
                        if element.mouse_check(mouse_pos) and self.is_clicking:
                            if element.type != "TextField":
                                program.button_handler(element.unicode_id, element.needs_shift, element.needs_shift)
                                element.colour = element.secondary_colour
                            else:
                                ...

    def mouse_button_up_handler(self, event):
        if event.button == 1:
            self.is_clicking = False

            for surface in self.surfaces:
                for element in surface.elements:

                    if element.type == "Button" or element.type == "LabelledButton":
                        element.colour = element.main_colour
