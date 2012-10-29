#!/usr/bin/env python
import os
import sys
import time
import pygame
import openphotoframe

DRIVERS = ['directfb', 'fbcon', 'svgalib']

def setup():
    if os.getenv('DISPLAY'):
        raise Exception("I'm running under X display = %s. Please run me from a bare console instead." % format(disp_no))

    found = False
    for driver in DRIVERS:
        os.putenv("SDL_VIDEODRIVER", driver)
        print "Trying %s..." % driver
        try:
            pygame.display.init()
        except pygame.error:
            print "Driver: %s failed." % driver
        else:
            found = True
            print "Driver %s successfully initialised" % driver
            break

    if not found:
        raise Exception('No suitable video driver found!')
    
    pygame.mouse.set_visible(False)
    size = get_display_size()
    print "Resolution: %dx%d" % size
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    screen.fill(pygame.Color("BLACK"))
    pygame.display.update()
    return screen

def letterbox(image):
    width, height = image.get_size()
    screen_width, screen_height = get_display_size()

    # First try to scale to the screen width
    scale_factor = 1.0 * width / screen_width
    # If it's still too high, scale to the screen height
    if int(height / scale_factor) > screen_height:
        scale_factor = 1.0 * height / screen_height

    return pygame.transform.scale(image, (int(width / scale_factor), 
                                          int(height / scale_factor)))

def get_display_size():
    display_info = pygame.display.Info()
    return display_info.current_w, display_info.current_h

def centre_offset(image):
    width, height = image.get_size()
    screen_width, screen_height = get_display_size()
    return ((screen_width / 2 - width / 2), (screen_height / 2 - height / 2))

def show_image(screen, image_file):
    image = pygame.image.load(image_file)
    # image = pygame.image.load("/home/pi/Mt Cook.JPG")
    image.convert()
    image = letterbox(image)
    screen.blit(image, centre_offset(image))
    pygame.display.update()

############################################################

def run():
    screen = setup()
    opp = openphotoframe.OpenPhotoFrame(*get_display_size())
    while True:
        show_image(screen, opp.random_image())
        time.sleep(5)

if __name__ == "__main__":
    run()


