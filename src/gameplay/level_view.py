import pygame
import os
from .button import PlayButton, CancelButton, RestartButton, StepByStepButton
from .simulation import Simulation, SimulationState
from .items_frame import BlocksPane
from .item import Item

#temp
from engine.blocks import Wall, TurnLeft, TurnRight

# frames and their elements display details
BOARD_FRAME_HEIGHT_PERCENTAGE = 85
BOARD_FRAME_WIDTH_PERCENTAGE = 85
CONTROLS_BUTTON_HEIGHT_PERCENTAGE = 60
CONTROLS_BUTTONS_INTERSPACE = 40
MAIN_FRAME_BACKGROUND_COLOR = (0, 0, 0)
BOARD_FRAME_BACKGROUND_COLOR = (33, 47, 61)
CONTROLS_FRAME_BACKGROUND_COLOR = (33, 47, 61)

# messages details
MESSAGES_FONT_SIZE = 100
MESSAGE_WIN = 'YOU WIN'
MESSAGE_LOSS = 'YOU LOSE'

# buttons textures
PLAY_BUTTON_TEXTURE_PATH = os.path.join(os.path.dirname(__file__), "../../assets/play-button.png")
PAUSE_BUTTON_TEXTURE_PATH = os.path.join(os.path.dirname(__file__), "../../assets/pause-button.png")
RESET_BUTTON_TEXTURE_PATH = os.path.join(os.path.dirname(__file__), "../../assets/restart-button.png")
STOP_BUTTON_TEXTURE_PATH = os.path.join(os.path.dirname(__file__), "../../assets/stop-button.png")
ACTIVE_STEPBYSTEP_BUTTON_TEXTURE_PATH = os.path.join(os.path.dirname(__file__), "../../assets/step-by-step-active.png")
INACTIVE_STEPBYSTEP_BUTTON_TEXTURE_PATH = os.path.join(os.path.dirname(__file__),
                                                       "../../assets/step-by-step-inactive.png")


class LevelView():
    def __init__(self, screen, level, frames_per_simulation_tick):

        def create_buttons():
            buttons = []
            buttons.append(PlayButton(self.simulation, pygame.image.load(PLAY_BUTTON_TEXTURE_PATH),
                                      pygame.image.load(PAUSE_BUTTON_TEXTURE_PATH)))
            buttons.append(RestartButton(self.simulation, pygame.image.load(RESET_BUTTON_TEXTURE_PATH)))
            buttons.append(CancelButton(self.simulation, pygame.image.load(STOP_BUTTON_TEXTURE_PATH)))
            buttons.append(StepByStepButton(self.simulation, pygame.image.load(ACTIVE_STEPBYSTEP_BUTTON_TEXTURE_PATH),
                                      pygame.image.load(INACTIVE_STEPBYSTEP_BUTTON_TEXTURE_PATH)))
            return buttons

        self.messages_font = pygame.font.Font(pygame.font.get_default_font(), MESSAGES_FONT_SIZE)
        self.frames_per_simulation_tick = frames_per_simulation_tick
        self.frames_till_next_tick = frames_per_simulation_tick
        self.level = level
        self.main_frame = screen
        self.simulation = Simulation(level, self)
        self.buttons = create_buttons()
        self.blocks_pane = BlocksPane(self.level.get_board(), 
                                      [Wall(pane_index=0), Wall(pane_index=1), TurnLeft(pane_index=2), TurnRight(pane_index=3)], 
                                      self)
        self.flowing_item = None

    def refresh(self):

        def create_board_frame(screen):
            frame_width = screen.get_width() * BOARD_FRAME_WIDTH_PERCENTAGE // 100
            frame_height = screen.get_height() * BOARD_FRAME_HEIGHT_PERCENTAGE // 100
            return screen.subsurface(pygame.Rect(0, 0, frame_width, frame_height))

        def create_controls_frame(screen, board_frame):
            width = board_frame.get_width()
            height = screen.get_height() - board_frame.get_height()
            return screen.subsurface(pygame.Rect(0, board_frame.get_height(), width, height))

        def create_items_frame(screen, board_frame):
            width = screen.get_width() - board_frame.get_width()
            height = screen.get_height()
            return screen.subsurface(pygame.Rect(board_frame.get_width(), 0, width, height))

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

        def refresh_board_and_blocks_pane():
            side_length = self.level.self_draw(self.board_frame)
            self.blocks_pane.self_draw(self.main_frame, self.items_frame, side_length)

        def refresh_items():
            if self.flowing_item is not None:
                self.flowing_item.self_draw(self.main_frame)

        def refresh_message():
            if self.simulation.get_state() in [SimulationState.WIN, SimulationState.LOSS]:
                message_content = MESSAGE_WIN if self.simulation.get_state() == SimulationState.WIN else MESSAGE_LOSS
                text = self.messages_font.render(message_content, True, (0, 0, 0))
                text_rectangle = text.get_rect()
                text_rectangle.center = self.board_frame.get_rect().center
                self.board_frame.blit(text, text_rectangle)

        self.board_frame = create_board_frame(self.main_frame)
        self.controls_frame = create_controls_frame(self.main_frame, self.board_frame)
        self.items_frame = create_items_frame(self.main_frame, self.board_frame)

        if self.simulation.get_state() != SimulationState.INACTIVE:
            self.frames_till_next_tick -= 1
            if self.frames_till_next_tick == 0:
                self.simulation.tick()
                self.frames_till_next_tick = self.frames_per_simulation_tick

        refresh_backgrounds()
        refresh_board_and_blocks_pane()
        refresh_buttons()
        refresh_items()
        refresh_message()

    def handle_click(self, pos):

        def try_move_from_board(pos):
            field = self.level.board.request_field_on_screen(pos)
            if field is not None and field.has_removable():
                block = field.request_removable()
                self.flowing_item = Item(block, self, pos, self.level.board.request_offset(field, pos, block.displayed_side_length), block.displayed_side_length)

        for button in self.buttons:
            button.process_mouse_click(pos)
        if self.simulation.get_state() != SimulationState.INACTIVE:
            return
        self.blocks_pane.handle_click(pos)
        try_move_from_board(pos)


        
        
    def handle_motion(self, pos):
        if self.simulation.get_state() != SimulationState.INACTIVE:
            return
        if self.flowing_item is not None:
            self.flowing_item.handle_motion(pos)
    
    def handle_unclick(self, pos):
        if self.flowing_item is not None:
            self.flowing_item.handle_unclick(pos)

    def handle_leftclick(self, pos):
        if self.simulation.get_state() != SimulationState.INACTIVE:
            return
        field = self.level.board.request_field_on_screen(pos)
        if field is not None:
            removable = field.request_removable()
            if removable is not None:
                self.blocks_pane.return_block(removable)

    def reset_simulation_ticks(self):
        self.frames_till_next_tick = self.frames_per_simulation_tick
