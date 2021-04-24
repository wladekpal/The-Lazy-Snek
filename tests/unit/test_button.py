from src.display.button import Button, CancelButton, PlayButton, RestartButton
import mock
import pytest


def test_cant_instantiate_button_object():
    simulation = mock.Mock()
    texture = mock.Mock()
    with pytest.raises(TypeError):
        Button(simulation, texture)


def test_instantiate_cancel_button_object():
    simulation = mock.Mock()
    texture = mock.Mock()
    button = CancelButton(simulation, texture)
    assert button.simulation == simulation
    assert button.texture == texture


def test_instantiate_play_button_object():
    simulation = mock.Mock()
    texture = mock.Mock()
    additional_texture = mock.Mock()
    button = PlayButton(simulation, texture, additional_texture)
    assert button.simulation == simulation
    assert button.texture == texture


def test_button_with_mouse_click_inside_its_area():
    simulation = mock.Mock()
    button = RestartButton(simulation, mock.Mock())
    button.position = (50, 50)
    button.displayed_side_length = 30
    mouse_position = (60, 70)
    button.process_mouse_click(mouse_position)
    simulation.restart.assert_called_once()


def test_button_with_mouse_click_outside_its_area():
    simulation = mock.Mock()
    button = CancelButton(simulation, mock.Mock())
    button.position = (50, 50)
    button.displayed_side_length = 30
    mouse_position = (40, 70)
    button.process_mouse_click(mouse_position)
    simulation.cancel.assert_not_called()


def test_button_replace_texture():
    button = RestartButton(mock.Mock(), mock.Mock())
    new_texture = mock.Mock()
    button.replace_texture(new_texture)
    assert button.texture == new_texture
