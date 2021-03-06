from src.engine.snake import Snake, BadSegmentOrientation, SegmentNotInSnake, SnakeState
import mock
import pytest


def test_snake_creation():
    mock_board = mock.Mock()
    segments = [(1, 1), (1, 2), (2, 2)]
    color = "green"
    mock_direction = mock.Mock()
    mock_direction.__str__ = mock.Mock(return_value='N')
    snake = Snake(segments, color, mock_direction, mock_board)
    assert str(snake.direction) == 'N'
    assert snake.color == "green"
    assert snake.segments == [(1, 1), (1, 2), (2, 2)]


def test_get_direction_betwen_segments():
    segment_one_list = [(0, 0), (1, 4), (5, 5), (4, 10)]
    segment_two_list = [(0, 1), (0, 4), (6, 5), (4, 9)]
    direction = ['S', 'W', 'E', 'N']

    for i in range(len(segment_one_list)):
        assert Snake.get_direction_betwen_segments(segment_one_list[i], segment_two_list[i]) == direction[i]

    with pytest.raises(BadSegmentOrientation):
        Snake.get_direction_betwen_segments((1, 0), (10, 10))


def test_calculate_neighbours_directions():
    mock_board = mock.Mock()
    segments = [(1, 1), (1, 2), (2, 2), (2, 3), (2, 4), (3, 4), (4, 4)]
    color = "green"
    mock_direction = mock.MagicMock()
    mock_direction.__str__.return_value = 'E'
    snake = Snake(segments, color, mock_direction, mock_board)

    directions_list = [['SS'], ['NE', 'EN'], ['WS', 'SW'], ['NS', 'SN'], ['NE', 'EN'], ['WE', 'EW'], ['EW', 'WE']]

    for i in range(len(segments)):
        assert snake.calculate_neighbours_directions(segments[i]) in directions_list[i]


def test_get_segment_texture():
    mock_board = mock.Mock()
    segments = [(1, 1), (1, 2), (2, 2), (2, 3), (2, 4), (3, 4), (4, 4)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)

    assert snake.get_segment_texture(segments[0], 'S') == snake.tail_texture
    assert snake.get_segment_texture(segments[1], 'NE') == snake.bent_body_texture
    assert snake.get_segment_texture(segments[3], 'NS') == snake.body_texture
    assert snake.get_segment_texture(segments[-1], 'E') == snake.head_texture


def test_get_segment_texture_bent_head():
    mock_board = mock.Mock()
    segments = [(2, 2), (2, 1), (2, 0)]
    color = "green"
    mock_direction = mock.MagicMock()
    snake = Snake(segments, color, mock_direction, mock_board)

    assert snake.get_segment_texture(segments[-1], 'ES') == snake.bent_head_texture


def test_get_rotation():
    rotation_table = [(['NN', 'NE', 'EN', 'NS'], 0),
                      (['EE', 'ES', 'SE', 'EW'], -90),
                      (['SS', 'SW', 'WS', 'SN'], -180),
                      (['WW', 'WN', 'NW', 'WE'], -270)]

    for rotation_list in rotation_table:
        desired_rotation = rotation_list[1]
        directions = rotation_list[0]
        for direction in directions:
            assert Snake.get_rotation(direction) == desired_rotation

    bad_directions = ['AB', 17, '$@', 'NNE', 'N', '']
    for bad_direction in bad_directions:
        with pytest.raises(BadSegmentOrientation):
            Snake.get_rotation(bad_direction)


def test_exception_in_segment_draw():
    mock_board = mock.Mock()
    segments = [(1, 1), (1, 2), (2, 2)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)

    mock_frame = mock.Mock()

    with pytest.raises(SegmentNotInSnake):
        snake.draw_segment(mock_frame, (0, 0), 1, (3, 3))


def test_snake_destroyed():
    mock_board = mock.Mock()
    segments = [(1, 1), (1, 2), (2, 2)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)

    snake.destroy()

    for segment_coords in segments:
        mock_board.request_field.assert_any_call(segment_coords)
        mock_field = mock_board.request_field(segment_coords)

    assert mock_field.remove_snake.call_count == len(segments)
    assert snake.state == SnakeState.DEAD


def test_snake_noticed_grow():
    mock_board = mock.Mock()
    segments = [(1, 1), (1, 2), (2, 2)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)

    snake.grow()

    assert snake.grow_at_next_move


def move_coord_north(coords):
    return coords[0], coords[1] - 1


