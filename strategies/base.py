import asyncio
from math import inf

import config
from utils.wallet import wallet


class StrategyGroup:
    """
    Groups together multiple similar strategies, with the aim of executing the one with the best score.
    """

    def __init__(self, strategies, name=None):
        self.strategies = strategies
        self.name = name

        self.history = {
            strategy: {
                'min': inf,
                'max': -inf,
            }
            for strategy in self.strategies
        }

        self.last_run = None

    async def get_scores(self):
        """
        Returns a dict mapping strategy names to their scores.
        """
        return dict(
            sorted(
                zip(
                    self.strategies,
                    await asyncio.gather(*[strategy.get_score() for strategy in self.strategies]),
                ),
                key=lambda x: -x[1]
            )
        )

    async def run(self):
        scores = await self.get_scores()

        self.last_run = scores

        # Update history
        for strategy, score in scores.items():
            self.history[strategy]['min'] = min(self.history[strategy]['min'], score)
            self.history[strategy]['max'] = max(self.history[strategy]['max'], score)

    def get_summary(self):
        """
        Returns a list of dicts, each containing information about a strategy.
        """
        return [
            {
                'protocol': strategy.protocol.get_name() if hasattr(strategy, 'protocol') else '',
                'name': strategy.get_name(),
                'score': score,
                'min': self.history[strategy]['min'],
                'max': self.history[strategy]['max'],
            }
            for strategy, score in self.last_run.items()
        ]

    async def execute(self):
        scores = self.last_run

        # Execute the best strategy that exceeds its threshold
        for strategy, score in scores.items():
            if score > strategy.threshold:
                await strategy.execute()
                return


class Strategy:
    """
    Base class for a strategy that checks for opportunities to execute beneficial actions.

    A strategy simulates actions on the blockchain and returns a score.

    A positive score indicates that the strategy is profitable.
    """
    name = None
    threshold = 0

    def __init__(self):
        assert self.protocol

    def get_name(self):
        return self.name

    def get_threshold(self):
        return self.threshold

    async def get_score(self):
        raise NotImplementedError()

    async def execute(self):
        raise NotImplementedError()


class ArbitrageStrategy(Strategy):
    """
    An arbitrage strategy checks for swapping between two tokens.

    If the swap results in a profit greater than a given threshold, it will return a positive score.

    The score is equal to the profit of the swap.
    """
    threshold = 5

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
        print('EXECUTING SWAP %f %s -> %s' % (
            amount / 10 ** 6,
            self.from_token,
            self.to_token,
        ))

        await self.protocol.swap(self.from_token, self.to_token, amount)