from src.engine.blocks import Block, Convex, Flat, Wall, WallInteractionError
import pytest
import mock


def test_wall_and_snake_cannot_interact():
    snake = mock.Mock()
    with pytest.raises(WallInteractionError):
        Wall().interact_with_snake(snake)


def test_wall_cannot_be_moved():
    direction = mock.Mock()
    with pytest.raises(WallInteractionError):
        Wall().move(direction)


def test_wall_denies_moving():
    direction = mock.Mock()
    assert not Wall().check_move(direction)


def test_snake_cant_move_towards_wall_when_next_to_it():
    direction = mock.Mock()
    assert not Wall().check_snake_move(direction)


def test_block_class_object_cant_be_created():
    with pytest.raises(TypeError):
        Block()


def test_convex_class_object_cant_be_created():
    with pytest.raises(TypeError):
        Convex()


def test_flat_class_object_cant_be_created():
    with pytest.raises(TypeError):
        Flat()


def test_wall_class_object_can_be_created():
    Wall()


def test_wall_class_object_cant_be_killed():
    with pytest.raises(WallInteractionError):
        Wall().kill()


def test_wall_class_object_cant_be_destroyed():
    with pytest.raises(WallInteractionError):
        Wall().destroy()


def test_wall_set_field():
    field = mock.Mock()
    wall = Wall()
    wall.set_field(field)
    assert wall.field == field