from src.engine.snake import Snake
import mock
import pytest


def test_snake_creation():
    mock_board = mock.Mock()
    segments = [(1,1), (1,2), (2,2)]
    color = "green"
    mock_direction = mock.Mock()
    mock_direction.__str__ = mock.Mock(return_value = 'N')
    snake = Snake(segments, color, mock_direction, mock_board)
    assert str(snake.direction) == 'N'
    assert snake.color == "green"
    assert snake.segments == [(1,1), (1,2), (2,2)]

def test_snake_destroyed():
    mock_board = mock.Mock()
    segments = [(1,1), (1,2), (2,2)]
    color = "green"
    mock_direction = mock.Mock()
    mock_direction.__str__ = mock.Mock(return_value = 'N')
    snake = Snake(segments, color, mock_direction, mock_board)

    snake.destroy()

    for segment_coords in segments:
        mock_board.request_field.assert_any_call(segment_coords)
        mock_field = mock_board.request_field(segment_coords)

    assert mock_field.remove_snake.call_count == len(segments)
    assert snake.is_alive == False

def test_snake_noticed_grow():
    mock_board = mock.Mock()
    segments = [(1,1), (1,2), (2,2)]
    color = "green"
    mock_direction = mock.Mock()
    mock_direction.__str__ = mock.Mock(return_value = 'N')
    snake = Snake(segments, color, mock_direction, mock_board)

    snake.grow()

    assert snake.grow_at_next_move == True

def move_coord_north(coords):
    return coords[0], coords[1] + 1

def test_check_snake_move_false():
    mock_board = mock.Mock()
    segments = [(1,1), (1,2), (2,2)]
    color = "green"
    mock_direction = mock.Mock()
    mock_direction.__str__ = mock.Mock(return_value = 'N')
    mock_direction.move_in_direction.side_effect = move_coord_north
    snake = Snake(segments, color, mock_direction, mock_board)

    mock_field = mock.Mock()
    mock_field.check_snake_move.return_value = False
    mock_board.request_field.return_value = mock_field

    snake.move()

    mock_direction.move_in_direction.assert_called_once()
    mock_board.request_field.assert_any_call((2,3))

    assert snake.is_alive == False

def test_snake_enters_field_no_grow():
    mock_board = mock.Mock()
    segments = [(1,1), (1,2), (2,2)]
    color = "green"
    mock_direction = mock.Mock()
    mock_direction.__str__ = mock.Mock(return_value = 'N')
    mock_direction.move_in_direction.side_effect = move_coord_north
    snake = Snake(segments, color, mock_direction, mock_board)

    mock_field = mock.Mock()
    mock_field.check_snake_move.return_value = True
    mock_board.request_field.return_value = mock_field

    snake.move()

    mock_field.snake_entered.assert_called_once_with(snake, mock_direction)
    assert snake.segments == [(1,2), (2,2), (2,3)]

def test_snake_enters_field_and_grows():
    mock_board = mock.Mock()
    segments = [(1,1), (1,2), (2,2)]
    color = "green"
    mock_direction = mock.Mock()
    mock_direction.__str__ = mock.Mock(return_value = 'N')
    mock_direction.move_in_direction.side_effect = move_coord_north
    snake = Snake(segments, color, mock_direction, mock_board)

    mock_field = mock.Mock()
    mock_field.check_snake_move.return_value = True
    mock_board.request_field.return_value = mock_field

    snake.grow()
    snake.move()

    mock_field.snake_entered.assert_called_once_with(snake, mock_direction)
    assert snake.segments == [(1,1), (1,2), (2,2), (2,3)]
    assert snake.grow_at_next_move == False

def test_growing_snake_dies_when_entering_field():
    mock_board = mock.Mock()
    segments = [(1,1), (1,2), (2,2)]
    color = "green"
    mock_direction = mock.Mock()
    mock_direction.__str__ = mock.Mock(return_value = 'N')
    mock_direction.move_in_direction.side_effect = move_coord_north
    snake = Snake(segments, color, mock_direction, mock_board)

    mock_field = mock.Mock()
    mock_field.check_snake_move.return_value = True
    mock_field.snake_entered.side_effect = lambda snake, direction: snake.destroy() 
    mock_board.request_field.return_value = mock_field

    snake.grow()
    snake.move()

    mock_field.snake_entered.assert_called_once_with(snake, mock_direction)
    assert mock_field.remove_snake.call_count == 3
    assert snake.is_alive == False
    assert snake.segments == [(1,1), (1,2), (2,2)]
    assert snake.grow_at_next_move == False

def test_snake_collides_with_snake_body():
    mock_board = mock.Mock()
    segments = [(1,2), (2,2),(3,2)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)

    other_segments = [(1,1), (1,2), (2,2)]
    other_snake = Snake(other_segments, color, mock_direction, mock_board)

    snake.interact_with_snake(other_snake)
    assert other_snake.is_alive == False
    assert snake.is_alive == True

def test_snake_collides_with_snake_head():
    mock_board = mock.Mock()
    segments = [(1,2), (2,2),(3,2)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)

    other_segments = [(5,2), (4,2), (3,2)]
    other_snake = Snake(other_segments, color, mock_direction, mock_board)

    snake.interact_with_snake(other_snake)
    assert other_snake.is_alive == False
    assert snake.is_alive == False

def test_snake_collides_with_itself():
    mock_board = mock.Mock()
    segments = [(0,0), (1,0), (1,1), (0,1), (0,0)]
    color = "green"
    mock_direction = mock.Mock()
    snake = Snake(segments, color, mock_direction, mock_board)

    snake.interact_with_snake(snake)
    assert snake.is_alive == False

    



    
    