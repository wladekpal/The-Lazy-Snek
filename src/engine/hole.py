import pygame
import os
from .field import Field
from .convex import Box


class Hole(Field):

    def __init__(self):
        super().__init__()
        self.plugged_hole_field = Field()
        self.plugged = False
        self.texture = pygame.image.load(os.path.join("assets/block/hole.png"))
        plugged_texture = pygame.image.load(os.path.join("assets/block/plugged-hole.png"))
        self.plugged_hole_field.texture = plugged_texture

    def set_coordinates(self, coordinates):
        super().set_coordinates(coordinates)
        self.plugged_hole_field.set_coordinates(coordinates)

    def set_board(self, board):
        super().set_board(board)
        self.plugged_hole_field.set_board(board)

    def check_snake_move(self, snake):
        if self.plugged:
            return self.plugged_hole_field.check_snake_move(snake)
        else:
            return True

    def snake_entered(self, snake):
        if self.plugged:
            self.plugged_hole_field.snake_entered(snake)
        else:
            snake.destroy()

    def snake_left(self):
        self.plugged_hole_field.snake_left()

    def remove_snake(self, snake):
        self.plugged_hole_field.remove_snake(snake)

    def place_snake(self, snake):
        return

    def remove_flat(self):
        return

    def place_flat(self, flat):
        return

    def check_convex_move(self, direction):
        if self.plugged:
            return self.plugged_hole_field.check_convex_move(direction)
        else:
            return True

    def convex_entered(self, convex, direction):
        if self.plugged:
            self.plugged_hole_field.convex_entered(convex, direction)
        else:
            if isinstance(convex, Box):
                self.plugged = True
            convex.destroy()

    def convex_left(self, direction):
        self.plugged_hole_field.convex_left(direction)

    def remove_convex(self, direction):
        self.plugged_hole_field.remove_convex(direction)

    def place_convex(self, convex):
        return

    def self_draw(self, frame, draw_coords, side_length):
        if self.plugged:
            self.plugged_hole_field.self_draw(frame, draw_coords, side_length)
        else:
            super().self_draw(frame, draw_coords, side_length)

    def try_placing(self, block):
        return False

    def has_removable(self):
        return False

    def request_removable(self):
        return None
