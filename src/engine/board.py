import pygame
from .id_parser import EntityKind, get_entity_kind, get_block_from_id, get_field_from_id


class Board:
    def __init__(self, fields):
        self.fields = fields
        self.state = "running"
        self.top_left_corner = None
        self.displayed_field_side = None

        if len(fields) == 0:
            raise WrongMatrix

        for row in self.fields:
            for field in row:
                if field is not None:
                    field.set_board(self)

        for row in self.fields:
            for field in row:
                if field is not None:
                    field.manage_additional_data()

    def self_draw(self, frame: pygame.Surface):
        board_height = frame.get_height()
        board_width = frame.get_width()

        max_field_height = board_height // len(self.fields)
        max_field_width = board_width // len(self.fields[0])

        field_side = min(max_field_height, max_field_width)

        if field_side < 1:
            raise ImpossibleToDraw

        field_area_height = field_side * len(self.fields)
        field_area_width = field_side * len(self.fields[0])

        start_x = (board_width - field_area_width) // 2
        start_y = (board_height - field_area_height) // 2
        self.top_left_corner = (start_x, start_y)

        # i - y-coordinate
        # j - x-coordinate
        for i in range(len(self.fields)):
            for j in range(len(self.fields[i])):
                if self.fields[i][j] is not None:
                    self.fields[i][j].self_draw(frame, (start_x+j*field_side, start_y+i*field_side), field_side)

        self.displayed_field_side = field_side
        return field_side

    def valid_coordinates(self, coordinates):
        x, y = coordinates
        return (len(self.fields) > y >= 0 and len(self.fields[0]) > x >= 0)

    def request_field(self, position):
        x, y = position
        if self.valid_coordinates((x, y)):
            if self.fields[y][x] is not None:
                return self.fields[y][x]
            else:
                raise NotExistingField
        else:
            raise OutOfRange

    def get_screen_position_coordinates(self, position):
        if not self.top_left_corner:
            raise ScreenPostionNotSet

        x = (position[0] - self.top_left_corner[0]) // self.displayed_field_side
        y = (position[1] - self.top_left_corner[1]) // self.displayed_field_side
        return (x, y)

    def request_field_on_screen(self, position):
        if not self.top_left_corner:
            return None
        x, y = self.get_screen_position_coordinates(position)
        try:
            return self.request_field((x, y))
        except (OutOfRange, NotExistingField):
            return None

    def request_offset(self, field, pos, field_side):
        x, y = self.top_left_corner
        for i in range(len(self.fields)):
            for j in range(len(self.fields[i])):
                if self.fields[i][j] == field:
                    bind_x = x + j * field_side
                    bind_y = y + i * field_side
                    return (pos[0] - bind_x, pos[1] - bind_y)

    def try_placing_entity(self, entity_id, position):
        field = self.request_field_on_screen(position)
        entity_kind = get_entity_kind(entity_id)

        if entity_kind == EntityKind.BLOCK:
            if field is None:
                return False

            block = get_block_from_id(entity_id)
            return field.try_placing(block)

        if entity_kind == EntityKind.FIELD:
            if field is not None:
                return False

            x, y = self.get_screen_position_coordinates(position)
            if self.valid_coordinates((x, y)):
                field = get_field_from_id(entity_id)
                field.set_coordinates((x, y))
                field.set_board(self)
                self.fields[y][x] = field
                return True

        return False

    def try_removing_highest(self, position):
        field = self.request_field_on_screen(position)
        if field is None:
            return False

        if field.convex_layer is not None:
            field.remove_convex()
        elif field.flat_layer is not None:
            field.remove_flat()
        else:
            x, y = self.get_screen_position_coordinates(position)
            if not self.valid_coordinates((x, y)):
                return False
            self.fields[y][x] = None
        return True


class OutOfRange(Exception):
    pass


class ImpossibleToDraw(Exception):
    pass


class NotExistingField(Exception):
    pass


class WrongMatrix(Exception):
    pass


class ScreenPostionNotSet(Exception):
    pass
