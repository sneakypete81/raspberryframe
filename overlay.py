import pygame
import sgc

class LayeredButton(sgc.Button):
    """
    Layered Button widget, to prevent click events from propagating
    through to the background frame
    """
    _layered = True

# TODO: Convert header/footer into themed images
class Background(sgc.Simple):
    _surf_flags = pygame.SRCALPHA

    def __init__(self, theme):
        surf = pygame.Surface((theme.screen_width, theme.screen_height),
                               self._surf_flags)
        surf.fill((16, 16, 16, theme.header_alpha),
                  rect=(theme.header_pos, theme.header_size))
        surf.fill((16, 16, 16, theme.footer_alpha),
                  rect=(theme.footer_pos, theme.footer_size))
        sgc.Simple.__init__(self, surf)

class Overlay:
    def __init__(self, theme):
        self.theme = theme
        self._is_active = False

        self.bg = Background(theme)
        self.back = LayeredButton(widget=self, surf=theme.back_button,
                                  pos=theme.back_pos)
        self.forward = LayeredButton(widget=self, surf=theme.forward_button,
                                     pos=theme.forward_pos)
        self.star = LayeredButton(widget=self, surf=theme.unstarred_button,
                                  pos=theme.star_pos)
        self.widgets = [self.bg,
                        self.back, self.forward, self.star]

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

