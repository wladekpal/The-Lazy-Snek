from abc import ABCMeta, abstractmethod
import pygame


class Block(metaclass=ABCMeta):
    def __init__(self, pane_index=None):
        self.field = None
        self.is_alive = True
        self.displayed_texture = None
        self.displayed_side_length = None
        self.pane_index = pane_index

    @staticmethod
    @abstractmethod
    def texture():
        pass

    @abstractmethod
    def interact_with_snake(self, snake):
        pass

    def self_draw(self, frame, position, side_length):
        if self.displayed_side_length != side_length:
            self.displayed_side_length = side_length
            self.displayed_texture = pygame.transform.scale(self.texture(), (side_length, side_length))
        frame.blit(self.displayed_texture, position)

    def set_field(self, field):
        self.field = field

    def copy(self):
        return type(self)(pane_index=self.pane_index)


class Flat(Block):

    @abstractmethod
    def interact_with_convex(self, convex):
        pass

    def check_snake_move(self, direction):
        return True

    def check_move(self, direction):
        return True


class Convex(Block):

    @abstractmethod
    def check_move(self, direction) -> bool:
        pass

    @abstractmethod
    def move(self, direction):
        pass

    @abstractmethod
    def check_snake_move(self) -> bool:
        pass

    def self_draw(self, frame, position, side_length):
        if not self.is_alive:
            self.destroy()
            return
        super().self_draw(frame, position, side_length)

    def kill(self):
        self.is_alive = False

    def destroy(self):
        self.kill()
        self.field.remove_convex()
