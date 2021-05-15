from .view_controller import ApplicationView
import enum
import pygame
from abc import ABCMeta, abstractmethod

BUTTONS_FRAME_HEIGTH_PERCENTAGE = 18

# these 3 values must add up to 100
BOARD_FRAME_WIDTH_PERCENTAGE = 70
ALL_BLOCKS_FRAME_WIDTH_PERCENTAGE = 15
LEVEL_BLOCKS_FRAME_WIDTH_PERCENTAGE = 15
assert BOARD_FRAME_WIDTH_PERCENTAGE + ALL_BLOCKS_FRAME_WIDTH_PERCENTAGE + LEVEL_BLOCKS_FRAME_WIDTH_PERCENTAGE == 100

BOARD_FRAME_BACKGROUND_COLOR = (25, 25, 25)
ALL_BLOCKS_FRAME_BACKGROUND_COLOR = (75, 75, 75)
LEVEL_BLOCKS_FRAME_BACKGROUND_COLOR = (125, 125, 125)
TOOLS_FRAME_BACKGROUND_COLOR = (175, 175, 175)

BOARD_FRAME_COLUMN_INDEX = 0
ALL_BLOCKS_FRAME_COLUMN_INDEX = 1
LEVEL_BLOCKS_FRAME_COLUMN_INDEX = 2

NON_TOOLS_FRAMES_ROW_INDEX = 0
TOOLS_FRAME_ROW_INDEX = 1

BOARD_FRAME_DETAILS_INDEX = 0
ALL_BLOCKS_FRAME_DETAILS_INDEX = 1
LEVEL_BLOCKS_FRAME_DETAILS_INDEX = 2
TOOLS_FRAME_DETAILS_INDEX = 3


# types of active editor tools
class EditorToolType(enum.Enum):
    pass


class EditorView(ApplicationView):

    def calculate_rows_and_columns_dimensions(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        second_row_height = screen_height * BUTTONS_FRAME_HEIGTH_PERCENTAGE // 100
        first_row_height = screen_height - second_row_height

        heights = [first_row_height, second_row_height]

        second_column_width = screen_width * ALL_BLOCKS_FRAME_WIDTH_PERCENTAGE // 100
        third_column_width = screen_width * LEVEL_BLOCKS_FRAME_WIDTH_PERCENTAGE // 100
        first_column_width = screen_width - (second_column_width + third_column_width)

        widths = [first_column_width, second_column_width, third_column_width]

        return [widths, heights]

    def calculate_frames_placements(self, widths, heights):
        placements = [
            (0, 0),
            (widths[BOARD_FRAME_COLUMN_INDEX], 0),
            (widths[BOARD_FRAME_COLUMN_INDEX] + widths[ALL_BLOCKS_FRAME_COLUMN_INDEX], 0),
            (0, heights[NON_TOOLS_FRAMES_ROW_INDEX])
        ]
        return placements

    def calculate_frames_dimensions(self, widths, heights):
        dimensions = [
            (widths[BOARD_FRAME_COLUMN_INDEX], heights[NON_TOOLS_FRAMES_ROW_INDEX]),
            (widths[ALL_BLOCKS_FRAME_COLUMN_INDEX], heights[NON_TOOLS_FRAMES_ROW_INDEX]),
            (widths[LEVEL_BLOCKS_FRAME_COLUMN_INDEX], heights[NON_TOOLS_FRAMES_ROW_INDEX]),
            (self.screen.get_width(), heights[TOOLS_FRAME_ROW_INDEX])
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
            BoardFrame(self.screen, details[BOARD_FRAME_DETAILS_INDEX]),
            AllBlocksFrame(self.screen, details[ALL_BLOCKS_FRAME_DETAILS_INDEX]),
            LevelBlocksFrame(self.screen, details[LEVEL_BLOCKS_FRAME_DETAILS_INDEX]),
            ToolsFrame(self.screen, details[TOOLS_FRAME_DETAILS_INDEX]),
        ]

    def resize_frames(self):
        details = self.calculate_frames_details()
        assert len(details) == len(self.frames)
        for i in range(len(details)):
            self.frames[i].resize(self.screen, details[i])

    def __init__(self, screen, level_dimensions):
        super().__init__(screen)
        self.frames = self.new_editor_view_frames()

    def refresh(self):
        self.screen.fill((21, 37, 69))
        self.resize_frames()
        for frame in self.frames:
            frame.refresh()

    def handle_pygame_event(self, event):
        pass


class EditorFrame(metaclass=ABCMeta):

    def __init__(self, screen, details):
        self.resize(screen, details)

    def resize(self, screen, details):
        position, dimensions = details
        self.position = position
        self.width, self.height = dimensions
        x, y = self.position
        self.surface = screen.subsurface(pygame.Rect(x, y, self.width, self.height))

    def pos_in_frame_area(self, pos):
        x, y = pos
        self_x, self_y = self.position
        return self_x <= x <= self_x + self.width and self_y <= y <= self_y + self.height

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def refresh(self):
        pass


class BoardFrame(EditorFrame):

    def handle_event(self, event):
        pass

    def refresh(self):
        self.surface.fill(BOARD_FRAME_BACKGROUND_COLOR)


class AllBlocksFrame(EditorFrame):

    def handle_event(self, event):
        pass

    def refresh(self):
        self.surface.fill(ALL_BLOCKS_FRAME_BACKGROUND_COLOR)


class LevelBlocksFrame(EditorFrame):

    def handle_event(self, event):
        pass

    def refresh(self):
        self.surface.fill(LEVEL_BLOCKS_FRAME_BACKGROUND_COLOR)


class ToolsFrame(EditorFrame):

    def handle_event(self, event):
        pass

    def refresh(self):
        self.surface.fill(TOOLS_FRAME_BACKGROUND_COLOR)
