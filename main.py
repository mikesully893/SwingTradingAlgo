import os
import pause
import argparse
import json
from datetime import datetime

from strategies.breakout import Breakout
from strategies.guvcga import Guvcga


def run_algorithm(config):
    # TODO: Add config validation
    with open(config) as file:
        config_json = json.load(file)
    symbols = config_json["breakout_symbols"]
    trade_value = config_json["notional-position-value"]
    if "max-loss" in config_json:
        max_loss = config_json["max-loss"]
    else:
        max_loss = None

    for symbol in symbols:
        # TODO: Add logic to run these in parallel
        print(f"Starting for loop for {symbol}...")
        breakout_trade = Breakout(symbol, trade_value, max_loss)
        breakout_trade.start_thread()
        breakout_trade.prepare_orders()
        breakout_trade.finish_thread()


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
    pause.until(datetime(2023, 11, 14, 14, 36))
    run_algorithm(args.config)
