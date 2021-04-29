from src.engine.convex import Wall, Skull, Apple, Box, InfinityTail, Door, Key, WallInteractionError
import pytest
import mock


def test_wall_class_object_can_be_created():
    Wall()


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


def test_wall_class_object_cant_be_killed():
    with pytest.raises(WallInteractionError):
        Wall().kill()


def test_wall_class_object_cant_be_destroyed():
    with pytest.raises(WallInteractionError):
        Wall().destroy()


def test_box_creation():
    Box()


def test_box_check_move_call_appropriate_method():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    return_mock = mock.Mock()
    direction_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock
    field_two_mock.check_convex_move.return_value = return_mock

    box = Box()
    box.set_field(field_one_mock)

    assert box.check_move(direction_mock) == return_mock
    field_one_mock.give_field_in_direction.assert_called_once_with(direction_mock)
    field_two_mock.check_convex_move.assert_called_once_with(direction_mock)


def test_box_moves():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    direction_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock

    box = Box()
    box.set_field(field_one_mock)
    box.move(direction_mock)

    field_one_mock.give_field_in_direction.assert_called_once_with(direction_mock)
    field_one_mock.convex_left.assert_called_once_with(direction_mock)
    field_two_mock.convex_entered.assert_called_once_with(box, direction_mock)


def test_box_destroys_snake_when_cant_be_moved():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    snake_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock
    field_two_mock.check_convex_move.return_value = False

    box = Box()
    box.set_field(field_one_mock)
    box.interact_with_snake(snake_mock)

    snake_mock.destroy.assert_called_once()


def test_box_moves_after_ineracting_with_snake():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    direction_mock = mock.Mock()
    snake_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock
    snake_mock.direction = direction_mock

    box = Box()
    box.set_field(field_one_mock)
    box.interact_with_snake(snake_mock)

    field_one_mock.give_field_in_direction.assert_called_with(direction_mock)
    assert field_one_mock.give_field_in_direction.call_count == 2
    field_one_mock.convex_left.assert_called_once_with(direction_mock)
    field_two_mock.convex_entered.assert_called_once_with(box, direction_mock)
    snake_mock.destroy.assert_not_called()


def test_box_checks_snake_move():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    return_mock = mock.Mock()
    direction_mock = mock.Mock()
    snake_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock
    field_two_mock.check_convex_move.return_value = return_mock
    snake_mock.direction = direction_mock

    box = Box()
    box.set_field(field_one_mock)

    assert box.check_snake_move(snake_mock) == return_mock
    field_one_mock.give_field_in_direction.assert_called_once_with(direction_mock)


def test_skull_creation():
    Skull()


def test_skull_check_move_calls_appropriate_method():
    skull = Skull()
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    return_mock = mock.Mock()
    direction_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock
    field_two_mock.check_convex_move.return_value = return_mock

    skull.set_field(field_one_mock)
    assert skull.check_move(direction_mock) == return_mock
    field_one_mock.give_field_in_direction.assert_called_once_with(direction_mock)
    field_two_mock.check_convex_move.assert_called_once_with(direction_mock)


def test_skull_moves():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    direction_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock

    skull = Skull()
    skull.set_field(field_one_mock)
    skull.move(direction_mock)

    field_one_mock.give_field_in_direction.assert_called_once_with(direction_mock)
    field_one_mock.convex_left.assert_called_once_with(direction_mock)
    field_two_mock.convex_entered.assert_called_once_with(skull, direction_mock)


def test_skull_destroys_snake_and_itself():
    snake_mock = mock.Mock()
    field_mock = mock.Mock()

    skull = Skull()
    skull.set_field(field_mock)
    skull.interact_with_snake(snake_mock)

    snake_mock.destroy.assert_called_once()
    field_mock.remove_convex.assert_called_once()
    assert not skull.is_alive


def test_skull_check_snake_move_always_true():
    skull = Skull()
    snake_mock = mock.Mock()

    assert skull.check_snake_move(snake_mock)


def test_apple_creation():
    Apple()


def test_apple_check_move_calls_appropriate_methods():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    return_mock = mock.Mock()
    direction_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock
    field_two_mock.check_convex_move.return_value = return_mock

    apple = Apple()
    apple.set_field(field_one_mock)

    assert apple.check_move(direction_mock) == return_mock
    field_one_mock.give_field_in_direction.assert_called_once_with(direction_mock)
    field_two_mock.check_convex_move.assert_called_once_with(direction_mock)


def test_apple_moves():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    direction_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock

    apple = Apple()
    apple.set_field(field_one_mock)
    apple.move(direction_mock)

    field_one_mock.give_field_in_direction.assert_called_once_with(direction_mock)
    field_one_mock.convex_left.assert_called_once_with(direction_mock)
    field_two_mock.convex_entered.assert_called_once_with(apple, direction_mock)


