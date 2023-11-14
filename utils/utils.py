import time
import datetime

from ibapi.contract import Contract


def stock_contract(symbol, sec_type="STK", exchange="SMART", currency="USD"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange = exchange
    contract.currency = currency
    return contract


def sleep_until(target: datetime.datetime):
    now = datetime.datetime.now()
    delta = target - now
    if delta > datetime.timedelta(0):
        time.sleep(delta.total_seconds())
