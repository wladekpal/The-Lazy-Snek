import pytest
from src.engine.board import Board, OutOfRange, NotExistingField, WrongMatrix


bad_fields = []

fields = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None]
    ]

board = Board(fields)


def wrong_matrix_test():
    try:
        Board(bad_fields)
        assert False
    except WrongMatrix:
        assert True


def negative_x_value_test():
    try:
        board.request_field(-1, 0)
        assert False
    except OutOfRange:
        assert True


def negative_y_value_test():
    try:
        board.request_field(0, -1)
        assert False
    except OutOfRange:
        assert True


def both_negative_values_test():
    try:
        board.request_field(-1, -1)
        assert False
    except OutOfRange:
        assert True


def higher_than_max_x_value_test():
    width = len(fields[0])
    try:
        board.request_field(width+1, 0)
        assert False
    except OutOfRange:
        assert True


def higher_than_max_y_value_test():
    height = len(fields)
    try:
        board.request_field(height+1, 0)
        assert False
    except OutOfRange:
        assert True


def none_field_request_test():
    try:
        board.request_field(0, 0)
        assert False
    except NotExistingField:
        assert True
