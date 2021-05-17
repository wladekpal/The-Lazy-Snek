from src.engine.level_validator import level_validator, check_parts, name_not_empty
from src.engine.level_validator import ids_in_range, wall_perimeter, teleports_connected, check_snakes
import os
import json

NUMBER_OF_BASE_LEVELS = 30
BASE_LEVELS_PATH = os.path.join(os.path.dirname(__file__), '../../../levels/base')
LOCAL_TEST_PATH = os.path.dirname(__file__)
FUNCTIONS_TO_CHECK = [check_parts,
                      name_not_empty,
                      ids_in_range,
                      wall_perimeter,
                      teleports_connected,
                      check_snakes,
                      level_validator]


def test_base_level_pass():
    for level in os.listdir(BASE_LEVELS_PATH):
        level_path = os.path.join(BASE_LEVELS_PATH, level)
        json_file = open(level_path)
        level_description = json.load(json_file)

        for function in FUNCTIONS_TO_CHECK:
            assert function(level_description)


def test_wall_perimeter():
    level_path = os.path.join(LOCAL_TEST_PATH, 'not_enclosed.json')
    json_file = open(level_path)
    level_description = json.load(json_file)

    assert not wall_perimeter(level_description)
    assert not level_validator(level_description)


def test_teleport_not_connected():
    level_path = os.path.join(LOCAL_TEST_PATH, 'teleports_not_connected.json')
    json_file = open(level_path)
    level_description = json.load(json_file)

    assert not teleports_connected(level_description)
    assert not level_validator(level_description)


def test_wrong_snake_placement():
    level_path = os.path.join(LOCAL_TEST_PATH, 'wrong_snake_placement.json')
    json_file = open(level_path)
    level_description = json.load(json_file)

    assert not check_snakes(level_description)
    assert not level_validator(level_description)
