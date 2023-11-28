import argparse
import json

from strategies.breakout import Breakout
from strategies.guvcga import Guvcga
from utils.exceptions import UnknownStrategyError
from utils.validation import validate_config_symbols, validate_config_json


def run_strategy(strategy_name, symbols, trade_value, max_loss):
    for symbol in symbols:
        print(f"Starting for {strategy_name}: {symbol}")
        if strategy_name == "Breakout":
            strategy = Breakout(symbol, trade_value, max_loss)
        elif strategy_name == "Guvcga":
            strategy = Guvcga(symbol, trade_value, max_loss)
        else:
            raise UnknownStrategyError(f"Unknown strategy: {strategy_name}")

        strategy.start_thread()
        strategy.prepare_orders()
        strategy.finish_thread()


def run_algorithm(config):
    with open(config) as file:
        config_json = json.load(file)
    valid_config = validate_config_json(config_json)
    strategies = valid_config["strategies"]
    trade_value = valid_config["notional_position_value"]
    if "max_loss" in valid_config:
        max_loss = valid_config["max_loss"]
    else:
        max_loss = None

    for strategy_name in strategies:
        symbols_key = f"{strategy_name.lower()}_symbols"
        symbols = config_json[symbols_key]
        symbols = validate_config_symbols(symbols)
        run_strategy(strategy_name, symbols, trade_value, max_loss)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        required=False,
        default="config.json",
        help="Path to config file. If omitted the config in the root directory of the project will be used.",
    )
    args = parser.parse_args()
    # pause.until(datetime(2023, 11, 14, 14, 36))
    run_algorithm(args.config)
