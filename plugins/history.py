from math import inf

from plugins import plugin_manager
from plugins.base import Plugin
from strategies import strategy_manager


@plugin_manager.register
class HistoryPlugin(Plugin):
    """
    Stores a history of min and max scores for each strategy in a strategy group.
    """
    id = 'history'

    def __init__(self):
        # Maps strategy to min score
        self.strategies_min = {}

        # Maps strategy to max score
        self.strategies_max = {}

    def after_scoring(self, **kwargs):
        for group in strategy_manager.get_strategy_groups():
            for strategy, score in group.last_run.items():
                self.strategies_min[strategy] = min(score, self.strategies_min.get(strategy, inf))
                self.strategies_max[strategy] = max(score, self.strategies_max.get(strategy, -inf))

    def min(self, strategy):
        return self.strategies_min.get(strategy, None)

    def max(self, strategy):
        return self.strategies_max.get(strategy, None)
