import os

from dotenv import load_dotenv


load_dotenv()


def env(name, default=None):
    return os.environ.get(name, default)


EXECUTE = False
USE_WALLET_FOR_SIMULATE = False
SLEEP_INTERVAL = 3
ENABLED_STRATEGY_GROUPS = [
    'luna_arb',
    'prism_arb',
    'luna_withdraw',
]
ACTIVE_PLUGINS = [
    'rich',
]

MNEMONIC = env('MNEMONIC')
NETWORK = env('NETWORK', 'testnet')
