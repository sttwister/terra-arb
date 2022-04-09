import config
from strategies.base import Strategy
from utils.wallet import wallet


class ArbitrageStrategy(Strategy):
    """
    An arbitrage strategy checks for swapping between two tokens.

    If the swap results in a profit greater than a given threshold, it will return a positive score.

    The score is equal to the profit of the swap.
    """
    threshold = 3

    protocol = None
    from_token = None
    to_token = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert self.from_token
        assert self.to_token
        assert self.protocol

    def get_name(self):
        return '%s -> %s' % (self.from_token, self.to_token)

    async def get_exchange_rate(self):
        return 1

    async def get_score(self):
        # Check whether to use real amounts from the wallet, or just simulate the price with 1 token
        if config.USE_WALLET_FOR_SIMULATE:
            amount = await wallet.get(self.from_token)
        else:
            amount = 10 ** 6

        if not amount:
            return 0

        exchange_rate = await self.get_exchange_rate()

        if not exchange_rate:
            return 0

        swapped = await self.protocol.simulate_swap(self.from_token, self.to_token, amount)

        if not swapped:
            return 0

        final_amount = swapped * exchange_rate

        arb_percent = (final_amount - amount) / amount * 100

        return arb_percent

    async def execute(self):
        amount = await wallet.get(self.from_token)

        if not amount:
            return

        await self.protocol.swap(self.from_token, self.to_token, amount)

    @classmethod
    def create(cls, strategy_protocol, strategy_from_token, strategy_to_token,
               strategy_get_exchange_rate=None):
        """
        A factory for arbitrage strategies.

        Takes a protocol, a from_token and a to_token and returns an arbitrage strategy.
        """
        class CustomArbitrageStrategy(cls):
            protocol = strategy_protocol
            from_token = strategy_from_token
            to_token = strategy_to_token

            def __repr__(self):
                return "CustomArbitrageStrategy(%s: %s -> %s)" % (self.protocol.get_name(), self.from_token, self.to_token)

            async def get_exchange_rate(self):
                if strategy_get_exchange_rate:
                    return await strategy_get_exchange_rate()
                else:
                    return await super().get_exchange_rate()

        return CustomArbitrageStrategy()