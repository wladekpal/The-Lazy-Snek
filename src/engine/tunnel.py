import pygame
import os
from .field import Field


class Tunnel(Field):

    def __init__(self, direction):
        super().__init__()
        self.lower_field = Field()
        self.upper_field = Field()
        self.direction = direction

        upper_texture = pygame.image.load(os.path.join("assets/block/tunnel-upper.png"))
        lower_texture = pygame.image.load(os.path.join("assets/block/tunnel-lower.png"))
        if str(direction) == 'E' or str(direction) == 'W':
            upper_texture = pygame.transform.rotate(upper_texture, -90)
            lower_texture = pygame.transform.rotate(lower_texture, -90)
        self.lower_field.texture = lower_texture
        self.upper_field.texture = upper_texture

    def copy(self):
        return type(self)(direction=self.direction)

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
        self.lower_field.set_coordinates(coordinates)
        self.upper_field.set_coordinates(coordinates)

    def set_board(self, board):
        super().set_board(board)
        self.lower_field.set_board(board)
        self.upper_field.set_board(board)

    def choose_field(self, direction):
        if direction == self.direction or direction == self.direction.give_reversed():
            return self.upper_field
        else:
            return self.lower_field

    def check_snake_move(self, snake):
        return self.choose_field(snake.direction).check_snake_move(snake)

    def snake_entered(self, snake):
        self.choose_field(snake.direction).snake_entered(snake)

    def snake_left(self):
        return

    def remove_snake(self, snake):
        segment_dir = snake.give_segment_direction(self.coordinates)
        self.choose_field(segment_dir).remove_snake(snake)

    def place_snake(self, snake):
        return

    def remove_flat(self):
        return

    def place_flat(self):
        return

    def check_convex_move(self, direction):
        return self.choose_field(direction).check_convex_move(direction)

    def convex_entered(self, convex, direction):
        self.choose_field(direction).convex_entered(convex, direction)

    def convex_left(self, direction):
        self.choose_field(direction).convex_left(direction)
        return

    def remove_convex(self):
        return

    def place_convex(self, convex):
        return

    def self_draw(self, frame, draw_coords, side_length):
        self.lower_field.self_draw(frame, draw_coords, side_length)
        self.upper_field.self_draw(frame, draw_coords, side_length)

    def try_placing(self, block):
        return False

    def has_removable(self):
        return False

    def request_removable(self):
        return None
