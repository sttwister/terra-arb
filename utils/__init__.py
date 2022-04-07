import base64
import json

from terra_sdk.core import Coins, Coin

from utils.network import network


def encode_msg(msg):
    return base64.b64encode(json.dumps(msg, separators=(',', ':')).encode()).decode()


def make_coins(token, amount):
    return Coins([
        Coin(network.NATIVE_COINS[token], amount)
    ])
