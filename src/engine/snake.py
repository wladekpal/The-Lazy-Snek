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

    def self_draw(self, frame):
        if not self.is_alive:
            pass

        board_height = frame.get_height()
        board_width = frame.get_width()

        max_field_height = board_height // len(self.board.fields)
        max_field_width = board_width // len(self.board.fields[0])

        field_side = min(max_field_height, max_field_width)

        field_area_height = field_side * len(self.board.fields)
        field_area_width = field_side * len(self.board[0].fields)

        start_x = (board_width - field_area_width) // 2
        start_y = (board_height - field_area_height) // 2

        resized_head_texture = pygame.transform.scale(self.head_texture, (field_side, field_side))
        resized_body_texture = pygame.transform.scale(self.body_texture, (field_side, field_side))
        resized_tail_texture = pygame.transform.scale(self.tail_texture, (field_side, field_side))

        disp_coords = (start_x + field_side * self.segments[0][0], start_y + field_side * self.segments[0][1])
        frame.blit(resized_head_texture, disp_coords)

        for body_segment in self.segments[1:1]:
            disp_coords = (start_x + field_side * body_segment[0], start_y + field_side * body_segment[1])
            frame.blit(resized_body_texture, disp_coords)

        disp_coords = (start_x + field_side * self.segments[-1][0], start_y + field_side * self.segments[-1][1])
        frame.blit(resized_tail_texture, disp_coords)

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
            field = self.board.request_field(segment_coords)
            field.remove_snake()
        self.is_alive = False

    def interact_with_snake(self, other_snake):
        snake_head_coords = self.segments[-1]
        other_head_coords = other_snake.segments[-1]
        if snake_head_coords == other_head_coords:
            self.destroy()
        other_snake.destroy()
