import pygame


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

    def request_field(self, position):
        x, y = position
        if len(self.fields) > y >= 0 and len(self.fields[0]) > x >= 0:
            if self.fields[y][x] is not None:
                return self.fields[y][x]
            else:
                raise NotExistingField
        else:
            raise OutOfRange

    def request_field_on_screen(self, position):
        if not self.top_left_corner:
            return None
        x = (position[0] - self.top_left_corner[0]) // self.displayed_field_side
        y = (position[1] - self.top_left_corner[1]) // self.displayed_field_side
        try:
            return self.request_field((x, y))
        except:
            return None

    def request_offset(self, field, pos, field_side):
        x, y = self.top_left_corner
        for i in range(len(self.fields)):
            for j in range(len(self.fields[i])):
                if self.fields[i][j] == field:
                    bind_x = x + j * field_side
                    bind_y = y + i * field_side
                    return (pos[0] - bind_x, pos[1] - bind_y)


class OutOfRange(Exception):
    pass


class ImpossibleToDraw(Exception):
    pass


class NotExistingField(Exception):
    pass


class WrongMatrix(Exception):
    pass
