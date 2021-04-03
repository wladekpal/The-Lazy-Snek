from abc import ABCMeta, abstractmethod
import pygame

class Block(metaclass=ABCMeta):
    def __init__(self):
        self.field = None
        self.is_alive = True
        self.displayed_texture = None
        self.displayed_side_length = None

    @staticmethod
    @abstractmethod
    def texture(self):
        pass

    @abstractmethod
    def interact_with_snake(self, snake):
        pass

    def self_draw(self, frame, x, y, side_length):
        if self.displayed_side_length != side_length:
            self.displayed_side_length = side_length
            self.displayed_texture = pygame.transform.scale(self.texture, (side_length, side_length)) 
        frame.blit(self.displayed_texture, (x, y))

    def set_field(self, field):
        self.field = field


class Flat(Block):
    def __init__(self):
        super().__init__()

    @staticmethod
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
        super().__init__()

    @staticmethod
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

    def self_draw(self, frame, x, y, side_length):
        if not self.is_alive:
            self.destroy()
            return
        super().self_draw(frame, x, y, side_length)

    def kill(self):
        self.is_alive = False

    def destroy(self):
        self.kill()
        self.field.remove_convex()


class WallInteractionError(Exception):
    pass


class Wall(Convex):
    def __init__(self):
        super().__init__()
    
    @property
    def texture(self):
        return pygame.image.load('../assets/wall.png')
    
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
    
