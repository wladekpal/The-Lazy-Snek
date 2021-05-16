import pygame
import os
import enum

from .direction import Direction


class SnakeState(enum.Enum):
    ALIVE = 1,
    DEAD = 2,
    FINISHED = 3,


class Snake:
    grow_at_next_move = False
    infinite_grow = False
    wait_turns = 0
    has_key = False
    rev = False

    def __init__(self, segments, color, direction, board):
        self.state = SnakeState.ALIVE
        self.segments = segments
        self.color = color
        self.direction = direction
        self.board = board
        self.initial_orientation()
        self.reload_textures()

        for segment in self.segments:
            field_to_place = self.board.request_field(segment)
            field_to_place.place_snake(self)

    def reload_textures(self):
        dirname = os.path.dirname(__file__)
        head_path = os.path.join(dirname, '../../assets/snake/snek-head-' + self.color + '.png')
        bent_head_path = os.path.join(dirname, '../../assets/snake/snek-bent-head-' + self.color + '.png')
        body_path = os.path.join(dirname, '../../assets/snake/snek-body-' + self.color + '.png')
        bent_body_path = os.path.join(dirname, '../../assets/snake/snek-bent-body-' + self.color + '.png')
        tail_path = os.path.join(dirname, '../../assets/snake/snek-tail-' + self.color + '.png')
        self.head_texture = pygame.image.load(head_path)
        self.bent_head_texture = pygame.image.load(bent_head_path)
        self.body_texture = pygame.image.load(body_path)
        self.bent_body_texture = pygame.image.load(bent_body_path)
        self.tail_texture = pygame.image.load(tail_path)

    def initial_orientation(self):
        self.segments_orientation = []
        for segment in self.segments:
            self.segments_orientation.append(self.calculate_neighbours_directions(segment))

    @staticmethod
    def get_direction_betwen_segments(segment, other_segments):
        if not other_segments:
            return None

        possible_direcitons = ['N', 'E', 'S', 'W']

        for direction_letter in possible_direcitons:
            direction = Direction(direction_letter)
            if direction.move_in_direction(segment) == other_segments:
                return str(direction)

        raise BadSegmentOrientation

    def calculate_neighbours_directions(self, segment):
        segment_index = self.segments.index(segment)
        neighbours_directions = ''

        prev_segment = self.segments[segment_index + 1] if segment_index + 1 < len(self.segments) else None
        next_segment = self.segments[segment_index - 1] if segment_index - 1 >= 0 else None

        prev_segment_orientation = Snake.get_direction_betwen_segments(segment, prev_segment)
        next_segment_orientation = Snake.get_direction_betwen_segments(segment, next_segment)

        neighbours_directions += prev_segment_orientation or str(self.direction)
        neighbours_directions += next_segment_orientation or neighbours_directions

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

    @staticmethod
    def get_rotation(neighbours_directions):
        if neighbours_directions in ['NN', 'NE', 'EN', 'NS']:
            return 0
        elif neighbours_directions in ['EE', 'ES', 'SE', 'EW']:
            return -90
        elif neighbours_directions in ['SS', 'SW', 'WS', 'SN']:
            return -180
        elif neighbours_directions in ['WW', 'WN', 'NW', 'WE']:
            return -270
        else:
            raise BadSegmentOrientation

    def draw_segment(self, frame, draw_coords, side_length, segment_coords):
        if segment_coords not in self.segments:
            raise SegmentNotInSnake

        if self.state != SnakeState.ALIVE:
            return

        neighbours_directions = self.segments_orientation[self.segments.index(segment_coords)]
        segment_texture = self.get_segment_texture(segment_coords, neighbours_directions)
        resized_segment_texture = pygame.transform.scale(segment_texture, (side_length, side_length))
        segment_rotation = Snake.get_rotation(neighbours_directions)
        rotated_segment_texture = pygame.transform.rotate(resized_segment_texture, segment_rotation)

        frame.blit(rotated_segment_texture, draw_coords)

    def handle_growing_at_move(self):
        if not self.grow_at_next_move:
            field_to_remove = self.board.request_field(self.segments[0])
            field_to_remove.remove_snake(self)
            self.segments.pop(0)
            self.segments_orientation.pop(0)
        else:
            self.grow_at_next_move = self.infinite_grow

    def handle_reverse_after_move(self):
        if self.rev:
            new_tail_orientation = str(Direction(self.segments_orientation[0][1]).give_reversed()) * 2
            self.segments_orientation = [new_tail_orientation] + self.segments_orientation
        else:
            new_head_orientation = str(self.direction) + str(Direction(self.segments_orientation[-1][0]).give_reversed())
            self.segments_orientation.append(new_head_orientation)
            self.segments_orientation[0] = self.segments_orientation[0][0]*2
        self.rev = False

    def move(self):
        if self.wait_turns > 0:
            self.wait_turns -= 1
            return

        current_head_coords = self.segments[-1]
        new_head_coords = self.direction.move_in_direction(current_head_coords)
        new_field = self.board.request_field(new_head_coords)

        if not new_field.check_snake_move(self):
            self.destroy()
            return

        self.handle_growing_at_move()
        self.segments.append(new_field.get_coords_to_move())
        new_field.snake_entered(self)
        self.handle_reverse_after_move()

    def grow(self):
        self.grow_at_next_move = True

    def get_key(self):
        self.has_key = True

    def enable_infinite_grow(self):
        self.infinite_grow = True
        self.grow_at_next_move = True

    def destroy(self, state=SnakeState.DEAD):
        for segment_coords in self.segments:
            field = self.board.request_field(segment_coords)
            field.remove_snake(self)
        self.state = state

    def finish(self):
        self.destroy(state=SnakeState.FINISHED)

    def interact_with_snake(self, other_snake):
        snake_head_coords = self.segments[-1]
        other_head_coords = other_snake.segments[-1]
        if snake_head_coords == other_head_coords:
            self.destroy()
        other_snake.destroy()

    def interact_with_convex(self, convex):
        self.destroy()

    def wait(self, turns):
        self.wait_turns = turns

    def reverse(self):
        self.rev = True
        self.direction = Direction(self.segments_orientation[0][0]).give_reversed()

        self.segments_orientation.reverse()
        for i in range(len(self.segments_orientation)):
            self.segments_orientation[i] = self.segments_orientation[i][::-1]

        self.segments.reverse()
        first_letter = str(Direction(self.segments_orientation[-1][1]).give_reversed())
        self.segments_orientation[-1] = first_letter + self.segments_orientation[-1][1]

    def change_color(self, new_color):
        self.color = new_color
        self.reload_textures()

    def give_segment_direction(self, coordinates):
        index = self.segments.index(coordinates)
        return Direction(self.segments_orientation[index][0])

    def rotate_head_right(self):
        forbidden_direction = Snake.get_direction_betwen_segments(self.segments[-1], self.segments[-2])
        self.direction.turn_right()
        self.segments_orientation[-1] = str(self.direction) + self.segments_orientation[-1][1]
        if str(self.direction) == forbidden_direction:
            self.direction.turn_right()
            self.segments_orientation[-1] = str(self.direction) + self.segments_orientation[-1][1]


class BadSegmentOrientation(Exception):
    pass


class SegmentNotInSnake(Exception):
    pass
