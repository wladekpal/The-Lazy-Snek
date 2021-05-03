import pygame
import os
from .blocks import Flat


class TurnLeft(Flat):

    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/turn-left.png")
        return pygame.image.load(texture_path)

    def interact_with_snake(self, snake):
        snake.direction.turn_left()

    def interact_with_convex(self, convex):
        pass


class TurnRight(Flat):

    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/turn-right.png")
        return pygame.image.load(texture_path)

    def interact_with_snake(self, snake):
        snake.direction.turn_right()

    def interact_with_convex(self, convex):
        pass


class Spikes(Flat):
    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/spikes.png")
        return pygame.image.load(texture_path)

    def interact_with_snake(self, snake):
        snake.destroy()

    def interact_with_convex(self, convex):
        pass


class Reverse(Flat):

    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/reverse.png")
        return pygame.image.load(texture_path)

    def interact_with_snake(self, snake):
        snake.reverse()

    def interact_with_convex(self, convex):
        pass


class Finish(Flat):

    def __init__(self, pane_index=None, color=None):
        self.color = color
        super().__init__(pane_index=pane_index)

    @staticmethod
    def texture(color):
        if color is None:
            texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/finish.png")
        else:
            texture_path = os.path.join(os.path.dirname(__file__), f"../../assets/block/finish-{color}.png")
        return pygame.image.load(texture_path)

    def self_draw(self, frame, position, side_length):
        if self.displayed_side_length != side_length:
            self.displayed_side_length = side_length
            self.displayed_texture = pygame.transform.scale(self.texture(self.color), (side_length, side_length))
        frame.blit(self.displayed_texture, position)

    def interact_with_convex(self, convex):
        pass

    def interact_with_snake(self, snake):
        if self.color is None or self.color == snake.color:
            snake.finish()

    def copy(self):
        return type(self)(pane_index=self.pane_index, color=self.color)


class VeniceBlock(Flat):
    def __init__(self, pane_index=None, direction=None):
        self.direction = direction
        super().__init__(pane_index=pane_index)

    def texture(self):
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/venice_block.png")
        unoriented_texture = pygame.image.load(texture_path)
        if str(self.direction) == 'E':
            return pygame.transform.rotate(unoriented_texture, -90)
        elif str(self.direction) == 'S':
            return pygame.transform.rotate(unoriented_texture, -180)
        elif str(self.direction) == 'W':
            return pygame.transform.rotate(unoriented_texture, -270)
        else:
            return unoriented_texture

    def interact_with_snake(self, snake):
        pass

    def interact_with_convex(self, convex):
        pass

    def check_move(self, direction):
        return direction == self.direction

    def check_snake_move(self, snake):
        return snake.direction == self.direction

    def copy(self):
        return type(self)(pane_index=self.pane_index, direction=self.direction)
