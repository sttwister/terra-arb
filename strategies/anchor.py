from protocols import protocol_manager
from strategies.base import Strategy
from utils.wallet import wallet

anchor = protocol_manager.get_protocol('anchor')


class AnchorWithdrawLunaStrategy(Strategy):
    """
    Tries to withdraw any pending LUNA from anchor.
    """
    protocol = anchor
    name = 'Withdraw LUNA'

    threshold = 0

    async def get_score(self):
        return await anchor.withdrawable_luna() / 10 ** 6

    async def execute(self):
        await anchor.withdraw_luna()


class AnchorUnbondBLunaStrategy(Strategy):
    """
    Unbonds any bLUNA on Anchor in order to withdraw LUNA.
    """
    protocol = anchor
    name = 'Unbond bLUNA'

    threshold = 0

    async def get_score(self):
        """
        Returns the amount of bLUNA that can be burned.
        """
        return await wallet.get('bLUNA') / 10 ** 6

    async def execute(self):
        await anchor.unbond_bluna()
