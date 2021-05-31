from pygame.constants import CONTROLLER_BUTTON_RIGHTSHOULDER
from src.engine.convex import InfinityTail
from src.engine.level import Level, LevelState
from src.engine.convex import Apple, Box, Key, Dye, Skull, InfinityTail, Door
from src.engine.flat import TurnLeft, TurnRight
from src.engine.direction import Direction
import os
import json


def test_level1_loss_after_expected_number_of_ticks():
    TEST_SOURCE_PATH = os.path.join(os.path.dirname(__file__), "level1.json")
    file = open(TEST_SOURCE_PATH)
    level = Level(json.load(file))
    EXPECTED_TICKS_UNTIL_LOSS = 18
    for _ in range(EXPECTED_TICKS_UNTIL_LOSS):
        assert level.tick() == LevelState.UNDECIDED
    assert level.tick() == LevelState.LOSS


def test_level1_loss_needs_same_number_of_ticks_after_reload():
    TEST_SOURCE_PATH = os.path.join(os.path.dirname(__file__), "level1.json")
    file = open(TEST_SOURCE_PATH)
    level = Level(json.load(file))
    EXPECTED_TICKS_UNTIL_LOSS = 18
    TICKS_UNTIL_RELOAD = 13
    for _ in range(TICKS_UNTIL_RELOAD):
        assert level.tick() == LevelState.UNDECIDED
    level.reload_level()
    for _ in range(EXPECTED_TICKS_UNTIL_LOSS):
        assert level.tick() == LevelState.UNDECIDED
    assert level.tick() == LevelState.LOSS


def create_convexes_list():
    return [
        [Apple, 2], 
        [Box, 2], 
        [Key, 1], 
        [Dye, 3],
        [Skull, 1],
        [InfinityTail, 1],
        [Door, 1]
    ]


def create_snake_path(level):
    x, y = 1, 8
    direction = Direction('N')
    path = []
    SNAKE_PATH_LENGTH = 64
    for _ in range(SNAKE_PATH_LENGTH):
        path.append((x, y))
        x, y = direction.move_in_direction((x, y))
        field = level.board.request_field((x, y))
        if field.flat_layer is not None:
            if isinstance(field.flat_layer, TurnLeft):
                direction.turn_left()
            if isinstance(field.flat_layer, TurnRight):
                direction.turn_right()
    return path


def create_expected_level_state(level):
    return {
        "snake_path": create_snake_path(level),
        "snake_head_position": 4,
        "snake_length": 5,
        "key": False,
        "color": "green",
        "infinity_tail": False,
        "move_on_next_tick": True,
        "convexes_on_board": create_convexes_list()
    }


def create_events():
    return {
        (2, 2): [("remove_convex", Apple)],
        (2, 3): [("remove_convex", Box)],
        (2, 6): [("snake_length", 6), ("remove_convex", Apple)],
        (3, 7): [("color", "blue"), ("remove_convex", Dye)],
        (3, 5): [("key", True), ("remove_convex", Key)],
        (4, 3): [("move_on_next_tick", False)],
        (4, 4): [("color", "red"), ("remove_convex", Dye)],
        (5, 7): [("color", "green"), ("remove_convex", Dye)],
        (5, 5): [("infinity_tail", True), ("snake_length", 7), ("remove_convex", InfinityTail)],
        (6, 4): [("remove_convex", Skull)],
        (6, 5): [("remove_convex", Box)],
        (8, 4): [("remove_convex", Door)]
    }


def handle_one_event(current_expected_level_state, event):
    if event[0] in current_expected_level_state:
        current_expected_level_state[event[0]] = event[1]
    elif event[0] == "remove_convex":
        convexes_list = current_expected_level_state["convexes_on_board"]
        for convex_info in convexes_list:
            if convex_info[0] == event[1]:
                convex_info[1] -= 1


