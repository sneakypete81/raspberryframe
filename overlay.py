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

class Footer(sgc.VBox):
    _layered = True
    def __init__(self, theme):
        self.tags = []
        self.theme = theme
        self.description = sgc.Label(font=sgc.Font["title"])
        self.tag_list = sgc.HBox(theme.footer_size, border=theme.tag_border,
                                 spacing=theme.tag_padding)

        sgc.VBox.__init__(self, theme.footer_size, pos=theme.footer_pos,
                          col=theme.footer_colour, border=theme.footer_border,
                          widgets=[self.description, self.tag_list])

    def set_description(self, description):
        self.description.text = description

    def set_tags(self, tags):
        self.tags = [Tag(text=tag, theme=self.theme)
                     for tag in tags]
        self.tag_list.config(widgets=self.tags)
        self.config()

class Overlay:
    def __init__(self, theme):
        self.theme = theme
        self._is_active = False

        self.back_button = LayeredButton(widget=self, surf=theme.back_button,
                                         pos=theme.back_pos)
        self.forward_button = LayeredButton(widget=self, surf=theme.forward_button,
                                            pos=theme.forward_pos)
        self.star_button = LayeredButton(widget=self, surf=theme.unstarred_button,
                                         pos=theme.star_pos)
        self.remove_button = LayeredButton(widget=self, surf=theme.unremoved_button,
                                           pos=theme.remove_pos)
        self.footer = Footer(theme)

        self.widgets = [self.back_button, self.forward_button,
                        self.star_button, self.remove_button,
                        self.footer]

    def add(self, fade=False):
        self._is_active = True
        for widget in self.widgets:
            widget.add(fade=fade)

    def remove(self, fade=False):
        self._is_active = False
        for widget in self.widgets:
            widget.remove(fade=fade)

    def active(self):
        return self._is_active

    def set_star(self, value=True):
        if value:
            self.star_button._create_base_images(self.theme.starred_button)
        else:
            self.star_button._create_base_images(self.theme.unstarred_button)
        self.star_button._switch()

    def set_remove(self, value=True):
        if value:
            self.remove_button._create_base_images(self.theme.removed_button)
        else:
            self.remove_button._create_base_images(self.theme.unremoved_button)
        self.remove_button._switch()

    def set_description(self, description):
        self.footer.set_description(description)

    def set_tags(self, tags):
        self.footer.set_tags(tags)
