from abc import ABCMeta, abstractmethod
import pygame
import enum


class EditorTool(enum.Enum):
    ADD_BLOCK = 1
    ERASE = 2
    SNAKE_CREATOR = 3
    SNAKE_CHANGE_COLOR = 4
    SNAKE_ROTATE_HEAD = 5
    TELEPORT_LINKER = 6
    ADD_TO_LEVEL = 7


class EditorFrame(metaclass=ABCMeta):

    def __init__(self, screen, details):
        self.resize(screen, details)

    def resize(self, screen, details):
        position, dimensions = details
        self.position = position
        self.width, self.height = dimensions
        x, y = self.position
        self.surface = screen.subsurface(pygame.Rect(x, y, self.width, self.height))

    def pos_in_frame_area(self, pos):
        x, y = pos
        self_x, self_y = self.position
        return self_x <= x <= self_x + self.width and self_y <= y <= self_y + self.height

    def get_relative_pos(self, screen_pos):
        pos_x, pos_y = screen_pos
        self_x, self_y = self.position
        return (pos_x - self_x, pos_y - self_y)

    @abstractmethod
    def handle_click(self, pos, active_tool, active_id, editor_container):
        pass

    @abstractmethod
    def refresh(self):
        pass
