import pytest
from src.engine.direction import Direction


def test_direction_creation():
    Direction('N')
    Direction('E')
    Direction('S')
    Direction('W')
    with pytest.raises(Exception) as exceptionInfo:
        Direction('X')
    assert "Wrong initial direction name" in str(exceptionInfo)


def test_direction_to_string():
    north = Direction('N')
    assert 'N' == str(north)

    east = Direction('E')
    assert 'E' == str(east)

    south = Direction('S')
    assert 'S' == str(south)

    west = Direction('W')
    assert 'W' == str(west)


def test_direction_changing_coordinates():
    coordinates = (0, 0)
    direction = Direction('N')
    coordinates = direction.move_in_direction(coordinates)
    assert coordinates == (0, -1)

    coordinates = (0, 0)
    direction = Direction('E')
    coordinates = direction.move_in_direction(coordinates)
    assert coordinates == (1, 0)

    coordinates = (0, 0)
    direction = Direction('S')
    coordinates = direction.move_in_direction(coordinates)
    assert coordinates == (0, 1)

    coordinates = (0, 0)
    direction = Direction('W')
    coordinates = direction.move_in_direction(coordinates)
    assert coordinates == (-1, 0)


def test_changing_direction():
    direction = Direction('N')
    direction.turn_left()
    assert 'W' == str(direction)

    direction.reverse()
    assert 'E' == str(direction)

    direction.turn_right()
    assert 'S' == str(direction)
