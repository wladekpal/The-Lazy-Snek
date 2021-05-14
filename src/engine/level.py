import json
import enum
from .blocks import Convex, Flat
from .field import Field
from .board import Board
from .snake import Snake, SnakeState
from .direction import Direction
from .id_parser import EntityKind, get_entity_kind, get_block_from_id, get_field_from_id


class LevelState(enum.Enum):
    UNDECIDED = 1,
    WIN = 2,
    LOSS = 3,


class Level:

    def __init__(self, file_name):
        with open(file_name) as json_file:
            self.level_description = json.load(json_file)

        self.level_name = self.level_description["level_name"]
        self.level_creator = self.level_description["level_creator"]
        self.block_placement = self.level_description["block_placement"]
        self.block_additional_data = self.level_description["block_additional_data"]
        self.snake_data = self.level_description["snake_data"]
        self.available_blocks_data = self.level_description["available_blocks"]

        self.snake_pointer = 0
        self.board = None
        self.snakes = None
        self.simulation_tick_counter = 0
        self.board_backup = None
        self.available_blocks = None

        self.create_initial_board()
        self.convert_snakes()
        self.convert_available_blocks()

    def reload_level(self):
        self.snake_pointer = 0
        self.simulation_tick_counter = 0
        self.board_backup = None

        self.create_initial_board()
        self.convert_snakes()
        self.convert_available_blocks()

    def reload_simulation(self):
        if self.simulation_tick_counter == 0:
            return

        assert(self.board_backup is not None)

        self.snake_pointer = 0
        self.simulation_tick_counter = 0

        self.reload_board_from_backup()
        self.convert_snakes()
        self.convert_available_blocks()

    def create_board_from_data(self, data, entity_creation):
        new_board = []
        x, y = 0, 0
        for row in data:
            new_board.append([])
            x = 0
            for data in row:
                entity = entity_creation(data, (x, y))
                new_board[-1].append(entity)
                x += 1
            y += 1

        return new_board

    def create_entity_from_id(self, id, coordinates):
        entity_kind = get_entity_kind(id)
        x, y = coordinates
        additional = self.block_additional_data[y][x]

        if entity_kind == EntityKind.EMPTY:
            return None

        if entity_kind == EntityKind.FIELD:
            field = get_field_from_id(id)
            field.set_coordinates((x, y))
            for key, val in additional.items():
                field.set_additional_data(key, val)

            return field

        if entity_kind == EntityKind.BLOCK:
            field = Field()
            field.set_coordinates((x, y))
            block = get_block_from_id(id)

            if isinstance(block, Convex):
                field.place_convex(block)
            elif isinstance(block, Flat):
                field.place_flat(block)
            block.set_field(field)

            return field

    def create_entity_from_field_dict(self, field_dict, coordinates):
        x, y = coordinates

        if field_dict is None:
            return None

        field = field_dict['field']
        field.set_coordinates((x, y))

        for key, val in field_dict['additional'].items():
            field.set_additional_data(key, val)

        flat_layer, convex_layer = field_dict['blocks']
        if flat_layer is not None:
            flat = flat_layer
            field.place_flat(flat)
        if convex_layer is not None:
            convex = convex_layer
            field.place_convex(convex)

        return field

    def create_backup_entity(self, field, _):
        if field is None:
            return None

        field_dict = {}
        field_dict['field'] = field.copy()
        field_dict['blocks'] = [None, None]
        field_dict['additional'] = field.get_additional_data()

        if field.flat_layer is not None:
            field_dict['blocks'][0] = field.flat_layer.copy()
        if field.convex_layer is not None:
            field_dict['blocks'][1] = field.convex_layer.copy()

        return field_dict

    def reload_board_from_backup(self):
        new_board = self.create_board_from_data(self.board_backup, self.create_entity_from_field_dict)
        self.board = Board(new_board)

    def create_initial_board(self):
        new_board = self.create_board_from_data(self.block_placement, self.create_entity_from_id)
        self.board = Board(new_board)

    def backup_board(self):
        self.board_backup = self.create_board_from_data(self.board.fields, self.create_backup_entity)

    def convert_snakes(self):
        self.snakes = []
        for snake_d in self.snake_data:
            snake = Snake(
                [(item[0], item[1]) for item in snake_d["placement"]],
                snake_d["color"],
                Direction(snake_d["direction"]),
                self.board
            )
            self.snakes.append(snake)

    def convert_available_blocks(self):
        self.available_blocks = []
        cur_pane_index = 0
        for block_id, count in self.available_blocks_data:
            for _ in range(count):
                self.available_blocks.append(get_block_from_id(block_id))
                self.available_blocks[-1].pane_index = cur_pane_index
                cur_pane_index += 1

    def is_any_dead(self):
        for snake in self.snakes:
            if snake.state == SnakeState.DEAD:
                return True
        return False

    def did_all_snakes_finish(self):
        for snake in self.snakes:
            if snake.state != SnakeState.FINISHED:
                return False
        return True

    def tick(self) -> int:
        if self.simulation_tick_counter == 0:
            self.backup_board()
        self.simulation_tick_counter += 1

        for snake in self.snakes:
            if snake.state != SnakeState.FINISHED and snake.state != SnakeState.DEAD:
                snake.move()

        if self.did_all_snakes_finish():
            return LevelState.WIN

        if self.is_any_dead():
            return LevelState.LOSS

        return LevelState.UNDECIDED

    def update_snake_pointer(self):
        if self.is_any_dead():
            raise Exception

        self.snake_pointer += 1
        self.snake_pointer %= len(self.snakes)
        while self.snakes[self.snake_pointer].state != SnakeState.ALIVE:
            self.snake_pointer += 1
            self.snake_pointer %= len(self.snakes)

    def self_draw(self, frame):
        return self.board.self_draw(frame)

    def get_board(self):
        return self.board
