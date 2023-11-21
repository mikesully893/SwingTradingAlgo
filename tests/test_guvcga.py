from unittest.mock import patch
import pytest

from strategies.guvcga import Guvcga


def test_prepare_orders(mock_guvcga):
    # Arrange
    mock_guvcga.data = [
        ["20220101120000", 150.0, 160.0],
        ["20220101120000", 160.0, 170.0],
        ["20220101120000", 162.0, 171.0],
        [
            "20220101120000",
            159.0,
            172.0,
        ],  # Example data, replace with your desired data
        # Add more rows as needed
    ]
    # Act
    with patch.object(Guvcga, "reqHistoricalData", return_value=None) as mock_hist_data:
        with patch.object(Guvcga, "placeOrder", return_value=None) as mock_place_order:
            mock_guvcga.prepare_orders()
            # Assert
            assert mock_place_order.call_count == 4
            assert mock_hist_data.call_count == 2
