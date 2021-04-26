import json
import enum
from .blocks import Convex, Flat
from .field import Field
from .board import Board
from .snake import Snake, SnakeState
from .tunnel import Tunnel
from .teleport import BeginTeleport, EndTeleport
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

        self.convert_board()
        self.convert_snakes()
        self.convert_available_blocks()

    def reload_level(self):
        self.snake_pointer = 0
        self.simulation_tick_counter = 0
        self.board_backup = None

        self.convert_board()
        self.convert_snakes()
        self.convert_available_blocks()

    def reload_simulation(self):
        if self.simulation_tick_counter == 0:
            return

        assert(self.board_backup is not None)

        self.snake_pointer = 0
        self.simulation_tick_counter = 0

        self.reload_board()
        self.convert_snakes()
        self.convert_available_blocks()

    def backup_board(self):
        self.board_backup = []
        for row in self.board.fields:
            self.board_backup.append([])
            for field in row:
                if field is None:
                    self.board_backup[-1].append(None)
                else:
                    field_dict = {}
                    field_dict['field'] = field.copy()
                    field_dict['blocks'] = [None, None]
                    field_dict['additional'] = field.get_additional_data()

                    if field.flat_layer is not None:
                        field_dict['blocks'][0] = field.flat_layer.copy()
                    if field.convex_layer is not None:
                        field_dict['blocks'][1] = field.convex_layer.copy()

                    self.board_backup[-1].append(field_dict)

    def reload_board(self):
        board = []
        for i in range(len(self.board_backup)):
            board.append([])
            for j in range(len(self.board_backup[i])):
                field_dict = self.board_backup[i][j]
                if field_dict is None:
                    board[-1].append(None)
                else:
                    field = field_dict['field']
                    field.set_coordinates((j, i))

                    for key, val in  field_dict['additional'].items():
                        field.set_additional_data(key, val)

                    flat_layer, convex_layer = field_dict['blocks']
                    if flat_layer is not None:
                        flat = flat_layer
                        field.place_flat(flat)
                    if convex_layer is not None:
                        convex = convex_layer
                        field.place_convex(convex)

                    board[-1].append(field)

        self.board = Board(board)

    def convert_board(self):
        board = []
        for i in range(len(self.block_placement)):
            board.append([])
            for j in range(len(self.block_placement[i])):
                id = self.block_placement[i][j]
                additional = self.block_additional_data[i][j]
                if id == 0:
                    board[i].append(None)
                elif get_entity_kind(id) == EntityKind.FIELD:
                    field = get_field_from_id(id)
                    field.set_coordinates((j, i))
                    for key, val in additional.items():
                        field.set_additional_data(key, val)
                    board[i].append(field)
                else:
                    field = Field()
                    field.set_coordinates((j, i))
                    block = get_block_from_id(id)
                    if block is not None:
                        if isinstance(block, Convex):
                            field.place_convex(block)
                        elif isinstance(block, Flat):
                            field.place_flat(block)
                        block.set_field(field)
                    else:
                        # it's custom field
                        pass
                    board[i].append(field)

        self.board = Board(board)

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

        self.snakes[self.snake_pointer].move()

        if self.did_all_snakes_finish():
            return LevelState.WIN

        if self.is_any_dead():
            return LevelState.LOSS

        self.update_snake_pointer()
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
