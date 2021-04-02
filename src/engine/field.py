
class Field:

    def __init__(self, texture, coordinates, board):
        self.texture = texture
        self.coordinates = coordinates
        self.board = board
        self.flat_layer = None
        self.convex_layer = None
        self.snake_layer = None

    # orientation
    def give_field_in_direction(self, direction):
        coordinates = direction.move_in_direction(self.coordinates)
        return self.board.give_field(coordinates)

    # snake
    def check_snake_move(self, snake):
        if self.convex_layer is None:
            return True
        else:
            return self.convex_layer.check_snake_move(snake)

    def snake_entered(self, snake):
        if self.snake_layer is not None:
            self.snake_layer.interact_with_snake(snake)
        elif self.convex_layer is not None:
            self.convex_layer.interact_with_snake(snake)

        if self.snake_layer is None:
            self.flat_layer.interact_with_snake(snake)

        self.snake_layer = snake

    def snake_left(self):
        self.snake_layer = None

    def remove_snake(self):
        self.snake_layer = None

    # flat
    def remove_flat(self):
        self.flat_layer = None

    def place_flat(self, flat):
        self.flat_layer = flat

    # convex
    def check_convex_move(self, direction):
        if self.convex_layer is None:
            return True
        else:
            return self.convex_layer.check_move(direction)

    def convex_entered(self, convex, direction):
        if self.snake_layer is not None:
            self.snake_layer.interact_with_convex()
        elif self.convex_layer is not None:
            self.convex_layer.move(direction)

        if self.flat_layer is not None:
            self.flat_layer.interact_with_convex(convex)

        self.convex_layer = convex

    def convex_left(self):
        self.convex_layer = None

    def remove_convex(self):
        self.convex_layer = None

    def place_convex(self, convex):
        self.convex_layer = convex

    # display
    def self_display(self, frame, x, y, side_length):
        pass
