import pygame
from .gameplay.menu_view import MenuView
from .gameplay.view_controller import ViewController

# window dimensions
GAME_WINDOW_WIDTH = 1600
GAME_WINDOW_HEIGHT = 900

FPS = 24


def run_lazy_snek():
    pygame.init()
    running = True
    screen = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT), pygame.RESIZABLE)
    initial_view = MenuView(screen)
    controller = ViewController(screen, initial_view)
    while running:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        controller.handle_events()
        controller.refresh()
        pygame.display.update()