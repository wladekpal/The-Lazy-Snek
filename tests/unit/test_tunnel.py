from src.engine.tunnel import Tunnel
import mock


def test_tunnel_creation():
    mock_direction = mock.MagicMock()
    Tunnel(mock_direction)

    mock_direction.__str__.return_value = 'E'
    Tunnel(mock_direction)


def test_set_coordinates():
    mock_direction = mock.Mock()
    tunnel = Tunnel(mock_direction)

    tunnel.set_coordinates((1, 1))
    assert tunnel.coordinates == (1, 1)


def test_set_board():
    mock_direction = mock.Mock()
    mock_board = mock.Mock()
    tunnel = Tunnel(mock_direction)

    tunnel.set_board(mock_board)
    assert tunnel.board == mock_board
    assert tunnel.upper_field.board == mock_board
    assert tunnel.lower_field.board == mock_board


def test_choose_field():
    mock_direction1 = mock.MagicMock()
    mock_direction2 = mock.Mock()

    mock_direction1.__eq__.return_value = False
    tunnel = Tunnel(mock_direction1)
    assert tunnel.choose_field(mock_direction2) == tunnel.lower_field

    mock_direction1.__eq__.return_value = True
    tunnel = Tunnel(mock_direction1)
    assert tunnel.choose_field(mock_direction2) == tunnel.upper_field
