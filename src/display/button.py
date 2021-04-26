import pygame
from abc import ABCMeta, abstractmethod
from .simulation import SimulationState


class Button(metaclass=ABCMeta):

    def __init__(self, simulation, texture):
        self.simulation = simulation
        self.texture = texture
        self.displayed_side_length = None
        self.displayed_texture = None

    @abstractmethod
    def action_when_clicked(self):
        pass

    def process_mouse_click(self, mouse_position):
        x, y = self.position
        x_fits = x <= mouse_position[0] <= x + self.displayed_side_length
        y_fits = y <= mouse_position[1] <= y + self.displayed_side_length
        if x_fits and y_fits:
            self.action_when_clicked()

    def self_draw(self, frame, position, side_length):
        self.position = position
        if self.displayed_side_length != side_length or self.displayed_side_length is None:
            self.displayed_side_length = side_length
            self.displayed_texture = pygame.transform.scale(self.texture, (side_length, side_length))
        frame.blit(self.displayed_texture, position)

    def replace_texture(self, texture):
        self.texture = texture
        self.displayed_side_length = None


class RestartButton(Button):

    def action_when_clicked(self):
        self.simulation.restart()


class PlayButton(Button):

    def __init__(self, simulation, texture, secondary_texture):
        super().__init__(simulation, texture)
        self.primary_texture = texture
        self.secondary_texture = secondary_texture

    def self_draw(self, frame, position, side_length):
        if self.simulation.get_state() == SimulationState.RUNNING:
            self.texture = self.secondary_texture
            self.displayed_side_length = None
        else:
            self.texture = self.primary_texture
            self.displayed_side_length = None
        super().self_draw(frame, position, side_length)

    def action_when_clicked(self):
        self.simulation.play()


class CancelButton(Button):

    def action_when_clicked(self):
        self.simulation.cancel()


class StepByStepButton(Button):

    def __init__(self, simulation, texture, secondary_texture):
        super().__init__(simulation, texture)
        self.primary_texture = texture
        self.secondary_texture = secondary_texture

    def self_draw(self, frame, position, side_length):
        if self.simulation.get_state() == SimulationState.RUNNING:
            self.texture = self.secondary_texture
            self.displayed_side_length = None
        else:
            self.texture = self.primary_texture
            self.displayed_side_length = None
        super().self_draw(frame, position, side_length)

    def action_when_clicked(self):
        if self.simulation.get_state() == SimulationState.PAUSED \
                or self.simulation.get_state() == SimulationState.INACTIVE:
            self.simulation.stepbystep()
