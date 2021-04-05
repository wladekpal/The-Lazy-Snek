from src.engine.level import Level
import os


def test_example_levels_loss_after_expected_number_of_ticks():
    TEST_SOURCE_PATH = os.path.join(os.path.dirname(__file__), "example_level_for_level_integration_test.json")
    level = Level(TEST_SOURCE_PATH)
    LEVEL_IN_PROGRESS = 0
    LEVEL_LOST = -1
    EXPECTED_TICKS_UNTIL_LOSS = 12
    for _ in range(EXPECTED_TICKS_UNTIL_LOSS):
        assert level.tick() == LEVEL_IN_PROGRESS
    assert level.tick() == LEVEL_LOST


def test_example_level_loss_needs_same_number_of_ticks_after_reload():
    TEST_SOURCE_PATH = os.path.join(os.path.dirname(__file__), "example_level_for_level_integration_test.json")
    level = Level(TEST_SOURCE_PATH)
    LEVEL_IN_PROGRESS = 0
    LEVEL_LOST = -1
    EXPECTED_TICKS_UNTIL_LOSS = 12
    TICKS_UNTIL_RELOAD = 5
    for _ in range(TICKS_UNTIL_RELOAD):
        assert level.tick() == LEVEL_IN_PROGRESS
    level.reload_level()
    for _ in range(EXPECTED_TICKS_UNTIL_LOSS):
        assert level.tick() == LEVEL_IN_PROGRESS
    assert level.tick() == LEVEL_LOST
