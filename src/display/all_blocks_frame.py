from .editor_frame import EditorFrame, EditorTool
from ..engine.id_parser import get_all_ids, EntityKind, get_entity_kind, get_block_from_id, get_field_from_id
import os
import pygame

ALL_BLOCKS_FRAME_BACKGROUND_COLOR = (75, 75, 75)
MAXIMUM_COLUMNS = 6
ITEMS_INTERSPACE = 5
ACTIVE_TEXTURE_PATH = os.path.join("assets/editor/active.png")

INVALID_LEVEL_AVAILABLE_BLOCKS_IDS = [1, 17, 18, 19, 20, 26, 2, 10, 11, 12, 13]

MAX_ITEM_SIZE = 30


class AllBlocksFrame(EditorFrame):

    def __init__(self, screen, details):

        super().__init__(screen, details)
        self.active_id = None
        self.items = [ItemWrapper(id) for id in get_all_ids()]
        self.background = ALL_BLOCKS_FRAME_BACKGROUND_COLOR

    def get_active_id(self):
        return self.active_id

    def refresh(self, fixed_number_of_items=1):

        def best_columns_number(number_of_items):

            def side_length_for_columns_number(columns_number, items_number):
                items_in_column = (items_number + columns_number - 1) // columns_number
                width_interspace = ITEMS_INTERSPACE * (columns_number + 1)
                height_interspace = ITEMS_INTERSPACE * (items_in_column + 1)
                width_space = self.surface.get_width() - width_interspace
                height_space = self.surface.get_height() - height_interspace
                max_width = width_space // columns_number
                max_height = height_space // items_in_column
                return min(max_width, max_height)

            best_side_length = -1
            best_columns = -1
            for i in range(1, MAXIMUM_COLUMNS + 1):
                side_length = side_length_for_columns_number(i, number_of_items)
                if side_length > best_side_length:
                    best_side_length = side_length
                    best_columns = i

            return (best_columns, best_side_length)

        def calculate_placements():

            def create_placements(number_of_columns, number_of_items, item_side_length):
                x_pos = (self.surface.get_width() - number_of_columns * (item_side_length + ITEMS_INTERSPACE)) // 2
                y_pos = ITEMS_INTERSPACE
                placements = []
                items_in_column = (number_of_items + number_of_columns - 1) // number_of_columns
                for _ in range(number_of_columns):
                    for _ in range(items_in_column):
                        placements.append((x_pos, y_pos))
                        y_pos += item_side_length + ITEMS_INTERSPACE
                    x_pos += item_side_length + ITEMS_INTERSPACE
                    y_pos = ITEMS_INTERSPACE
                return placements[:number_of_items]

            number_of_items = max(len(self.items), fixed_number_of_items)
            number_of_columns, item_side_length = best_columns_number(number_of_items)
            return (create_placements(number_of_columns, number_of_items, item_side_length), item_side_length)

        placements, side_length = calculate_placements()
        self.surface.fill(self.background)
        for i in range(len(self.items)):
            self.items[i].self_draw(placements[i], side_length, self.surface)

    def add_to_level_handler(self, pos, active_id, editor_container):
        for item in self.items:
            if item.pos_in_area(pos):
                clicked_id = item.get_id()
                if clicked_id not in INVALID_LEVEL_AVAILABLE_BLOCKS_IDS:
                    if len(self.items) < MAX_ITEM_SIZE:
                        editor_container.add_available_block(clicked_id)

    TOOLS_HANDLERS = {
        EditorTool.ADD_TO_LEVEL: add_to_level_handler,
    }

    def set_all_items_inactive(self):
        for item in self.items:
            item.set_inactive()

    def default_click_handler(self, pos):
        for item in self.items:
            if item.pos_in_area(pos):
                self.set_all_items_inactive()
                item.set_active()
                self.active_id = item.get_id()
                return

    def handle_click(self, pos, active_tool, active_id, editor_container):
        if active_tool not in self.TOOLS_HANDLERS:
            self.default_click_handler(pos)
            return None
        self.TOOLS_HANDLERS[active_tool](self, pos, active_id, editor_container)


class ItemWrapper():

    def refresh_active_texture(self, size):
        if self.active_texture_size != size:
            self.active_texture = pygame.transform.scale(self.active_texture_base, (size, size))

    def __init__(self, item_id):
        kind = get_entity_kind(item_id)
        if kind == EntityKind.BLOCK:
            self.wrapped_entity = get_block_from_id(item_id)
        elif kind == EntityKind.FIELD:
            self.wrapped_entity = get_field_from_id(item_id)
        else:
            raise ValueError
        self.active = False
        self.active_texture_size = None
        self.active_texture_base = pygame.image.load(ACTIVE_TEXTURE_PATH)
        self.id = item_id

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def get_id(self):
        return self.id

    def pos_in_area(self, pos):
        self_x, self_y = self.pos
        x, y = pos
        return self_x <= x <= self_x + self.side_length and self_y <= y <= self_y + self.side_length

    def self_draw(self, pos, side_length, surface):
        self.pos = pos
        self.side_length = side_length
        self.wrapped_entity.self_draw(surface, pos, side_length)
        if self.active:
            self.refresh_active_texture(side_length)
            surface.blit(self.active_texture, pos)
