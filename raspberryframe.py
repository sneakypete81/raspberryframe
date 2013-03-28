#!/usr/bin/env python
import os
import sys
import time
import argparse
import pygame
import gobject
import openphotoframe

CACHE_PATH = os.path.expanduser("~/.raspberryframe_cache")
CACHE_SIZE_MB = 1024 # Limit cache to 1GB

DRIVERS = ['directfb', 'fbcon', 'svgalib']

class RaspberryFrame:
    def __init__(self, width=None, height=None, crop_threshold=10):
        self.screen = self._setup(width, height)
        if width and height:
            self.width, self.height = width, height
        else:
            self.width, self.height = self._get_display_size()
        self.crop_threshold = crop_threshold

    def _setup(self, width, height):
        if os.getenv('DISPLAY'):
            pygame.display.init()
            if width and height:
                screen = pygame.display.set_mode((width, height))
            else:
                screen = pygame.display.set_mode()
        else:
            self._setup_framebuffer_driver()
            screen = pygame.display.set_mode(self._get_display_size(), pygame.FULLSCREEN)

        screen.fill(pygame.Color("BLACK"))
        pygame.mouse.set_visible(False)
        pygame.display.update()
        return screen

    @staticmethod
    def _setup_framebuffer_driver():
        found = False
        for driver in DRIVERS:
            os.putenv("SDL_VIDEODRIVER", driver)
            print "Trying %s..." % driver
            try:
                pygame.display.init()
            except pygame.error as error:
                print "Driver: %s failed: %s" % (driver, str(error))
            else:
                print "Driver %s successfully loaded" % driver
                found = True
                break
        if not found:
            raise Exception('No suitable video driver found!')

    @staticmethod
    def _get_display_size():
        display_info = pygame.display.Info()
        return display_info.current_w, display_info.current_h

    def letterbox(self, image):
        width, height = image.get_size()

        width_scale_factor = 1.0 * width / self.width
        height_scale_factor = 1.0 * height / self.height

        # Use the largest scale factor, to prevent cropping
        scale_factor = max(width_scale_factor, height_scale_factor)

        # If the difference in aspect ratios is less than aspect_error,
        # crop the image instead of letterboxing
        aspect_error = abs((width_scale_factor - height_scale_factor) /
                           max(width_scale_factor, height_scale_factor))
        if aspect_error <= self.crop_threshold / 100.0:
            scale_factor = min(width_scale_factor, height_scale_factor)

        new_width = int(width / scale_factor)
        new_height = int(height / scale_factor)

        return pygame.transform.scale(image, (int(width / scale_factor), 
                                              int(height / scale_factor)))

    def centre_offset(self, image):
        width, height = image.get_size()
        return ((self.width / 2 - width / 2), (self.height / 2 - height / 2))

    def show_image(self, image_file):
        image = pygame.image.load(image_file)
        image.convert()
        image = self.letterbox(image)
        self.screen.fill(pygame.Color("BLACK"))
        self.screen.blit(image, self.centre_offset(image))
        pygame.display.update(pygame.Rect(0, 0, self.width, self.height))

############################################################

class Main:
    def __init__(self, slide_seconds, width=None, height=None, crop_threshold=10):
        self.frame = RaspberryFrame(width, height, crop_threshold)
        self.opf = openphotoframe.OpenPhotoFrame(self.frame.width, self.frame.height, CACHE_PATH, CACHE_SIZE_MB)
        self.clock = pygame.time.Clock()
        self.slide_seconds = slide_seconds
        self.timer = None

    def run(self):
        gobject.idle_add(self.pygame_loop_cb)
        self.slideshow_next_cb()
        gobject.MainLoop().run()

    def slideshow_next_cb(self):
        self.frame.show_image(self.opf.random_image())
        self.timer = gobject.timeout_add(self.slide_seconds*1000, self.slideshow_next_cb)
        return False

    def pygame_loop_cb(self):
        self.clock.tick(2)
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
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plays an OpenPhoto slideshow to a framebuffer.")
    parser.add_argument("-t", "--slide_seconds", type=int, default=5,
                        help="Delay between slides in seconds (default:5)")
    parser.add_argument("-s", "--size", default=None,
                        help="Target image size (default:screen resolution)")
    parser.add_argument("-c", "--crop_threshold", type=int, default=10,
                        help="Crop the image if the image/screen aspect ratios are within this percentage")
    options = parser.parse_args()

    width = None
    height = None
    if options.size:
        try:
            width, height = options.size.split("x")
            width, height = int(width), int(height)
        except ValueError:
            parser.error("Please specify image size as 'widthxheight'\n(eg: -r 1920x1080)")

    Main(slide_seconds=options.slide_seconds,
        width=width, height=height,
        crop_threshold=options.crop_threshold).run()


