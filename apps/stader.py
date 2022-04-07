from apps.base import Protocol
from utils import network
from utils.wallet import wallet


class Stader(Protocol):
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


stader = Stader()