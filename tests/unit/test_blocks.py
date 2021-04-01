from src.engine.blocks import Block, Convex, Flat, Wall, WallInteractionError
from src.engine.direction import Direction
import pytest
import pygame

def test_wall_and_snake_cannot_interact():
    try:
        Wall().interact_with_snake('snake')
        assert False
    except WallInteractionError:
        assert True


def test_wall_cannot_be_moved_north():
    try:
        Wall().move(Direction('N'))
        assert False
    except WallInteractionError:
        assert True


def test_wall_cannot_be_moved_south():
    try:
        Wall().move(Direction('S'))
        assert False
    except WallInteractionError:
        assert True


def test_wall_cannot_be_moved_east():
    try:
        Wall().move(Direction('E'))
        assert False
    except WallInteractionError:
        assert True


def test_wall_cannot_be_moved_west():
    try:
        Wall().move(Direction('W'))
        assert False
    except WallInteractionError:
        assert True


def test_wall_denies_moving_north():
    assert not Wall().check_move(Direction('N'))


def test_wall_denies_moving_south():
    assert not Wall().check_move(Direction('S'))


def test_wall_denies_moving_east():
    assert not Wall().check_move(Direction('E'))


def test_wall_denies_moving_west():
    assert not Wall().check_move(Direction('W'))


def test_snake_cant_move_towards_wall_when_next_to_it():
    assert not Wall().check_snake_move(Direction('E'))
    assert not Wall().check_snake_move(Direction('W'))
    assert not Wall().check_snake_move(Direction('N'))
    assert not Wall().check_snake_move(Direction('S'))


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
