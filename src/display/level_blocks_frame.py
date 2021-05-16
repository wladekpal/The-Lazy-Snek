from .editor_frame import EditorFrame, EditorTool
from .all_blocks_frame import AllBlocksFrame, ItemWrapper

LEVEL_BLOCKS_FRAME_BACKGROUND_COLOR = (125, 125, 125)

class LevelBlocksFrame(AllBlocksFrame):

    def handle_click_erase_tool(self, pos, active_id, editor_container):
        for item in self.items:
            if item.pos_in_area(pos):
                clicked_id = item.get_id()
                editor_container.remove_available_block(clicked_id)

    TOOLS_HANDLERS = {
        EditorTool.ERASE: handle_click_erase_tool,
    }

    def __init__(self, screen, details, editor_container):
        super().__init__(screen, details)
        self.items = []
        self.editor_container = editor_container
        self.last_items_count = 0
        self.background = LEVEL_BLOCKS_FRAME_BACKGROUND_COLOR

    def refresh(self):
        items_compressed = self.editor_container.available_blocks
        if len(self.items) == self.last_items_count:
            self.items = []
            for block_id, count in items_compressed:
                for _ in range(count):
                    self.items.append(ItemWrapper(block_id))
            self.last_items_count = len(self.items)
        super().refresh(fixed_number_of_items=30)

    def handle_click(self, pos, active_tool, active_id, editor_container):
        if active_tool not in self.TOOLS_HANDLERS:
            return None
        self.TOOLS_HANDLERS[active_tool](self, pos, active_id, editor_container)
