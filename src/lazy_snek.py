import pygame
from engine.blocks import Wall
from engine.field import Field
from engine.board import Board
from engine.level import Level
from gameplay.level_screen import LevelView
import os, sys

# window dimensions
GAME_WINDOW_WIDTH = 1600
GAME_WINDOW_HEIGHT = 900

FPS = 15
FRAMES_PER_SIMULATION_TICK = 7

# example levels
EXAMPLE_LEVEL_PATH = os.path.join(os.path.dirname(__file__), "../assets/data.json")


def handle_events(levelView):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            levelView.handle_click()


if __name__ == "__main__":
    pygame.init()
    running = True
    screen = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
    levelView = LevelView(screen, Level(EXAMPLE_LEVEL_PATH), FRAMES_PER_SIMULATION_TICK)
    while running:
        handle_events(levelView)
        clock = pygame.time.Clock()
        clock.tick(FPS)
        levelView.refresh()
        pygame.display.update()
