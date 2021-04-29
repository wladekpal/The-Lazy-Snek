from src.engine.blocks import Block, Convex, Flat
import pytest
import mock


def test_block_class_object_cant_be_created():
    with pytest.raises(TypeError):
        Block()


def test_convex_class_object_cant_be_created():
    with pytest.raises(TypeError):
        Convex()


def test_flat_class_object_cant_be_created():
    with pytest.raises(TypeError):
        Flat()


def test_block_class_has_static_empty_method_texture():
    Block.__abstractmethods__ = set()
    assert Block.texture() is None


def test_block_class_has_empty_method_interact_with_snake():
    Block.__abstractmethods__ = set()
    snake = mock.Mock()
    assert Block().interact_with_snake(snake) is None


def test_block_class_set_field():
    field = mock.Mock()
    Block.__abstractmethods__ = set()
    block = Block()
    block.set_field(field)
    assert block.field == field


def test_flat_class_has_empty_method_interact_with_convex():
    Flat.__abstractmethods__ = set()
    convex = mock.Mock()
    assert Flat().interact_with_convex(convex) is None


def test_convex_class_has_empty_method_move():
    Convex.__abstractmethods__ = set()
    direction = mock.Mock()
    assert Convex().move(direction) is None


def test_convex_class_has_empty_method_check_snake_move():
    Convex.__abstractmethods__ = set()
    assert Convex().check_snake_move() is None


def test_convex_class_has_empty_method_check_move():
    Convex.__abstractmethods__ = set()
    direction = mock.Mock()
    assert Convex().check_move(direction) is None


def test_block_self_draw_when_drawing_same_size_as_remembered():
    Block().__abstractmethods__ = set()
    frame = mock.Mock()
    position = mock.Mock()
    displayed_texture = mock.Mock()
    block = Block()
    block.displayed_side_length = 10
    block.displayed_texture = displayed_texture
    block.self_draw(frame, position, 10)
    assert block.displayed_texture == displayed_texture
    frame.blit.assert_called_once_with(displayed_texture, position)


def test_convex_that_is_not_alive_self_draw_wont_draw_in_frame_and_will_be_removed_from_its_field():
    Convex().__abstractmethods__ = set()
    convex = Convex()
    convex.is_alive = False
    frame = mock.Mock()
    position = mock.Mock()
    field = mock.Mock()
    convex.field = field
    convex.self_draw(frame, position, 77)
    field.remove_convex.assert_called_once()
    assert not frame.blit.called


def test_convex_that_is_alive_self_draw_will_draw_in_frame_when_remembered_size_equals_current_one():
    Convex().__abstractmethods__ = set()
    convex = Convex()
    convex.is_alive = True
    frame = mock.Mock()
    position = mock.Mock()
    field = mock.Mock()
    convex.field = field
    convex.displayed_side_length = 1234
    convex.self_draw(frame, position, 1234)
    frame.blit.assert_called_once()
