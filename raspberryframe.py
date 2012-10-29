#!/usr/bin/env python
import os
import sys
import time
import argparse
import pygame
import openphotoframe

DRIVERS = ['directfb', 'fbcon', 'svgalib']

class RaspberryFrame:
    def __init__(self):
        self.screen = self._setup()
        self.width, self.height = self._get_display_size()

    def _setup(self):
        if os.getenv('DISPLAY'):
            raise Exception("I'm running under X. Please run me from a bare console instead.")

        found = False
        for driver in DRIVERS:
            os.putenv("SDL_VIDEODRIVER", driver)
            print "Trying %s..." % driver
            try:
                pygame.display.init()
            except pygame.error:
                print "Driver: %s failed." % driver
            else:
                print "Driver %s successfully loaded" % driver
                found = True
                break
        if not found:
            raise Exception('No suitable video driver found!')
    
        pygame.mouse.set_visible(False)
        size = self._get_display_size()
        print "Resolution: %dx%d" % size
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        screen.fill(pygame.Color("BLACK"))
        pygame.display.update()
        return screen

    @staticmethod
    def _get_display_size():
        display_info = pygame.display.Info()
        return display_info.current_w, display_info.current_h

    def letterbox(self, image):
        width, height = image.get_size()

        # First try to scale to the screen width
        scale_factor = 1.0 * width / self.width
        # If it's still too high, scale to the screen height
        if int(height / scale_factor) > self.height:
            scale_factor = 1.0 * height / self.height

        return pygame.transform.scale(image, (int(width / scale_factor), 
                                              int(height / scale_factor)))

    def centre_offset(self, image):
        width, height = image.get_size()
        return ((self.width / 2 - width / 2), (self.height / 2 - height / 2))

    def show_image(self, image_file):
        image = pygame.image.load(image_file)
        # image = pygame.image.load("/home/pi/Mt Cook.JPG")
        image.convert()
        image = self.letterbox(image)
        self.screen.fill(pygame.Color("BLACK"))
        self.screen.blit(image, self.centre_offset(image))
        pygame.display.update()

############################################################

def run(slide_seconds):
    frame = RaspberryFrame()
    opf = openphotoframe.OpenPhotoFrame(frame.width, frame.height)
    while True:
        frame.show_image(opf.random_image())
        time.sleep(slide_seconds)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plays an OpenPhoto slideshow on a framebuffer.")
    parser.add_argument("-t", "--slide_seconds", type=int, default=5, 
                        help="Delay between slides, in seconds (default:5)")
    options = parser.parse_args()

    run(options.slide_seconds)


