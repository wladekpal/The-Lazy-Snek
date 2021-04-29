import pygame
import os
from .blocks import Convex


class WallInteractionError(Exception):
    pass


class Wall(Convex):

    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/wall.png")
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


class Box(Convex):

    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/box.png")
        return pygame.image.load(texture_path)

    def check_move(self, direction) -> bool:
        field_in_direction = self.field.give_field_in_direction(direction)
        return field_in_direction.check_convex_move(direction)

    def move(self, direction):
        field_in_direction = self.field.give_field_in_direction(direction)
        self.field.convex_left(direction)
        field_in_direction.convex_entered(self, direction)

    def interact_with_snake(self, snake):
        if self.check_move(snake.direction):
            self.move(snake.direction)
        else:
            snake.destroy()

    def check_snake_move(self, snake) -> bool:
        field_in_direction = self.field.give_field_in_direction(snake.direction)
        return field_in_direction.check_convex_move(snake.direction)


class Skull(Convex):
    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/skull.png")
        return pygame.image.load(texture_path)

    def check_move(self, direction) -> bool:
        field_in_direction = self.field.give_field_in_direction(direction)
        return field_in_direction.check_convex_move(direction)

    def move(self, direction):
        field_in_direction = self.field.give_field_in_direction(direction)
        self.field.convex_left(direction)
        field_in_direction.convex_entered(self, direction)

    def interact_with_snake(self, snake):
        snake.destroy()
        self.destroy()

    def check_snake_move(self, snake) -> bool:
        return True


class Apple(Convex):
    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/apple.png")
        return pygame.image.load(texture_path)

    def check_move(self, direction) -> bool:
        field_in_direction = self.field.give_field_in_direction(direction)
        return field_in_direction.check_convex_move(direction)

    def move(self, direction):
        field_in_direction = self.field.give_field_in_direction(direction)
        self.field.convex_left(direction)
        field_in_direction.convex_entered(self, direction)

    def interact_with_snake(self, snake):
        self.destroy()

    def check_snake_move(self, snake) -> bool:
        snake.grow()
        return True


class InfinityTail(Convex):
    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/infinity_tail.png")
        return pygame.image.load(texture_path)

    def check_move(self, direction) -> bool:
        field_in_direction = self.field.give_field_in_direction(direction)
        return field_in_direction.check_convex_move(direction)

    def move(self, direction):
        field_in_direction = self.field.give_field_in_direction(direction)
        self.field.convex_left(direction)
        field_in_direction.convex_entered(self, direction)

    def interact_with_snake(self, snake):
        self.destroy()

    def check_snake_move(self, snake) -> bool:
        snake.enable_infinite_grow()
        return True


class Dye(Convex):
    def __init__(self, pane_index=None, color=None):
        self.color = color
        super().__init__(pane_index=pane_index)

    @staticmethod
    def texture(color):
        texture_path = os.path.join(os.path.dirname(__file__), f"../../assets/block/dye-{color}.png")
        return pygame.image.load(texture_path)

    def self_draw(self, frame, position, side_length):
        if self.displayed_side_length != side_length:
            self.displayed_side_length = side_length
            self.displayed_texture = pygame.transform.scale(self.texture(self.color), (side_length, side_length))
        frame.blit(self.displayed_texture, position)

    def check_move(self, direction) -> bool:
        field_in_direction = self.field.give_field_in_direction(direction)
        return field_in_direction.check_convex_move(direction)

    def move(self, direction):
        field_in_direction = self.field.give_field_in_direction(direction)
        self.field.convex_left(direction)
        field_in_direction.convex_entered(self, direction)

    def interact_with_snake(self, snake):
        self.destroy()

    def check_snake_move(self, snake) -> bool:
        snake.change_color(self.color)
        return True

    def copy(self):
        return type(self)(pane_index=self.pane_index, color=self.color)


class Timer(Convex):
    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/timer.png")
        return pygame.image.load(texture_path)

    def check_move(self, direction) -> bool:
        field_in_direction = self.field.give_field_in_direction(direction)
        return field_in_direction.check_convex_move(direction)

    def move(self, direction):
        field_in_direction = self.field.give_field_in_direction(direction)
        self.field.convex_left(direction)
        field_in_direction.convex_entered(self, direction)

    def interact_with_snake(self, snake):
        snake.wait(1)
        self.destroy()

    def check_snake_move(self, snake) -> bool:
        return True


class Key(Convex):
    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/key.png")
        return pygame.image.load(texture_path)

    def check_move(self, direction) -> bool:
        field_in_direction = self.field.give_field_in_direction(direction)
        return field_in_direction.check_convex_move(direction)

    def move(self, direction):
        field_in_direction = self.field.give_field_in_direction(direction)
        self.field.convex_left(direction)
        field_in_direction.convex_entered(self, direction)

    def interact_with_snake(self, snake):
        self.destroy()

    def check_snake_move(self, snake) -> bool:
        snake.get_key()
        return True


class DoorInteractionError(Exception):
    pass


class Door(Convex):
    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/block/door.png")
        return pygame.image.load(texture_path)

    def check_move(self, direction) -> bool:
        return False

    def move(self, direction):
        raise DoorInteractionError

    def interact_with_snake(self, snake):
        if snake.has_key:
            self.destroy()
        else:
            snake.destroy()

    def check_snake_move(self, direction) -> bool:
        return True
