from src.display.level_view import LEFT_MOUSE_BUTTON
from pygame.constants import KEYDOWN, K_BACKSPACE, K_ESCAPE, MOUSEBUTTONDOWN
import pytest
import mock
from src.display.editor_size_view import InputBox, SubmitButton, EditorSizeView, UnsupportedEvent
from src.display.view_controller import ViewInitAction


def test_input_box_creation():
    input_box = InputBox()
    assert input_box.color == (255, 255, 255)
    assert not input_box.is_focused
    assert input_box.input_text == ''


def test_input_box_handle_click():
    input_box_pos = (100, 200)
    input_box_size = (50, 100)
    INPUT_BOX_COLOR = (255, 255, 255)
    INPUT_BOX_COLOR_SELECTED = (100, 100, 100)
    test_table = [
        [(125, 250), INPUT_BOX_COLOR_SELECTED, True],
        [(149, 200), INPUT_BOX_COLOR_SELECTED, True],
        [(99, 250), INPUT_BOX_COLOR, False],
        [(300, 201), INPUT_BOX_COLOR, False],
        [(125, 0), INPUT_BOX_COLOR, False]]

    for test in test_table:
        input_box = InputBox()
        input_box.pos = input_box_pos
        input_box.width, input_box.height = input_box_size

        return_value = input_box.handle_click(test[0])
        assert input_box.color == test[1]
        assert input_box.is_focused == test[2]

        if test[2]:
            assert return_value == input_box
        else:
            assert return_value is None


def test_input_box_handle_key_exception():
    input_box = InputBox()

    event_mock = mock.Mock()
    event_mock.type = MOUSEBUTTONDOWN

    with pytest.raises(UnsupportedEvent):
        input_box.handle_key(event_mock)


def test_input_box_handle_key_backspace():
    input_box = InputBox()

    event_mock = mock.Mock()
    event_mock.type = KEYDOWN
    event_mock.key = K_BACKSPACE

    input_box.handle_key(event_mock)

    assert input_box.input_text == ''

    input_box.input_text = '1'
    input_box.handle_key(event_mock)

    assert input_box.input_text == ''

    input_box.input_text = '12'
    input_box.handle_key(event_mock)

    assert input_box.input_text == '1'


def test_input_box_handle_key():
    input_box = InputBox()

    event_mock = mock.Mock()
    event_mock.type = KEYDOWN

    event_mock.unicode = '0'
    input_box.handle_key(event_mock)

    assert input_box.input_text == '0'

    event_mock.unicode = 'a'
    input_box.handle_key(event_mock)

    assert input_box.input_text == '0'

    event_mock.unicode = '9'
    input_box.handle_key(event_mock)

    assert input_box.input_text == '09'

    event_mock.unicode = '5'
    input_box.handle_key(event_mock)

    assert input_box.input_text == '09'


def test_input_box_get_value_empty():
    input_box = InputBox()
    assert input_box.get_value() is None


def test_input_box_get_value():
    input_box = InputBox()

    input_box.input_text = '0'
    assert input_box.get_value() is None

    input_box.input_text = '3'
    assert input_box.get_value() == 3

    input_box.input_text = '24'
    assert input_box.get_value() == 24

    input_box.input_text = '92'
    assert input_box.get_value() is None


def test_submit_button_creation():
    width_input = mock.Mock()
    height_input = mock.Mock()

    submit_button = SubmitButton(width_input, height_input)
    assert submit_button.width_input == width_input
    assert submit_button.height_input == height_input


def test_submit_button_handle_click():
    width_input = mock.Mock()
    height_input = mock.Mock()

    submit_button = SubmitButton(width_input, height_input)
    submit_button.pos = (100, 200)
    submit_button.width, submit_button.height = (50, 100)

    width_input.get_value.return_value = None
    width_input.get_value.return_value = None
    assert submit_button.handle_click((20, 250)) is None
    assert submit_button.handle_click((500, 100)) is None
    assert submit_button.handle_click((52, 205)) is None

    width_input.get_value.return_value = 35
    assert submit_button.handle_click((20, 250)) is None
    assert submit_button.handle_click((500, 100)) is None
    assert submit_button.handle_click((52, 205)) is None

    width_input.get_value.return_value = None
    height_input.get_value.return_value = 25
    assert submit_button.handle_click((20, 250)) is None
    assert submit_button.handle_click((500, 100)) is None
    assert submit_button.handle_click((52, 205)) is None

    width_input.get_value.return_value = 35
    height_input.get_value.return_value = 25
    assert submit_button.handle_click((20, 250)) is None
    assert submit_button.handle_click((500, 100)) is None


def test_edtitor_size_view_creation():
    screen_mock = mock.Mock()
    editor_size_view = EditorSizeView(screen_mock)
    assert editor_size_view.focused_input is None


def test_edtitor_handle_event_mouse():
    screen_mock = mock.Mock()
    editor_size_view = EditorSizeView(screen_mock)

    event_mock = mock.Mock()
    event_mock.type = MOUSEBUTTONDOWN
    event_mock.button = LEFT_MOUSE_BUTTON
    event_mock.pos = (100, 100)

    editor_size_view.height_input.pos = (50, 50)
    editor_size_view.height_input.width, editor_size_view.height_input.height = (100, 100)

    editor_size_view.width_input.pos = (200, 200)
    editor_size_view.width_input.width, editor_size_view.width_input.height = (100, 100)

    editor_size_view.submit.pos = (400, 400)
    editor_size_view.submit.width, editor_size_view.submit.height = (100, 100)

    assert editor_size_view.handle_pygame_event(event_mock) is None
    assert editor_size_view.focused_input == editor_size_view.height_input


def test_editor_handle_event_escape():
    screen_mock = mock.Mock()
    editor_size_view = EditorSizeView(screen_mock)

    event_mock = mock.Mock()
    event_mock.type = KEYDOWN
    event_mock.key = K_ESCAPE

    assert editor_size_view.handle_pygame_event(event_mock) == (None, ViewInitAction.POP)
