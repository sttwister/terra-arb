import asyncio
from math import inf


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
        scores = await asyncio.gather(*[strategy.get_score() for strategy in self.strategies])

        # Return a dict mapping strategy names to their scores, sorted desc by score
        return {
            strategy: score
            for strategy, score in sorted(zip(self.strategies, scores), key=lambda x: x[1], reverse=True)
        }

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
                'strategy': strategy,
                'protocol_name': strategy.protocol.get_name() if hasattr(strategy, 'protocol') else '',
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


