import pygame
import sgc

class LayeredButton(sgc.Button):
    """
    Layered Button widget, to prevent click events from propagating
    through to the background frame
    """
    _layered = True

class Tag(sgc.HBox):
    def __init__(self, text, theme):
        self.label = sgc.Label(text=text, col=theme.tag_text_colour)
        height = self.label.rect.h

        surf = pygame.Surface((height/2, height), flags=pygame.SRCALPHA)
        pygame.draw.circle(surf, theme.tag_colour, (height/2, height/2), height/2)
        left = sgc.Simple(surf)

        surf = pygame.Surface((height/2, height), flags=pygame.SRCALPHA)
        pygame.draw.circle(surf, theme.tag_colour, (0, height/2), height/2)
        right = sgc.Simple(surf)

        coloured_label = sgc.HBox(widgets=[self.label], col=theme.tag_colour,
                                  border=0, spacing=0)

        sgc.HBox.__init__(self, widgets=[left, coloured_label, right],
                          border=0, spacing=0)

    def get_tag(self):
        return self.label.text

class TagList(sgc.HBox):
    _layered = True
    def __init__(self, theme):
        self.tags = []
        self.theme = theme
        sgc.HBox.__init__(self, theme.tag_size, pos=theme.tag_pos,
                          col=theme.tag_bg_colour,
                          border=theme.tag_border,
                          spacing=theme.tag_padding)

    def set_tags(self, tags):
        self.tags = [Tag(text=tag, theme=self.theme)
                     for tag in tags]
        self.config(widgets=self.tags)

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
        self.tag_list = TagList(theme)

        self.widgets = [self.back, self.forward, self.star, self.tag_list]

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

    def set_tags(self, tags):
        self.tag_list.set_tags(tags)
