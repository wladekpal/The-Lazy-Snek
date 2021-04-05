import pygame
import os
from .button import PlayButton, CancelButton, RestartButton
from .simulation import Simulation, SimulationState
import enum

# frames and their elements display details
BOARD_FRAME_HEIGHT_PERCENTAGE = 85
BOARD_FRAME_WIDTH_PERCENTAGE = 100
CONTROLS_BUTTON_HEIGHT_PERCENTAGE = 60
CONTROLS_BUTTONS_INTERSPACE = 40
MAIN_FRAME_BACKGROUND_COLOR = (0, 0, 0)
BOARD_FRAME_BACKGROUND_COLOR = (33, 47, 61)
CONTROLS_FRAME_BACKGROUND_COLOR = (33, 47, 61)

# messages details
MESSAGES_FONT_SIZE = 100
MESSAGE_WIN = 'YOU WON'
MESSAGE_LOSS = 'YOU LOST'

# buttons textures
PLAY_BUTTON_TEXTURE_PATH = os.path.join(os.path.dirname(__file__), "../../assets/play-button.png")
PAUSE_BUTTON_TEXTURE_PATH = os.path.join(os.path.dirname(__file__), "../../assets/pause-button.png")
RESET_BUTTON_TEXTURE_PATH = os.path.join(os.path.dirname(__file__), "../../assets/restart-button.png")
STOP_BUTTON_TEXTURE_PATH = os.path.join(os.path.dirname(__file__), "../../assets/stop-button.png")


class LevelView():
    def __init__(self, screen, level, frames_per_simulation_tick):

        def create_board_frame(screen):
            frame_width = screen.get_width() * BOARD_FRAME_WIDTH_PERCENTAGE // 100
            frame_height = screen.get_height() * BOARD_FRAME_HEIGHT_PERCENTAGE // 100
            return screen.subsurface(pygame.Rect(0, 0, frame_width, frame_height))

        def create_controls_frame(screen, board_frame):
            width = board_frame.get_width()
            height = screen.get_height() - board_frame.get_height()
            return screen.subsurface(pygame.Rect(0, board_frame.get_height(), width, height))

        def create_buttons():
            buttons = []
            buttons.append(PlayButton(self.simulation, pygame.image.load(PLAY_BUTTON_TEXTURE_PATH), pygame.image.load(PAUSE_BUTTON_TEXTURE_PATH)))
            buttons.append(RestartButton(self.simulation, pygame.image.load(RESET_BUTTON_TEXTURE_PATH)))
            buttons.append(CancelButton(self.simulation, pygame.image.load(STOP_BUTTON_TEXTURE_PATH)))
            return buttons
        
        self.messages_font = pygame.font.Font(pygame.font.get_default_font(), MESSAGES_FONT_SIZE)
        self.frames_per_simulation_tick = frames_per_simulation_tick
        self.frames_till_next_tick = frames_per_simulation_tick
        self.level = level
        self.simulation = Simulation(level, self)
        self.main_frame = screen
        self.board_frame = create_board_frame(self.main_frame)
        self.controls_frame = create_controls_frame(self.main_frame, self.board_frame)
        self.buttons = create_buttons()

    def refresh(self):

        def refresh_backgrounds():
            self.main_frame.fill(MAIN_FRAME_BACKGROUND_COLOR)
            self.board_frame.fill(BOARD_FRAME_BACKGROUND_COLOR)
            self.controls_frame.fill(CONTROLS_FRAME_BACKGROUND_COLOR)

        def refresh_buttons():
            side_length = self.controls_frame.get_height() * CONTROLS_BUTTON_HEIGHT_PERCENTAGE // 100
            y = ((self.controls_frame.get_height() - side_length) // 2) + self.board_frame.get_height()
            center_x = self.controls_frame.get_width() / 2
            x_buttons_offset = len(self.buttons) * side_length / 2
            x_interspace_offset = (len(self.buttons) - 1) * CONTROLS_BUTTONS_INTERSPACE / 2
            x = int(center_x - x_buttons_offset - x_interspace_offset)
            for button in self.buttons:
                button.self_draw(self.main_frame, (x, y), side_length)
                x += side_length + CONTROLS_BUTTONS_INTERSPACE

        def refresh_board():
            self.level.self_draw(self.board_frame)

        def refresh_message():
            if self.simulation.get_state() in [SimulationState.WIN, SimulationState.LOSS]:
                message_content = MESSAGE_WIN if self.simulation.get_state() == SimulationState.WIN else MESSAGE_LOSS
                text = self.messages_font.render(message_content, True, (0, 0, 0))
                text_rectangle = text.get_rect()
                text_rectangle.center = self.board_frame.get_rect().center
                self.board_frame.blit(text, text_rectangle)
        
        self.frames_till_next_tick -= 1
        if self.frames_till_next_tick == 0:
            self.simulation.tick()
            self.frames_till_next_tick = self.frames_per_simulation_tick
        
        refresh_backgrounds()
        refresh_board()
        refresh_buttons()
        refresh_message()

    def handle_click(self):
        for button in self.buttons:
            mouse_position = pygame.mouse.get_pos()
            button.process_mouse_click(mouse_position)

    def reset_simulation_ticks(self):
        self.frames_till_next_tick = self.frames_per_simulation_tick