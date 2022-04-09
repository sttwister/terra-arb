from terra_sdk.exceptions import LCDResponseError

from protocols import protocol_manager
from protocols.base import Protocol
from utils import network
from utils.wallet import wallet


@protocol_manager.register
class Anchor(Protocol):
    id = 'anchor'
    name = 'Anchor'

    async def unbond_bluna(self, amount):
        bluna_hub_contract = network.CONTRACTS['ANCHOR_BLUNA_HUB']

        msg = {
            'unbond': {}
        }

        return await wallet.call_contract_with_token(bluna_hub_contract, msg, 'bLUNA', amount)

    async def withdrawable_luna(self):
        bluna_hub_contract = network.CONTRACTS['ANCHOR_BLUNA_HUB']

        msg = {
            'withdrawable_unbonded': {
                'address': wallet.address,
            }
        }

        try:
            return int((await wallet.query_contract(bluna_hub_contract, msg))['withdrawable'])
        except LCDResponseError:
            pass

    async def withdraw_luna(self):
        bluna_hub_contract = network.CONTRACTS['ANCHOR_BLUNA_HUB']

        msg = {
            'withdraw_unbonded': {}
        }

        return await wallet.call_contract(bluna_hub_contract, msg)
