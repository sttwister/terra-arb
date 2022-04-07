from strategies.anchor import AnchorWithdrawLunaStrategy
from strategies.astroport import AstroportbLunaStrategy, AstroportLunaXStrategy, AstroportReversebLunaStrategy, \
    AstroportReverseLunaXStrategy
from strategies.base import StrategyGroup
from strategies.prism import PrismcLunaStrategy, xPrismStrategy, PrismWithdrawLunaStrategy, PrismReversecLunaStrategy
from strategies.terraswap import TerraswapbLunaStrategy, TerraswapLunaXStrategy, TerraswapReversebLunaStrategy, \
    TerraswapReverseLunaXStrategy

STRATEGY_GROUPS = [
    StrategyGroup(
        [
            AstroportbLunaStrategy(),
            TerraswapbLunaStrategy(),
            AstroportLunaXStrategy(),
            TerraswapLunaXStrategy(),
            PrismcLunaStrategy(),
        ],
        name='LUNA arbitrage',
    ),
    StrategyGroup(
        [
            AstroportReversebLunaStrategy(),
            TerraswapReversebLunaStrategy(),
            AstroportReverseLunaXStrategy(),
            TerraswapReverseLunaXStrategy(),
            PrismReversecLunaStrategy(),
        ],
        name='Reverse LUNA arbitrage',
    ),
    StrategyGroup(
        [
            xPrismStrategy(),
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
