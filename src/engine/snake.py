import pygame

class Snake:
    is_alive = True
    grow_at_next_move = False

    def __init__(self, segments, color, direction, board):
        self.segments = segments
        self.color = color
        self.direction = direction
        self.board = board
        head_path = 'assets/snek-head-' + color + '.png'
        body_path = 'assets/snek-body-' + color + '.png'
        tail_path = 'assets/snek-tail-' + color + '.png'
        self.head_texture = pygame.image.load(head_path)
        self.body_texture = pygame.image.load(body_path)
        self.tail_texture = pygame.image.load(tail_path)

        for segment in self.segments:
            field_to_place = self.board.request_field(segment)
            field_to_place.place_snake(self)

    def draw_segment(self, frame, x_coord, y_coord, side_length, segment_coords):
        # Wyjątek segment_coords poza segments
        draw_coords = x_coord, y_coord
        resized_head_texture = pygame.transform.scale(self.head_texture, (field_side, field_side))
        resized_body_texture = pygame.transform.scale(self.body_texture, (field_side, field_side))
        resized_tail_texture = pygame.transform.scale(self.tail_texture, (field_side, field_side))

        if not self.is_alive:
            pass
        if self.segments[-1] == segment_coords:
            frame.blit(resized_body_texture, draw_coords)
        elif self.segments[0] == segment_coords:
            frame.blit(resized_tail_texture, draw_coords)
        else:
            frame.blit(resized_body_texture, draw_coords)

    def move(self):
        current_head_coords = self.segments[-1]
        new_head_coords = self.direction.move_in_direction(current_head_coords)
        new_field = self.board.request_field(new_head_coords)

        if not new_field.check_snake_move(self, self.direction):
            self.destroy()

        if not self.grow_at_next_move:
            self.segments.pop(0)
            field_to_remove = self.board.request_field(self.segments[0])
            field_to_remove.remove_snake()
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
            field = self.board.request_field(segment_coords)
            field.remove_snake()
        self.is_alive = False

    def interact_with_snake(self, other_snake):
        snake_head_coords = self.segments[-1]
        other_head_coords = other_snake.segments[-1]
        if snake_head_coords == other_head_coords:
            self.destroy()
        other_snake.destroy()
