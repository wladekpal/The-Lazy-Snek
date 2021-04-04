from unittest import mock
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

    x_neg_pos = (-1, 0)
    try:
        board.request_field(x_neg_pos)
        assert False
    except OutOfRange:
        assert True


def test_negative_y_value():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    y_neg_pos = (0, -1)
    try:
        board.request_field(y_neg_pos)
        assert False
    except OutOfRange:
        assert True


def test_both_negative_values():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    both_neg_pos = (-1, -1)
    try:
        board.request_field(both_neg_pos)
        assert False
    except OutOfRange:
        assert True


def test_higher_than_max_x_value():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    width = len(fields[0])

    x_too_big_pos = (width + 1, 0)
    try:
        board.request_field(x_too_big_pos)
        assert False
    except OutOfRange:
        assert True


def test_higher_than_max_y_value():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    height = len(fields)

    y_too_big_pos = (0, height + 1)
    try:
        board.request_field(y_too_big_pos)
        assert False
    except OutOfRange:
        assert True


def test_none_field_request():
    fields = build_matrix(10, 8, None)
    board = Board(fields)

    correct_pos = (0, 0)
    try:
        board.request_field(correct_pos)
        assert False
    except NotExistingField:
        assert True


def test_good_field_request():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    correct_pos = (0, 0)
    assert board.request_field(correct_pos) == field


def test_self_draw():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    frame = mock.Mock()
    frame.get_width.return_value = 400
    frame.get_height.return_value = 500

    board.self_draw(frame)
    assert field.self_draw.call_count == len(fields) * len(fields[0])


def test_too_small_board():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    frame = mock.Mock()
    frame.get_width.return_value = 8
    frame.get_height.return_value = 8

    try:
        board.self_draw(frame)
        assert False
    except ImpossibleToDraw:
        assert True


def test_make_tick():
    fields = build_matrix(10, 8, field)
    board = Board(fields)

    board.make_tick()
    assert field.make_tick.call_count == len(fields) * len(fields[0])
