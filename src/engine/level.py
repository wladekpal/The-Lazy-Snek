import json
from .blocks import Wall, TurnLeft, TurnRight
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
        self.available_blocks = self.level_description["available_blocks"]

        self.snake_pointer = 0
        self.board = None
        self.snakes = None

        self.convert_board()
        self.convert_snakes()

    def reload_level(self):
        self.level_name = self.level_description["level_name"]
        self.level_creator = self.level_description["level_creator"]
        self.block_placement = self.level_description["block_placement"]
        self.snake_data = self.level_description["snake_data"]
        self.available_blocks = self.level_description["available_blocks"]

        self.snake_pointer = 0
        self.board = None
        self.snakes = None

        self.convert_board()
        self.convert_snakes()

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

    def is_any_alive(self):
        alive = False
        for snake in self.snakes:
            alive = alive or snake.is_alive
        return alive

    def tick(self) -> int:
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
        self.board.self_draw(frame)
