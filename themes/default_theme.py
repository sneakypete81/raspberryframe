import pygame
import theme

FOOTER_HEIGHT = 50
OVERLAY_ALPHA = 128

BUTTON_HEIGHT = 128
BUTTON_WIDTH = 128
BUTTON_OFFSET = 10

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
        self.star_pos = ((self.screen_width - BUTTON_WIDTH) / 2,
                         BUTTON_OFFSET)

        self.tag_pos = (50, self.screen_height - FOOTER_HEIGHT)
        self.tag_size = (self.screen_width-100, FOOTER_HEIGHT)
        self.tag_text_colour = pygame.Color("Black")
        self.tag_colour = (255, 255, 128, 168)
        self.tag_padding = 5
