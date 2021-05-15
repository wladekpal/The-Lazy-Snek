from .editor_frame import EditorFrame, EditorTool

BOARD_FRAME_BACKGROUND_COLOR = (25, 25, 25)


class BoardFrame(EditorFrame):

    def handle_example_tool_click(self, pos):
        pass

    TOOLS_HANDLERS = {
        EditorTool.EXAMPLE: handle_example_tool_click
    }

    def handle_click(self, pos, active_tool, active_id):
        if active_tool not in self.TOOLS_HANDLERS:
            return None
        self.TOOLS_HANDLERS[active_tool](pos)

    def refresh(self):
        self.surface.fill(BOARD_FRAME_BACKGROUND_COLOR)
