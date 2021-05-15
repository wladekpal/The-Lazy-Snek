from .editor_frame import EditorFrame, EditorTool

LEVEL_BLOCKS_FRAME_BACKGROUND_COLOR = (125, 125, 125)


class LevelBlocksFrame(EditorFrame):

    def refresh(self):
        self.surface.fill(LEVEL_BLOCKS_FRAME_BACKGROUND_COLOR)

    def handle_example_tool_click(self, pos):
        pass

    TOOLS_HANDLERS = {
        EditorTool.EXAMPLE: handle_example_tool_click
    }

    def handle_click(self, pos, active_tool, active_id, editor_container):
        if active_tool not in self.TOOLS_HANDLERS:
            return None
        self.TOOLS_HANDLERS[active_tool](pos)
