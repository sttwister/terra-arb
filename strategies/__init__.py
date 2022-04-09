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
loop = DexProtocol.create('Loop', 'LOOP_PAIRS')


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
                astroport, 'LUNA', 'LunaX', strategy_get_exchange_rate=stader_app.get_lunax_exchange_rate,
            ),
            ArbitrageStrategy.create(
                terraswap, 'LUNA', 'LunaX', strategy_get_exchange_rate=stader_app.get_lunax_exchange_rate,
            ),
            ArbitrageStrategy.create(
                loop, 'LUNA', 'LunaX', strategy_get_exchange_rate=stader_app.get_lunax_exchange_rate,
            ),

            # cLUNA
            ArbitrageStrategy.create(
                terraswap, 'LUNA', 'cLUNA',
            ),
            ArbitrageStrategy.create(
                loop, 'LUNA', 'cLUNA',
            ),
            ArbitrageStrategy.create(
                prism_app, 'LUNA', 'cLUNA',
            ),
            # While this pair does exist on Astroport, it is very illiquid and not worth arbitrage
            # ArbitrageStrategy.create(
            #     astroport, 'LUNA', 'cLUNA',
            # ),
        ],
        name='LUNA arbitrage',
    ),
    'reverse_luna_arb': StrategyGroup(
        [
            # bLuna
            ArbitrageStrategy.create(
                astroport, 'bLUNA', 'LUNA',
            ),
            ArbitrageStrategy.create(
                terraswap, 'bLUNA', 'LUNA',
            ),
            ArbitrageStrategy.create(
                loop, 'bLUNA', 'LUNA',
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
            ArbitrageStrategy.create(
                loop, 'LunaX', 'LUNA',
                strategy_get_exchange_rate=reverse_exchange_rate(stader_app.get_lunax_exchange_rate),
            ),

            # cLUNA
            ArbitrageStrategy.create(
                terraswap, 'cLUNA', 'LUNA',
            ),
            ArbitrageStrategy.create(
                loop, 'cLUNA', 'LUNA',
            ),
            ArbitrageStrategy.create(
                prism_app, 'cLUNA', 'LUNA',
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
    'reverse_prism_arb': StrategyGroup(
        [
            ArbitrageStrategy.create(
                astroport, 'xPRISM', 'PRISM',
                strategy_get_exchange_rate=reverse_exchange_rate(prism_app.get_xprism_exchange_rate),
            ),
            ArbitrageStrategy.create(
                terraswap, 'xPRISM', 'PRISM',
                strategy_get_exchange_rate=reverse_exchange_rate(prism_app.get_xprism_exchange_rate),
            ),
            ArbitrageStrategy.create(
                prism_app, 'xPRISM', 'PRISM',
                strategy_get_exchange_rate=reverse_exchange_rate(prism_app.get_xprism_exchange_rate),
            ),
        ],
        name='Reverse xPRISM arbitrage',
    ),
    'luna_withdraw': StrategyGroup(
        [
            AnchorWithdrawLunaStrategy(),
            PrismWithdrawLunaStrategy(),
        ],
        name='Withdraw LUNA',
    )
}
