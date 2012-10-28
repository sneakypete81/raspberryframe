#!/usr/bin/env python
import os
import sys
import pygame

DRIVERS = ['directfb', 'fbcon', 'svgalib']

def setup():
    if os.getenv('DISPLAY'):
        raise Exception("I'm running under X display = %s. Please run me from a bare console instead." % format(disp_no))

    found = False
    for driver in DRIVERS:
        os.putenv("SDL_VIDEODRIVER", driver)
        try:
            pygame.display.init()
        except pygame.error:
            print "Driver: %s failed." % driver
        else:
            found = True
            break

    if not found:
        raise Exception('No suitable video driver found!')

    pygame.mouse.set_visible(False)
    return pygame.display.set_mode(get_display_size(), pygame.FULLSCREEN)

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

screen = setup()

screen.fill(pygame.Color("BLACK"))
image = letterbox(pygame.image.load("/home/pi/Mt Cook.JPG"))
screen.blit(image, centre_offset(image))
pygame.display.update()
raw_input()

