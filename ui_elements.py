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

    def rotate(self, angles):
        self.texture = pygame.transform.rotate(self.texture, angles)

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
        self.font = new_font
        self.text = new_text
        self.colour = new_colour

    def change_text(self, new_text):
        self.change_texture(self.font, new_text, self.colour)
        self.text = new_text

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

        self.is_highlighted = False

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

    def push_text_right(self):
        self.label.x_cord = self.x_cord + self.x_size - self.label.width - 5


class TextField(LabelledButton):
    def __init__(self, surface, x_cord, y_cord, x_size, y_size, colour, text,  text_colour, text_font, max_length, unicode_range=[], additional_characters=[], return_characters=[pygame.K_RETURN, pygame.K_ESCAPE], backspace_characters=[pygame.K_BACKSPACE], is_numerical=False, needs_shift=False, is_visible=True):
        super().__init__(surface, x_cord, y_cord, x_size, y_size, colour, 0, colour, text,  text_colour, text_font, needs_shift, is_visible)

        self.type = "TextField"
        self.max_length = max_length

        self.unicode_range = unicode_range
        self.additional_characters = additional_characters

        self.return_characters = return_characters
        self.backspace_characters = backspace_characters

        self.is_numerical = is_numerical
        self.has_comma = False

    def write(self, unicode, is_shifting):

        if unicode == pygame.K_PERIOD and self.is_numerical and self.has_comma:
            return 1

        if unicode == pygame.K_PERIOD:
            self.has_comma = True

        if len(self.label.text) < self.max_length:

            if self.unicode_range[1] >= unicode >= self.unicode_range[0]:
                if not self.is_numerical:
                    if is_shifting:
                        self.label.change_text(self.label.text + chr(unicode).upper())
                    else:
                        self.label.change_text(self.label.text + chr(unicode))
                else:
                    if self.label.text == "0":
                        if unicode != pygame.K_PERIOD:
                            self.label.change_text(chr(unicode))
                    else:
                        self.label.change_text(self.label.text + chr(unicode))

            else:
                for character in self.additional_characters:
                    if character == unicode:
                        self.label.change_text(self.label.text + chr(unicode))

        for character in self.backspace_characters:
            if unicode == character:
                if len(self.label.text):
                    txt_list = list(self.label.text)
                    char = txt_list.pop()
                    if char == chr(pygame.K_PERIOD):
                        self.has_comma = False
                    self.label.change_text(''.join(txt_list))
                if not len(self.label.text):
                    if not self.is_numerical:
                        self.label.change_text('')
                    else:
                        self.label.change_text("0")

        for character in self.return_characters:
            if unicode == character:
                self.is_highlighted = False
