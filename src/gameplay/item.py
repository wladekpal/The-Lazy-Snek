

class Item():

    def __init__(self, block, level_view, pos, offset, side_length):
        self.block = block
        self.pos = pos
        self.offset = offset
        self.level_view = level_view
        self.side_length = side_length
        self.pos = self.apply_offset(self.pos)

    def apply_offset(self, pos):
        return (pos[0] - self.offset[0], pos[1] - self.offset[1])

    def self_draw(self, frame):
        self.block.self_draw(frame, self.pos, self.side_length)

    def handle_motion(self, pos):
        self.pos = self.apply_offset(pos)

    def handle_unclick(self, pos):
        field_to_place = self.level_view.level.board.request_field_on_screen(pos)
        if field_to_place is not None:
            block_placed = field_to_place.try_placing(self.block)
            if block_placed:
                self.level_view.blocks_pane.notify_flowing_block_placed()
                self.level_view.flowing_item = None
                return
        # block placing unsuccessful, returning to block pane
        if self.level_view.blocks_pane.inactive_index is None:
            # block was dragged from board
            self.level_view.blocks_pane.return_block(self.block)
            self.level_view.flowing_item = None
        else:
            # block was dragged from block pane
            self.level_view.blocks_pane.inactive_index = None
            self.level_view.flowing_item = None
