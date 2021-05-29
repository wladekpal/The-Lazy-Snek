import pygame
from .view_controller import ApplicationView, ViewInitAction
from .editor_size_view import EditorSizeView
from .level_view import EditorLevelView, LevelView
from .file_explorer import import_level
from ..engine.level_validator import level_validator
from abc import ABCMeta
import json
import os
from ..engine.level import Level
from pygame.locals import K_ESCAPE

TITLE_FRAME_HEIGHT_PERCENTAGE = 20
TITLE_HEIGHT_PERCENTAGE_IN_TITLE_FRAME = 60
TILE_WIDTH_MAX_PERCENTAGE = 50
TILE_WIDTH = 600
TILE_HEIGHT_MAX_PERCENTAGE = 70
TILE_HEIGHT = 100
TILES_INTERSPACE = 30
TEXT_TILE_HEIGHT_PERCENTAGE = 50

TITLE_FRAME_BACKGROUND_COLOR = (207, 207, 207)
TITLE_TEXT_COLOR = (0, 112, 144)
TILES_FRAME_BACKGROUND_COLOR = (207, 207, 207)
TILE_BACKGROUND_COLOR = (1, 167, 194)
TILE_TEXT_COLOR = (0, 0, 0)
INVALID_LEVEL_TEXT_COLOR = (255, 0, 0)

LEFT_MOUSE_BUTTON = 1
SCROLL_UP = 4
SCROLL_DOWN = 5

FRAMES_PER_SIMULATION_TICK = 8

BASE_LEVELS_PATH = os.path.join(os.path.dirname(__file__), "../../levels/base")
CUSTOM_LEVELS_PATH = os.path.join(os.path.dirname(__file__), "../../levels/custom")


