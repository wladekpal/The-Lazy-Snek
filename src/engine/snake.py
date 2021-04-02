from src.engine.direction import Direction
from src.engine.field import Field
from src.engine.board import Board

import pygame


class Snake:
    is_alive = True
    grow_at_next_move = False

    def __init__(self, segments, color, direction, board):
        self.segments = segments
        self.color = color
        self.direction = direction
        self.board = board
        self.head_texture = pygame.image.load('../assets/snek-head-' + color + '.png')
        self.body_texture = pygame.image.load('../assets/snek-body-' + color + '.png')
        self.tail_texture = pygame.image.load('../assets/snek-tail-' + color + '.png')

    def self_draw(self, frame):
        if not self.is_alive:
            pass
        
        board_height = frame.get_height()
        board_width = frame.get_width()

        max_field_height = board_height // len(self.board.fields)
        max_field_width = board_width // len(self.board.fields[0])

        field_side = min(max_field_height, max_field_width)

        field_area_height = field_side * len(self.board.fields)
        field_are_width = field_side * len(self.board[0].fields)

        frame.blit(self.head_texture, (field_area_width + field_side * self.segments[0][0], field_area_height + field_side * self.segments[0][1]))

        for body_segment in segments[1:1]:
            frame.blit(self.body_texture, (field_area_width + field_side * body_segment[0], field_area_height + field_side * body_segment[1]))

        frame.blit(self.tail_texture, (field_area_width + field_side * self.segments[-1][0], field_area_height + field_side * self.segments[-1][1]))

    def move(self):
        current_head_coords = self.segments[-1]
        new_head_coords = self.direction.move_in_direction(current_head_coords)
        new_field = self.board.request_field(new_head_coords)

        if not new_field.check_snake_move(self, self.direction):
            self.destroy()

        if not self.grow_at_next_move:
            self.segments.pop(0)
        else:
            self.grow_at_next_move = False

        new_field.snake_entered(self, self.direction)

        if not self.is_alive:
            return

        self.segments.append(new_head_coords)

    def grow(self):
        self.grow_at_next_move = True

    def destroy(self):
        for segment_coords in self.segments:
            field = self.board.request_field(segment)
            field.remove_snake()
        self.is_alive = False
        self.board.snake_died(self)

    def interact_with_snake(self, other_snake):
        snake_head_coords = self.segments[-1]
        other_head_coords = other_snake.segments[-1]
        if snake_head_coords == other_head_coords:
            self.destroy()
        other_snake.destroy()
        
