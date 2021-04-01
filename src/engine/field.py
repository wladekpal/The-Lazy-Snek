
class Field:
    flat_layer = EmptyFlat()
    convex_layer = EmptyConvex()
    snake_layer = None
    texture = None
    coordinates = (0, 0)
    board = None

    def __init__(self, texture, coordinates, board):
        self.texture = texture
        self.coordinates = coordinates
        self.board = board

    # orientation
    def give_field_in_direction(self, direction):
        coordinates = direction.move_in_direction(self.coordinates)
        return self.board.give_field(coordinates)

    # snake
    def check_snake_move(self, snake):
        return self.convex_layer.check_snake_move(snake)

    def snake_entered(self, snake, direction):
        if self.snake_layer is not None:
            self.snake_layer.interact_with_snake(snake)
        self.convex_layer.interact_with_snake(snake, direction)
        self.flat_layer.interact_with_snake(snake)

    def snake_left(self):
        self.snake_layer = None

    # flat
    def remove_flat(self):
        self.flat_layer = EmptyFlat()

    def place_flat(self, flat):
        self.flat_layer = flat

    # convex
    def check_convex_move(self, direction):
        return self.convex_layer.interact_with_convex(direction)

    def convex_entered(self, convex, direction):
        self.convex_layer.interact_with_convex(direction)
        if self.snake_layer is not None:
            self.snake_layer.perform_death()
        self.flat_layer.interact_with_convex(convex) #czy potrzebne direction?

    def convex_left(self):
        self.convex_layer = None

    def remove_convex(self):
        self.convex_layer = EmptyConvex()

    def place_convex(self, convex):
        self.convex_layer = convex

    # display
    def self_display(self, frame, x, y, side_length):
        pass
