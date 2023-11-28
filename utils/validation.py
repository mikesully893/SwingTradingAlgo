import yfinance as yf
import json

from utils.exceptions import (
    NoStrategyProvidedError,
    NoModeProvidedError,
    NoMaxLossProvidedError,
    NoPositionValueProvidedError,
    InvalidConfigValueError,
)


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
        raise NoStrategyProvidedError(
            "No strategies have been provided in the json config"
        )
    if "mode" not in config_json:
        raise NoModeProvidedError("mode must be provided in the json config")
    if config_json["mode"] != "PAPER":
        raise InvalidConfigValueError(
            f"{config_json['mode']} is not a valid value for mode. Must be PAPER or LIVE."
        )
    if "max_loss" not in config_json:
        raise NoMaxLossProvidedError("max_loss must be provided in the json config")
    if not isinstance(config_json["max_loss"], int):
        raise InvalidConfigValueError(
            f"{config_json['max_loss']} is not a valid value for max_loss. Must be an integer"
        )
    if "notional_position_value" not in config_json:
        raise NoPositionValueProvidedError(
            "notional_position_value must be provided in the json config"
        )
    if not isinstance(config_json["notional_position_value"], int):
        raise InvalidConfigValueError(
            f"{config_json['notional_position_value']} is not a valid value for notional_position_value. Must be an integer"
        )
    return config_json
