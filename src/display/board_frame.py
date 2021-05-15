from src.engine.editor_container import EditorContainer
from .editor_frame import EditorFrame, EditorTool

BOARD_FRAME_BACKGROUND_COLOR = (25, 25, 25)


class BoardFrame(EditorFrame):

    def __init__(self, screen, details):
        super().__init__(screen, details)
        self.editor_container = EditorContainer((10, 10), "abba", "ojcze")

    def handle_example_tool_click(self, pos):
        pass

    TOOLS_HANDLERS = {
        EditorTool.EXAMPLE: handle_example_tool_click
    }

    def handle_click(self, pos, active_tool, active_id):
        # if active_tool not in self.TOOLS_HANDLERS:
        #     return None
        # self.TOOLS_HANDLERS[active_tool](pos)
        if not self.editor_container.try_placing_entity(active_id, pos):
            self.editor_container.remove_highest_entity(pos)


    def refresh(self):
        self.surface.fill(BOARD_FRAME_BACKGROUND_COLOR)
        self.editor_container.self_draw(self.surface)
