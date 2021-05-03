from src.engine.flat import Reverse, VeniceBlock, TurnLeft, TurnRight, Spikes
import mock


def test_turn_left_creation():
    TurnLeft()


def test_turn_righ_creation():
    TurnRight()


def test_turn_left_changes_snake_direction():
    turn_left = TurnLeft()
    snake = mock.Mock()
    turn_left.interact_with_snake(snake)

    snake.direction.turn_left.assert_called_once()


def test_turn_right_changes_snake_direction():
    turn_right = TurnRight()
    snake = mock.Mock()
    turn_right.interact_with_snake(snake)

    snake.direction.turn_right.assert_called_once()


def test_spikes_creation():
    Spikes()


def test_spikes_destroy_snake():
    snake_mock = mock.Mock()
    spikes = Spikes()
    spikes.interact_with_snake(snake_mock)

    snake_mock.interact_with_snake.destroy()


def test_spikes_not_interacting_with_convex():
    convex_mock = mock.Mock()
    spikes = Spikes()
    spikes.interact_with_convex(convex_mock)

    assert convex_mock.mock_calls == []


def test_reverse_creation():
    Reverse()


def test_reverse_informs_snake_to_reverse():
    snake_mock = mock.Mock()
    reverse = Reverse()
    reverse.interact_with_snake(snake_mock)
    snake_mock.reverse.assert_called_once()


def test_venice_creation():
    direction_mock = mock.Mock()
    venice = VeniceBlock(direction=direction_mock)
    assert venice.direction == direction_mock


def test_venice_interact_with_snake_has_no_effect():
    direction_mock = mock.Mock()
    venice = VeniceBlock(direction=direction_mock)
    snake_mock = mock.Mock()
    venice.interact_with_snake(snake_mock)
    assert snake_mock.mock_calls == []


def test_venice_interact_with_convex_has_no_effect():
    direction_mock = mock.Mock()
    venice = VeniceBlock(direction=direction_mock)
    convex_mock = mock.Mock()
    venice.interact_with_convex(convex_mock)
    assert convex_mock.mock_calls == []


def test_venice_check_move():
    direction_mock = mock.Mock()
    direction2_mock = mock.Mock()
    venice = VeniceBlock(direction=direction_mock)

    assert venice.check_move(direction_mock)
    assert not venice.check_move(direction2_mock)


def test_venice_check_snake_move():
    direction_mock = mock.Mock()
    direction2_mock = mock.Mock()
    venice = VeniceBlock(direction=direction_mock)
    snake_mock = mock.Mock()
    snake_mock.direction = direction_mock
    snake2_mock = mock.Mock()
    snake2_mock.direction = direction2_mock

    assert venice.check_snake_move(snake_mock)
    assert not venice.check_snake_move(snake2_mock)
