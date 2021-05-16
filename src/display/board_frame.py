from .editor_frame import EditorFrame, EditorTool

BOARD_FRAME_BACKGROUND_COLOR = (25, 25, 25)


class BoardFrame(EditorFrame):

    def __init__(self, screen, details, editor_container):
        super().__init__(screen, details)
        self.editor_container = editor_container

    def handle_add_block_tool_click(self, pos, active_id, editor_container):
        editor_container.try_placing_entity(active_id, pos)

    def handle_erase_tool_click(self, pos, active_id, editor_container):
        editor_container.remove_highest_entity(pos)

    def handle_snake_creator_tool_click(self, pos, active_id, editor_container):
        editor_container.try_placing_snake(pos)

    TOOLS_HANDLERS = {
        EditorTool.ADD_BLOCK: handle_add_block_tool_click,
        EditorTool.ERASE: handle_erase_tool_click,
        EditorTool.SNAKE_CREATOR: handle_snake_creator_tool_click,
    }

    def handle_click(self, pos, active_tool, active_id, editor_container):
        if active_tool not in self.TOOLS_HANDLERS:
            return
        self.TOOLS_HANDLERS[active_tool](self, pos, active_id, editor_container)

    def refresh(self):
        self.surface.fill(BOARD_FRAME_BACKGROUND_COLOR)
        self.editor_container.self_draw(self.surface)
