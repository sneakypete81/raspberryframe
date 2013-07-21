import pygame
import theme

FOOTER_HEIGHT = 100
OVERLAY_ALPHA = 128

BUTTON_HEIGHT = 128
BUTTON_WIDTH = 128
BUTTON_OFFSET = 10
BUTTON_SPACING = 50

class Default(theme.Theme):
    def __init__(self, *args, **kwds):
        theme.Theme.__init__(self, *args, **kwds)

        self.back_button = dict(image="themes/default/arrow-left.png",
                                over="themes/default/arrow-left.png",
                                down="themes/default/arrow-left-glow.png")
        self.back_pos = (BUTTON_OFFSET,
                         (self.screen_height - BUTTON_HEIGHT) / 2)

        self.forward_button = dict(image="themes/default/arrow-right.png",
                                   over="themes/default/arrow-right.png",
                                   down="themes/default/arrow-right-glow.png")
        self.forward_pos = (self.screen_width - BUTTON_WIDTH - BUTTON_OFFSET,
                            (self.screen_height - BUTTON_HEIGHT) / 2)

        self.unstarred_button = dict(image="themes/default/star-outline.png",
                                     over="themes/default/star-outline.png",
                                     down="themes/default/star-outline-glow.png")
        self.starred_button = dict(image="themes/default/star-fill.png",
                                   over="themes/default/star-fill.png",
                                   down="themes/default/star-fill-glow.png")
        self.star_pos = ((self.screen_width - BUTTON_WIDTH*2 - BUTTON_SPACING) / 2,
                         BUTTON_OFFSET)

        self.unremoved_button = dict(image="themes/default/remove-outline.png",
                                     over="themes/default/remove-outline.png",
                                     down="themes/default/remove-outline-glow.png")
        self.removed_button = dict(image="themes/default/remove-fill.png",
                                   over="themes/default/remove-fill.png",
                                   down="themes/default/remove-fill-glow.png")
        self.remove_pos = ((self.screen_width + BUTTON_SPACING) / 2,
                         BUTTON_OFFSET)

        self.footer_colour = (0, 0, 0, 128)
        self.footer_pos = (0, self.screen_height - FOOTER_HEIGHT)
        self.footer_size = (self.screen_width, FOOTER_HEIGHT)
        self.footer_border = 20

        self.tag_text_colour = pygame.Color("Black")
        self.tag_colour = (255, 255, 128)
        self.tag_border = 0
        self.tag_padding = 5
