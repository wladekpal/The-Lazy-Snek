import json
from src.engine.blocks import Block, Wall
from src.engine.field import Field


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
            for j in self.block_placement[i]:
                if j == 1:
                    board[i].append(Field((j, i)))
                elif j == 2:
                    field = Field((j, i))
                    wall = Wall()
                    field.place_convex(wall)
                    board[i].append(field)
                else:
                    board[i].append(None)

        self.board = Board(board)

    def convert_snakes(self):
        self.snakes = []
        for snake_d in self.snake_data:
            snake = Snake(
                snake_d["placement"],
                snake_d["color"],
                snake_d["direction"],
                self.board
            )
            self.snakes.append(snake)

    def tick(self) -> bool:
        self.snakes[self.snake_pointer].move()
        self.snake_pointer += 1
        self.snake_pointer %= len(self.snakes)

        for snake in self.snakes:
            if not snake.is_alive:
                return False
        return True

    def self_draw(self, frame, x, y, side_length):
        self.board.self_draw(frame, x, y, side_length)
