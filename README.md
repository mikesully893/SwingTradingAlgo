# SwingTradingAlgo
This python application generates orders as per pre-defined strategies for an Interactive Brokers account using the 
Interactive Brokers TWS Python API. 

## Requirements
* Python 3
* Interactive Brokers TWS Python API
* Interactive Brokers account
* Interactive Brokers Trader Workstation desktop application installed and running, logged into the desired trading account

## Usage

### Strategies
Custom strategies can easily be developed. The two strategies defined here inherit from the `BaseStrategy` base class. This can
be used and extended however seen fit once it implements the `prepare_orders` method. Once this is done, it must be added 
as an option in the `run_strategy` function in `main.py`.

### Config file
The programme is config driven. The details of the config file are outlined in the table below. By default, the programme will 
look for a `config.json`. If you wanted to have different config files for different scenarios, you can specify the name of the
config file to be used by passing it after the `-c` or `--config` flags when running the programme.


| Field Name | Description |
|------------| --- |
| mode       | The trading mode you are using. Opetions are ```PAPER``` and ```LIVE``` |
| max_loss   | The max amount in dollars that would be lost between entry point and stop loss |
| strategies | Include the name of the strategies to be used by the programme |
| notional_position_value | The size in dollars of each position |
| {strategy_name}_symbols | Add a new field for each strategy named as such. The value will be an array of ticker symbols to be used by the strategy |

### Running the Programme

```commandline
usage: main.py [-h] [-c CONFIG]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
```
To run using the default config file, run:
```commandline
python main.py
```