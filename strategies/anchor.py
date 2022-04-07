from apps.anchor import anchor_app
from strategies.base import Strategy


class AnchorWithdrawLunaStrategy(Strategy):
    protocol = anchor_app
    name = 'Withdraw Luna'

    threshold = 0

    async def get_score(self):
        if await anchor_app.withdrawable_luna():
            return 0.0001

        return 0

    async def execute(self):
        await anchor_app.withdraw_luna()