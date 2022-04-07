import json

from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core import Coins
from terra_sdk.core.wasm import MsgExecuteContract
from terra_sdk.key.mnemonic import MnemonicKey

from config import MNEMONIC
from utils import encode_msg, network


class Wallet:
    def __init__(self, mnemonic):
        self.mk = MnemonicKey(mnemonic=mnemonic, coin_type=330)
        self.wallet = network.lcd.wallet(self.mk)

        self.cached = {}

    @property
    def address(self):
        return self.wallet.key.acc_address

    #
    # Coins / tokens
    #

    def reset_cache(self):
        self.cached = {}

    async def populate_cache(self):
        for coin in network.NATIVE_COINS.keys():
            await self.get(coin)

        for token in network.TOKENS.keys():
            await self.get(token)

    def get_summary(self):
        """
        Returns a list of (token, amount) tuples for all cached tokens.
        """
        return [
            (token, '%.2f' % (amount / 1000000))
            for token, amount in self.cached.items()
        ]

    async def get_native_coins_amounts(self):
        coins = (await network.lcd.bank.balance(self.address))[0]
        amounts = {}
        for coin in coins:
            amounts[coin.denom] = coin.amount
        return amounts

    async def get_token_amount(self, contract):
        if not contract:
            return

        msg = {
            'balance': {
                'address': self.address
            }
        }
        return int((await wallet.query_contract(contract, msg))['balance'])

    async def get(self, token):
        if token in self.cached:
            return self.cached[token]

        if token in network.NATIVE_COINS:
            result = (await self.get_native_coins_amounts()).get(network.NATIVE_COINS[token], 0)
        elif token in network.TOKENS:
            result = await self.get_token_amount(network.TOKENS[token])

        if result is not None:
            self.cached[token] = result

        return result

    #
    # Contracts
    #

    async def query_contract(self, contract, msg):
        return await network.lcd.wasm.contract_query(contract, msg)

    async def call_contract(self, contract, msg, coins=Coins()):
        print(f'Calling contract:')
        print(f'Contract: {contract}')
        print(f'Msg: {json.dumps(msg, indent=2)}')
        if coins:
            print(f'Coins: {coins}')

        print('Creating transaction and estimating fee... ', end='', flush=True)
        execute_msg = MsgExecuteContract(
            sender=self.address,
            contract=contract,
            execute_msg=msg,
            coins=coins,
        )

        tx = await self.wallet.create_and_sign_tx(
            CreateTxOptions(msgs=[execute_msg])
        )

        print('Done!')

        print('Broadcasting transaction... ', end='', flush=True)

        result = await network.lcd.tx.broadcast(tx)

        print('Done!')

        return result

    async def call_contract_with_token(self, contract, msg, token, amount):
        token_contract = network.TOKENS[token]
        send_msg = {
            'send': {
                'amount': str(amount),
                'contract': contract,
                'msg': encode_msg(msg),
            }
        }

        return await self.call_contract(token_contract, send_msg)


wallet = Wallet(MNEMONIC)
