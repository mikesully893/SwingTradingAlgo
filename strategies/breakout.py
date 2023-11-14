import time
import threading
from datetime import datetime

import pandas as pd

from utils.utils import stock_contract
from utils.ib_api import IBapi


class Breakout(IBapi):
    def __init__(self, symbol, notional_value, max_loss):
        super().__init__()
        self.symbol = symbol
        self.notional_value = notional_value
        self.max_loss = max_loss
        self.nextorderId = 0
        self.contract = stock_contract(symbol)

    def run_app(self):
        print(f"Preparing to start thread for {self.symbol}..")
        self.run()

    def start_thread(self):
        self.connect("127.0.0.1", 7497, 123)
        api_thread = threading.Thread(target=self.run_app, daemon=True)
        api_thread.start()
        time.sleep(1)
        print(api_thread.name)

    def finish_thread(self):
        time.sleep(5)
        print(f"Finishing thread for {self.symbol}")
        self.disconnect()

    def prepare_orders(self):
        self.reqHistoricalData(
            1, self.contract, "", "120 S", "1 min", "ASK", 0, 2, False, []
        )
        time.sleep(2)
        df = pd.DataFrame(self.data, columns=["DateTime", "Close", "High"])
        current_price = df.iloc[0, 1]
        quantity = round(self.notional_value / current_price, 0)
        self.reqHistoricalData(
            1, self.contract, "", "2 D", "1 day", "ASK", 0, 2, False, []
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

        self.placeOrder(order.orderId, self.contract, order)
        self.placeOrder(stop_order.orderId, self.contract, stop_order)