class PickView(ApplicationView):

    def __init__(self, screen, title, tiles):
        super().__init__(screen)

        self.cached_screen_width = None
        self.cached_screen_height = None
        self.title = title
        self.tiles = tiles
        self.first_tile_index = 0
        self.current_tiles_capacity = 0

    def create_title_frame(self):
        frame_width = self.screen.get_width()
        frame_height = self.screen.get_height() * TITLE_FRAME_HEIGHT_PERCENTAGE // 100
        return self.screen.subsurface(pygame.Rect(0, 0, frame_width, frame_height))

    def create_tiles_frame(self):
        frame_width = self.screen.get_width()
        frame_height = self.screen.get_height() - self.title_frame.get_height()
        return self.screen.subsurface(pygame.Rect(0, self.title_frame.get_height(), frame_width, frame_height))

    def refresh_title(self):
        font_size = self.title_frame.get_height() * TITLE_HEIGHT_PERCENTAGE_IN_TITLE_FRAME // 100
        title_font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        text = title_font.render(self.title, True, TITLE_TEXT_COLOR)
        text_rectangle = text.get_rect()
        text_rectangle.center = self.title_frame.get_rect().center
        self.title_frame.blit(text, text_rectangle)

    def refresh_tiles(self):
        width = min(TILE_WIDTH, self.tiles_frame.get_width() * TILE_WIDTH_MAX_PERCENTAGE // 100)
        height = min(TILE_HEIGHT, self.tiles_frame.get_height() * TILE_HEIGHT_MAX_PERCENTAGE // 100)
        self.current_tiles_capacity = min(1 + (self.tiles_frame.get_height() - height) // (height + TILES_INTERSPACE),
                                          len(self.tiles))
        number_of_tiles = self.current_tiles_capacity
        self.first_tile_index = min(self.first_tile_index, len(self.tiles) - self.current_tiles_capacity)
        all_tiles_height = number_of_tiles * (height + TILES_INTERSPACE) - TILES_INTERSPACE
        x, y = self.tiles_frame.get_rect().center
        next_point = (x - width // 2, y - all_tiles_height // 2)
        for tile in self.tiles:
            tile.pos = None
        for tile in self.tiles[self.first_tile_index:self.first_tile_index + self.current_tiles_capacity]:
            tile.self_draw(self.tiles_frame, next_point, (width, height))
            old_x, old_y = next_point
            next_point = (old_x, old_y + height + TILES_INTERSPACE)

    def force_refresh(self):
        self.cached_screen_height = None
        self.cached_screen_width = None
        self.refresh()

    def refresh(self):
        if self.cached_screen_width and self.cached_screen_height:
            if self.cached_screen_width == self.screen.get_width() and self.cached_screen_height == self.screen.get_height():
                return

        self.cached_screen_height = self.screen.get_height()
        self.cached_screen_width = self.screen.get_width()

        self.title_frame = self.create_title_frame()
        self.tiles_frame = self.create_tiles_frame()
        self.refresh_tiles()

        self.title_frame.fill(TITLE_FRAME_BACKGROUND_COLOR)
        self.tiles_frame.fill(TILES_FRAME_BACKGROUND_COLOR)
        self.refresh_title()
        self.refresh_tiles()

    def handle_scrollup(self):
        self.first_tile_index = max(0, self.first_tile_index - self.current_tiles_capacity)

    def handle_scrolldown(self):
        self.first_tile_index = min(len(self.tiles) - self.current_tiles_capacity,
                                    self.first_tile_index + self.current_tiles_capacity)

    def handle_pygame_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON:
            for tile in self.tiles:
                x, y = event.pos
                view = tile.handle_click((x, y - self.title_frame.get_height()))
                if view:
                    return view
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == SCROLL_UP:
            self.handle_scrollup()
            self.force_refresh()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == SCROLL_DOWN:
            self.handle_scrolldown()
            self.force_refresh()


class MenuView(PickView):

    def __init__(self, screen):

        tiles = [
            PickLevelViewTile('Base levels', screen),
            CustomLevelsTile('Custom levels', screen),
            LevelEditorTile('Level editor', screen),
            QuitTile('Quit game'),
        ]

        title = 'The Lazy Snek'

        super().__init__(screen, title, tiles)

    def restore(self):
        self.force_refresh()


class LevelSubmenuView(PickView):

    def __init__(self, screen):

        tiles = [
            GoBackTile('Resume level'),
            PickLevelViewTile('Choose another level', screen),
            MenuTile('Main menu', screen),
            QuitTile('Quit game'),
        ]

        title = 'Level paused'

        super().__init__(screen, title, tiles)

    def handle_pygame_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            return (None, ViewInitAction.POP)
        else:
            return super().handle_pygame_event(event)


class Tile(metaclass=ABCMeta):
    def __init__(self, text):
        self.text = text

    @staticmethod
    def action(self):
        pass

    def self_draw(self, frame, pos, dimensions):
        self.pos = pos
        self.width, self.height = dimensions
        rectangle = pygame.Rect(pos, dimensions)
        pygame.draw.rect(frame, TILE_BACKGROUND_COLOR, rectangle)
        text_font = pygame.font.Font(pygame.font.get_default_font(),
                                     self.height * TEXT_TILE_HEIGHT_PERCENTAGE // 100)
        text = text_font.render(self.text, True, TILE_TEXT_COLOR)
        text_rectangle = text.get_rect()
        text_rectangle.center = rectangle.center
        frame.blit(text, text_rectangle)

    def handle_click(self, pos):
        if self.pos is None:
            return None
        self_x, self_y = self.pos
        mouse_x, mouse_y = pos
        if self_x <= mouse_x <= self_x + self.width and self_y <= mouse_y <= self_y + self.height:
            return self.action()
        else:
            return None


class QuitTile(Tile):

    def action(self):
        pygame.quit()
        exit()


class PickLevelViewTile(Tile):

    def __init__(self, text, screen):
        self.screen = screen
        super().__init__(text)

    def action(self):
        return (PickLevelView(self.screen), ViewInitAction.EMPTY_STACK)


class LevelEditorTile(Tile):
    def __init__(self, text, screen):
        self.screen = screen
        super().__init__(text)

    def action(self):
        return (EditorSizeView(self.screen), ViewInitAction.PUSH)


# temporary class to display example tiles that will be implemented in the future
class DummyTile(Tile):

    def action(self):
        pass


class MenuTile(Tile):

    def __init__(self, text, screen):
        self.screen = screen
        super().__init__(text)

    def action(self):
        return (MenuView(self.screen), ViewInitAction.EMPTY_STACK)


class PickLevelView(PickView):

    def __init__(self, screen):

        tiles = [
            MenuTile('Back to menu', screen)
        ]

        for file in os.listdir(BASE_LEVELS_PATH):
            level_path = os.path.join(BASE_LEVELS_PATH, file)
            data = json.load(open(level_path,))
            tiles.append(LevelTile(data['level_name'], screen, level_path))

        title = 'Choose your level!'

        super().__init__(screen, title, tiles)


class LevelTile(Tile):

    def __init__(self, text, screen, level_path):
        self.level_path = level_path
        self.screen = screen
        super().__init__(text)

    def action(self):
        with open(self.level_path) as json_file:
            level_description = json.load(json_file)
            return (LevelView(self.screen, Level(level_description), FRAMES_PER_SIMULATION_TICK),
                    ViewInitAction.EMPTY_STACK)


class GoBackTile(Tile):

    def action(self):
        return (None, ViewInitAction.POP)


class CustomLevelsTile(Tile):

    def __init__(self, text, screen):
        self.screen = screen
        super().__init__(text)

    def action(self):
        return (CustomLevelsView(self.screen), ViewInitAction.EMPTY_STACK)


class AddLevelTile(Tile):
    def __init__(self, text, screen):
        self.screen = screen
        super().__init__(text)

    def action(self):
        import_level()


class CustomLevelsView(PickView):
    def __init__(self, screen):

        tiles = [
            MenuTile('Back to menu', screen),
            AddLevelTile('Add level', screen)
        ]

        tiles.extend(self.load_levels(screen))

        title = 'Custom levels'

        super().__init__(screen, title, tiles)

    def load_levels(self, screen):
        levels = []
        for file in os.listdir(CUSTOM_LEVELS_PATH):
            level_path = os.path.join(CUSTOM_LEVELS_PATH, file)
            data = json.load(open(level_path,))
            if level_validator(data):
                levels.append(CustomLevelTile(data['level_name'], screen, level_path))
            else:
                levels.append(InvalidLevelTile(data['level_name'], screen, level_path))

        return levels

    def handle_pygame_event(self, event):
        result = super().handle_pygame_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON:
            i = 0
            while i < len(self.tiles):
                tile = self.tiles[i]
                if isinstance(tile, CustomLevelTile):
                    if not os.path.exists(tile.level_path,):
                        self.tiles.pop(i)
                elif isinstance(tile, AddLevelTile):
                    self.tiles = self.tiles[:2]
                    self.tiles.extend(self.load_levels(self.screen))
                i += 1
        self.force_refresh()
        return result


class InvalidLevelTile(LevelTile):
    def self_draw(self, frame, pos, dimensions):
        x, y = pos
        self.width, self.height = dimensions
        self.pos = pos
        self.name_pos = pos
        self.delete_pos = (x + self.width - self.height, y)
        self.name_dimensions = (self.width - self.height, self.height)
        self.delete_dimensions = (self.height, self.height)
        name_rectangle = pygame.Rect(self.name_pos, self.name_dimensions)
        delete_rectangle = pygame.Rect(self.delete_pos, self.delete_dimensions)
        pygame.draw.rect(frame, TILE_BACKGROUND_COLOR, name_rectangle)
        pygame.draw.rect(frame, (130, 130, 130), delete_rectangle)
        text_font = pygame.font.Font(pygame.font.get_default_font(),
                                     self.height * TEXT_TILE_HEIGHT_PERCENTAGE // 100)
        text = text_font.render(self.text, True, INVALID_LEVEL_TEXT_COLOR)
        text_rectangle = text.get_rect()
        text_rectangle.center = name_rectangle.center
        delete_text = text_font.render('X', True, TILE_TEXT_COLOR)
        delete_text_rectangle = delete_text.get_rect()
        delete_text_rectangle.center = delete_rectangle.center
        frame.blit(text, text_rectangle)
        frame.blit(delete_text, delete_text_rectangle)

    def delete_level(self):
        os.remove(self.level_path)

    def handle_click(self, pos):
        if self.pos is None:
            return None
        del_x, del_y = self.delete_pos
        mouse_x, mouse_y = pos
        del_w, del_h = self.delete_dimensions
        if del_x <= mouse_x <= del_x + del_w and del_y <= mouse_y <= del_y + del_h:
            return self.delete_level()
        else:
            return None


class CustomLevelTile(LevelTile):
    def self_draw(self, frame, pos, dimensions):
        x, y = pos
        self.width, self.height = dimensions
        self.pos = pos
        self.name_pos = pos
        self.delete_pos = (x + self.width - self.height, y)
        self.name_dimensions = (self.width - self.height, self.height)
        self.delete_dimensions = (self.height, self.height)
        name_rectangle = pygame.Rect(self.name_pos, self.name_dimensions)
        delete_rectangle = pygame.Rect(self.delete_pos, self.delete_dimensions)
        pygame.draw.rect(frame, TILE_BACKGROUND_COLOR, name_rectangle)
        pygame.draw.rect(frame, (130, 130, 130), delete_rectangle)
        text_font = pygame.font.Font(pygame.font.get_default_font(),
                                     self.height * TEXT_TILE_HEIGHT_PERCENTAGE // 100)
        text = text_font.render(self.text, True, TILE_TEXT_COLOR)
        text_rectangle = text.get_rect()
        text_rectangle.center = name_rectangle.center
        delete_text = text_font.render('X', True, TILE_TEXT_COLOR)
        delete_text_rectangle = delete_text.get_rect()
        delete_text_rectangle.center = delete_rectangle.center
        frame.blit(text, text_rectangle)
        frame.blit(delete_text, delete_text_rectangle)

    def action(self):
        with open(self.level_path) as json_file:
            level_description = json.load(json_file)
            return (EditorLevelView(self.screen, Level(level_description), FRAMES_PER_SIMULATION_TICK),
                    ViewInitAction.PUSH)

    def delete_level(self):
        os.remove(self.level_path)

    def handle_click(self, pos):
        if self.pos is None:
            return None
        self_x, self_y = self.name_pos
        del_x, del_y = self.delete_pos
        mouse_x, mouse_y = pos
        name_w, name_h = self.name_dimensions
        del_w, del_h = self.delete_dimensions
        if self_x <= mouse_x <= self_x + name_w and self_y <= mouse_y <= self_y + name_h:
            return self.action()
        elif del_x <= mouse_x <= del_x + del_w and del_y <= mouse_y <= del_y + del_h:
            return self.delete_level()
        else:
            return None
