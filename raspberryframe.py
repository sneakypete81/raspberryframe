#!/usr/bin/env python
import os
import sys
import pygame

disp_no = os.getenv('DISPLAY')
if disp_no:
    print "I'm running under X display = %s. Please run me from a bare console instead." % format(disp_no)
    sys.exit(1)

drivers = ['directfb', 'fbcon', 'svgalib']

found = False
for driver in drivers:
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
    except pygame.error:
        print 'Driver: {0} failed.'.format(driver)
        continue
    found = True
    break

if not found:
   raise Exception('No suitable video driver found!')

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
