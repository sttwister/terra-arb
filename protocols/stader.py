from protocols import protocol_manager
from protocols.base import Protocol
from utils import network
from utils.wallet import wallet


@protocol_manager.register
class Stader(Protocol):
    id = 'stader'
    name = 'Stader'

    async def get_lunax_exchange_rate(self):
        contract = network.CONTRACTS['STADER_LIQUID_STAKING']

        if not contract:
            return

        return float(
            (
                await wallet.query_contract(
                    contract,
                    {'state': {}}
                )
            )['state']['exchange_rate']
        )
