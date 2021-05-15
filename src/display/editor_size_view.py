from src.display.level_view import LEFT_MOUSE_BUTTON
import pygame
from pygame.constants import KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN
from .view_controller import ApplicationView, ViewInitAction
from .editor_view import EditorView

BACKGROUND_COLOR = (207, 207, 207)
INPUT_BOX_COLOR = (255, 255, 255)
INPUT_BOX_COLOR_SELECTED = (100, 100, 100)
TILE_BACKGROUND_COLOR = (1, 167, 194)
OPAQUE_TILE_BACKGROUND_COLOR = (140, 157, 163)
MAX_LEVEL_SIZE = 50
TEXT_COLOR = (0, 0, 0)
OPAQUE_TEXT_COLOR = (60, 65, 66)


class UnsupportedEvent(Exception):
    pass


class InputBox():
    def __init__(self):
        self.color = INPUT_BOX_COLOR
        self.is_focused = False
        self.input_text = ''

    def self_draw(self, frame, pos, dimensions):
        self.pos = pos
        self.width, self.height = dimensions
        rectangle = pygame.Rect(pos, dimensions)
        font = pygame.font.Font(pygame.font.get_default_font(), 50)
        text = font.render(self.input_text, True, TEXT_COLOR)
        text_box = text.get_rect(center=rectangle.center)
        pygame.draw.rect(frame, self.color, rectangle)
        frame.blit(text, text_box)

    def handle_click(self, pos):
        self_x, self_y = self.pos
        mouse_x, mouse_y = pos

        if self_x <= mouse_x <= self_x + self.width and self_y <= mouse_y <= self_y + self.height:
            self.color = INPUT_BOX_COLOR_SELECTED
            self.is_focused = True
        else:
            self.color = INPUT_BOX_COLOR
            self.is_focused = False

        return self if self.is_focused else None

    def handle_key(self, event):
        if event.type != KEYDOWN:
            raise UnsupportedEvent

        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        else:
            if len(self.input_text) < 2 and event.unicode >= '0' and event.unicode <= '9':
                self.input_text += event.unicode

    def get_value(self):
        if self.input_text == '':
            return None

        value = int(self.input_text)
        if value > 0 and value <= MAX_LEVEL_SIZE:
            return value
        else:
            return None


class SubmitButton():
    def __init__(self, width_input, height_input):
        self.width_input = width_input
        self.height_input = height_input

    def action(self, width_value, height_value):
        level_dimensions = (height_value, width_value)
        return (EditorView(pygame.display.get_surface(), level_dimensions), ViewInitAction.EMPTY_STACK)

    def self_draw(self, frame, pos, dimensions):
        self.pos = pos
        self.width, self.height = dimensions
        rectangle = pygame.Rect(pos, dimensions)
        width_value = self.width_input.get_value()
        height_value = self.height_input.get_value()
        if width_value and height_value:
            tile_color = TILE_BACKGROUND_COLOR
            text_color = TEXT_COLOR
        else:
            tile_color = OPAQUE_TILE_BACKGROUND_COLOR
            text_color = OPAQUE_TEXT_COLOR

        pygame.draw.rect(frame, tile_color, rectangle)
        text_font = pygame.font.Font(pygame.font.get_default_font(), 50)
        text = text_font.render('Create level', True, text_color)
        text_rectangle = text.get_rect()
        text_rectangle.center = rectangle.center
        frame.blit(text, text_rectangle)

    def handle_click(self, pos):
        self_x, self_y = self.pos
        mouse_x, mouse_y = pos
        if self_x <= mouse_x <= self_x + self.width and self_y <= mouse_y <= self_y + self.height:
            width_value = self.width_input.get_value()
            height_value = self.height_input.get_value()
            if width_value and height_value:
                return self.action(width_value, height_value)

        return None


class EditorSizeView(ApplicationView):
    def __init__(self, screen):
        super().__init__(screen)
        self.width_input = InputBox()
        self.height_input = InputBox()
        self.submit = SubmitButton(self.width_input, self.height_input)
        self.focused_input = None

    def handle_pygame_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON:
            width_input_selector = self.width_input.handle_click(event.pos)
            height_input_selector = self.height_input.handle_click(event.pos)
            self.focused_input = width_input_selector or height_input_selector
            submit_return = self.submit.handle_click(event.pos)
            if submit_return:
                return submit_return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            return (None, ViewInitAction.POP)
        elif event.type == KEYDOWN and self.focused_input is not None:
            self.focused_input.handle_key(event)

    def refresh(self):
        frame_width = self.screen.get_width()
        frame_height = self.screen.get_height()
        background = self.screen.subsurface(pygame.Rect(0, 0, frame_width, frame_height))

        font = pygame.font.Font(pygame.font.get_default_font(), 50)
        instruction_text = font.render('Input new level size:', True, TEXT_COLOR)
        instruction_text_box = instruction_text.get_rect(center=(frame_width * 0.5, frame_height * 0.2))

        height_text = font.render('Height:', True, TEXT_COLOR)
        height_text_box = height_text.get_rect(center=(frame_width * 0.5, frame_height * 0.3))
        height_text_box.right = frame_width * 0.5

        width_text = font.render('Width:', True, TEXT_COLOR)
        width_text_box = width_text.get_rect(center=(frame_width * 0.5, frame_height * 0.4))
        width_text_box.right = frame_width * 0.5

        background.fill(BACKGROUND_COLOR)
        self.screen.blit(instruction_text, instruction_text_box)
        self.screen.blit(height_text, height_text_box)
        self.screen.blit(width_text, width_text_box)
        self.height_input.self_draw(self.screen, (frame_width * 0.5, frame_height * 0.3 - 25), (75, 50))
        self.width_input.self_draw(self.screen, (frame_width * 0.5, frame_height * 0.4 - 25), (75, 50))
        self.submit.self_draw(self.screen, (frame_width * 0.5 - 150, frame_height * 0.5), (300, 50))
