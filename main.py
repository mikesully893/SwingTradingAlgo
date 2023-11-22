import argparse
import json

from strategies.breakout import Breakout
from strategies.guvcga import Guvcga
from utils.utils import validate_config_symbols


def run_strategy(strategy_name, symbols, trade_value, max_loss):
    for symbol in symbols:
        print(f"Starting for {strategy_name}: {symbol}")
        if strategy_name == "Breakout":
            strategy = Breakout(symbol, trade_value, max_loss)
        elif strategy_name == "Guvcga":
            strategy = Guvcga(symbol, trade_value, max_loss)
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        strategy.start_thread()
        strategy.prepare_orders()
        strategy.finish_thread()


def run_algorithm(config):
    with open(config) as file:
        config_json = json.load(file)
    strategies = config_json["strategies"]
    trade_value = config_json["notional_position_value"]
    if "max_loss" in config_json:
        max_loss = config_json["max_loss"]
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
