import threading
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.order import Order


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.contract_details = {}
        self.data = []

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print("The next valid order id is: ", self.nextorderId)

    def historicalData(self, reqId, bar):
        print(f"Time: {bar.date} Close: {bar.close} High: {bar.high}")
        self.data.append([bar.date, bar.close, bar.high])

    def orderStatus(
        self,
        orderId,
        status,
        filled,
        remaining,
        avgFullPrice,
        permId,
        parentId,
        lastFillPrice,
        clientId,
        whyHeld,
        mktCapPrice,
    ):
        print(
            "orderStatus - orderid:",
            orderId,
            "status:",
            status,
            "filled",
            filled,
            "remaining",
            remaining,
            "lastFillPrice",
            lastFillPrice,
        )

    def openOrder(self, orderId, contract, order, orderState):
        print(
            "openOrder id:",
            orderId,
            contract.symbol,
            contract.secType,
            "@",
            contract.exchange,
            ":",
            order.action,
            order.orderType,
            order.totalQuantity,
            orderState.status,
        )

    def execDetails(self, reqId, contract, execution):
        print(
            "Order Executed: ",
            reqId,
            contract.symbol,
            contract.secType,
            contract.currency,
            execution.execId,
            execution.orderId,
            execution.shares,
            execution.lastLiquidity,
        )

    def run_app(self):
        self.run()

    def start_thread(self):
        self.connect("127.0.0.1", 7497, 123)
        api_thread = threading.Thread(target=self.run_app, daemon=True)
        api_thread.start()
        time.sleep(1)
        print(api_thread.name)

    def finish_thread(self):
        time.sleep(2)
        self.disconnect()

    def create_order(
        self, order_type, quantity, price, order_ref, action="BUY", transmit=False
    ):
        order = Order()
        order.action = action
        order.totalQuantity = quantity
        order.orderType = order_type
        order.auxPrice = price
        order.orderId = self.nextorderId
        order.orderRef = order_ref
        self.nextorderId += 1
        order.transmit = transmit
        return order

    def create_stop_loss(
        self, parent_order, quantity, price, order_ref, action="SELL", transmit=True
    ):
        stop_order = Order()
        stop_order.action = action
        stop_order.totalQuantity = quantity
        stop_order.orderType = "STP"
        stop_order.auxPrice = price
        stop_order.tif = "GTC"
        stop_order.orderId = self.nextorderId
        stop_order.orderRef = order_ref
        self.nextorderId += 1
        stop_order.parentId = parent_order.orderId
        parent_order.transmit = transmit
        return stop_order

    # def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
    #     if errorCode == 202:
    #         print("order canceled")
