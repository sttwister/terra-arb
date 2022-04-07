import os

from dotenv import load_dotenv


load_dotenv()


def env(name, default=None):
    return os.environ.get(name, default)


EXECUTE = False
USE_WALLET_FOR_SIMULATE = False
SLEEP_INTERVAL = 3

MNEMONIC = env('MNEMONIC')
NETWORK = env('NETWORK', 'testnet')
