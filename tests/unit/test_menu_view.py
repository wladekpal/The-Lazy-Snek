from unittest import mock
import pygame
from src.gameplay.menu_view import MenuView


def test_instantiate_menu_view():
    screen = mock.Mock()
    view = MenuView(screen)
    assert view.screen == screen


def test_menu_view_frames_heights_add_up_to_screen_height_after_refresh():
    pygame.init()
    screen = pygame.display.set_mode((251, 315))
    menu_view = MenuView(screen)
    menu_view.refresh()
    height_sum = menu_view.title_frame.get_height() + menu_view.tiles_frame.get_height()
    assert height_sum == screen.get_height()


def test_menu_view_title_frame_width_equal_to_screen_width_after_refresh():
    pygame.init()
    screen = pygame.display.set_mode((217, 639))
    menu_view = MenuView(screen)
    menu_view.refresh()
    assert menu_view.title_frame.get_width() == screen.get_width()


def test_menu_view_tiles_frame_width_equal_to_screen_width_after_refresh():
    pygame.init()
    screen = pygame.display.set_mode((187, 366))
    menu_view = MenuView(screen)
    menu_view.refresh()
    assert menu_view.tiles_frame.get_width() == screen.get_width()
