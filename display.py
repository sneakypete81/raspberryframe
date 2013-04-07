import os
import logging
import pygame

logger = logging.getLogger("Raspberry Frame")

def init(width=None, height=None):
    screen = _setup(width, height)
    if not (width and height):
        width, height = _get_display_size()
    return screen, width, height

def _setup(width, height):
    if os.getenv('DISPLAY'):
        logger.info("X session found - using an X window for output")
        pygame.display.init()
        if width and height:
            screen = pygame.display.set_mode((width, height))
        else:
            screen = pygame.display.set_mode()
    else:
        _setup_framebuffer_driver()
        screen = pygame.display.set_mode(_get_display_size(), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)

    screen.fill(pygame.Color("BLACK"))
    pygame.display.update()
    return screen

def _setup_framebuffer_driver():
    found = False
    for driver in DRIVERS:
        os.putenv("SDL_VIDEODRIVER", driver)
        logger.debug("Trying to load %s..." % driver)
        try:
            pygame.display.init()
        except pygame.error as error:
            logger.debug("%s failed to load: %s" % (driver, str(error)))
        else:
            logger.info("%s successfully loaded" % driver)
            found = True
            break
    if not found:
        raise Exception('No suitable video driver found!')

def _get_display_size():
    display_info = pygame.display.Info()
    return display_info.current_w, display_info.current_h
