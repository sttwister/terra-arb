from terra_sdk.exceptions import LCDResponseError

from apps.base import Protocol
from utils import make_coins, network
from utils.wallet import wallet


class Prism(Protocol):
    name = 'Prism'

    #
    # Swap
    #

    @classmethod
    def get_token_identifier(cls, token):
        if token in network.NATIVE_COINS:
            return {
                'native': network.NATIVE_COINS[token]
            }

        return {
            'cw20': network.TOKENS[token]
        }

    def get_prism_swap(self, from_token, to_token):
        return {
            'prism_swap': {
                'offer_asset_info': self.get_token_identifier(from_token),
                'ask_asset_info': self.get_token_identifier(to_token),
            }
        }

    async def simulate_swap(self, from_token, to_token, amount=1000000):
        operations = []
        if from_token != 'PRISM':
            operations.append(
                self.get_prism_swap(from_token, 'PRISM'),
            )

        if to_token != 'PRISM':
            operations.append(
                self.get_prism_swap('PRISM', to_token)
            )

        msg = {
            'simulate_swap_operations': {
                'offer_amount': str(amount),
                'operations': operations
            }
        }

        return float((await wallet.query_contract(network.CONTRACTS['PRISM_SWAP_ROUTER'], msg))['amount'])

    #
    # Unbond & withdraw cLUNA
    #

    async def unbond_cluna(self, amount):
        prism_luna_vault_contract = network.CONTRACTS['PRISM_LUNA_VAULT']

        msg = {
            'unbond': {}
        }

        return await wallet.call_contract_with_token(prism_luna_vault_contract, msg, 'cLUNA', amount)

    async def withdrawable_luna(self):
        luna_vault_contract = network.CONTRACTS['PRISM_LUNA_VAULT']

        msg = {
            'withdrawable_unbonded': {
                'address': wallet.address,
            }
        }

        try:
            return int((await wallet.query_contract(luna_vault_contract, msg))['withdrawable'])
        except LCDResponseError:
            pass

    async def withdraw_luna(self):
        luna_vault_contract = network.CONTRACTS['PRISM_LUNA_VAULT']

        msg = {
            'withdraw_unbonded': {}
        }

        return await wallet.call_contract(luna_vault_contract, msg)

    #
    # Refract
    #

    async def refract_luna(self, amount):
        luna_vault_contract = network.CONTRACTS['PRISM_LUNA_VAULT']

        msg = {
            'bond_split': {}
        }
        coins = make_coins('LUNA', amount)

        return await wallet.call_contract(luna_vault_contract, msg, coins)

    #
    # xPRISM
    #

    async def get_xprism_exchange_rate(self):
        return float(
            (
                await wallet.query_contract(
                    network.CONTRACTS['PRISM_GOVERNANCE'],
                    {'xprism_state': {}}
                )
            )['exchange_rate']
        )


prism_app = Prism()
