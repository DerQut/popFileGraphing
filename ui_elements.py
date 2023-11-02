import pygame


class Rect:

    def __init__(self, surface, x_cord, y_cord, x_size, y_size, main_colour, is_visible=True):

        self.surface = surface

        self.x_cord = x_cord
        self.y_cord = y_cord

        self.x_size = x_size
        self.y_size = y_size

        self.main_colour = main_colour
        self.colour = main_colour

        self.is_visible = is_visible

        self.type = "Rect"

        self.rect = pygame.rect.Rect(x_cord, y_cord, x_size, y_size)

        self.surface.elements.append(self)

    def draw(self):
        self.surface.pg_surface.fill(self.colour, self.rect)


class Element:

    def __init__(self, surface, x_cord, y_cord, texture, is_visible=True):

        self.surface = surface

        self.x_cord = x_cord
        self.y_cord = y_cord

        self.is_visible = is_visible

        self.surface.elements.append(self)

        self.texture = texture

        self.width = self.texture.get_width()
        self.height = self.texture.get_height()

        self.type = "Element"

    def draw(self):
        self.surface.pg_surface.blit(self.texture, (self.x_cord, self.y_cord))

    def change_texture(self, new_texture):
        self.texture = new_texture

        self.width = self.texture.get_width()
        self.height = self.texture.get_height()


class Text(Element):

    def __init__(self, surface, x_cord, y_cord, font, text, colour, is_visible=True):
        super().__init__(surface, x_cord, y_cord, font.render(text, True, colour), is_visible)

        self.font = font
        self.text = text
        self.colour = colour

        self.type = "Text"

    def change_texture(self, new_font, new_text, new_colour):
        super().change_texture(new_font.render(new_text, True, new_colour))

    def change_text(self, new_text):
        self.change_texture(self.font, new_text, self.colour)

    def reload(self):
        self.change_texture(self.font, self.text, self.colour)

    def push_right(self, offset):

        self.x_cord = self.surface.x_size - self.texture.get_width() - offset


class Button(Rect):

    def __init__(self, surface, x_cord, y_cord, x_size, y_size, main_colour, unicode_id, secondary_colour, needs_shift=False, is_visible=True):
        super().__init__(surface, x_cord, y_cord, x_size, y_size, main_colour, is_visible)

        self.unicode_id = unicode_id

        self.secondary_colour = secondary_colour

        self.type = "Button"

        self.is_highlighted = True

        self.needs_shift = needs_shift

    def mouse_check(self, mouse_pos):
        if self.x_cord + self.x_size > mouse_pos[0] - self.surface.x_cord > self.x_cord and self.y_cord + self.y_size > mouse_pos[1] - self.surface.y_cord > self.y_cord:
            self.is_highlighted = True
        else:
            self.is_highlighted = False

        return self.is_highlighted


class LabelledButton(Button):

    def __init__(self, surface, x_cord, y_cord, x_size, y_size, colour, unicode_id, secondary_colour, text,  text_colour, text_font, needs_shift=False, is_visible=True):
        super().__init__(surface, x_cord, y_cord, x_size, y_size, colour, unicode_id, secondary_colour, needs_shift, is_visible)

        self.label = Text(self.surface, self.x_cord, self.y_cord, text_font, text, text_colour, is_visible)

        self.center_text()

        self.type = "LabelledButton"

    def center_text(self):
        self.label.x_cord = self.x_cord + (self.x_size - self.label.width)*0.5
        self.label.y_cord = self.y_cord + (self.y_size - self.label.height) * 0.5
