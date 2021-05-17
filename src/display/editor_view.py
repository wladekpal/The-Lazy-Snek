from .view_controller import ApplicationView, ViewInitAction
import pygame
from .tools_frame import ToolsFrame
from .nontools_frame import NonToolsFrame
from .board_frame import BoardFrame
from .all_blocks_frame import AllBlocksFrame
from .level_blocks_frame import LevelBlocksFrame
from ..engine.editor_container import EditorContainer
from pygame import K_ESCAPE

BUTTONS_FRAME_HEIGTH_PERCENTAGE = 14
TOOLS_FRAME_WIDTH_PERCENTAGE = 74
NON_TOOLS_FRAME_WIDTH_PERCENTAGE = 26

# these 3 values must add up to 100
BOARD_FRAME_WIDTH_PERCENTAGE = 74
ALL_BLOCKS_FRAME_WIDTH_PERCENTAGE = 13
LEVEL_BLOCKS_FRAME_WIDTH_PERCENTAGE = 13
assert BOARD_FRAME_WIDTH_PERCENTAGE + ALL_BLOCKS_FRAME_WIDTH_PERCENTAGE + LEVEL_BLOCKS_FRAME_WIDTH_PERCENTAGE == 100

BOARD_FRAME_COLUMN_INDEX = 0
ALL_BLOCKS_FRAME_COLUMN_INDEX = 2
LEVEL_BLOCKS_FRAME_COLUMN_INDEX = 1

TOOLS_FRAME_COLUMN_INDEX = 0
NON_TOOLS_FRAME_COLUMN_INDEX = 1

NON_BUTTONS_FRAMES_ROW_INDEX = 0
BUTTONS_FRAME_ROW_INDEX = 1

BOARD_FRAME_DETAILS_INDEX = 0
ALL_BLOCKS_FRAME_DETAILS_INDEX = 2
LEVEL_BLOCKS_FRAME_DETAILS_INDEX = 1
TOOLS_FRAME_DETAILS_INDEX = 3
NON_TOOLS_FRAME_DETAILS_INDEX = 4

LEFT_MOUSE_BUTTON = 1

BOARD_FRAME_BACKGROUND_COLOR = (33, 47, 61)


class EditorView(ApplicationView):

    def calculate_rows_and_columns_dimensions(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        second_row_height = screen_height * BUTTONS_FRAME_HEIGTH_PERCENTAGE // 100
        lower_first_column_width = screen_width * TOOLS_FRAME_WIDTH_PERCENTAGE // 100
        lower_second_column_width = screen_width * NON_TOOLS_FRAME_WIDTH_PERCENTAGE // 100
        first_row_height = screen_height - second_row_height

        heights = [first_row_height, second_row_height]

        second_column_width = screen_width * ALL_BLOCKS_FRAME_WIDTH_PERCENTAGE // 100
        third_column_width = screen_width * LEVEL_BLOCKS_FRAME_WIDTH_PERCENTAGE // 100
        first_column_width = screen_width - (second_column_width + third_column_width)

        widths = [[first_column_width, second_column_width, third_column_width],
                  [lower_first_column_width, lower_second_column_width]]

        return [widths, heights]

    def calculate_frames_placements(self, widths, heights):
        placements = [
            (0, 0),
            (widths[NON_BUTTONS_FRAMES_ROW_INDEX][BOARD_FRAME_COLUMN_INDEX], 0),
            (widths[NON_BUTTONS_FRAMES_ROW_INDEX][BOARD_FRAME_COLUMN_INDEX] +
             widths[NON_BUTTONS_FRAMES_ROW_INDEX][LEVEL_BLOCKS_FRAME_COLUMN_INDEX], 0),
            (0, heights[NON_BUTTONS_FRAMES_ROW_INDEX]),
            (widths[BUTTONS_FRAME_ROW_INDEX][TOOLS_FRAME_COLUMN_INDEX], heights[NON_BUTTONS_FRAMES_ROW_INDEX])
        ]
        return placements

    def calculate_frames_dimensions(self, widths, heights):
        dimensions = [
            (widths[NON_BUTTONS_FRAMES_ROW_INDEX][BOARD_FRAME_COLUMN_INDEX], heights[NON_BUTTONS_FRAMES_ROW_INDEX]),
            (widths[NON_BUTTONS_FRAMES_ROW_INDEX][LEVEL_BLOCKS_FRAME_COLUMN_INDEX], heights[NON_BUTTONS_FRAMES_ROW_INDEX]),
            (widths[NON_BUTTONS_FRAMES_ROW_INDEX][ALL_BLOCKS_FRAME_COLUMN_INDEX], heights[NON_BUTTONS_FRAMES_ROW_INDEX]),
            (widths[BUTTONS_FRAME_ROW_INDEX][TOOLS_FRAME_COLUMN_INDEX], heights[BUTTONS_FRAME_ROW_INDEX]),
            (widths[BUTTONS_FRAME_ROW_INDEX][NON_TOOLS_FRAME_COLUMN_INDEX], heights[BUTTONS_FRAME_ROW_INDEX])
        ]
        return dimensions

    def calculate_frames_details(self):
        widths, heights = self.calculate_rows_and_columns_dimensions()
        placements = self.calculate_frames_placements(widths, heights)
        dimensions = self.calculate_frames_dimensions(widths, heights)
        assert len(placements) == len(dimensions)
        details = []
        for i in range(len(placements)):
            details.append((placements[i], dimensions[i]))
        return details

    def new_editor_view_frames(self):
        details = self.calculate_frames_details()
        return [
            BoardFrame(self.screen, details[BOARD_FRAME_DETAILS_INDEX], self.editor_container),
            LevelBlocksFrame(self.screen, details[ALL_BLOCKS_FRAME_DETAILS_INDEX], self.editor_container),
            AllBlocksFrame(self.screen, details[LEVEL_BLOCKS_FRAME_DETAILS_INDEX]),
            ToolsFrame(self.screen, details[TOOLS_FRAME_DETAILS_INDEX]),
            NonToolsFrame(self.screen, details[NON_TOOLS_FRAME_DETAILS_INDEX])
        ]

    def get_active_tool(self):
        return self.frames[TOOLS_FRAME_DETAILS_INDEX].get_active_tool()

    def get_active_id(self):
        return self.frames[ALL_BLOCKS_FRAME_DETAILS_INDEX].get_active_id()

    def resize_frames(self):
        details = self.calculate_frames_details()
        assert len(details) == len(self.frames)
        for i in range(len(details)):
            self.frames[i].resize(self.screen, details[i])

    def __init__(self, screen, level_data):
        super().__init__(screen)
        dimensions = (level_data[1], level_data[0])
        name = level_data[2]
        author = level_data[3]
        self.editor_container = EditorContainer(dimensions, name, author)
        self.frames = self.new_editor_view_frames()

    def refresh(self):
        self.screen.fill(BOARD_FRAME_BACKGROUND_COLOR)
        self.resize_frames()
        self.frames[-1].validate_level(self.editor_container)
        for frame in self.frames:
            frame.refresh()

    def handle_pygame_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON:
            for frame in self.frames:
                if frame.pos_in_frame_area(event.pos):
                    return frame.handle_click(frame.get_relative_pos(event.pos),
                                              self.get_active_tool(),
                                              self.get_active_id(),
                                              self.editor_container)
        elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            return (None, ViewInitAction.POP)
