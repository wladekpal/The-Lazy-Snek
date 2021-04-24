from abc import ABCMeta, abstractmethod
import pygame


class ApplicationView(metaclass=ABCMeta):

    def __init__(self, screen):
        self.screen = screen

    @abstractmethod
    def handle_pygame_event(self, event):
        pass

    @abstractmethod
    def refresh(self):
        pass


class ViewController():

    def __init__(self, screen, initial_view):
        self.screen = screen
        self.current_view = initial_view

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            else:
                view = self.current_view.handle_pygame_event(event)
                if view:
                    self.current_view = view

    def refresh(self):
        self.current_view.refresh()
