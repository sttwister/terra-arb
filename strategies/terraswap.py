from apps.stader import stader
from apps.terraswap import terraswap
from strategies.base import ArbitrageStrategy


class TerraswapbLunaStrategy(ArbitrageStrategy):
    protocol = terraswap
    from_token = 'LUNA'
    to_token = 'bLUNA'


class TerraswapReversebLunaStrategy(ArbitrageStrategy):
    protocol = terraswap
    from_token = 'bLUNA'
    to_token = 'LUNA'


class TerraswapLunaXStrategy(ArbitrageStrategy):
    protocol = terraswap
    from_token = 'LUNA'
    to_token = 'LunaX'

    async def get_exchange_rate(self):
        return await stader.get_lunax_exchange_rate()


class TerraswapReverseLunaXStrategy(ArbitrageStrategy):
    protocol = terraswap
    from_token = 'LunaX'
    to_token = 'LUNA'

    async def get_exchange_rate(self):
        lunax_exchange_rate = await stader.get_lunax_exchange_rate()
        if lunax_exchange_rate:
            return 1 / lunax_exchange_rate
