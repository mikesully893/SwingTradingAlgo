from unittest.mock import patch
import pytest

from strategies.breakout import Breakout


def test_prepare_orders(mock_breakout):
    # Arrange
    mock_breakout.data = [
        ["20220101120000", 150.0, 160.0],
        ["20220101120000", 160.0, 170.0],
    ]
    # Act
    with patch.object(
        Breakout, "reqHistoricalData", return_value=None
    ) as mock_hist_data:
        with patch.object(
            Breakout, "placeOrder", return_value=None
        ) as mock_place_order:
            mock_breakout.prepare_orders()
            # Assert
            assert mock_place_order.call_count == 2
            assert mock_hist_data.call_count == 2
