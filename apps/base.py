from utils import make_coins, network
from utils.wallet import wallet


class Protocol:
    name = None

    def get_name(self):
        return self.name


class DexProtocol(Protocol):

    PAIRS_IDENTIFIER = None

    @classmethod
    def get_token_identifier(cls, token):
        if token in network.NATIVE_COINS:
            return {
                'native_token': {
                    'denom': network.NATIVE_COINS[token]
                }

            }

        return {
            'token': {
                'contract_addr': network.TOKENS[token],
            }
        }

    @classmethod
    def get_pair_contract(cls, token1, token2):
        return (
                network.CONTRACTS[cls.PAIRS_IDENTIFIER].get((token1, token2)) or
                network.CONTRACTS[cls.PAIRS_IDENTIFIER].get((token2, token1))
        )

    async def simulate_swap(self, from_token, to_token, amount=1000000):
        contract = self.get_pair_contract(from_token, to_token)

        if not contract:
            return

        msg = {
            'simulation': {
                'offer_asset': {
                    'amount': str(amount),
                    'info': self.get_token_identifier(from_token)
                }
            }
        }

        return float((await wallet.query_contract(contract, msg))['return_amount'])

    async def swap(self, from_token, to_token, amount, max_spread=0.005):
        if from_token in network.NATIVE_COINS:
            return await self.swap_native_coin(from_token, to_token, amount, max_spread=max_spread)
        elif from_token in network.TOKENS:
            return await self.swap_cw20_token(from_token, to_token, amount, max_spread=max_spread)

    async def swap_native_coin(self, from_token, to_token, amount, max_spread=0.005):
        pair_contract = self.get_pair_contract(from_token, to_token)

        belief_price = 10 ** 6 / await self.simulate_swap(from_token, to_token)

        msg = {
            'swap': {
                'belief_price': str(belief_price),
                'max_spread': str(max_spread),
                'offer_asset': {
                    'amount': str(amount),
                    'info': self.get_token_identifier(from_token),
                }
            }
        }

        coins = make_coins(from_token, amount)

        return await wallet.call_contract(pair_contract, msg, coins=coins)

    async def swap_cw20_token(self, from_token, to_token, amount, max_spread=0.005):
        belief_price = 10 ** 6 / await self.simulate_swap(from_token, to_token)

        pair_contract = self.get_pair_contract(from_token, to_token)

        msg = {
            'swap': {
                'max_spread': str(max_spread),
                'belief_price': '%.18f' % belief_price,
            }
        }

        return await wallet.call_contract_with_token(pair_contract, msg, from_token, amount)

