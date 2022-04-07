from apps.astroport import astroport
from apps.stader import stader
from strategies.base import ArbitrageStrategy


class AstroportbLunaStrategy(ArbitrageStrategy):
    protocol = astroport
    from_token = 'LUNA'
    to_token = 'bLUNA'


class AstroportReversebLunaStrategy(ArbitrageStrategy):
    protocol = astroport
    from_token = 'bLUNA'
    to_token = 'LUNA'


class AstroportLunaXStrategy(ArbitrageStrategy):
    protocol = astroport
    from_token = 'LUNA'
    to_token = 'LunaX'

    async def get_exchange_rate(self):
        return await stader.get_lunax_exchange_rate()


class AstroportReverseLunaXStrategy(ArbitrageStrategy):
    protocol = astroport
    from_token = 'LunaX'
    to_token = 'LUNA'

    async def get_exchange_rate(self):
        lunax_exchange_rate = await stader.get_lunax_exchange_rate()
        if lunax_exchange_rate:
            return 1 / lunax_exchange_rate
