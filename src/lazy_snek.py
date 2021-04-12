import pygame
from engine.level import Level
from gameplay.level_view import LevelView
import os

# window dimensions
GAME_WINDOW_WIDTH = 1600
GAME_WINDOW_HEIGHT = 900

FPS = 40
FRAMES_PER_SIMULATION_TICK = 10

# example levels
EXAMPLE_LEVEL_PATH = os.path.join(os.path.dirname(__file__), "../assets/example2.json")


def handle_events(displayed_view):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            displayed_view.handle_click(event.pos)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            displayed_view.handle_unclick(event.pos)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            displayed_view.handle_leftclick(event.pos)
        if event.type == pygame.MOUSEMOTION:
            displayed_view.handle_motion(event.pos)


if __name__ == "__main__":
    pygame.init()
    running = True
    screen = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
    displayed_view = LevelView(screen, Level(EXAMPLE_LEVEL_PATH), FRAMES_PER_SIMULATION_TICK)
    while running:
        handle_events(displayed_view)
        clock = pygame.time.Clock()
        clock.tick(FPS)
        displayed_view.refresh()
        pygame.display.update()
