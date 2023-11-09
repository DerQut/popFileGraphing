import pygame

import ui_elements


class RoundedLabelledButton(ui_elements.LabelledButton):

    def __init__(self, surface, x_cord, y_cord, x_size, y_size, colour, unicode_id, secondary_colour, text,  text_colour, text_font, border_colour, needs_shift=0.5, border_thickness=2, circle_radius=7, is_visible=True):
        super().__init__(surface, x_cord, y_cord, x_size, y_size, colour, unicode_id, secondary_colour, text,  text_colour, text_font, needs_shift, is_visible)

        self.circle_radius = circle_radius

        self.border_colour = border_colour
        self.border_thickness = border_thickness

        self.rect1 = pygame.rect.Rect(self.x_cord, self.y_cord+self.circle_radius, self.x_size, self.y_size-2*circle_radius)
        self.rect2 = pygame.rect.Rect(self.x_cord+self.circle_radius, self.y_cord, self.x_size-2*circle_radius, self.y_size)
        
        self.rect1b = pygame.rect.Rect(self.x_cord-self.border_thickness, self.y_cord+self.circle_radius, self.x_size+2*self.border_thickness, self.y_size-2*circle_radius)
        self.rect2b = pygame.rect.Rect(self.x_cord+self.circle_radius, self.y_cord-self.border_thickness, self.x_size-2*circle_radius, self.y_size+2*self.border_thickness)

    def draw(self):

        pygame.draw.rect(self.surface.pg_surface, self.border_colour, self.rect1b)
        pygame.draw.rect(self.surface.pg_surface, self.border_colour, self.rect2b)
        
        pygame.draw.circle(self.surface.pg_surface, self.border_colour, (self.x_cord+self.circle_radius, self.y_cord+self.circle_radius), self.circle_radius+self.border_thickness)
        pygame.draw.circle(self.surface.pg_surface, self.border_colour, (self.x_cord+self.circle_radius, self.y_cord+self.y_size-self.circle_radius), self.circle_radius+self.border_thickness)
        pygame.draw.circle(self.surface.pg_surface, self.border_colour, (self.x_cord+self.x_size-self.circle_radius, self.y_cord+self.circle_radius), self.circle_radius+self.border_thickness)
        pygame.draw.circle(self.surface.pg_surface, self.border_colour, (self.x_cord+self.x_size-self.circle_radius, self.y_cord+self.y_size-self.circle_radius), self.circle_radius+self.border_thickness)

        pygame.draw.circle(self.surface.pg_surface, self.colour, (self.x_cord+self.circle_radius, self.y_cord+self.circle_radius), self.circle_radius)
        pygame.draw.circle(self.surface.pg_surface, self.colour, (self.x_cord+self.circle_radius, self.y_cord+self.y_size-self.circle_radius), self.circle_radius)
        pygame.draw.circle(self.surface.pg_surface, self.colour, (self.x_cord+self.x_size-self.circle_radius, self.y_cord+self.circle_radius), self.circle_radius)
        pygame.draw.circle(self.surface.pg_surface, self.colour, (self.x_cord+self.x_size-self.circle_radius, self.y_cord+self.y_size-self.circle_radius), self.circle_radius)

        pygame.draw.rect(self.surface.pg_surface, self.colour, self.rect1)
        pygame.draw.rect(self.surface.pg_surface, self.colour, self.rect2)


class RoundedTextField(ui_elements.TextField):

    def __init__(self, surface, x_cord, y_cord, x_size, y_size, colour, text,  text_colour, text_font, max_length, highlight_colour, unicode_range=[], additional_characters=[], return_characters=[pygame.K_RETURN, pygame.K_ESCAPE], backspace_characters=[pygame.K_BACKSPACE], is_numerical=False, highlight_width=4, circle_radius=7, needs_shift=False, is_visible=True):
        super().__init__(surface, x_cord, y_cord, x_size, y_size, colour, text,  text_colour, text_font, max_length, unicode_range, additional_characters, return_characters, backspace_characters, is_numerical, needs_shift, is_visible)

        self.circle_radius = circle_radius
        self.highlight_colour = highlight_colour
        self.highlight_width = highlight_width

        self.rect1 = pygame.rect.Rect(self.x_cord, self.y_cord + self.circle_radius, self.x_size, self.y_size - 2 * self.circle_radius)
        self.rect2 = pygame.rect.Rect(self.x_cord + self.circle_radius, self.y_cord, self.x_size - 2 * self.circle_radius, self.y_size)

        self.rect1h = pygame.rect.Rect(self.x_cord-self.highlight_width, self.y_cord+self.circle_radius, self.x_size+2*self.highlight_width, self.y_size-2*self.circle_radius)
        self.rect2h = pygame.rect.Rect(self.x_cord + self.circle_radius, self.y_cord-self.highlight_width, self.x_size-2*self.circle_radius, self.y_size+2*self.highlight_width)

    def draw(self):

        if self.is_highlighted:
            pygame.draw.rect(self.surface.pg_surface, self.highlight_colour, self.rect1h)
            pygame.draw.rect(self.surface.pg_surface, self.highlight_colour, self.rect2h)
            
            pygame.draw.circle(self.surface.pg_surface, self.highlight_colour, (self.x_cord + self.circle_radius, self.y_cord + self.circle_radius), self.circle_radius+self.highlight_width)
            pygame.draw.circle(self.surface.pg_surface, self.highlight_colour, (self.x_cord + self.circle_radius, self.y_cord + self.y_size - self.circle_radius), self.circle_radius+self.highlight_width)
            pygame.draw.circle(self.surface.pg_surface, self.highlight_colour, (self.x_cord + self.x_size - self.circle_radius, self.y_cord + self.circle_radius), self.circle_radius+self.highlight_width)
            pygame.draw.circle(self.surface.pg_surface, self.highlight_colour, (self.x_cord + self.x_size - self.circle_radius, self.y_cord + self.y_size - self.circle_radius), self.circle_radius+self.highlight_width)

        pygame.draw.circle(self.surface.pg_surface, self.colour, (self.x_cord + self.circle_radius, self.y_cord + self.circle_radius), self.circle_radius)
        pygame.draw.circle(self.surface.pg_surface, self.colour, (self.x_cord + self.circle_radius, self.y_cord + self.y_size - self.circle_radius), self.circle_radius)
        pygame.draw.circle(self.surface.pg_surface, self.colour, (self.x_cord + self.x_size - self.circle_radius, self.y_cord + self.circle_radius), self.circle_radius)
        pygame.draw.circle(self.surface.pg_surface, self.colour, (self.x_cord + self.x_size - self.circle_radius, self.y_cord + self.y_size - self.circle_radius), self.circle_radius)

        pygame.draw.rect(self.surface.pg_surface, self.colour, self.rect1)
        pygame.draw.rect(self.surface.pg_surface, self.colour, self.rect2)
