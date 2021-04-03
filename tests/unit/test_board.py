import pytest
import mock
from src.engine.board import Board, OutOfRange, NotExistingField, ImpossibleToDraw, WrongMatrix

field = mock.Mock()


def build_matrix(rows, cols, elem):
    matrix = []

    for r in range(0, rows):
        matrix.append([elem for c in range(0, cols)])

    return matrix


def test_wrong_matrix():
    bad_fields = build_matrix(0, 0, field)

    try:
        Board(bad_fields)
        assert False
    except WrongMatrix:
        assert True


def test_negative_x_value():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    try:
        board.request_field(-1, 0)
        assert False
    except OutOfRange:
        assert True


def test_negative_y_value():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    try:
        board.request_field(0, -1)
        assert False
    except OutOfRange:
        assert True


def test_both_negative_values():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    try:
        board.request_field(-1, -1)
        assert False
    except OutOfRange:
        assert True


def test_higher_than_max_x_value():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    width = len(fields[0])

    try:
        board.request_field(width+1, 0)
        assert False
    except OutOfRange:
        assert True


def test_higher_than_max_y_value():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    height = len(fields)

    try:
        board.request_field(height+1, 0)
        assert False
    except OutOfRange:
        assert True


def test_none_field_request():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    try:
        board.request_field(0, 0)
        assert False
    except NotExistingField:
        assert True


def test_self_draw():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    frame = mock.Mock()
    frame.get_width.return_value = 500
    frame.get_height.return_value = 400

    board.self_draw(frame)
    assert field.self_draw.call_count == len(fields) * len(fields[0])


def test_too_small_board():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    frame = mock.Mock()
    frame.get_width.return_value = 8
    frame.get_width.return_value = 8

    try:
        board.self_draw(frame)
        assert False
    except ImpossibleToDraw:
        assert True
