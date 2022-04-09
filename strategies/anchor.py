from protocols import protocol_manager
from strategies.base import Strategy


anchor = protocol_manager.get_protocol('anchor')


class AnchorWithdrawLunaStrategy(Strategy):
    protocol = anchor
    name = 'Withdraw Luna'

    threshold = 0

    async def get_score(self):
        if await anchor.withdrawable_luna():
            return 0.0001

        return 0

    async def execute(self):
        await anchor.withdraw_luna()