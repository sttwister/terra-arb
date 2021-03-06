import config
from protocols import protocol_manager
from strategies.anchor import AnchorWithdrawLunaStrategy, AnchorUnbondBLunaStrategy
from strategies.arbitrage import ArbitrageStrategy
from strategies.base import StrategyGroup
from strategies.prism import PrismWithdrawLunaStrategy, PrismUnbondCLunaStrategy, PrismUnstakeXPrismStrategy, \
    RefractLunaStrategy, PrismMergeLunaStrategy
from utils import reverse_exchange_rate


astroport = protocol_manager.get_protocol('astroport')
loop = protocol_manager.get_protocol('loop')
prism = protocol_manager.get_protocol('prism')
stader = protocol_manager.get_protocol('stader')
terraswap = protocol_manager.get_protocol('terraswap')


STRATEGY_GROUPS = {
    'luna_arb': StrategyGroup(
        [
            # bLuna
            ArbitrageStrategy.create(
                astroport, 'LUNA', 'bLUNA',
            ),
            ArbitrageStrategy.create(
                terraswap, 'LUNA', 'bLUNA',
            ),
            ArbitrageStrategy.create(
                loop, 'LUNA', 'bLUNA',
            ),

            # LunaX
            ArbitrageStrategy.create(
                astroport, 'LUNA', 'LunaX', strategy_get_exchange_rate=stader.get_lunax_exchange_rate,
            ),
            ArbitrageStrategy.create(
                terraswap, 'LUNA', 'LunaX', strategy_get_exchange_rate=stader.get_lunax_exchange_rate,
            ),
            ArbitrageStrategy.create(
                loop, 'LUNA', 'LunaX', strategy_get_exchange_rate=stader.get_lunax_exchange_rate,
            ),

            # cLUNA
            ArbitrageStrategy.create(
                terraswap, 'LUNA', 'cLUNA',
            ),
            ArbitrageStrategy.create(
                loop, 'LUNA', 'cLUNA',
            ),
            ArbitrageStrategy.create(
                prism, 'LUNA', 'cLUNA',
            ),
            # While this pair does exist on Astroport, it is very illiquid and not worth arbitrage
            # ArbitrageStrategy.create(
            #     astroport, 'LUNA', 'cLUNA',
            # ),

            # Refract LUNA
            RefractLunaStrategy(),
        ],
        name='LUNA arbitrage',
    ),
    'reverse_luna_arb': StrategyGroup(
        [
            # bLuna
            ArbitrageStrategy.create(
                astroport, 'bLUNA', 'LUNA',
                strategy_threshold=-0.5,
            ),
            ArbitrageStrategy.create(
                terraswap, 'bLUNA', 'LUNA',
                strategy_threshold=-0.5,
            ),
            ArbitrageStrategy.create(
                loop, 'bLUNA', 'LUNA',
                strategy_threshold=-0.5,
            ),

            # LunaX
            ArbitrageStrategy.create(
                astroport, 'LunaX', 'LUNA',
                strategy_get_exchange_rate=reverse_exchange_rate(stader.get_lunax_exchange_rate),
                strategy_threshold=-0.5,
            ),
            ArbitrageStrategy.create(
                terraswap, 'LunaX', 'LUNA',
                strategy_get_exchange_rate=reverse_exchange_rate(stader.get_lunax_exchange_rate),
                strategy_threshold=-0.5,
            ),
            ArbitrageStrategy.create(
                loop, 'LunaX', 'LUNA',
                strategy_get_exchange_rate=reverse_exchange_rate(stader.get_lunax_exchange_rate),
                strategy_threshold=-0.5,
            ),

            # cLUNA
            ArbitrageStrategy.create(
                terraswap, 'cLUNA', 'LUNA',
                strategy_threshold=-0.5,
            ),
            ArbitrageStrategy.create(
                loop, 'cLUNA', 'LUNA',
                strategy_threshold=-0.5,
            ),
            ArbitrageStrategy.create(
                prism, 'cLUNA', 'LUNA',
                strategy_threshold=-0.5,
            ),
            # While this pair does exist on Astroport, it is very illiquid and not worth arbitrage
            # ArbitrageStrategy.create(
            #     astroport, 'cLUNA', 'LUNA',
            # ),
        ],
        name='Reverse LUNA arbitrage',
    ),
    'prism_arb': StrategyGroup(
        [
            ArbitrageStrategy.create(
                astroport, 'PRISM', 'xPRISM', strategy_get_exchange_rate=prism.get_xprism_exchange_rate,
                strategy_threshold=5,
            ),
            ArbitrageStrategy.create(
                terraswap, 'PRISM', 'xPRISM', strategy_get_exchange_rate=prism.get_xprism_exchange_rate,
                strategy_threshold=5,
            ),
            ArbitrageStrategy.create(
                prism, 'PRISM', 'xPRISM', strategy_get_exchange_rate=prism.get_xprism_exchange_rate,
                strategy_threshold=5,
            ),
        ],
        name='xPRISM arbitrage',
    ),
    'reverse_prism_arb': StrategyGroup(
        [
            ArbitrageStrategy.create(
                astroport, 'xPRISM', 'PRISM',
                strategy_get_exchange_rate=reverse_exchange_rate(prism.get_xprism_exchange_rate),
                strategy_threshold=-1,
            ),
            ArbitrageStrategy.create(
                terraswap, 'xPRISM', 'PRISM',
                strategy_get_exchange_rate=reverse_exchange_rate(prism.get_xprism_exchange_rate),
                strategy_threshold=-1,
            ),
            ArbitrageStrategy.create(
                prism, 'xPRISM', 'PRISM',
                strategy_get_exchange_rate=reverse_exchange_rate(prism.get_xprism_exchange_rate),
                strategy_threshold=-1,
            ),
        ],
        name='Reverse xPRISM arbitrage',
    ),
    'luna_withdraw': StrategyGroup(
        [
            AnchorUnbondBLunaStrategy(),
            AnchorWithdrawLunaStrategy(),
            PrismMergeLunaStrategy(),
            PrismUnbondCLunaStrategy(),
            PrismWithdrawLunaStrategy(),
            PrismUnstakeXPrismStrategy(),
        ],
        name='Recycle tokens',
    )
}


class StrategyManager:
    def __init__(self):
        self.strategy_groups = {
            strategy_group: STRATEGY_GROUPS.get(strategy_group)
            for strategy_group in config.ENABLED_STRATEGY_GROUPS
        }

    def get_strategy_groups(self):
        return self.strategy_groups.values()


strategy_manager = StrategyManager()
