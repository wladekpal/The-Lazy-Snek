from .item import Item


ITEMS_INTERSPACE = 20
MAXIMUM_ITEM_WIDTH_PERCENTAGE = 80


class BlocksPane():

    class ItemArea():

        def __init__(self, pos, side_length, block):
            self.pos = pos
            self.side_length = side_length
            self.block = block

        def handle_click(self, pos):

            def is_click_in_area(pos):
                x_fits = self.pos[0] <= pos[0] <= self.pos[0] + self.side_length
                y_fits = self.pos[1] <= pos[1] <= self.pos[1] + self.side_length
                return x_fits and y_fits

            return self.block if is_click_in_area(pos) else None

        def self_draw(self, screen):
            self.block.self_draw(screen, self.pos, self.side_length)

    def __init__(self, board, blocks, level_view):
        self.board = board
        self.blocks = blocks
        self.level_view = level_view
        self.item_areas = None
        self.inactive_index = None
        self.side_length = None

    def self_draw(self, screen, items_frame, block_side_length):

        self.side_length = block_side_length

        def create_top_lefts(main_frame, own_frame, block_side_length):

            block_side_length = min(own_frame.get_width() * MAXIMUM_ITEM_WIDTH_PERCENTAGE // 100, block_side_length)
            n = len(self.blocks)
            x = main_frame.get_width() - (own_frame.get_width() // 2) - block_side_length // 2
            y = own_frame.get_height() // 2 - block_side_length // 2
            y_offset = (n - 1) * (block_side_length + ITEMS_INTERSPACE) // 2
            y -= y_offset
            top_lefts = []
            while len(top_lefts) < len(self.blocks):
                top_lefts.append((x, y))
                y += block_side_length + ITEMS_INTERSPACE
            return top_lefts

        top_lefts = create_top_lefts(screen, items_frame, block_side_length)

        self.item_areas = []

        for i in range(len(top_lefts)):
            item_area = self.ItemArea(top_lefts[i], block_side_length, self.blocks[i])
            self.item_areas.append(item_area)

        for i in range(len(self.item_areas)):
            if i != self.inactive_index:
                self.item_areas[i].self_draw(screen)

    def handle_click(self, pos):
        for i in range(len(self.item_areas)):
            clicked_block = self.item_areas[i].handle_click(pos)
            if clicked_block is not None and i != self.inactive_index:
                x_offset = pos[0] - self.item_areas[i].pos[0]
                y_offset = pos[1] - self.item_areas[i].pos[1]
                item = Item(self.blocks[i], self.level_view, pos, (x_offset, y_offset), self.side_length)
                self.level_view.flowing_item = item
                self.inactive_index = i

    def notify_flowing_block_placed(self):
        if self.inactive_index is not None:
            del self.blocks[self.inactive_index]
            self.inactive_index = None

    def return_block(self, block):
        index = 0
        while index < len(self.blocks) and self.blocks[index].pane_index < block.pane_index:
            index += 1
        self.blocks.insert(index, block)

    def set_available_blocks(self, blocks):
        self.blocks = blocks
        self.inactive_index = None
