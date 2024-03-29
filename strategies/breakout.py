import time
from datetime import datetime
import logging

import pandas as pd

from strategies.base_strategy import BaseStrategy


logger = logging.getLogger(__name__)


class Breakout(BaseStrategy):
    def __init__(self, symbol, notional_value, max_loss):
        super().__init__(symbol, notional_value, max_loss, "Breakout")

    def prepare_orders(self):
        self.reqHistoricalData(
            1, self.contract, "", "180 S", "1 min", "ASK", 0, 2, False, []
        )
        time.sleep(2)
        df = pd.DataFrame(self.data, columns=["DateTime", "Close", "High"])
        current_price = df.iloc[0, 1]
        quantity = round(self.notional_value / current_price, 0)
        self.reqHistoricalData(
            1, self.contract, "", "2 D", "1 day", "ASK", 1, 2, False, []
        )
        time.sleep(2)
        df = pd.DataFrame(self.data, columns=["DateTime", "Close", "High"])
        entry_price = str(round(df.iloc[0, 2] * 1.015, 2))
        stop_price = round(
            ((float(entry_price) * quantity) - self.max_loss) / quantity, 2
        )
        timestamp_string = datetime.now().strftime("%Y%m%d%H%M%S%f")
        order_ref = f"Breakout-{timestamp_string}"

        order = self.create_order("STP", quantity, entry_price, order_ref)
        stop_order = self.create_stop_loss(order, quantity, stop_price, order_ref)

        # logger.info("Testing placing a trade now")
        self.placeOrder(order.orderId, self.contract, order)
        self.placeOrder(stop_order.orderId, self.contract, stop_order)
