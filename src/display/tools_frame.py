from .editor_frame import EditorFrame, EditorTool
import os
import pygame

BUTTONS_GRAPHICS_PATH = os.path.join(os.path.dirname(__file__), "../../assets/editor/")

BUTTONS_HEIGHT_PERCENTAGE = 80
MAXIMUM_BUTTONS_WIDTH_PERCENTAGE = 96
BUTTONS_INTERSPACE_PERCENTAGE = 20

TOOLS_FRAME_BACKGROUND_COLOR = (175, 175, 175)


class ToolsFrame(EditorFrame):

    def create_buttons(self):
        buttons = [
            ToolButton(EditorTool.ADD_BLOCK, 'add-to-board', active=True),
            ToolButton(EditorTool.ERASE, 'erase'),
            ToolButton(EditorTool.SNAKE_CREATOR, 'snake-creator'),
            ToolButton(EditorTool.SNAKE_CHANGE_COLOR, 'snake-change-color'),
            ToolButton(EditorTool.SNAKE_ROTATE_HEAD, 'snake-head-rotate'),
            ToolButton(EditorTool.TELEPORT_LINKER, 'teleport-linker'),
            ToolButton(EditorTool.ADD_TO_LEVEL, 'add-to-solve'),
        ]
        return buttons

    def __init__(self, screen, details):

        def find_active_tool():
            for button in self.buttons:
                if button.active:
                    self.active_tool = button.tool_type
                    return
            self.active_tool = None

        super().__init__(screen, details)
        self.buttons = self.create_buttons()
        find_active_tool()

    def set_all_buttons_inactive(self):
        for button in self.buttons:
            button.active = False

    def handle_click(self, pos, active_tool, active_id, editor_container):
        for button in self.buttons:
            if button.pos_in_area(pos):
                self.set_all_buttons_inactive()
                button.active = True
                self.active_tool = button.tool_type

    def get_active_tool(self):
        return self.active_tool

    def refresh(self):
        def calculate_buttons_dimensions_and_placement():
            all_buttons_maximum_space = self.surface.get_width() * MAXIMUM_BUTTONS_WIDTH_PERCENTAGE // 100
            number_of_buttons = len(self.buttons)
            all_buttons_percentage = number_of_buttons * 100 + (number_of_buttons - 1) * BUTTONS_INTERSPACE_PERCENTAGE
            button_maximum_width = int(all_buttons_maximum_space / all_buttons_percentage * 100)
            default_button_width = self.surface.get_height() * BUTTONS_HEIGHT_PERCENTAGE // 100
            button_width = min(button_maximum_width, default_button_width)
            buttons_interspace = int(button_width * BUTTONS_INTERSPACE_PERCENTAGE / 100)
            all_buttons_width_with_interspace = number_of_buttons * (button_width + buttons_interspace) - buttons_interspace
            first_button_x_pos = (self.surface.get_width() - all_buttons_width_with_interspace) // 2
            return (button_width, buttons_interspace, first_button_x_pos)

        def refresh_buttons():
            button_width, buttons_interspace, x_pos = calculate_buttons_dimensions_and_placement()
            y_pos = (self.surface.get_height() - button_width) // 2
            for button in self.buttons:
                button.refresh((x_pos, y_pos), button_width, self.surface)
                x_pos += button_width + buttons_interspace

        self.surface.fill(TOOLS_FRAME_BACKGROUND_COLOR)
        refresh_buttons()


class ToolButton():

    def __init__(self, tool_type, texture_name_core, active=False, tools_pool=True):
        self.active = active
        self.tool_type = tool_type
        self.active_texture = pygame.image.load(os.path.join(BUTTONS_GRAPHICS_PATH, f'{texture_name_core}-active.png'))
        self.inactive_texture = pygame.image.load(os.path.join(BUTTONS_GRAPHICS_PATH, f'{texture_name_core}-inactive.png'))
        self.side_length = None
        self.tools_pool = tools_pool

    def scale_textures(self):
        self.displayed_active_texture = pygame.transform.scale(self.active_texture, (self.side_length, self.side_length))
        self.displayed_inactive_texture = pygame.transform.scale(self.inactive_texture, (self.side_length, self.side_length))

    def refresh(self, pos, side_length, surface):
        self.pos = pos
        if self.side_length != side_length:
            self.side_length = side_length
            self.scale_textures()
        self.self_draw(surface)

    def self_draw(self, surface):
        if self.active:
            surface.blit(self.displayed_active_texture, self.pos)
        else:
            surface.blit(self.displayed_inactive_texture, self.pos)

    def pos_in_area(self, pos):
        x, y = pos
        self_x, self_y = self.pos
        return self_x <= x <= self_x + self.side_length and self_y <= y <= self_y + self.side_length
