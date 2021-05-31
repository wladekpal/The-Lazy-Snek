from abc import ABCMeta, abstractmethod
import pygame
import enum
import sys


class ViewInitAction(enum.Enum):
    PUSH = 1
    REPLACE = 2
    POP = 3
    EMPTY_STACK = 4


class ApplicationView(metaclass=ABCMeta):

    def __init__(self, screen):
        self.screen = screen

    @abstractmethod
    def handle_pygame_event(self, event):
        pass

    @abstractmethod
    def refresh(self):
        pass

    def restore(self):
        self.refresh()


class ViewController():

    def __init__(self, screen, initial_view):
        self.screen = screen
        self.current_view = initial_view
        self.stack = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            else:
                new_view_details = self.current_view.handle_pygame_event(event)
                if new_view_details:
                    new_view, action_type = new_view_details
                    if action_type == ViewInitAction.PUSH:
                        self.stack.append(self.current_view)
                        self.current_view = new_view
                    elif action_type == ViewInitAction.POP:
                        self.current_view = self.stack.pop()
                        self.current_view.restore()
                    elif action_type == ViewInitAction.REPLACE:
                        self.current_view = new_view
                    elif action_type == ViewInitAction.EMPTY_STACK:
                        self.stack = []
                        self.current_view = new_view
                    else:
                        raise ValueError

    def refresh(self):
        self.current_view.refresh()
