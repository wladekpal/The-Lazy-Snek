import pygame
import os
from .direction import Direction


class Snake:
    is_alive = True
    grow_at_next_move = False

    def __init__(self, segments, color, direction, board):
        self.segments = segments
        self.color = color
        self.direction = direction
        self.board = board
        dirname = os.path.dirname(__file__)
        head_path = os.path.join(dirname, '../../assets/snek-head-' + color + '.png')
        bent_head_path = os.path.join(dirname, '../../assets/snek-bent-head-' + color + '.png')
        body_path = os.path.join(dirname, '../../assets/snek-body-' + color + '.png')
        bent_body_path = os.path.join(dirname, '../../assets/snek-bent-body-' + color + '.png')
        tail_path = os.path.join(dirname, '../../assets/snek-tail-' + color + '.png')
        self.head_texture = pygame.image.load(head_path)
        self.bent_head_texture = pygame.image.load(bent_head_path)
        self.body_texture = pygame.image.load(body_path)
        self.bent_body_texture = pygame.image.load(bent_body_path)
        self.tail_texture = pygame.image.load(tail_path)

        for segment in self.segments:
            field_to_place = self.board.request_field(segment)
            field_to_place.place_snake(self)

    def get_direction_betwen_segments(segment, other_segments):
        possible_direcitons = ['N', 'E', 'S', 'W']

        for direction_letter in possible_direcitons:
            direction = Direction(direction_letter)
            if direction.move_in_direction(segment) == other_segments:
                return str(direction)

        raise BadSegmentOrientation

    def calculate_neighbours_directions(self, segment):
        segment_index = self.segments.index(segment)
        neighbours_directions = ''

        if segment_index + 1 < len(self.segments):
            prev_segment = self.segments[segment_index + 1]
        else:
            prev_segment = None

        if segment_index - 1 >= 0:
            next_segment = self.segments[segment_index - 1]
        else:
            next_segment = None

        if prev_segment is not None:
            neighbours_directions += Snake.get_direction_betwen_segments(segment, prev_segment)
        else:
            neighbours_directions += str(self.direction)

        if next_segment is not None:
            neighbours_directions += Snake.get_direction_betwen_segments(segment, next_segment)

        return neighbours_directions

    def get_segment_texture(self, segment, neighbours_directions):
        bent_directions = ['NE', 'EN', 'ES', 'SE', 'SW', 'WS', 'WN', 'NW']
        mirror_head_directions = ['EN', 'SE', 'WS', 'NW']
        if segment == self.segments[0]:
            return self.tail_texture
        elif segment == self.segments[-1] and neighbours_directions in bent_directions:
            if neighbours_directions in mirror_head_directions:
                mirrored_bent_head_texture = pygame.transform.flip(self.bent_head_texture, True, False)
                return pygame.transform.rotate(mirrored_bent_head_texture, -90)
            else:
                return self.bent_head_texture
        elif segment == self.segments[-1]:
            return self.head_texture
        elif neighbours_directions in bent_directions:
            return self.bent_body_texture
        else:
            return self.body_texture

    def draw_segment(self, frame, draw_coords, side_length, segment_coords):
        if segment_coords not in self.segments:
            raise SegmentNotInSnake

        if not self.is_alive:
            return

        neighbours_directions = self.calculate_neighbours_directions(segment_coords)
        segment_texture = self.get_segment_texture(segment_coords, neighbours_directions)
        resized_segment_texture = pygame.transform.scale(segment_texture, (side_length, side_length))

        if neighbours_directions in ['N', 'NE', 'EN', 'NS']:
            rotated_segment_texture = resized_segment_texture
        elif neighbours_directions in ['E', 'ES', 'SE', 'EW']:
            rotated_segment_texture = pygame.transform.rotate(resized_segment_texture, -90)
        elif neighbours_directions in ['S', 'SW', 'WS', 'SN']:
            rotated_segment_texture = pygame.transform.rotate(resized_segment_texture, -180)
        elif neighbours_directions in ['W', 'WN', 'NW', 'WE']:
            rotated_segment_texture = pygame.transform.rotate(resized_segment_texture, -270)

        frame.blit(rotated_segment_texture, draw_coords)

    def move(self):
        current_head_coords = self.segments[-1]
        new_head_coords = self.direction.move_in_direction(current_head_coords)
        new_field = self.board.request_field(new_head_coords)

        if not new_field.check_snake_move(self):
            self.destroy()
            return

        if not self.grow_at_next_move:
            field_to_remove = self.board.request_field(self.segments[0])
            field_to_remove.remove_snake(self)
            self.segments.pop(0)
        else:
            self.grow_at_next_move = False

        self.segments.append(new_head_coords)
        new_field.snake_entered(self)

    def grow(self):
        self.grow_at_next_move = True

    def destroy(self):
        for segment_coords in self.segments:
            field = self.board.request_field(segment_coords)
            field.remove_snake(self)
        self.is_alive = False

    def interact_with_snake(self, other_snake):
        snake_head_coords = self.segments[-1]
        other_head_coords = other_snake.segments[-1]
        if snake_head_coords == other_head_coords:
            self.destroy()
        other_snake.destroy()

    def interact_with_convex(self, convex):
        self.destroy


class BadSegmentOrientation(Exception):
    pass


class SegmentNotInSnake(Exception):
    pass