def update_current_level_state(current_expected_level_state, events):
    if current_expected_level_state['move_on_next_tick']:
        current_expected_level_state['snake_head_position'] += 1
    current_expected_level_state['move_on_next_tick'] = True
    
    if current_expected_level_state['infinity_tail']:
        current_expected_level_state['snake_length'] += 1
    
    snake_head_position = current_expected_level_state['snake_head_position']
    head_coords = current_expected_level_state['snake_path'][snake_head_position]
    if head_coords in events:
        event_list = events[head_coords]
        for event in event_list:
            handle_one_event(current_expected_level_state, event)
        events[head_coords] = []


def check_convex_placement(current_expected_level_state, level):
    convexes_list = current_expected_level_state["convexes_on_board"]
    board = level.board
    for convex, expected_convex_count in convexes_list:
        real_convex_count = 0
        for row in board.fields:
            for field in row:
                if field and field.convex_layer and isinstance(field.convex_layer, convex):
                    real_convex_count += 1
        assert real_convex_count == expected_convex_count


def check_snake_position(current_expected_level_state, level):
    snake_head_position = current_expected_level_state['snake_head_position']
    snake_length = current_expected_level_state['snake_length']
    snake_tail_position = snake_head_position - snake_length + 1
    expected_snake_placement = current_expected_level_state['snake_path'][snake_tail_position:snake_head_position+1]
    real_snake = level.snakes[0]
    assert len(real_snake.segments) == len(expected_snake_placement)
    assert real_snake.segments == expected_snake_placement


def check_snake_modification(current_expected_level_state, level):
    real_snake = level.snakes[0]
    assert real_snake.color == current_expected_level_state['color']
    assert real_snake.has_key == current_expected_level_state['key']
    assert real_snake.infinite_grow == current_expected_level_state['infinity_tail']


def test_level2_expected_game_length():
    TEST_SOURCE_PATH = os.path.join(os.path.dirname(__file__), "level2.json")
    file = open(TEST_SOURCE_PATH)
    level = Level(json.load(file))
    EXPECTED_TICS_WITHOUT_WIN = 59
    for _ in range(EXPECTED_TICS_WITHOUT_WIN):
        assert level.tick() == LevelState.UNDECIDED
    assert level.tick() == LevelState.WIN


def test_level2_is_convexes_count_on_board_correct():
    TEST_SOURCE_PATH = os.path.join(os.path.dirname(__file__), "level2.json")
    file = open(TEST_SOURCE_PATH)
    level = Level(json.load(file))
    current_expected_level_state = create_expected_level_state(level)
    events = create_events()
    EXPECTED_TICS_WITHOUT_WIN = 59
    for _ in range(EXPECTED_TICS_WITHOUT_WIN):
        level.tick()
        update_current_level_state(current_expected_level_state, events)
        check_convex_placement(current_expected_level_state, level)


def test_level2_is_snake_position_correct():
    TEST_SOURCE_PATH = os.path.join(os.path.dirname(__file__), "level2.json")
    file = open(TEST_SOURCE_PATH)
    level = Level(json.load(file))
    current_expected_level_state = create_expected_level_state(level)
    events = create_events()
    EXPECTED_TICS_WITHOUT_WIN = 59
    for _ in range(EXPECTED_TICS_WITHOUT_WIN):
        level.tick()
        update_current_level_state(current_expected_level_state, events)
        check_snake_position(current_expected_level_state, level)


def test_level2_is_snake_modification_correct():
    TEST_SOURCE_PATH = os.path.join(os.path.dirname(__file__), "level2.json")
    file = open(TEST_SOURCE_PATH)
    level = Level(json.load(file))
    current_expected_level_state = create_expected_level_state(level)
    events = create_events()
    EXPECTED_TICS_WITHOUT_WIN = 59
    for _ in range(EXPECTED_TICS_WITHOUT_WIN):
        level.tick()
        update_current_level_state(current_expected_level_state, events)
        check_snake_modification(current_expected_level_state, level)