def test_apple_destroyed_after_interacting_with_snake():
    snake_mock = mock.Mock()
    field_mock = mock.Mock()
    apple = Apple()
    apple.set_field(field_mock)

    apple.interact_with_snake(snake_mock)
    assert snake_mock.mock_calls == []
    assert not apple.is_alive
    field_mock.remove_convex.assert_called_once()


def test_apple_informs_snake_to_grow():
    snake_mock = mock.Mock()
    apple = Apple()
    assert apple.check_snake_move(snake_mock)
    snake_mock.grow.assert_called_once()


def test_infinity_tail_creation():
    InfinityTail()


def test_infinity_tail_check_move_calls_appropriate_methods():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    return_mock = mock.Mock()
    direction_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock
    field_two_mock.check_convex_move.return_value = return_mock

    infinity_tail = InfinityTail()
    infinity_tail.set_field(field_one_mock)

    assert infinity_tail.check_move(direction_mock) == return_mock
    field_one_mock.give_field_in_direction.assert_called_once_with(direction_mock)
    field_two_mock.check_convex_move.assert_called_once_with(direction_mock)


def test_infinity_tail_moves():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    direction_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock

    infinity_tail = InfinityTail()
    infinity_tail.set_field(field_one_mock)
    infinity_tail.move(direction_mock)

    field_one_mock.give_field_in_direction.assert_called_once_with(direction_mock)
    field_one_mock.convex_left.assert_called_once_with(direction_mock)
    field_two_mock.convex_entered.assert_called_once_with(infinity_tail, direction_mock)


def test_infinity_tail_destroyed_after_interacting_with_snake():
    snake_mock = mock.Mock()
    field_mock = mock.Mock()
    infinity_tail = InfinityTail()
    infinity_tail.set_field(field_mock)

    infinity_tail.interact_with_snake(snake_mock)
    assert snake_mock.mock_calls == []
    assert not infinity_tail.is_alive
    field_mock.remove_convex.assert_called_once()


def test_apple_informs_snake_to_grow_infinitely():
    snake_mock = mock.Mock()
    infinity_tail = InfinityTail()
    assert infinity_tail.check_snake_move(snake_mock)
    snake_mock.enable_infinite_grow.assert_called_once()


def test_key_creation():
    Key()


def test_key_check_move_calls_appropriate_methods():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    return_mock = mock.Mock()
    direction_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock
    field_two_mock.check_convex_move.return_value = return_mock

    key = Key()
    key.set_field(field_one_mock)

    assert key.check_move(direction_mock) == return_mock
    field_one_mock.give_field_in_direction.assert_called_once_with(direction_mock)
    field_two_mock.check_convex_move.assert_called_once_with(direction_mock)


def test_key_moves():
    field_one_mock = mock.Mock()
    field_two_mock = mock.Mock()
    direction_mock = mock.Mock()

    field_one_mock.give_field_in_direction.return_value = field_two_mock

    key = Key()
    key.set_field(field_one_mock)
    key.move(direction_mock)

    field_one_mock.give_field_in_direction.assert_called_once_with(direction_mock)
    field_one_mock.convex_left.assert_called_once_with(direction_mock)
    field_two_mock.convex_entered.assert_called_once_with(key, direction_mock)


def test_key_destroyed_after_interacting_with_snake():
    snake_mock = mock.Mock()
    field_mock = mock.Mock()
    key = Key()
    key.set_field(field_mock)

    key.interact_with_snake(snake_mock)
    assert snake_mock.mock_calls == []
    assert not key.is_alive
    field_mock.remove_convex.assert_called_once()


def test_key_informs_snake_about_collecting():
    snake_mock = mock.Mock()
    key = Key()
    assert key.check_snake_move(snake_mock)
    snake_mock.get_key.assert_called_once()


def test_snake_destroys_door_when_snake_with_key():
    snake_mock = mock.Mock()
    field_mock = mock.Mock()
    snake_mock.has_key = True

    door = Door()
    door.set_field(field_mock)

    door.interact_with_snake(snake_mock)
    assert snake_mock.mock_calls == []
    assert not door.is_alive
    field_mock.remove_convex.assert_called_once()


def test_snake_destroys_snake_when_snake_without_key():
    snake_mock = mock.Mock()
    field_mock = mock.Mock()
    snake_mock.has_key = False

    door = Door()
    door.set_field(field_mock)

    door.interact_with_snake(snake_mock)
    assert snake_mock.destroy
    assert door.is_alive
