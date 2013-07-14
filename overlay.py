import pygame
import sgc

class LayeredButton(sgc.Button):
    """
    Layered Button widget, to prevent click events from propagating
    through to the background frame
    """
    _layered = True

# TODO: Convert header/footer into themed images
class Header(sgc.Simple):
    _surf_flags = pygame.SRCALPHA

    def __init__(self, theme):
        surf = pygame.Surface(theme.header_size, self._surf_flags)
        surf.fill((0, 0, 0, theme.header_alpha))
        sgc.Simple.__init__(self, surf, pos=theme.header_pos)

class Footer(sgc.Simple):
    _surf_flags = pygame.SRCALPHA

    def __init__(self, theme):
        surf = pygame.Surface(theme.footer_size, self._surf_flags)
        surf.fill((0, 0, 0, theme.footer_alpha))
        sgc.Simple.__init__(self, surf, pos=theme.footer_pos)

class Overlay:
    def __init__(self, theme):
        self.theme = theme
        self._is_active = False

        self.header = Header(theme)
        self.footer = Footer(theme)
        self.back = LayeredButton(widget=self, surf=theme.back_button,
                                  pos=theme.back_pos)
        self.forward = LayeredButton(widget=self, surf=theme.forward_button,
                                     pos=theme.forward_pos)
        self.star = LayeredButton(widget=self, surf=theme.unstarred_button,
                                  pos=theme.star_pos)
        self.widgets = [self.header,
                        self.back, self.forward, self.star,
                        self.footer]

    def add(self, fade=True, fade_delay=1):
        self._is_active = True
        for widget in self.widgets:
            widget.add(fade=fade, fade_delay=fade_delay)

    def remove(self, fade=True, fade_delay=1):
        self._is_active = False
        for widget in self.widgets:
            widget.remove(fade=fade, fade_delay=fade_delay)

    def active(self):
        return self._is_active

    def set_star(self, value=True):
        if value:
            self.star._create_base_images(self.theme.starred_button)
        else:
            self.star._create_base_images(self.theme.unstarred_button)
        self.star._switch()

