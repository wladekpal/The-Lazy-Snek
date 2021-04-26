from unittest import mock
from src.display.menu_view import MenuView


def test_instantiate_menu_view():
    screen = mock.Mock()
    view = MenuView(screen)
    assert view.screen == screen
