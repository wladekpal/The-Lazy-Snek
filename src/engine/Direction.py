class Direction:
    delta = [(0, 1), (1, 0), (0, -1), (-1, 0)]
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

    def turnRight(self):
        self.index += 1
        self.index %= 4

    def turnLeft(self):
        self.index -= 1
        self.index %= 4

    def reverse(self):
        self.index += 2
        self.index %= 4
