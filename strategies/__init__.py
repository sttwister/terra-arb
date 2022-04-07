from apps.base import DexProtocol
from apps.stader import stader_app
from strategies.anchor import AnchorWithdrawLunaStrategy
from strategies.arbitrage import ArbitrageStrategy
from strategies.base import StrategyGroup
from strategies.prism import PrismWithdrawLunaStrategy
from utils import reverse_exchange_rate

from apps.prism import prism_app

astroport = DexProtocol.create('Astroport', 'ASTROPORT_PAIRS')
terraswap = DexProtocol.create('Terraswap', 'TERRASWAP_PAIRS')


STRATEGY_GROUPS = [
    StrategyGroup(
        [
            # bLuna
            ArbitrageStrategy.create(
                astroport, 'LUNA', 'bLUNA',
            ),
            ArbitrageStrategy.create(
                terraswap, 'LUNA', 'bLUNA',
            ),

            # LunaX
            ArbitrageStrategy.create(
                astroport, 'LUNA', 'LunaX', strategy_get_exchange_rate=stader_app.get_lunax_exchange_rate,
            ),
            ArbitrageStrategy.create(
                terraswap, 'LUNA', 'LunaX', strategy_get_exchange_rate=stader_app.get_lunax_exchange_rate,
            ),

            # cLUNA
            ArbitrageStrategy.create(
                astroport, 'LUNA', 'cLUNA',
            ),
            ArbitrageStrategy.create(
                terraswap, 'LUNA', 'cLUNA',
            ),
            ArbitrageStrategy.create(
                prism_app, 'LUNA', 'cLUNA',
            ),
        ],
        name='LUNA arbitrage',
    ),
    StrategyGroup(
        [
            # bLuna
            ArbitrageStrategy.create(
                astroport, 'bLUNA', 'LUNA',
            ),
            ArbitrageStrategy.create(
                terraswap, 'LUNA', 'bLUNA',
            ),

            # LunaX
            ArbitrageStrategy.create(
                astroport, 'LunaX', 'LUNA',
                strategy_get_exchange_rate=reverse_exchange_rate(stader_app.get_lunax_exchange_rate),
            ),
            ArbitrageStrategy.create(
                terraswap, 'LunaX', 'LUNA',
                strategy_get_exchange_rate=reverse_exchange_rate(stader_app.get_lunax_exchange_rate),
            ),

            # cLUNA
            ArbitrageStrategy.create(
                astroport, 'cLUNA', 'LUNA',
            ),
            ArbitrageStrategy.create(
                terraswap, 'cLUNA', 'LUNA',
            ),
            ArbitrageStrategy.create(
                prism_app, 'cLUNA', 'LUNA',
            ),
        ],
        name='Reverse LUNA arbitrage',
    ),
    StrategyGroup(
        [
            ArbitrageStrategy.create(
                astroport, 'PRISM', 'xPRISM', strategy_get_exchange_rate=prism_app.get_xprism_exchange_rate,
            ),
            ArbitrageStrategy.create(
                terraswap, 'PRISM', 'xPRISM', strategy_get_exchange_rate=prism_app.get_xprism_exchange_rate,
            ),
            ArbitrageStrategy.create(
                prism_app, 'PRISM', 'xPRISM', strategy_get_exchange_rate=prism_app.get_xprism_exchange_rate,
            ),
        ],
        name='xPRISM arbitrage',
    ),
    StrategyGroup(
        [
            AnchorWithdrawLunaStrategy(),
            PrismWithdrawLunaStrategy(),
        ],
        name='Withdraw LUNA',
    )
]
