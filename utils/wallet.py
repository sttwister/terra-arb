import json

from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core import Coins
from terra_sdk.core.wasm import MsgExecuteContract
from terra_sdk.key.mnemonic import MnemonicKey

import config
from plugins import plugin_manager
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
        self.reset_cache()
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
            for token, amount in sorted(
                self.cached.items(),
                key=lambda x: (-x[1], x[0])  # Sort by amount desc, name asc
            )
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
        plugin_manager.dispatch('before_query_contract', contract, msg)

        response = await network.lcd.wasm.contract_query(contract, msg)

        plugin_manager.dispatch('after_query_contract', contract, msg, response)

        return response

    async def query_contract_at_height(self, contract_address, query, height):
        import base64
        import json
        params = {
            "query_msg": base64.b64encode(json.dumps(query).encode("utf-8")).decode(
                "utf-8"
            )
        }
        if height:
            params['height'] = height
        res = await wallet.wallet.lcd.wasm._c._get(
            f"/terra/wasm/v1beta1/contracts/{contract_address}/store", params
        )
        return res.get("query_result")

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

    async def call_contract(self, contract, msg, coins=Coins()):
        plugin_manager.dispatch('before_call_contract', contract, msg, coins)

        execute_msg = MsgExecuteContract(
            sender=self.address,
            contract=contract,
            execute_msg=msg,
            coins=coins,
        )

        result = await self.broadcast_msgs([execute_msg])

        return result

    async def broadcast_msgs(self, msgs):
        if not config.BROADCAST_TX:
            return

        tx = await self.wallet.create_and_sign_tx(
            CreateTxOptions(msgs=msgs)
        )

        plugin_manager.dispatch('before_broadcast_tx', tx)

        result = await network.lcd.tx.broadcast(tx)

        return result

    async def call_contracts_multiple(self, contract_calls):
        """
        Executes a list of multiple contract call msgs in a single transaction.

        Each item in contract_calls must be a dict with the following structure:

            {
                'contract': <...>,
                'msg': <...>,
                'coins': <...>,
            }
        """
        msgs = []
        for call in contract_calls:
            coins = call.get('coins', Coins())

            plugin_manager.dispatch('before_call_contract', call['contract'], call['msg'], coins=coins)

            msgs.append(
                MsgExecuteContract(
                    sender=self.address,
                    contract=call['contract'],
                    execute_msg=call['msg'],
                    coins=coins,
                )
            )

        return await self.broadcast_msgs(msgs)


wallet = Wallet(config.MNEMONIC)
