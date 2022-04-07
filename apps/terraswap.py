from apps.base import DexProtocol


class Terraswap(DexProtocol):
    name = 'Terraswap'

    PAIRS_IDENTIFIER = 'TERRASWAP_PAIRS'


terraswap = Terraswap()