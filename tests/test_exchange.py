import pytest

from workers.exchange import ExchangeClient, OrderPlacementError


def test_succeeds(mocker):
    mocker.patch("workers.exchange.random.random", return_value=0.5)
    mocker.patch("workers.exchange.time.sleep")
    ExchangeClient().place_order("order-1")


def test_raises_on_bad_luck(mocker):
    mocker.patch("workers.exchange.random.random", return_value=0.05)
    mocker.patch("workers.exchange.time.sleep")
    with pytest.raises(OrderPlacementError):
        ExchangeClient().place_order("order-1")


def test_sleeps_half_second(mocker):
    mocker.patch("workers.exchange.random.random", return_value=0.5)
    mock_sleep = mocker.patch("workers.exchange.time.sleep")
    ExchangeClient().place_order("order-1")
    mock_sleep.assert_called_once_with(0.5)
