RIGHT_TURN_SHIFT = 1
LEFT_TURN_SHIFT = -1
REVERSE_SHIFT = 2


class Direction:
    delta = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    direction_name = ['N', 'E', 'S', 'W']
    index = 0

    def __init__(self, direction):
        try:
            self.index = self.direction_name.index(direction)
        except ValueError:
            raise ValueError("Wrong initial direction name")

    def __str__(self):
        return self.direction_name[self.index]

    def move_in_direction(self, coords):
        current_delta = self.delta[self.index]
        return current_delta[0] + coords[0], current_delta[1] + coords[1]

    def turn_right(self):
        self.index += RIGHT_TURN_SHIFT
        self.index %= len(self.direction_name)

    def turn_left(self):
        self.index += LEFT_TURN_SHIFT
        self.index %= len(self.direction_name)

    def reverse(self):
        self.index += REVERSE_SHIFT
        self.index %= len(self.direction_name)
