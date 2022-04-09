from terra_sdk.exceptions import LCDResponseError

from protocols import protocol_manager
from protocols.base import Protocol
from protocols.dex import DexProtocol
from utils import make_coins, network
from utils.wallet import wallet


@protocol_manager.register
class Prism(DexProtocol):
    id = 'prism'
    name = 'Prism'

    PAIRS_IDENTIFIER = 'PRISM_PAIRS'

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

    def get_swap_operations(self, from_token, to_token):
        operations = []
        if from_token != 'PRISM':
            operations.append(
                self.get_prism_swap(from_token, 'PRISM'),
            )

        if to_token != 'PRISM':
            operations.append(
                self.get_prism_swap('PRISM', to_token)
            )

        return operations

    async def simulate_swap(self, from_token, to_token, amount=1000000):
        operations = self.get_swap_operations(from_token, to_token)

        msg = {
            'simulate_swap_operations': {
                'offer_amount': str(amount),
                'operations': operations
            }
        }

        return float((await wallet.query_contract(network.CONTRACTS['PRISM_SWAP_ROUTER'], msg))['amount'])

    async def swap_native_coin(self, from_token, to_token, amount, max_spread=0.005):
        expected = await self.simulate_swap(from_token, to_token, amount)
        minimum_receive = int(expected * (1 - max_spread))

        operations = self.get_swap_operations(from_token, to_token)

        msg = {
            'execute_swap_operations': {
                'minimum_received': str(minimum_receive),
                'offer_amount': str(amount),
                'operations': operations
            }
        }

        coins = make_coins(from_token, amount)

        return await wallet.call_contract(network.CONTRACTS['PRISM_SWAP_ROUTER'], msg, coins=coins)

    #
    # Unbond & withdraw cLUNA
    #

    async def unbond_cluna(self):
        prism_luna_vault_contract = network.CONTRACTS['PRISM_LUNA_VAULT']
        amount = await wallet.get('cLUNA')

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
            return 0

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

    async def unstake_xprism(self):
        prism_governance_contract = network.CONTRACTS['PRISM_GOVERNANCE']
        amount = await wallet.get('xPRISM')

        msg = {
            'redeem_xprism': {}
        }

        return await wallet.call_contract_with_token(prism_governance_contract, msg, 'xPRISM', amount)
