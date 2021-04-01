from src.engine.blocks import Block, Convex, Flat, Wall, WallInteractionError
from src.engine.direction import Direction
import pytest
import pygame

@pytest.fixture
def wall():
    return Wall()


@pytest.fixture
def direction_north():
    return Direction('N')


@pytest.fixture
def direction_south():
    return Direction('S')


@pytest.fixture
def direction_east():
    return Direction('E')


@pytest.fixture
def direction_west():
    return Direction('W')


@pytest.fixture
def snake_to_interact_with_wall():
    return 'snake'


def test_wall_and_snake_cannot_interact():
    try:
        wall().interact_with_snake(snake_to_interact_with_wall())
        assert False
    except WallInteractionError:
        assert True


def test_wall_cannot_be_moved_north():
    try:
        wall().move(direction_north())
        assert False
    except WallInteractionError:
        assert True


def test_wall_cannot_be_moved_south():
    try:
        wall().move(direction_south())
        assert False
    except WallInteractionError:
        assert True


def test_wall_cannot_be_moved_east():
    try:
        wall().move(direction_east())
        assert False
    except WallInteractionError:
        assert True


def test_wall_cannot_be_moved_west():
    try:
        wall().move(direction_west())
        assert False
    except WallInteractionError:
        assert True


def test_wall_denies_moving_north():
    wall = Wall()
    assert not wall.check_move(direction_north())


def test_wall_denies_moving_south():
    wall = Wall()
    assert not wall.check_move(direction_south())


def test_wall_denies_moving_east():
    wall = Wall()
    assert not wall.check_move(direction_east())


def test_wall_denies_moving_west():
    wall = Wall()
    assert not wall.check_move(direction_west())


def test_snake_cant_move_towards_wall_when_next_to_it():
    wall = Wall()
    assert not wall.check_snake_move(direction_east())
    assert not wall.check_snake_move(direction_west())
    assert not wall.check_snake_move(direction_north())
    assert not wall.check_snake_move(direction_south())


def test_block_class_object_cant_be_created():
    try:
        block = Block()
        assert False
    except TypeError:
        assert True


def test_convex_class_object_cant_be_created():
    try:
        convex = Convex()
        assert False
    except TypeError:
        assert True


def test_flat_class_object_cant_be_created():
    try:
        flat = Flat()
        assert False
    except TypeError:
        assert True

def test_wall_class_object_can_be_created():
    try:
        wall = Wall()
        assert True
    except:
        assert False
