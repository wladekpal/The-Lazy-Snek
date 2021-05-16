from abc import ABCMeta, abstractmethod
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
MAX_TEXT_LENGTH = 15
TEXT_COLOR = (0, 0, 0)
OPAQUE_TEXT_COLOR = (60, 65, 66)


class UnsupportedEvent(Exception):
    pass


class InputBox(metaclass=ABCMeta):
    def __init__(self):
        self.color = INPUT_BOX_COLOR
        self.is_focused = False
        self.input_text = ''
        self.pos = (0, 0)
        self.width, self.height = (0, 0)

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

    @abstractmethod
    def handle_key(self, event):
        pass

    @abstractmethod
    def get_value(self):
        pass


class NumberInputBox(InputBox):
    def handle_key(self, event):
        if event.type != KEYDOWN:
            raise UnsupportedEvent

        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif len(self.input_text) < 2 and event.unicode >= '0' and event.unicode <= '9':
            self.input_text += event.unicode

    def get_value(self):
        if self.input_text == '':
            return None

        value = int(self.input_text)
        if value > 0 and value <= MAX_LEVEL_SIZE:
            return value
        else:
            return None


class TextInputBox(InputBox):
    def handle_key(self, event):
        if event.type != KEYDOWN:
            raise UnsupportedEvent

        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif len(self.input_text) < MAX_TEXT_LENGTH:
            self.input_text += event.unicode

    def get_value(self):
        if self.input_text == '':
            return None

        return self.input_text


class SubmitButton():
    def __init__(self, inputs):
        self.inputs = inputs

    def self_draw(self, frame, pos, dimensions):
        self.pos = pos
        self.width, self.height = dimensions
        rectangle = pygame.Rect(pos, dimensions)
        value_list = [input.get_value() for input in self.inputs]
        if all(value_list):
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

    def action(self, level_data):
        return (EditorView(pygame.display.get_surface(), level_data), ViewInitAction.REPLACE)

    def handle_click(self, pos):
        self_x, self_y = self.pos
        mouse_x, mouse_y = pos
        if self_x <= mouse_x <= self_x + self.width and self_y <= mouse_y <= self_y + self.height:
            level_data = [input.get_value() for input in self.inputs]
            if all(level_data):
                return self.action(level_data)

        return None


class EditorSizeView(ApplicationView):
    def __init__(self, screen):
        super().__init__(screen)
        self.width_input = NumberInputBox()
        self.height_input = NumberInputBox()
        self.name_input = TextInputBox()
        self.author_input = TextInputBox()
        self.submit = SubmitButton([self.width_input, self.height_input, self.name_input, self.author_input])
        self.focused_input = None

    def handle_pygame_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON:
            width_input_selector = self.width_input.handle_click(event.pos)
            height_input_selector = self.height_input.handle_click(event.pos)
            name_input_selector = self.name_input.handle_click(event.pos)
            author_input_selector = self.author_input.handle_click(event.pos)
            self.focused_input = width_input_selector or height_input_selector or name_input_selector or author_input_selector
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

        name_text = font.render('Level name:', True, TEXT_COLOR)
        name_text_box = name_text.get_rect(center=(frame_width * 0.5, frame_height * 0.5))
        name_text_box.right = frame_width * 0.5

        author_text = font.render('Author name:', True, TEXT_COLOR)
        author_text_box = author_text.get_rect(center=(frame_width * 0.5, frame_height * 0.6))
        author_text_box.right = frame_width * 0.5

        background.fill(BACKGROUND_COLOR)
        self.screen.blit(instruction_text, instruction_text_box)
        self.screen.blit(height_text, height_text_box)
        self.screen.blit(width_text, width_text_box)
        self.screen.blit(name_text, name_text_box)
        self.screen.blit(author_text, author_text_box)
        self.height_input.self_draw(self.screen, (frame_width * 0.5, frame_height * 0.3 - 25), (75, 50))
        self.width_input.self_draw(self.screen, (frame_width * 0.5, frame_height * 0.4 - 25), (75, 50))
        self.name_input.self_draw(self.screen, (frame_width * 0.5, frame_height * 0.5 - 25), (700, 50))
        self.author_input.self_draw(self.screen, (frame_width * 0.5, frame_height * 0.6 - 25), (700, 50))
        self.submit.self_draw(self.screen, (frame_width * 0.5 - 150, frame_height * 0.7), (300, 50))
