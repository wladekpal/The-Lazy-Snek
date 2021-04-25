import pygame
import os
from .blocks import Flat, Convex
from .snake import SnakeState


class Field:

    def __init__(self):
        self.coordinates = None
        self.board = None
        self.flat_layer = None
        self.convex_layer = None
        self.snake_layer = None
        self.texture = pygame.image.load(os.path.join(os.path.dirname(__file__), "../../assets/field.png"))

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    # orientation
    def give_field_in_direction(self, direction):
        coordinates = direction.move_in_direction(self.coordinates)
        return self.board.request_field(coordinates)

    # board
    def set_board(self, board):
        self.board = board

    # snake
    def check_snake_move(self, snake) -> bool:
        flat_permission = True
        convex_permission = True
        if self.flat_layer is not None:
            flat_permission = self.flat_layer.check_snake_move(snake)
        if self.convex_layer is not None:
            convex_permission = self.convex_layer.check_snake_move(snake)

        return flat_permission and convex_permission

    def snake_entered(self, snake):
        if self.snake_layer is not None:
            self.snake_layer.interact_with_snake(snake)
        elif self.convex_layer is not None:
            self.convex_layer.interact_with_snake(snake)

        if self.snake_layer is None and self.flat_layer is not None:
            self.flat_layer.interact_with_snake(snake)

        if snake.state == SnakeState.ALIVE:
            self.snake_layer = snake

    def snake_left(self):
        self.snake_layer = None

    def remove_snake(self, snake):
        if self.snake_layer == snake:
            self.snake_layer = None

    def place_snake(self, snake):
        self.snake_layer = snake

    # flat
    def remove_flat(self):
        self.flat_layer = None

    def place_flat(self, flat):
        self.flat_layer = flat
        self.flat_layer.set_field(self)

    # convex
    def check_convex_move(self, direction) -> bool:
        flat_permission = True
        convex_permission = True
        if self.flat_layer is not None:
            flat_permission = self.flat_layer.check_move(direction)
        if self.convex_layer is not None:
            convex_permission = self.convex_layer.check_move(direction)

        return flat_permission and convex_permission

    def convex_entered(self, convex, direction):
        if self.snake_layer is not None:
            self.snake_layer.interact_with_convex(convex)
        elif self.convex_layer is not None:
            self.convex_layer.move(direction)

        if self.flat_layer is not None:
            self.flat_layer.interact_with_convex(convex)

        self.convex_layer = convex
        self.convex_layer.set_field(self)

    def convex_left(self, direction):
        self.convex_layer = None

    def remove_convex(self):
        self.convex_layer = None

    def place_convex(self, convex):
        self.convex_layer = convex
        self.convex_layer.set_field(self)

    # display
    def self_draw(self, frame, draw_coords, side_length):
        displayed_texture = pygame.transform.scale(self.texture, (side_length, side_length))
        frame.blit(displayed_texture, draw_coords)

        if self.flat_layer is not None:
            self.flat_layer.self_draw(frame, draw_coords, side_length)
        if self.snake_layer is not None:
            self.snake_layer.draw_segment(frame, draw_coords, side_length, self.coordinates)
        if self.convex_layer is not None:
            self.convex_layer.self_draw(frame, draw_coords, side_length)

    def try_placing(self, block):
        if self.flat_layer is None and self.convex_layer is None and self.snake_layer is None:
            if isinstance(block, Convex):
                self.convex_layer = block
            elif isinstance(block, Flat):
                self.flat_layer = block
            else:
                raise UnknownBlockType
            block.set_field(self)
            return True
        else:
            return False

    def has_removable(self):
        if self.flat_layer is not None and self.flat_layer.pane_index is not None:
            return True
        if self.convex_layer is not None and self.convex_layer.pane_index is not None:
            return True
        return False

    def request_removable(self):
        if self.flat_layer is not None and self.flat_layer.pane_index is not None:
            returned = self.flat_layer
            self.flat_layer = None
            return returned
        if self.convex_layer is not None and self.convex_layer.pane_index is not None:
            returned = self.convex_layer
            self.convex_layer = None
            return returned
        return None


class UnknownBlockType(Exception):
    pass
