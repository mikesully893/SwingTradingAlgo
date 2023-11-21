import logging
import time
from datetime import datetime

import pandas as pd

from strategies.base_strategy import BaseStrategy


logger = logging.getLogger(__name__)


class Guvcga(BaseStrategy):
    def __init__(self, symbol, notional_value, max_loss):
        super().__init__(symbol, notional_value, max_loss, "Guvcga")
        self.half_position_loss = 10

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

        entry_price = round(df.iloc[-2, 2] + 0.02, 2)
        stop_price_1 = round(
            ((float(entry_price) * quantity) - self.half_position_loss) / quantity, 2
        )
        stop_price_2 = round(
            ((float(entry_price) * quantity) - self.max_loss) / quantity, 2
        )
        timestamp_string = datetime.now().strftime("%Y%m%d%H%M%S%f")
        order_ref = f"Guvcga-{timestamp_string}"

        order_1 = self.create_order("STP", quantity, entry_price, order_ref)
        order_2 = self.create_order("STP", quantity, entry_price, order_ref)
        stop_order_1 = self.create_stop_loss(order_1, quantity, stop_price_1, order_ref)
        stop_order_2 = self.create_stop_loss(order_2, quantity, stop_price_2, order_ref)

        self.placeOrder(order_1.orderId, self.contract, order_1)
        self.placeOrder(order_2.orderId, self.contract, order_2)
        self.placeOrder(stop_order_1.orderId, self.contract, stop_order_1)
        self.placeOrder(stop_order_2.orderId, self.contract, stop_order_2)
