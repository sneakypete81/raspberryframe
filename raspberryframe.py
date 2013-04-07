#!/usr/bin/env python
import os
import sys
import time
import argparse
import logging
import pygame
import gobject
import sgc

import display
from providers import openphoto_provider

CACHE_PATH = os.path.expanduser("~/.raspberryframe_cache")
CACHE_SIZE_MB = 1024 # Limit cache to 1GB

logger = logging.getLogger("Raspberry Frame")
logger.addHandler(logging.StreamHandler())

class RaspberryFrame:
    def __init__(self, screen, width, height, crop_threshold=10):
        self.screen = screen
        self.width = width
        self.height = height
        self.crop_threshold = crop_threshold
        self.photo = None

    def show_photo(self, photo_file):
        logger.debug("Loading photo...")
        photo = pygame.image.load(photo_file)
        photo.convert()
        self.photo = self._letterbox(photo)
        self.paint()

    def paint(self):
        logger.debug("Painting photo...")
        self.screen.fill(pygame.Color("BLACK"))
        if self.photo:
            self.screen.blit(self.photo, self._centre_offset(self.photo))

    def _letterbox(self, photo):
        width, height = photo.get_size()

        width_scale_factor = 1.0 * width / self.width
        height_scale_factor = 1.0 * height / self.height

        # Use the largest scale factor, to prevent cropping
        scale_factor = max(width_scale_factor, height_scale_factor)

        # If the difference in aspect ratios is less than aspect_error,
        # crop the photo instead of letterboxing
        aspect_error = abs((width_scale_factor - height_scale_factor) /
                           max(width_scale_factor, height_scale_factor))
        if aspect_error <= self.crop_threshold / 100.0:
            scale_factor = min(width_scale_factor, height_scale_factor)

        new_width = int(width / scale_factor)
        new_height = int(height / scale_factor)

        return pygame.transform.scale(photo, (int(width / scale_factor),
                                              int(height / scale_factor)))

    def _centre_offset(self, photo):
        width, height = photo.get_size()
        return ((self.width / 2 - width / 2), (self.height / 2 - height / 2))

class Overlay:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._is_active = False

        self.left = sgc.Button(label="<", pos=(10, height/2-10))
        self.right = sgc.Button(label=">", pos=(width-120, height/2-10))
        self.star = sgc.Button(label="*", pos=(width/2-10, 10))
        self.widgets = [self.left, self.right, self.star]

    def add(self):
        logger.debug("Add overlay")
        self._is_active = True
        for widget in self.widgets:
            widget.add()

    def remove(self):
        logger.debug("Remove overlay")
        self._is_active = False
        for widget in self.widgets:
            widget.remove(fade=False)

    def active(self):
        return self._is_active

############################################################

class Main:
    def __init__(self, slide_seconds, width=None, height=None, crop_threshold=10, swap_axes=False):
        self.screen, self.width, self.height = display.init(width, height)

        self.frame = RaspberryFrame(self.screen, self.width, self.height, crop_threshold)
        self.overlay = Overlay(self.width, self.height)
        self.provider = openphoto_provider.OpenPhoto(self.width, self.height, CACHE_PATH, CACHE_SIZE_MB)

        self.clock = pygame.time.Clock()
        self.slide_seconds = slide_seconds
        self.swap_axes = swap_axes
        self.timer = None

    def run(self):
        gobject.idle_add(self.pygame_loop_cb)
        self.slideshow_next_cb()
        gobject.MainLoop().run()

    def slideshow_next_cb(self):
        self.frame.show_photo(self.provider.random_photo())
        self.timer = gobject.timeout_add(self.slide_seconds*1000, self.slideshow_next_cb)
        return False

    def pygame_loop_cb(self):
        time = self.clock.tick(30)
        sgc.update(time)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key < pygame.K_a or event.key > pygame.K_z:
                    continue
                if self.timer is not None:
                    gobject.source_remove(self.timer)
                self.slideshow_next_cb()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.overlay.active():
                    self.overlay.remove()
                    self.frame.paint()
                else:
                    self.overlay.add()

                pos = event.pos
                if self.swap_axes:
                    pos = (pos[1]*self.width/self.height,
                           pos[0]*self.height/self.width)
                print pos
        return True



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plays an OpenPhoto slideshow to a framebuffer.")
    parser.add_argument("-t", "--slide_seconds", type=int, default=5,
                        help="Delay between slides in seconds (default:5)")
    parser.add_argument("-s", "--size", default=None,
                        help="Target photo size (default:screen resolution)")
    parser.add_argument("-x", "--swap_axes", action="store_true",
                        help="Swap the x/y axes of the touchscreen")
    parser.add_argument("-c", "--crop_threshold", type=int, default=10,
                        help="Crop the photo if the photo/screen aspect ratios are within this percentage")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Print additional debug information")
    options = parser.parse_args()

    if options.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    width = None
    height = None
    if options.size:
        try:
            width, height = options.size.split("x")
            width, height = int(width), int(height)
        except ValueError:
            parser.error("Please specify photo size as 'widthxheight'\n(eg: -r 1920x1080)")

    Main(slide_seconds=options.slide_seconds,
         width=width, height=height,
         crop_threshold=options.crop_threshold,
         swap_axes=options.swap_axes).run()


