from src.engine.direction import Direction
from src.engine.field import Field
from src.engine.board import Board


class Snake:
    is_alive = True
    grow_at_next_move = False

    def __init__(self, segments, color, direction, board):
        self.segments = segments
        self.color = color
        self.direction = direction
        self.board = board

    def self_draw(self, frame, x, y):
        pass

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
        
