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


class Box(Convex):

    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/box.png")
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


class Spikes(Flat):
    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/spikes.png")
        return pygame.image.load(texture_path)

    def interact_with_snake(self, snake):
        snake.destroy()

    def interact_with_convex(self, convex):
        pass


class Skull(Convex):
    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/skull.png")
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
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/apple.png")
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
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/infinity_tail.png")
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


class Reverse(Flat):

    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/reverse.png")
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
            texture_path = os.path.join(os.path.dirname(__file__), "../../assets/finish.png")
        else:
            texture_path = os.path.join(os.path.dirname(__file__), f"../../assets/finish-{color}.png")
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


class Dye(Convex):
    def __init__(self, pane_index=None, color=None):
        self.color = color
        super().__init__(pane_index=pane_index)

    @staticmethod
    def texture(color):
        texture_path = os.path.join(os.path.dirname(__file__), f"../../assets/dye-{color}.png")
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


class VeniceBlock(Flat):
    def __init__(self, pane_index=None, direction=None):
        self.direction = direction
        super().__init__(pane_index=pane_index)

    def texture(self):
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/venice_block.png")
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


class Timer(Convex):
    @staticmethod
    def texture():
        texture_path = os.path.join(os.path.dirname(__file__), "../../assets/timer.png")
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
        snake.wait(1)
        return True
