import json


class Level:
    def __init__(self, file_name):
        self.file_name = file_name

        self.level_name = None
        self.level_creator = None
        self.block_placement = None
        self.board = None
        self.snakes = None
        self.available_blocks = None
        self.snake_pointer = 0

    def reload_level(self):
        with open(self.file_name) as json_file:
            level_description = json.load(json_file)

        self.level_name = level_description["level_name"]
        self.level_creator = level_description["level_creator"]
        self.block_placement = level_description["block_placement"]
        self.snakes = level_description["snake_data"]
        self.available_blocks = level_description["available_blocks"]
        self.snake_pointer = 0
        self.board = None
        self.convert_board()

    def convert_board(self):
        board = []
        for i in range(len(self.block_placement)):
            board.append([])
            for j in self.block_placement[i]:
                if j == 1:
                    board[i].append(Field())
                elif j == 2:
                    field = Field((j, i))
                    wall = Wall()
                    field.place_convex(wall)
                    board[i].append(field)
                else:
                    board[i].append(None)

        self.board = Board(board)

    def tick(self):
        pass
