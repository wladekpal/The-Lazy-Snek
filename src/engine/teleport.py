import pygame
import os
from .field import Field


class EndTeleport(Field):
    def __init__(self):
        super().__init__()
        self.texture = pygame.image.load(os.path.join(os.path.dirname(__file__), "../../assets/block/end-teleport.png"))
        self.active_texture = pygame.image.load(os.path.join(os.path.dirname(__file__), "../../assets/block/active.png"))
        self.active = False

    def place_flat(self, flat):
        return

    def place_convex(self, convex):
        return

    def try_placing(self, block):
        return False

    def self_draw(self, frame, draw_coords, side_length):
        super().self_draw(frame, draw_coords, side_length)
        if self.active is True:
            displayed_texture = pygame.transform.scale(self.active_texture, (side_length, side_length))
            frame.blit(displayed_texture, draw_coords)


class BeginTeleport(Field):
    def __init__(self):
        super().__init__()
        self.texture = pygame.image.load(os.path.join(os.path.dirname(__file__), "../../assets/block/begin-teleport.png"))
        self.linked_coordinates = None
        self.linked_end = None

    def get_additional_data(self):
        return {"end_coordinates": self.linked_coordinates}

    def set_additional_data(self, key, data):
        if key == "end_coordinates":
            self.linked_coordinates = (data[0], data[1])

    def manage_additional_data(self):
        self.linked_end = self.board.request_field(self.linked_coordinates)

    def link(self):
        self.linked_end = self.board.request_field(self.linked_coordinates)

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def set_board(self, board):
        self.board = board

    def check_snake_move(self, snake):
        return self.linked_end.check_snake_move(snake)

    def snake_entered(self, snake):
        self.linked_end.snake_entered(snake)

    def get_coords_to_move(self):
        return self.linked_end.get_coords_to_move()

    def place_snake(self, snake):
        return

    def place_flat(self, flat):
        return

    def check_convex_move(self, direction):
        return self.linked_end.check_convex_move(direction)

    def convex_entered(self, convex, direction):
        self.linked_end.convex_entered(convex, direction)

    def place_convex(self, convex):
        return

    def try_placing(self, block):
        return False
