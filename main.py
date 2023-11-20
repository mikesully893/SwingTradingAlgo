import os
import pause
import argparse
import json
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
from strategies.breakout import Breakout
from strategies.guvcga import Guvcga


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
    # TODO: Add config validation
    with open(config) as file:
        config_json = json.load(file)
    # symbols = config_json["breakout_symbols"]
    strategies = config_json["strategies"]
    trade_value = config_json["notional_position_value"]
    if "max_loss" in config_json:
        max_loss = config_json["max_loss"]
    else:
        max_loss = None

    with ProcessPoolExecutor() as executor:
        futures = []
        for strategy_name in strategies:
            symbols_key = f"{strategy_name.lower()}_symbols"
            symbols = config_json[symbols_key]
            future = executor.submit(run_strategy, strategy_name, symbols, trade_value, max_loss)
            futures.append(future)

        for future in futures:
            future.result()

    # for symbol in symbols:
    #     # TODO: Add logic to run these in parallel
    #     print(f"Starting for loop for {symbol}...")
    #     breakout_trade = Breakout(symbol, trade_value, max_loss)
    #     breakout_trade.start_thread()
    #     breakout_trade.prepare_orders()
    #     breakout_trade.finish_thread()


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
