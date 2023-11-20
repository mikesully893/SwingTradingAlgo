from utils.ib_api import IBapi
from utils.utils import stock_contract


class BaseStrategy(IBapi):
    def __init__(self, symbol, notional_value, max_loss, strategy_name):
        super().__init__()
        self.symbol = symbol
        self.notional_value = notional_value
        self.max_loss = max_loss
        self.strategy_name = strategy_name
        self.nextorderId = 0
        self.contract = stock_contract(symbol)

    def prepare_orders(self):
        raise NotImplementedError("Subclasses must implement prepare_orders method")
