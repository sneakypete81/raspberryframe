import pygame
import sgc

class LayeredButton(sgc.Button):
    """
    Layered Button widget, to prevent click events from propagating
    through to the background frame
    """
    _layered = True

class TagButton(LayeredButton):
    def __init__(self, widget, label, theme):
        LayeredButton.__init__(self, widget=widget, label=label,
                               label_col=theme.tag_text_colour)
        label_rect = self._settings["label"][1].rect
        label_size = (label_rect.width, label_rect.height)
        print label_size
        surf = pygame.Surface(label_size)
        surf.fill((255, 255, 128))
        # Blit label onto button
        for line in self._settings["label"][1:]:
            surf.blit(line.image, (0,0))
        self._create_base_images(surf)
        self._switch()

    def get_tag(self):
        return self._settings["label"][0]

class TagList(sgc.HBox):
    _layered = True

    def __init__(self, theme):
        self.buttons = []
        self.theme = theme
        sgc.HBox.__init__(self, theme.tag_size, pos=theme.tag_pos)

    def set_tags(self, tags):
        self.buttons = [TagButton(widget=self, label=tag, theme=self.theme)
                        for tag in tags]
        self.config(widgets=self.buttons)

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
