
import yfinance as yf
import json

from utils.exceptions import NoStrategyProvidedError


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


def validate_config_json(config_json):
    if "strategies" not in config_json or len(config_json["strategies"]) == 0:
        raise NoStrategyProvidedError("No strategies have been provided in the json config")

    return config_json
