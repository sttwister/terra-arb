import os

from dotenv import load_dotenv


load_dotenv()


def env(name, default=None):
    return os.environ.get(name, default)


MNEMONIC = env('MNEMONIC')
NETWORK = env('NETWORK', 'testnet')

ENABLED_STRATEGY_GROUPS = [
    'luna_arb',
    'prism_arb',
    'luna_withdraw',
]
ACTIVE_PLUGINS = [
    'rich',
]

EXECUTE = bool(env('EXECUTE', False))
BROADCAST_TX = bool(env('BROADCAST_TX', False))
USE_WALLET_FOR_SIMULATE = bool(env('USE_WALLET_FOR_SIMULATE', False))
SLEEP_INTERVAL = int(env('SLEEP_INTERVAL', 3))