def test_check_snake_move_false():
    mock_board = mock.Mock()
    segments = [(1, 1), (1, 2), (2, 2)]
    color = "green"
    mock_direction = mock.MagicMock()
    mock_direction.move_in_direction.side_effect = move_coord_north
    mock_direction.__str__.return_value = 'N'
    snake = Snake(segments, color, mock_direction, mock_board)

    mock_field = mock.Mock()
    mock_field.check_snake_move.return_value = False
    mock_board.request_field.return_value = mock_field

    snake.move()

    mock_direction.move_in_direction.assert_called_once()
    mock_board.request_field.assert_any_call((2, 1))

    assert snake.state == SnakeState.DEAD


def test_snake_enters_field_no_grow():
    mock_board = mock.Mock()
    segments = [(1, 1), (1, 2), (2, 2)]
    color = "green"
    mock_direction = mock.MagicMock()
    mock_direction.move_in_direction.side_effect = move_coord_north
    mock_direction.__str__.return_value = 'N'
    snake = Snake(segments, color, mock_direction, mock_board)

    mock_field = mock.Mock()
    mock_field.check_snake_move.return_value = True
    mock_field.get_coords_to_move.return_value = (2, 1)
    mock_board.request_field.return_value = mock_field

    snake.move()

    mock_field.snake_entered.assert_called_once_with(snake)
    assert snake.segments == [(1, 2), (2, 2), (2, 1)]


def test_snake_enters_field_and_grows():
    mock_board = mock.Mock()
    segments = [(1, 1), (1, 2), (2, 2)]
    color = "green"
    mock_direction = mock.MagicMock()
    mock_direction.move_in_direction.side_effect = move_coord_north
    mock_direction.__str__.return_value = 'N'
    snake = Snake(segments, color, mock_direction, mock_board)

    mock_field = mock.Mock()
    mock_field.check_snake_move.return_value = True
    mock_field.get_coords_to_move.return_value = (2, 1)
    mock_board.request_field.return_value = mock_field

    snake.grow()
    snake.move()

    mock_field.snake_entered.assert_called_once_with(snake)
    assert snake.segments == [(1, 1), (1, 2), (2, 2), (2, 1)]
    assert not snake.grow_at_next_move


def test_growing_snake_dies_when_entering_field():
    mock_board = mock.Mock()
    segments = [(1, 1), (1, 2), (2, 2)]
    color = "green"
    mock_direction = mock.MagicMock()
    mock_direction.move_in_direction.side_effect = move_coord_north
    mock_direction.__str__.return_value = 'N'

    mock_field = mock.Mock()
    mock_field.check_snake_move.return_value = True
    mock_field.snake_entered.side_effect = lambda snake: snake.destroy()
    mock_field.get_coords_to_move.return_value = (2, 1)
    mock_board.request_field.return_value = mock_field

    snake = Snake(segments, color, mock_direction, mock_board)

    snake.grow()
    snake.move()

    mock_field.snake_entered.assert_called_once_with(snake)
    assert mock_field.remove_snake.call_count == 4
    assert snake.state == SnakeState.DEAD
    assert snake.segments == [(1, 1), (1, 2), (2, 2), (2, 1)]
    assert not snake.grow_at_next_move


def test_snake_collides_with_snake_body():
    mock_board = mock.Mock()
    segments = [(1, 2), (2, 2), (3, 2)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)

    other_segments = [(1, 1), (1, 2), (2, 2)]
    other_snake = Snake(other_segments, color, mock_direction, mock_board)

    snake.interact_with_snake(other_snake)
    assert other_snake.state == SnakeState.DEAD
    assert snake.state == SnakeState.ALIVE


def test_snake_collides_with_snake_head():
    mock_board = mock.Mock()
    segments = [(1, 2), (2, 2), (3, 2)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)

    other_segments = [(5, 2), (4, 2), (3, 2)]
    other_snake = Snake(other_segments, color, mock_direction, mock_board)

    snake.interact_with_snake(other_snake)
    assert other_snake.state == SnakeState.DEAD
    assert snake.state == SnakeState.DEAD


def test_snake_collides_with_itself():
    mock_board = mock.Mock()
    segments = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)

    snake.interact_with_snake(snake)
    assert snake.state == SnakeState.DEAD


def test_snake_reverses():
    mock_board = mock.Mock()
    segments = [(1, 2), (2, 2), (3, 2)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)

    snake.reverse()
    assert snake.segments == [(3, 2), (2, 2), (1, 2)]


def test_snake_infinite_growth():
    mock_board = mock.Mock()
    segments = [(1, 1), (1, 2), (2, 2)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)
    assert not snake.infinite_grow
    snake.enable_infinite_grow()
    assert snake.infinite_grow
