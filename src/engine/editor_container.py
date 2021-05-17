from .direction import Direction
from .board import Board
from .snake import Snake
from .teleport import BeginTeleport, EndTeleport


class EditorContainer():

    def __init__(self, dimensions, name, creator):
        self.name = name
        self.creator = creator
        self.dimensions = dimensions
        self.board = Board(self.create_entity_filled_board(dimensions, lambda: None))
        self.additional_data = self.create_entity_filled_board(dimensions, dict)
        self.block_placement_stack_matrix = self.create_entity_filled_board(dimensions, lambda: [0])
        self.snakes = []
        self.available_blocks = []
        self.tags = []
        self.active_snake = None
        self.chosen_teleport = None

    def create_entity_filled_board(self, dimensions, entity_constructor):
        new_board = []
        y, x = dimensions
        for _ in range(y):
            new_board.append([entity_constructor() for _ in range(x)])
        return new_board

    def try_placing_entity(self, entity_id, position):
        is_placed = self.board.try_placing_entity(entity_id, position)
        if is_placed:
            x, y = self.board.get_screen_position_coordinates(position)
            self.block_placement_stack_matrix[y][x].append(entity_id)
        return is_placed

    def remove_snake(self, snake):
        self.snakes.remove(snake)
        snake.destroy()

    def remove_all_connected_fields(self, coordinates):
        for y in range(len(self.board.fields)):
            for x in range(len(self.board.fields[y])):
                if coordinates in self.additional_data[y][x].values():
                    self.board.fields[y][x] = None
                    self.additional_data[y][x] = {}
                    self.block_placement_stack_matrix[y][x].pop()

    def remove_highest_entity(self, position):
        field = self.board.request_field_on_screen(position)
        if field is not None and field.snake_layer is not None:
            self.remove_snake(field.snake_layer)
            return

        if self.board.try_removing_highest(position):
            x, y = field.coordinates
            self.block_placement_stack_matrix[y][x].pop()
            if len(self.block_placement_stack_matrix[y][x]) == 1:
                self.additional_data[y][x] = {}
                self.remove_all_connected_fields((x, y))

    def add_available_block(self, block_id):
        for block_data in self.available_blocks:
            if block_data[0] == block_id:
                block_data[1] += 1
                return
        self.available_blocks.append([block_id, 1])

    def remove_available_block(self, block_id_to_remove):
        for i in range(len(self.available_blocks)):
            block_id, count = self.available_blocks[i]
            if block_id == block_id_to_remove:
                if count > 1:
                    self.available_blocks[i][1] -= 1
                else:
                    self.available_blocks.pop(i)
                return

    def get_block_placement(self):
        block_placement = []
        for row in self.block_placement_stack_matrix:
            block_placement.append([])
            for stack in row:
                block_placement[-1].append(stack[-1])
        return block_placement

    def get_snake_data(self):
        snake_data = []
        for snake in self.snakes:
            snake_data.append({
                "name": "snake",
                "type": 0,
                "color": snake.color,
                "placement": snake.segments,
                "direction": str(snake.direction)
            })
        return snake_data

    def check_snake_new_block(self, field, snake):
        head_x, head_y = snake.segments[-1]
        x, y = field.coordinates
        if abs(head_x - x) + abs(head_y - y) == 1:
            new_segments = snake.segments + [(x, y)]
            new_direction = Snake.get_direction_betwen_segments(snake.segments[-1], (x, y))
            snake.destroy()
            self.snakes.pop()
            new_snake = Snake(new_segments, 'green', Direction(new_direction), self.board)
            self.snakes.append(new_snake)
            self.active_snake = new_snake

    def try_placing_snake(self, position):
        field = self.board.request_field_on_screen(position)
        if not field:
            return

        if field.snake_layer is None and field.convex_layer is None and field.flat_layer is None:
            if self.active_snake:
                self.check_snake_new_block(field, self.active_snake)
            else:
                self.snakes.append(Snake([field.coordinates], 'green', Direction('N'), self.board))
                self.active_snake = self.snakes[-1]

    def finish_snake_building(self):
        if not self.active_snake:
            return
        if len(self.active_snake.segments) < 2:
            self.remove_snake(self.active_snake)
        self.active_snake = None

    def finish_teleport_linking(self):
        self.chosen_teleport = None

    def rotate_snake_head(self, position):
        field = self.board.request_field_on_screen(position)
        if field is not None and field.snake_layer is not None:
            snake = field.snake_layer
            snake.rotate_head_right()

    def change_snake_color(self, position):
        field = self.board.request_field_on_screen(position)
        if field is not None and field.snake_layer is not None:
            snake = field.snake_layer
            new_color = {
                "green": "blue",
                "blue": "red",
                "red": "green",
            }
            snake.change_color(new_color[snake.color])

    def link_teleport(self, position):
        field = self.board.request_field_on_screen(position)
        if isinstance(field, BeginTeleport):
            if self.chosen_teleport:
                out_teleport_coordinates = self.chosen_teleport.coordinates
                in_x, in_y = field.coordinates
                self.additional_data[in_y][in_x] = {"end_coordinates": out_teleport_coordinates}
        elif isinstance(field, EndTeleport):
            self.chosen_teleport = field

    def convert_level_to_dictionary(self):
        return {
            "level_name": self.name,
            "level_creator": self.creator,
            "level_tags": self.tags,
            "block_placement": self.get_block_placement(),
            "block_additional_data": self.additional_data,
            "snake_data": self.get_snake_data(),
            "available_blocks": self.available_blocks
        }

    def get_available_blocks(self):
        return self.available_blocks

    def self_draw(self, frame):
        self.board.self_draw(frame)
