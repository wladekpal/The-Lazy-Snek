from abc import ABCMeta, abstractmethod
import pygame
import os


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


class Flat(Block):

    @abstractmethod
    def interact_with_convex(self, convex):
        pass


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


class WallInteractionError(Exception):
    pass


class Wall(Convex):

    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/wall.png")
        return pygame.image.load(texture_path)

    def check_move(self, direction) -> bool:
        return False

    def move(self, direction):
        raise WallInteractionError

    def interact_with_snake(self, snake):
        raise WallInteractionError

    def check_snake_move(self, direction) -> bool:
        return False

    def kill(self):
        raise WallInteractionError

    def destroy(self):
        raise WallInteractionError


class TurnLeft(Flat):

    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/turn_left.png")
        return pygame.image.load(texture_path)

    def interact_with_snake(self, snake):
        snake.direction.turn_left()

    def interact_with_convex(self, convex):
        pass


class TurnRight(Flat):

    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/turn_right.png")
        return pygame.image.load(texture_path)

    def interact_with_snake(self, snake):
        snake.direction.turn_right()

    def interact_with_convex(self, convex):
        pass
