import pytest
from unittest.mock import Mock, patch

from strategies.guvcga import Guvcga
from utils.ib_api import IBapi
from strategies.breakout import Breakout


class MockBreakout(Breakout):
    def __init__(self):
        super().__init__("AAPL", 1000, 10)


class MockGuvcga(Guvcga):
    def __init__(self):
        super().__init__("TSLA", 200, 10)


@pytest.fixture
def ibapi_instance():
    ibapi = IBapi()
    ibapi.start_thread()
    yield ibapi
    ibapi.finish_thread()


@pytest.fixture
def mock_breakout():
    return MockBreakout()


@pytest.fixture
def mock_guvcga():
    return MockGuvcga()
