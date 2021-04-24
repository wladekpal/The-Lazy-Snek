import json
from .blocks import Wall, TurnLeft, TurnRight, Box, Spikes, Skull, Reverse
from .field import Field
from .board import Board
from .snake import Snake
from .direction import Direction


class Level:

    def __init__(self, file_name):
        with open(file_name) as json_file:
            self.level_description = json.load(json_file)

        self.level_name = self.level_description["level_name"]
        self.level_creator = self.level_description["level_creator"]
        self.block_placement = self.level_description["block_placement"]
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
                    field_layers = [None, None]

                    if field.flat_layer is not None:
                        field_layers[0] = (type(field.flat_layer), field.flat_layer.pane_index)
                    if field.convex_layer is not None:
                        field_layers[1] = (type(field.convex_layer), field.convex_layer.pane_index)

                    self.board_backup[-1].append(field_layers)

    def reload_board(self):
        board = []
        for i in range(len(self.board_backup)):
            board.append([])
            for j in range(len(self.board_backup[i])):
                if self.board_backup[i][j] is None:
                    board[-1].append(None)
                else:
                    field = Field((j, i))
                    flat_layer, convex_layer = self.board_backup[i][j]

                    if flat_layer is not None:
                        flat = flat_layer[0](flat_layer[1])
                        field.place_flat(flat)
                    if convex_layer is not None:
                        convex = convex_layer[0](convex_layer[1])
                        field.place_convex(convex)

                    board[-1].append(field)

        self.board = Board(board)

    def convert_board(self):
        board = []
        for i in range(len(self.block_placement)):
            board.append([])
            for j in range(len(self.block_placement[i])):
                if self.block_placement[i][j] == 1:
                    board[i].append(Field((j, i)))
                elif self.block_placement[i][j] == 2:
                    field = Field((j, i))
                    wall = Wall()
                    field.place_convex(wall)
                    board[i].append(field)
                elif self.block_placement[i][j] == 3:
                    field = Field((j, i))
                    turn_left = TurnLeft()
                    field.place_flat(turn_left)
                    board[i].append(field)
                elif self.block_placement[i][j] == 4:
                    field = Field((j, i))
                    turn_right = TurnRight()
                    field.place_flat(turn_right)
                    board[i].append(field)
                elif self.block_placement[i][j] == 5:
                    field = Field((j, i))
                    box = Box()
                    field.place_convex(box)
                    board[i].append(field)
                elif self.block_placement[i][j] == 6:
                    field = Field((j, i))
                    spikes = Spikes()
                    field.place_flat(spikes)
                    board[i].append(field)
                elif self.block_placement[i][j] == 7:
                    field = Field((j, i))
                    rev = Reverse()
                    field.place_flat(rev)
                    board[i].append(field)
                else:
                    board[i].append(None)

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
            if block_id == 2:
                block_type = Wall
            elif block_id == 3:
                block_type = TurnLeft
            else:
                block_type = TurnRight

            for i in range(count):
                self.available_blocks.append(block_type(cur_pane_index))
                cur_pane_index += 1

    def is_any_alive(self):
        alive = False
        for snake in self.snakes:
            alive = alive or snake.is_alive
        return alive

    def tick(self) -> int:
        if self.simulation_tick_counter == 0:
            self.backup_board()
        self.simulation_tick_counter += 1

        self.snakes[self.snake_pointer].move()

        if not self.is_any_alive():
            return -1

        self.update_snake_pointer()
        return 0

    def update_snake_pointer(self):
        if not self.is_any_alive():
            raise Exception

        self.snake_pointer += 1
        self.snake_pointer %= len(self.snakes)
        while not self.snakes[self.snake_pointer].is_alive:
            self.snake_pointer += 1
            self.snake_pointer %= len(self.snakes)

    def self_draw(self, frame):
        return self.board.self_draw(frame)

    def get_board(self):
        return self.board
