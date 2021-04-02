from abc import ABCMeta, abstractmethod
import pygame

class Block(metaclass=ABCMeta):
    def __init__(self):
        self.field = None
        self.is_alive = True

    @property
    @abstractmethod
    def texture(self):
        pass

    @abstractmethod
    def interact_with_snake(self, snake):
        pass

    def self_draw(self, frame, x, y):
        frame.blit(self.texture, (x, y))


class Flat(Block):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def texture(self):
        pass

    @abstractmethod
    def interact_with_snake(self, snake):
        pass

    @abstractmethod
    def interact_with_convex(self, convex, direction):
        pass


class Convex(Block):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def texture(self):
        pass

    @abstractmethod
    def interact_with_snake(self, snake):
        pass

    @abstractmethod
    def check_move(self, direction) -> bool:
        pass

    @abstractmethod
    def move(self, direction):
        pass

    @abstractmethod
    def check_snake_move(self) -> bool:
        pass

    def self_draw(self, frame, x, y):
        if not self.is_alive:
            self.destroy()
            return
        frame.blit(self.texture, (x, y))

    def kill(self):
        self.is_alive = False

    def destroy(self):
        self.kill()
        self.field.remove_convex()


class WallInteractionError(Exception):
    pass


class Wall(Convex):
    def __init__(self):
        pass
    
    @property
    def texture(self):
        return pygame.image.load('assets/wall.png')
    
    def check_move(self, direction) -> bool:
        return False

    def move(self, direction):
        raise WallInteractionError

    def interact_with_snake(self, snake):
        raise WallInteractionError

    def check_snake_move(self, direction) -> bool:
        return False
