from src.engine.field import Field
import mock


def create_field_snake_flat(coords):
    field = Field(coords)
    flat = mock.Mock()
    snake = mock.Mock()
    field.place_snake(snake)
    field.place_flat(flat)
    return field, snake, flat


def create_field_convex_flat(coords):
    field = Field(coords)
    flat = mock.Mock()
    convex = mock.Mock()
    field.place_convex(convex)
    field.place_flat(flat)
    return field, convex, flat


def create_field_convex(coords):
    field = Field(coords)
    convex = mock.Mock()
    field.place_convex(convex)
    return field, convex


def create_field_snake(coords):
    field = Field(coords)
    snake = mock.Mock()
    field.place_snake(snake)
    return field, snake


def create_field_flat(coords):
    field = Field(coords)
    flat = mock.Mock()
    field.place_flat(flat)
    return field, flat


def test_field_creation():
    field = Field((1, 2))
    assert field.coordinates == (1, 2)


def test_self_board():
    field = Field((1, 1))
    mock_board = mock.Mock()
    field.set_board(mock_board)
    assert field.board == mock_board


def test_give_field_in_direction():
    mock_direction = mock.Mock()
    mock_direction.move_in_direction.side_effect = lambda x: (x[0], x[1]+1)
    mock_board = mock.Mock()
    field = Field((5, 5))
    field.set_board(mock_board)
    field.give_field_in_direction(mock_direction)
    mock_board.request_field.assert_called_once_with((5, 6))


def test_check_snake_move_no_convex():
    field = Field((3, 3))
    mock_snake = mock.Mock()
    assert field.check_snake_move(mock_snake)


def test_check_snake_move_with_convex():
    field = Field((3, 3))
    mock_snake = mock.Mock()
    mock_convex = mock.Mock()
    mock_convex.check_snake_move.return_value = True

    field.place_convex(mock_convex)
    assert field.check_snake_move(mock_snake)

    mock_convex.check_snake_move.return_value = False
    field.place_convex(mock_convex)
    assert not field.check_snake_move(mock_snake)


def test_snake_entered_snake_on_field():
    mock_snake_entering = mock.Mock()
    field, mock_snake, mock_flat = create_field_snake_flat((1, 1))
    field.snake_entered(mock_snake_entering)
    assert mock_flat.interact_with_snake.call_count == 0
    mock_snake.interact_with_snake.assert_called_once_with(mock_snake_entering)

    assert field.snake_layer == mock_snake_entering


def test_snake_entered_snake_not_on_field():
    mock_snake_entering = mock.Mock()
    field, mock_convex, mock_flat = create_field_convex_flat((1, 1))
    field.snake_entered(mock_snake_entering)
    mock_convex.interact_with_snake.assert_called_once_with(mock_snake_entering)
    mock_flat.interact_with_snake.assert_called_once_with(mock_snake_entering)

    assert field.snake_layer == mock_snake_entering


def test_snake_entered_and_died_after():
    mock_snake_entering = mock.Mock()
    field, mock_convex, mock_flat = create_field_convex_flat((1, 1))
    mock_snake_entering.is_alive = False
    field.snake_entered(mock_snake_entering)

    assert not field.snake_layer == mock_snake_entering


def test_snake_left():
    field, mock_snake = create_field_snake((1, 1))
    field.snake_left()
    assert field.snake_layer is None


def test_remove_snake():
    field, mock_snake = create_field_snake((1, 1))
    mock_snake2 = mock.Mock()
    field.remove_snake(mock_snake2)
    assert field.snake_layer is not None
    field.remove_snake(mock_snake)
    assert field.snake_layer is None


def test_place_snake():
    field = Field((1, 1))
    mock_snake = mock.Mock()
    field.place_snake(mock_snake)
    assert field.snake_layer == mock_snake


def test_remove_flat():
    field, _ = create_field_flat((1, 1))
    field.remove_flat()
    assert field.flat_layer is None


def test_place_flat():
    field = Field((1, 1))
    mock_flat = mock.Mock()
    field.place_flat(mock_flat)
    assert field.flat_layer == mock_flat
    mock_flat.set_field.asset_called_once_with(field)


def test_check_convex_move_no_convex():
    field = Field((3, 3))
    mock_direction = mock.Mock()
    assert field.check_convex_move(mock_direction)


def test_check_convex_move_with_convex():
    field = Field((3, 3))
    mock_direction = mock.Mock()
    mock_convex = mock.Mock()
    mock_convex.check_move.return_value = True

    field.place_convex(mock_convex)
    assert field.check_convex_move(mock_direction)

    mock_convex.check_move.return_value = False
    field.place_convex(mock_convex)
    assert not field.check_convex_move(mock_direction)


def test_convex_entered_snake_on_field():
    mock_convex_entering = mock.Mock()
    field, mock_snake, mock_flat = create_field_snake_flat((1, 1))
    mock_direction = mock.Mock()
    field.convex_entered(mock_convex_entering, mock_direction)
    mock_snake.interact_with_convex.assert_called_once_with(mock_convex_entering)


def test_convex_entered_snake_not_on_field():
    mock_convex_entering = mock.Mock()
    field, mock_convex, mock_flat = create_field_convex_flat((1, 1))
    mock_direction = mock.Mock()
    field.convex_entered(mock_convex_entering, mock_direction)
    mock_convex.move.assert_called_once_with(mock_direction)
    mock_flat.interact_with_convex.assert_called_once_with(mock_convex_entering)


def test_convex_left():
    field, mock_convex = create_field_convex((1, 1))
    field.convex_left()
    assert field.convex_layer is None


def test_remove_convex():
    field, mock_convex = create_field_convex((1, 1))
    field.remove_convex()
    assert field.convex_layer is None


def test_self_draw_flat():
    field, mock_flat = create_field_flat((1, 1))
    mock_frame = mock.Mock()
    draw_coords = (100, 100)
    side_length = 100

    field.self_draw(mock_frame, draw_coords, side_length)
    assert mock_frame.blit.call_count == 1
    mock_flat.self_draw.assert_called_once_with(mock_frame, draw_coords, side_length)


def test_self_draw_snake():
    field, mock_snake = create_field_snake((1, 1))
    mock_frame = mock.Mock()
    draw_coords = (100, 100)
    side_length = 100

    field.self_draw(mock_frame, draw_coords, side_length)
    assert mock_frame.blit.call_count == 1
    mock_snake.draw_segment.assert_called_once_with(mock_frame, draw_coords, side_length, (1, 1))


def test_self_draw_convex():
    field, mock_convex = create_field_convex((1, 1))
    mock_frame = mock.Mock()
    draw_coords = (100, 100)
    side_length = 100

    field.self_draw(mock_frame, draw_coords, side_length)
    assert mock_frame.blit.call_count == 1
    mock_convex.self_draw.assert_called_once_with(mock_frame, draw_coords, side_length)
