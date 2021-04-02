import pygame


class Board:
    def __init__(self, fields):
        self.fields = fields
        self.state = 'running'

        for row in self.fields:
            for field in row:
                field.set_board()

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

        for i in range(len(self.fields)):
            for j in range(len(self.fields[i])):
                if self.fields[i][j] is not None:
                    self.fields[i][j].self_draw(frame, start_x+j*field_side, start_y+i*field_side, field_side)

    def request_field(self, x, y):
        if len(self.fields) > x > 0 and len(self.fields[0]) > y > 0:
            if self.fields[x][y] is not None:
                return self.fields[x][y]
            else:
                raise NotExistingField
        else:
            raise OutOfRange

    def make_tick(self):
        for row in self.fields:
            for field in row:
                if field is not None:
                    field.make_tick()

    def game_over(self):
        self.state = 'lost'

    def game_won(self):
        self.state = 'won'


class OutOfRange(Exception):
    pass


class ImpossibleToDraw(Exception):
    pass


class NotExistingField(Exception):
    pass
