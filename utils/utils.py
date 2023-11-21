import time
import datetime
import yfinance as yf

from ibapi.contract import Contract


def stock_contract(symbol, sec_type="STK", exchange="SMART", currency="USD"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange = exchange
    contract.currency = currency
    return contract


def validate_config_symbols(symbols: list):
    valid_symbols = []
    for symbol in symbols:
        if not isinstance(symbol, str):
            print(f"{symbol} is not a string")
            continue
        data = yf.Ticker(symbol.upper()).history(period="7d", interval="1d")
        if not len(data):
            print(f"Could not find a valid ticker for value {symbol.upper()}")
            continue
        valid_symbols.append(symbol.upper())
    return valid_symbols


def sleep_until(target: datetime.datetime):
    now = datetime.datetime.now()
    delta = target - now
    if delta > datetime.timedelta(0):
        time.sleep(delta.total_seconds())
