
from .id_parser import EntityKind, get_entity_kind
from typing import get_type_hints
from .board import Board
from .field import Field


class EditorContainer():

    def __init__(self, dimensions, name, creator):
        self.name = name
        self.creator = creator
        self.dimensions = dimensions
        self.board = Board(self.create_entity_filled_board(dimensions, lambda: None))
        self.additional_data = self.create_entity_filled_board(dimensions, dict)
        self.block_placement_stack_matrix = self.create_entity_filled_board(dimensions, lambda: [])
        self.snakes = []
        self.available_blocks = []
        self.tags = []

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

    def try_place_snake(self, snake, position):
        pass

    def remove_highest_entity(self, position):
        field = self.board.request_field_on_screen(position)
        if field is not None and field.snake_layer is not None:
            pass
        else:
            is_removed = self.board.try_removing_highest(position)
            if is_removed:
                x, y = self.board.get_screen_position_coordinates(position)
                self.block_placement_stack_matrix[y][x].pop()

    def add_available_block(self, block_id):
        for block_data in self.available_blocks:
            if block_data[0] == block_id:
                block_data[1] += 1
                return
        self.available_blocks.append([block_id, 1])

    def get_block_placement(self):
        block_placement = []
        for row in self.block_placement_stack_matrix:
            block_placement.append([])
            for stack in row:
                block_placement[-1].append(0 if len(stack) == 0 else stack[-1])

    def get_snake_data(self):
        return []

    def convert_level_to_dictionary(self):
        dict = {
            "level_name": self.name,
            "level_creator": self.creator,
            "level_tags": self.tags,
            "block_placement": self.get_block_placement(),
            "block_additional_data": self.additional_data,
            "snake_data": self.get_snake_data(),
            "available_blocks": self.available_blocks
        }
        return dict

    def get_available_blocks(self):
        return self.available_blocks

    def self_draw(self, frame):
        self.board.self_draw(frame)
