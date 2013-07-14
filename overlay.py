import pygame
import sgc

class LayeredButton(sgc.Button):
    """
    Layered Button widget, to prevent click events from propagating
    through to the background frame
    """
    _layered = True

class Overlay:
    def __init__(self, theme):
        self.theme = theme
        self._is_active = False

        self.back = LayeredButton(widget=self, surf=theme.back_button,
                                  pos=theme.back_pos)
        self.forward = LayeredButton(widget=self, surf=theme.forward_button,
                                     pos=theme.forward_pos)
        self.star = LayeredButton(widget=self, surf=theme.unstarred_button,
                                  pos=theme.star_pos)
        self.widgets = [self.back, self.forward, self.star]

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

